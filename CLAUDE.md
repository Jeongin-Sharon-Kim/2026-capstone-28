# CLAUDE.md — Tenein (K-pop 안무 유사도 분석 시스템)

## 프로젝트 개요

Tenein은 K-pop 안무 영상 간 유사도를 자동으로 분석하는 AI 풀스택 웹 서비스이다.
두 영상을 업로드하면 딥러닝 파이프라인이 동작을 추출하고, 구간별 유사도를 계산한 뒤, LLM이 자연어 분석 보고서를 생성한다.

- **레포**: `kookmin-sw/2026-capstone-28` (public)
- **브랜치 전략**: feature → develop → main (PR 기반 머지), 브랜치 프리픽스 `fe-`/`be-`
- **배포**: AWS EC2 × 2 (Frontend/Backend) + Docker Compose, GitHub Actions CI/CD

## 디렉토리 구조

```
2026-capstone-28/
├── .github/workflows/deploy.yml    # CI/CD (main push → EC2 SSH deploy)
├── backend/                        # FastAPI + PyTorch ML 파이프라인
│   ├── main.py                     # FastAPI 진입점 (lifespan으로 모델 로드)
│   ├── api/
│   │   ├── router.py               # POST /api/analyze 엔드포인트
│   │   └── video_upload.py         # POST /api/videos 영상 업로드
│   ├── core/
│   │   ├── config.py               # 경로, 디바이스, 하이퍼파라미터, Supabase 설정
│   │   └── model_loader.py         # ModelRegistry 싱글턴 (YOLO/HRNet/MotionBERT/GCN)
│   ├── model_pipeline/             # 7단계 AI 파이프라인
│   │   ├── analyze.py              # 메인 오케스트레이터 (ThreadPoolExecutor 병렬)
│   │   ├── object_extractor.py     # YOLO 인물 검출 + HRNet 2D 키포인트
│   │   ├── object_processor.py     # HRNet 후처리
│   │   ├── bert_3d_lifting.py      # HRNet 2D → MotionBERT 3D 리프팅
│   │   ├── bert_embedder.py        # MotionBERT 임베딩 [F, 17, 512]
│   │   ├── feature_extractor.py    # 특징 추출
│   │   ├── stgcn_pose_encoder.py   # ST-GCN 포즈 인코더
│   │   ├── pose_tag.py             # Pose+Tag 멀티모달 유사도
│   │   ├── tag_extractor.py        # Tag Feature 추출 (관절 각도/방향/속도)
│   │   ├── inferrence.py           # 유사도 추론 (5초 슬라이딩 윈도우, 부위별)
│   │   ├── report.py               # LangChain + GPT LLM 보고서 생성
│   │   └── result_formatter.py     # 프론트엔드용 결과 포맷팅
│   ├── models/                     # AI 모델 정의
│   │   ├── yolo/detector.py
│   │   ├── HRnet/HRnet_loader.py
│   │   ├── motion_bert/architecture.py, embedder.py
│   │   └── gcn_mlp/lightweight_gcn.py, siamese_mlp.py, inferencer.py
│   ├── repository/video_repository.py
│   ├── schemas/analyze_schemas.py, video.py
│   ├── utils/ffmpeg_utils.py, supabase_client.py, validation.py
│   └── requirements.txt
├── frontend/                       # React 18 + Vite 5 SPA
│   ├── src/
│   │   ├── App.jsx                 # 페이지 라우팅 (state 기반)
│   │   ├── Login.jsx               # 로그인/회원가입
│   │   ├── home_page.jsx           # 영상 업로드 + 분석 요청
│   │   ├── loading_page.jsx        # 분석 대기 (단계별 메시지)
│   │   ├── result_page.jsx         # 분석 결과 + 아코디언 구간
│   │   ├── profile_page.jsx        # 유저 정보 + 히스토리 + 상세 모달
│   │   ├── about_us_page.jsx       # 서비스 소개
│   │   ├── hooks/useIsMobile.js
│   │   ├── lib/supabaseClient.js   # Supabase 클라이언트 (anon key)
│   │   ├── utils/generatePDF.jsx   # @react-pdf/renderer PDF 보고서 생성
│   │   └── assets/                 # 배경 이미지, PDF 배경
│   ├── public/fonts/               # NotoSansKR TTF (PDF용 로컬 서빙)
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 기술 스택

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **ML**: PyTorch (CPU), YOLO v8, HRNet-W48, MotionBERT, LightweightGCN
- **LLM**: LangChain + OpenAI GPT (report.py)
- **DB/Storage**: Supabase (PostgreSQL + Storage)

### Frontend
- **Framework**: React 18 + Vite 5 (JSX, TypeScript 미사용)
- **디자인 시스템**: "Emerald Luxe" — glassmorphism, 딥 포레스트 그린~에메랄드~민트 그라디언트
- **폰트**: Chakra Petch (제목), Rajdhani (본문), NotoSansKR (PDF)
- **PDF**: @react-pdf/renderer (브라우저 내 생성)
- **Auth**: Supabase Auth (이메일/비밀번호)

### Infra
- **배포**: AWS EC2 × 2, Docker Compose, ECR
- **CI/CD**: GitHub Actions → SSH → docker compose up -d --build

## API 응답 스키마 (POST /api/analyze)

```json
{
  "video_a_id": 1,
  "video_b_id": 2,
  "video_url_a": "https://...",
  "video_url_b": "https://...",
  "overall": {
    "score": 68.0,
    "interpretation": "전체 유사도는 중간 이상으로..."
  },
  "summary": "두 영상의 전체 유사도는...",
  "key_differences": ["팔 동작 디테일에서...", "후반부로 갈수록..."],
  "segments": [
    {
      "id": 1,
      "score": 66.7,
      "video_a": { "start": 15.0, "end": 20.0 },
      "video_b": { "start": 10.0, "end": 15.0 },
      "description": "영상 A의 15~20초와...",
      "body_parts": { "torso": 0.72, "left_arm": 0.65, ... }
    }
  ]
}
```

## DB 스키마 (Supabase)

```sql
profiles (id UUID PK, user_name TEXT)
analyses (aid BIGINT PK, user_id UUID, created_at TIMESTAMP, result_data JSONB)
videos   (vid BIGINT PK, ...)
-- Storage: videos 버킷 (public)
```

## 환경 변수

### Backend (.env)
- `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` (절대 프론트엔드/git 노출 금지)
- `OPENAI_API_KEY`
- `SUPABASE_BUCKET` (기본값 "videos")

### Frontend (.env)
- `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY` (anon key는 RLS 하에 프론트 사용 가능)

## 코딩 컨벤션

- 코드 수정 시 **변경할 라인만 명시** (변경 범위가 큰 경우 전체 파일 수용)
- 파일명, 함수명 변경 금지 (기존 네이밍 유지)
- Python: snake_case, type hints 사용
- JavaScript/JSX: 인라인 스타일 객체 패턴 (CSS-in-JS), React 함수형 컴포넌트
- 간결하고 직접적인 표현, 문학적/수사적 표현 지양
- 코드 파일명 수정 및 파일 삭제 절대 금지
- 허가 없이 git에 commit, push 금지


## 주요 주의사항

1. **모델 가중치**: `.bin`, `.pth`, `.pt` 파일은 100MB 초과 → `.gitignore`에 `backend/models/` weights 포함
2. **Yoga 레이아웃**: @react-pdf/renderer의 absolute 포지셔닝은 표준 CSS와 다름 → `height: 0, overflow: visible` 래퍼 필요
3. **영상 스크린샷**: 병렬 캡처 시 동일 프레임 반환 → 단일 video 엘리먼트로 순차 처리
4. **normalizeData 듀얼 경로**: `generatePDF.jsx`의 `normalizeData`에는 ResultPage 경로(`raw.overall` 존재)와 ProfilePage 경로(폴백)가 있으며, 양쪽 모두에 변환 로직 적용 필요
5. **CPU 스레드 예산**: `analyze.py`가 ThreadPoolExecutor(max_workers=2)로 병렬 처리 → `config.py`의 TORCH_THREADS/CV2_THREADS와 동기화 필요
6. **Supabase 키 분리**: service_role key는 FastAPI 전용, anon key는 프론트엔드 전용
