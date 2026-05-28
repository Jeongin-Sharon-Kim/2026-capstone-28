"""
분석 API 라우터.
HTTP 요청을 받아 pipeline.analyze() 함수에 위임하고,
완료 후 analyses 테이블의 result_data를 UPDATE한다.
"""
import asyncio
import logging
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from model_pipeline.analyze import analyze
from utils.supabase_client import get_supabase

logger = logging.getLogger(__name__)
router = APIRouter()

# 단일 GPU에서 동시 forward는 VRAM 압박 + 직렬화로 오히려 느려진다.
# 분석은 한 번에 하나만 GPU에 들어가도록 게이트하고, 나머지는 대기열로 흐른다.
# VRAM/성능 측정 후 값 상향 가능.
_ANALYZE_CONCURRENCY = 1
_analyze_semaphore = asyncio.Semaphore(_ANALYZE_CONCURRENCY)


# ===== 요청 schema =====
class AnalyzeRequest(BaseModel):
    video_a_id: int
    video_b_id: int
    analysis_id: Optional[int] = None  # 업로드 단계에서 발급된 analyses.aid


# ===== 엔드포인트 =====
@router.post("/analyze")
async def analyze_videos(req: AnalyzeRequest):
    """
    두 영상의 안무 유사도를 분석하고, 완료 시 analyses 테이블에 결과를 저장한다.

    프론트엔드 호출 예:
        POST /api/analyze
        Content-Type: application/json
        { "video_a_id": 1, "video_b_id": 2, "analysis_id": 3 }
    """
    try:
        logger.info(f"분석 요청: A={req.video_a_id}, B={req.video_b_id}, analysis_id={req.analysis_id}")

        # ── 분석 실행 ────────────────────────────────────
        # 1) 세마포어로 동시 분석 수 제한 → GPU OOM/슬로다운 방지
        # 2) to_thread로 동기 CPU/GPU 작업을 워커 스레드에 위임 →
        #    이벤트 루프 살아있어 업로드/health 등 다른 요청은 계속 처리됨
        async with _analyze_semaphore:
            result = await asyncio.to_thread(
                analyze, req.video_a_id, req.video_b_id
            )

        # ── analyses 테이블 UPDATE ────────────────────────
        if req.analysis_id is not None:
            try:
                sb = get_supabase()
                sb.table("analyses").update({
                    "result_data": result,
                }).eq("aid", req.analysis_id).execute()
                logger.info(f"analyses 저장 완료: aid={req.analysis_id}")
            except Exception as db_err:
                # DB 저장 실패는 결과 반환을 막지 않음 (경고만)
                logger.warning(f"analyses 저장 실패 (aid={req.analysis_id}): {db_err}")

        return result

    except ValueError as e:
        logger.warning(f"분석 요청 검증 실패: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"분석 실패: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"분석 중 오류 발생: {str(e)}",
        )