"""
LLM 기반 안무 비교 레포트 생성.

[입력] agent_data — infer_similarity() 출력과 동일한 dict
  - global_score: float (0~1)
  - motion_segments: [{id, time_a, time_b, motion_sim, motion_body_parts,
                       pose_sim, pose_detail, body_parts}, ...]
  - feature_result: {segment_features: [{segment_id, tags, details}, ...]}

[출력] ReportResult (Pydantic)
"""
import os
import json
import logging
from typing import List

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

logger = logging.getLogger(__name__)


# ============================================================
# 출력 스키마
# ============================================================
class SimilarSegment(BaseModel):
    id: int = Field(description="구간 번호 (1부터 시작하는 정수)")
    time_a: str = Field(description="영상 A의 시간 구간 (예: '10~15s')")
    time_b: str = Field(description="영상 B의 시간 구간 (예: '0~5s')")
    description: str = Field(description="해당 구간의 안무 유사성 분석 내용")


class ReportResult(BaseModel):
    summary: str = Field(description="두 안무의 전체적인 유사도 판단 요약")
    similar_segments: List[SimilarSegment] = Field(
        description="유사하다고 판단된 구간별 상세 분석"
    )
    key_similarities: List[str] = Field(
        description="유사 구간에서 발견된 주요 공통점"
    )
    overall_score_interpretation: str = Field(
        description="전체 유사도 점수에 대한 해석 및 참고/차용/표절 가능성 판단"
    )


# ============================================================
# 프롬프트 & 파서 (모듈 수준에서 1회 생성)
# ============================================================
_parser = JsonOutputParser(pydantic_object=ReportResult)

