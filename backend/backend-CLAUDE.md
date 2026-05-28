# CLAUDE.md — Backend (FastAPI + ML Pipeline)

## 개요

FastAPI 기반 백엔드 서버. 7단계 AI 파이프라인으로 K-pop 안무 유사도를 분석한다.

## 실행 방법

```bash
cd backend
pip install -r requirements.txt
# PyTorch CPU 전용 설치 시:
# pip install torch --index-url https://download.pytorch.org/whl/cpu
# 시스템에 ffmpeg 필수 설치

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 아키텍처

### 서버 라이프사이클 (main.py)
- `lifespan`에서 서버 시작 시 모델 1회 로드 (`ModelRegistry.get().load_all()`)
- CPU 스레드 예산 설정: `torch.set_num_threads()`, `cv2.setNumThreads()`
- CORS: localhost:5173, kpopstand.com 허용
- 오래된 영상 캐시 자동 정리 (1시간 초과 mp4)

### API 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | `/api/analyze` | 두 영상 유사도 분석 (video_a_id, video_b_id, analysis_id) |
| POST | `/api/videos` | 영상 업로드 → Supabase Storage |
| GET | `/` | Health check |
| GET | `/health` | 모델 로드 상태 확인 |

### ML 파이프라인 (analyze.py)

```
Step 1: extract_objects (YOLO + HRNet)       ← ThreadPoolExecutor 병렬 2개
Step 2-1: extract_3d_from_hrnet (MotionBERT 3D Lifting) ← 병렬
Step 2: embed_motion (MotionBERT 임베딩)     ← 병렬
Step 3: infer_similarity (GCN 유사도 추론)   ← 순차
Step 4: generate_similarity_report (LLM)     ← 순차
→ format_result (프론트엔드용 포맷팅)
```

### 모델 구성

| 모델 | 역할 | 가중치 경로 |
|------|------|------------|
| YOLOv8n | 인물 검출 | `models/yolo/weights/yolov8n.pt` |
| HRNet-W48 | 2D 포즈 추정 (17관절) | `models/hrnet/weights/pose_hrnet_w48_384x288.pth` |
| MotionBERT | 2D→3D 리프팅 + 임베딩 [F,17,512] | `models/motion_bert/weights/mega_latest_epoch.bin` |
| LightweightGCN | ST-GCN 포즈 인코더 (512→256→128) | `models/gcn_mlp/weights/best_global_model.pth` |

### 유사도 추론 파라미터 (inferrence.py)

- Motion 단위: 5초 슬라이딩 윈도우 (`MOTION_SEGMENT_SEC = 5`)
- Pose 단위: 1초 세분화 (`POSE_SEGMENT_SEC = 1`)
- FPS: 10 (다운샘플링)
- Refine: ±2초 sliding window로 정밀 정렬
- Body Parts (H36M-17): torso, left_arm, right_arm, left_leg, right_leg

### LLM 보고서 (report.py)

- LangChain + ChatOpenAI (GPT)
- 출력 스키마: `ReportResult` (Pydantic)
  - `summary`: 전체 유사도 판단 요약
  - `similar_segments`: 구간별 상세 분석 (time_a, time_b, description)
  - `key_similarities`: 주요 공통점
  - `overall_score_interpretation`: 전체 점수 해석
- 프롬프트에 한국 저작권법 + Hanagami v. Epic Games 판례 기반 판단 기준 포함

### 결과 포맷팅 (result_formatter.py)

- `format_result()`: analyze() 출력 → 프론트엔드 소비 형태로 변환
- video_url: Supabase `videos` 테이블에서 vid로 조회
- segment score: `motion_sim` 기반 (0~1 → 백분율)
- time_range 파싱: `"10~15s"` → `{"start": 10.0, "end": 15.0}`

## 디렉토리별 역할

| 디렉토리 | 역할 |
|----------|------|
| `api/` | REST API 엔드포인트 (router.py, video_upload.py) |
| `core/` | 설정(config.py), 모델 로더(model_loader.py) |
| `model_pipeline/` | 7단계 처리 로직 |
| `models/` | AI 모델 구조 정의 (가중치는 .gitignore) |
| `repository/` | 데이터 접근 계층 |
| `schemas/` | Pydantic 스키마 |
| `utils/` | ffmpeg, Supabase 클라이언트, 검증 |
| `temp/` | 다운로드 임시 영상 (자동 생성) |

## 주의사항

- `models/` 하위 weights 디렉토리는 `.gitignore`에 포함 (100MB 초과 바이너리)
- `config.py`의 `PARALLEL_VIDEOS = 2`는 `analyze.py`의 `max_workers`와 반드시 동기화
- `SUPABASE_SERVICE_ROLE_KEY`는 이 서버에서만 사용 (프론트엔드 노출 금지)
- HRNet 사용을 위해 별도 레포 클론 필요: `HRNet-Human-Pose-Estimation`
- 시스템에 `ffmpeg` 설치 필수