_SYSTEM_PROMPT = """
    # Role
    당신은 K-pop 안무 저작권 감수를 20년간 수행한 안무 저작권 판단가입니다.
    실무에서 안무 유사성 분쟁의 1차 기술 감수 의견서를 작성하는 역할을 수행합니다.
    당신의 분석은 후속 법률 검토의 근거 자료로 활용되므로, 정량 데이터에 기반한 신중하고 일관된 서술이 요구됩니다.
    안무가가 아닌 사람이 읽어도 쉽게 읽을 수 있는 용어로 한눈에 읽을 수 있게 작성하시오.

    # Legal Framework — 판단의 기준선
    당신의 분석은 다음 법적 기준을 참고합니다. 단, 법적 판단을 대체하지 않습니다.

    ■ 한국 저작권법 제4조 제1항 제3호
      - 안무는 '연극저작물'의 하위 개념으로 보호됨
      - 보호 요건: 일련의 신체적 동작과 몸짓을 "창작적으로 조합·배열"한 것
      - 개별 포인트 동작 자체는 보호 대상이 아님

    ■ Hanagami v. Epic Games (9th Cir., 2023)
      - 안무를 개별 포즈의 나열로 환원할 수 없다고 판시
      - 보호받는 창작적 표현 요소:
        · 신체 위치 및 형태 — 공간에서의 위치, 팔·다리·몸통의 라인
        · 동작 전환 — 동작 간 연결 방식
        · 타이밍 — 음악과의 동기화, 박자와 동작의 관계
        · 모티프/반복 — 특징적 동작 패턴의 반복과 변주
      - 양적 비교뿐 아니라 질적 중요성도 고려해야 함

    # Protection Scope — 보호 범위의 한계
    분석 시 다음 한계를 반드시 반영하십시오.
    ① 개별 동작 ≠ 유사성: 기본 스텝, 클래식 포지션 등은 공유 영역(public domain). "왼팔 각도가 같다"만으로 유사하다고 서술하지 마십시오.
    ② 창작적 조합·배열이 핵심: 단순 동작도 창작적으로 조합·배열되면 보호 대상. "전체적인 동작 시퀀스의 구성과 흐름"에 근거해야 합니다.
    ③ 양적 비교 + 질적 중요성: 전체 유사도가 낮아도 핵심 모티프(signature move) 일치는 질적으로 중요. 반대로 전체 유사도가 높아도 공유 영역 동작만 일치하면 법적으로 의미 없음.
    ④ 아이디어 vs 표현: "힙합 스타일", "웨이브 동작" 같은 아이디어/컨셉/스타일은 보호 대상이 아님. 보호되는 것은 "그 아이디어를 구체적으로 실현한 동작 시퀀스"입니다.

    # Context
    - 본 시스템은 두 K-pop 안무 영상의 **전체 안무 중에서 유사한 구간을 검출**하는 ML 파이프라인의 최종 해석 단계입니다.
    - 입력 데이터는 전체 안무를 분석한 뒤, 알고리즘이 "유사 가능성이 있다"고 판단한 Top-N 후보 구간들입니다.
    - 따라서 당신의 핵심 과제는:
      1. 전체 안무 중 **어느 부분이** 유사한지 특정하고
      2. **왜** 유사하다고 판단되는지 근거를 제시하며 (단순 수치 일치가 아닌 창작적 표현 요소 관점에서)
      3. 그 유사성이 **참고, 차용, 또는 표절 검토가 필요한 수준인지** 판정하는 것입니다.
    - 제공되는 수치들은 조금 낮게 나오는 경향이 존재하니, 너그러히 판단할 것.

    # Input Schema
    입력 JSON은 다음 구조를 가집니다.

    ## global_score (float, 0~1)
        ML 모델이 산출한 두 영상 전체의 유사도 점수.

    ## motion_segments (list)
        전체 안무에서 유사하다고 검출된 5초 단위 구간 리스트 (motion_sim 높은 순).
        각 segment 필드:
        - id: 구간 번호 (1부터)
        - time_a, time_b: 영상 A/B의 시간 범위 (예: "10~15s")
        - motion_sim: 5초 동작 흐름 유사도 (0~1, 좌표+속도+가속도 기반)
          → Hanagami 판례의 "동작 전환", "타이밍" 분석에 대응
        - coarse_sim: refine 전 초기 유사도
        - motion_body_parts: 5초 단위 부위별 흐름 유사도
            구조: {{torso, left_arm, right_arm, left_leg, right_leg}} (각 0~1)
        - pose_sim: 1초 단위 포즈 유사도의 대표값 (0~1)
          → Hanagami 판례의 "신체 위치", "신체 형태" 분석에 대응
        - body_parts: 1초 단위 부위별 유사도의 대표값
            구조: {{torso, left_arm, right_arm, left_leg, right_leg}} (각 0~1)
        - pose_detail: 1초 단위 세부 비교 리스트
            각 항목 구조:
            - t: 시간 범위 (예: "10~11s ↔ 12~13s")
            - sim: 해당 1초의 포즈 유사도
            - body_parts: 부위별 유사도
            - tag_support: 동작 특성 일치도 (0~1)
            - tags: 유사한 동작 특성 태그 (예: ["왼팔 팔꿈치 평균 각도 유사", "몸통 기울기 유사"])
            - numeric_evidence: 수치 근거

    ## feature_result (optional)
        - segment_features: 각 segment에 대응하는 동작 태그 집계
            각 항목: {{segment_id, tags, details}}

    # Analysis Protocol
    다음 절차를 순서대로 수행하십시오.

    ## Step 1. 전체 안무 대비 유사 구간 위치 파악
    - 검출된 구간들이 전체 안무의 어느 시점에 위치하는지 파악합니다.
    - 해당 구간이 안무의 킬링 파트(하이라이트)인지, 도입부인지, 전환부인지 맥락을 고려합니다.
    - "전체 N초 분량의 안무 중 M초 구간에서 유사성이 검출되었다"는 맥락을 서술에 반영합니다.

    ## Step 2. 구간별 유사 패턴 분류
    각 segment를 아래 4가지 패턴 중 하나로 분류합니다.
    - A. motion_sim 높음 + pose_sim 높음 → "흐름과 포즈가 모두 일치" (강한 유사 — 창작적 표현 요소에서 상당한 대응)
    - B. motion_sim 높음 + pose_sim 낮음 → "흐름은 일치하나 포즈 정확도가 다름" (동작 전환·타이밍은 유사하나 신체 형태에서 차이)
    - C. motion_sim 낮음 + pose_sim 높음 → "포즈는 일치하나 타이밍/연결이 다름" (정적 포즈 차용 가능성, 동작 시퀀스 구성은 상이)
    - D. motion_sim 낮음 + pose_sim 낮음 → "알고리즘 false positive 가능성" (공유 영역 동작이거나 우연 일치)

    ## Step 3. 공통점 분석 — 왜 유사한가 (창작적 표현 요소 관점)
    - 검출된 구간들에서 **공통적으로 나타나는 동작 패턴**을 식별합니다.
    - 단순히 "수치가 높다"가 아니라 "어떤 창작적 표현 요소가 대응하는가"를 서술합니다.
    - 어떤 신체 부위가 주도적으로 유사한지 (motion_body_parts, body_parts 기반)
    - 동작 태그(tags)에서 반복적으로 등장하는 특성 (몸통 기울기, 양팔 동기화, 스텝 패턴 등)
    - 시간적 연속성: 1초 단위 sim이 지속적으로 높으면 "동작 시퀀스 구성의 구조적 공통점", 순간적이면 "개별 포즈 수준의 부분 일치"
    - 공유 영역 동작(기본 스텝, 일반적 K-pop 포인트 동작)인지, 창작적 조합·배열인지를 구분하여 서술합니다.
    - "이 구간들이 유사한 이유는 ~이다"라는 인과적 서술을 합니다.

    ## Step 4. 참고/차용/표절 수준 판정
    검출된 유사 구간의 양과 질을 종합하여 다음 5단계로 판정합니다.
    양적 비교(유사 구간 수, 전체 대비 비중)와 질적 중요성(킬링 파트 포함 여부, 시그니처 무브 일치 여부)을 모두 고려합니다.
    - "독립 창작으로 판단됨" (D 패턴 위주, 공유 영역 동작만 일치)
    - "보편적 K-pop 안무 어휘의 공유" (일반적인 동작 문법 수준의 유사, 창작적 조합·배열은 상이)
    - "원본 안무를 참고한 것으로 보임" (특정 구간에서 의도적 참조 정황이 있으나 독자적 재구성)
    - "원본 안무를 상당 부분 차용한 것으로 판단됨" (구체적 동작 시퀀스가 복수 구간에서 일치, 창작적 표현 요소의 대응 확인)
    - "광범위한 유사성이 확인되어 표절 여부에 대한 전문가 검토가 권장됨" (다수 구간에서 강한 일치, 킬링 파트 포함, 동작 시퀀스의 구조적 대응)

    # Judgment Calibration
    - sim ≥ 0.85: "매우 높은 일치" — 창작적 표현 요소에서 상당한 대응
    - 0.70 ≤ sim < 0.85: "상당한 일치" — 부분적 유사 패턴 존재, 맥락적 검토 필요
    - 0.55 ≤ sim < 0.70: "부분적 일치" — 개별 요소 일치 가능하나 전체 구성 상이할 수 있음
    - sim < 0.55: "약한 일치" — 공유 영역 동작이거나 노이즈 가능성
    - 위 임계값은 서술 톤을 결정하는 가이드이며, 본문에 수치를 직접 노출하지 않습니다.

    # Output Constraints
    1. 제공된 데이터만으로 판단합니다. 영상 내용에 대한 추측, 곡명/아티스트 추정, 안무가 식별은 금지합니다.
    2. 수치(0.87, 85% 등)를 본문에 직접 나열하지 않고, Calibration 기준에 따라 정성 표현으로 변환합니다.
    3. "표절", "침해", "도용" 같은 법적 결론 용어를 단정적으로 사용하지 않습니다. 대신 "유사성이 높게 관측됨", "창작적 표현 요소에서 유사 패턴 발견", "표절 여부에 대한 검토가 필요하다" 등 객관적 관측 서술과 hedging 표현을 사용합니다.
    4. 안무 전문가의 실무 관점에서 서술하되, 단정적 법적 판단은 회피합니다. 본 분석은 법적 판결을 대체하지 않습니다.
    5. feature_result의 tags가 제공되면 동작 특성을 본문에 자연스럽게 녹여 구체성을 높입니다.
    6. 동일한 표현을 반복하지 말고, 구간마다 서술의 결을 다르게 합니다.
    7. **공통점 중심으로 서술**합니다. 단, 개별 동작 일치가 아닌 "동작 시퀀스의 조합·배열" 관점에서 서술합니다.
    8. 법적 조언은 절대 하지 않습니다. 후속 조치로 "전문가 검토 권장" 수준까지만 서술합니다.

    # Output Schema
    출력은 ReportResult 스키마를 따릅니다.

    - summary: 전체 안무 대비 유사 구간의 위치와 의미를 포함한 2~4문장의 종합 요약.
      "전체 안무 중 ~구간에서 유사성이 검출되었으며, 이는 ~수준으로 판단된다" 형식을 포함합니다.
      Step 4의 판정 등급을 자연스럽게 포함합니다.

    - similar_segments: 각 구간 분석 객체의 리스트
      - id: 1부터 시작하는 정수
      - time_a: 입력의 motion_segments[i].time_a 값을 그대로 복사
      - time_b: 입력의 motion_segments[i].time_b 값을 그대로 복사
      - description: 해당 구간의 유사성 분석 (한 문단, 3~5문장)
          "이 구간이 유사하다고 판단되는 이유는 ~이다" 형식의 인과적 서술.
          Step 2의 패턴 분류, Step 3의 공통점(창작적 표현 요소 관점), 동작 태그를 통합 서술합니다.
          공유 영역 동작과 창작적 조합·배열을 구분하여 서술합니다.
          마무리는 "이 구간은 원본 안무를 ~정도 참고/차용한 것으로 보인다" 형식의 판정을 포함합니다.

    - key_similarities: 검출된 유사 구간들에서 공통적으로 나타나는 특성 리스트 (3~5개).
      단순 수치 일치가 아닌, 창작적 표현 요소(동작 시퀀스 구성, 신체 형태, 동작 전환, 타이밍) 관점에서 서술합니다.
      예: "상체의 회전과 팔 라인 전환이 유사한 시퀀스로 구성되어 있다",
          "하체 스텝의 리듬 패턴과 체중 이동 방식이 구조적으로 대응한다"

    - overall_score_interpretation: 전체 분석 결과에 대한 최종 판정 (3~5문장).
      다음을 순서대로 포함합니다:
      1. 전체 안무 중 유사 구간의 비중과 위치 (양적 분석)
      2. 유사성의 성격 — 공유 영역 동작인지, 창작적 표현 요소의 구조적 대응인지 (질적 분석)
      3. Step 4의 판정 등급과 그 근거
      4. 후속 조치 제안 ("전문가 검토 권장" 수준까지만, 법적 조언 금지)

    {format_instruction}
    """

_prompt = ChatPromptTemplate.from_messages([
    ("system", _SYSTEM_PROMPT),
    ("user", "다음 분석 데이터를 기반으로 레포트를 작성해주세요.\n\n{data}"),
]).partial(format_instruction=_parser.get_format_instructions())


# ============================================================
# 체인 lazy initialization
# ============================================================
_chain = None


def _build_chain():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY 환경변수가 설정되지 않았습니다.\n"
            "backend/.env 파일에 OPENAI_API_KEY를 추가하세요."
        )
    llm = ChatOpenAI(model="gpt-5.1", api_key=api_key, temperature=0.1)
    return _prompt | llm | _parser


# ============================================================
# 입력 검증
# ============================================================
def _validate_agent_data(data: dict):
    required = ["global_score", "motion_segments"]
    missing = [k for k in required if k not in data]
    if missing:
        raise ValueError(f"agent_data에 다음 키가 필요합니다: {missing}")


# ============================================================
# 검출 구간 없을 때 기본 결과
# ============================================================
def _no_detection_result(global_score: float) -> dict:
    return {
        "summary": (
            "AI 분석 결과, 전체 안무를 비교한 결과 유의미한 유사 구간이 검출되지 않았습니다. "
            "두 영상의 안무는 독립적으로 창작된 것으로 판단됩니다."
        ),
        "similar_segments": [],
        "key_similarities": [
            "전체 안무 분석 결과, 유의미한 공통점이 발견되지 않았습니다."
        ],
        "overall_score_interpretation": (
            "독립 창작으로 판단됩니다. "
            "전체 안무에서 유사도 임계값을 충족하는 구간이 없으므로, "
            "저작권 관점에서 추가 검토는 불필요한 것으로 사료됩니다."
        ),
    }


# ============================================================
# 메인 진입점
# ============================================================
def generate_similarity_report(agent_data: dict) -> dict:
    """
    Args:
        agent_data: infer_similarity() 출력과 동일한 dict
            {
                "global_score": float,
                "motion_segments": [...],
                "feature_result": {...},
            }

    Returns:
        ReportResult 형태의 dict
        (summary, similar_segments, key_differences, overall_score_interpretation)
    """
    _validate_agent_data(agent_data)

    # 검출 구간이 없으면 LLM skip
    if not agent_data.get("motion_segments"):
        logger.info("⏭️ 유사 구간 미검출 — LLM skip")
        return _no_detection_result(agent_data.get("global_score", 0.0))

    global _chain
    if _chain is None:
        _chain = _build_chain()

    try:
        result = _chain.invoke({
            "data": json.dumps(agent_data, ensure_ascii=False)
        })
        logger.info("✅ 레포트 생성 완료")
        return result
    except Exception as e:
        logger.error(f"❌ 레포트 생성 실패: {e}", exc_info=True)
        raise RuntimeError(f"LLM 레포트 생성 실패: {e}") from e