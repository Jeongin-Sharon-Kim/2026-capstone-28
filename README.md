<div align="center">

# 🎵 Tenein — K-pop 안무 유사도 분석 시스템

**AI 기반 K-pop 안무 영상 비교 · 분석 · 보고서 자동 생성 웹 서비스**
<br/>
*두 K-pop 안무 영상을 업로드하면 AI가 유사 구간을 탐지하고,*
*신체 부위별 유사도를 분석하여 PDF 보고서를 자동 생성합니다.*


<img width="1570" height="885" alt="image" src="https://github.com/user-attachments/assets/f1f2e40e-7191-480e-a950-465cc38467da" />

</div>

---

## 📋 목차

- [프로젝트 소개](#-프로젝트-소개)
- [팀원 소개](#-팀원-소개)
- [Tech Stack](#-Tech-Stack)
- [서비스 플로우](#-서비스-플로우)
- [웹 서비스](#-웹-서비스)
- [AWS 배포 아키텍처](#-aws-배포-아키텍처)
- [연구 성과](#-연구-성과)

---

## 🎬 프로젝트 소개

K-pop 안무 영상 간 유사도를 자동으로 분석하는 풀스택 AI 웹 서비스입니다.
두 영상을 업로드하면 딥러닝 파이프라인이 동작을 추출하고, 구간별 유사도를 계산한 뒤, LLM이 자연어 분석 보고서를 생성합니다.

### 🎥 시연 영상
프로젝트 시연 및 소개 영상 링크 : https://youtu.be/C7zSym6TCzI

### 주요 기능

| 기능 | 설명 |
|:---:|------|
| 🎯 **전체 유사도 분석** | 두 안무 영상의 전체 유사도 점수 산출 |
| 🔍 **구간별 탐지** | 시간 구간별 유사 안무 구간 자동 탐지 |
| 🦴 **부위별 분석** | 왼팔, 오른팔, 왼다리, 오른다리, 몸통 부위별 유사도 |
| 📊 **AI 보고서** | GPT-5.1 기반 자연어 분석 보고서 자동 생성 |
| 📄 **PDF 내보내기** | 분석 결과를 PDF 보고서로 다운로드 |
| 👤 **분석 히스토리** | 과거 분석 기록 조회 및 상세 보기 |


<div align="center">

#### 🔐 인증 및 메인

| 메인 화면 | 로그인 및 회원가입 | 프로필 및 히스토리 조회 |
|:-----:|:------:|:-----:|
| <img width="2735" height="1823" alt="Image" src="https://github.com/user-attachments/assets/6af9c0c6-e8df-4c18-bdc2-4d988b9a2c24" /> | <img width="2735" height="1556" alt="Image" src="https://github.com/user-attachments/assets/2a2a938b-0ca7-4c7e-8531-4a95b25426f5" />| <img width="2694" height="1549" alt="Image" src="https://github.com/user-attachments/assets/9be6e8c5-f70f-42db-8941-6eeeccbeb279" /> |

#### 🎬 분석 기능

| 영상 업로드 | 분석 보고서 |
|:----------:|:----------:|
|<img width="2701" height="1401" alt="Image" src="https://github.com/user-attachments/assets/f4850894-5abc-4206-ab54-03e5d2af55fb" /> |<img width="1449" height="1442" alt="Image" src="https://github.com/user-attachments/assets/d9944161-d8a7-4a25-9fd7-472d180d62c4" />|

</div>

## 🌟 기대효과

<div align="center">

Tenein은 K-pop 산업의 **안무 저작권 보호**, **댄스 교육 혁신**, **콘텐츠 생태계 활성화**에 기여합니다.

</div>

---

<table>
  <tr>
    <td width="33%">
      <h3>💼 안무 저작권 분쟁 해결</h3>
      <p><b>문제</b>: 주관적 전문가 평가의 한계</p>
      <p><b>솔루션</b>: AI 기반 객관적 정량 측정</p>
      <p><b>가치</b>:</p>
      <ul>
        <li>법정 증거 보조지표로 이용 가능한 분석 리포트</li>
        <li>시간 구간별·부위별 상세 분석</li>
        <li>"87.6% 일치" 같은 수치 증거 제공</li>
        <li>전문가 육안 평가의 주관성 극복</li>
      </ul>
    </td>
    <td width="33%">
      <h3>🎓 댄스 교육 피드백 고도화</h3>
      <p><b>문제</b>: 추상적 피드백 ("더 잘 춰")</p>
      <p><b>솔루션</b>: 정량적 구체적 피드백</p>
      <p><b>가치</b>:</p>
      <ul>
        <li>"팔 각도 15도 더 벌리세요" 정밀 지도</li>
        <li>신체 부위별 유사도 점수 제공</li>
        <li>학습 성장 추적 및 개선점 시각화</li>
        <li>학습자 동기 부여 및 목표 설정</li>
      </ul>
    </td>
    <td width="33%">
      <h3>🎬 소셜 미디어 생태계 확장</h3>
      <p><b>문제</b>: 주관적 인기도 평가</p>
      <p><b>솔루션</b>: 객관적 자동 순위 시스템</p>
      <p><b>가치</b>:</p>
      <ul>
        <li>"원곡과 95% 일치" 배지 부여</li>
        <li>커버 댄서 실시간 리더보드</li>
        <li>공정한 경쟁 환경 조성</li>
        <li>SNS 챌린지 참여 동기 강화</li>
      </ul>
    </td>
  </tr>
</table>

---

<div align="center">

### 🎯 브랜드 아이덴티티

| Objective (객관성) | Interpretable (해석 가능성) | Accessible (접근성) |
|:------------------:|:-------------------------:|:------------------:|
| **97.66% 정확도**<br/>데이터로 말합니다 | **부위별 상세 분석**<br/>객관적 지표를 통한 설명 | **3초 처리**<br/>전문가 수준을 누구나 |

</div>


---
## 👥 팀원 소개
Team, Tenein
> *Tenein — 고대어로 "안무"를 뜻합니다.*

<table>
<tr>

<td align="center">
<img width="200" height="200" alt="suman" src="https://github.com/user-attachments/assets/150f446a-a4ce-4106-8cb9-c8a67a3394e5" /><br/>
<b> 김수만(팀장)</b><br/>
PM / AI
</td>

<td align="center">
<img width="200" height="200" alt="jeongin" src="https://github.com/user-attachments/assets/071ec714-a421-452d-a334-1573f4c09738" /><br/>
<b> 김정인</b><br/>
AI / QA
</td>

<td align="center">
<img width="200" height="200" alt="moongyeong" src="https://github.com/user-attachments/assets/5a42d5a8-b0cb-4c51-856f-1c0b2d3d4689" /><br/>
<b> 배문경</b><br/>
AI / FE
</td>

<td align="center">
<img width="200" height="200" alt="gyeongji" src="https://github.com/user-attachments/assets/ec33f2fb-bad0-4344-ac73-955fa77bf455" /><br/>
<b> 백경지</b><br/>
BE
</td>

</tr>
</table>

---
##  🛠 Tech Stack

#### AI / Backend

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLOv8-black?style=for-the-badge)
![HRNet](https://img.shields.io/badge/HRNet-W48-blue?style=for-the-badge)
![MotionBERT](https://img.shields.io/badge/MotionBERT-purple?style=for-the-badge)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)

#### Frontend

![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)

#### External Services

![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)

#### Deployment

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![GitHubActions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white)

---

## 🏗 서비스 플로우

<div align="center">
  <img src="https://github.com/user-attachments/assets/e9b490c2-0b7f-4a06-9ffc-8933eeccd66a" alt="시스템 아키텍처" width="900" />
</div>

---

## 🌐 웹 서비스

### 프론트엔드

| 항목 | 내용 |
|------|------|
| **프레임워크** | React 18 + Vite 5 (JSX, TypeScript 미사용) |
| **디자인 시스템** | Glassmorphism (backdrop-filter blur + 반투명 그라디언트) |
| **인증** | Supabase Auth (이메일/비밀번호) |
| **PDF 생성** | @react-pdf/renderer (브라우저 내 생성, 서버 부하 없음) |
| **폰트** | Chakra Petch (제목), Rajdhani (본문), NotoSansKR (PDF) |

#### 페이지 구성

| 페이지 | 파일 | 기능 |
|:------:|------|------|
| 🔐 | `Login.jsx` | 로그인 / 회원가입 |
| 🏠 | `home_page.jsx` | 영상 업로드 + 분석 요청 |
| ⏳ | `loading_page.jsx` | 분석 대기 (단계별 메시지 + 경과시간) |
| 📊 | `result_page.jsx` | 분석 결과 + 아코디언 구간 + PDF 다운로드 |
| 👤 | `profile_page.jsx` | 유저 정보 + 히스토리 + 상세 모달 |
| ℹ️ | `about_us_page.jsx` | 서비스 소개 |

### 백엔드

| 항목 | 내용 |
|------|------|
| **프레임워크** | FastAPI + AWS |
| **ML 런타임** | PyTorch (CPU), YOLO, MediaPipe, MotionBERT, GCN |
| **LLM** | LangChain + GPT-5.1 |
| **DB/Storage** | Supabase (PostgreSQL + Storage) |

#### API 엔드포인트

```http
POST /api/analyze
Content-Type: application/json

{
  "video_a_id": 1,
  "video_b_id": 2
}
```

```json
// Response
{
  "overall": {
    "score": 68.0,
    "interpretation": "전체 유사도는 중간 이상으로..."
  },
  "summary": "두 영상의 전체 유사도는...",
  "key_differences": [
    "팔 동작 디테일에서 의도적 변형이 관찰됨",
    "후반부로 갈수록 포즈 일치도가 감소"
  ],
  "segments": [
    {
      "id": 1,
      "score": 66.7,
      "video_a": { "start": 15.0, "end": 20.0 },
      "video_b": { "start": 10.0, "end": 15.0 },
      "description": "영상 A의 15~20초와 영상 B의 10~15초는..."
    }
  ]
}
```

### 데이터베이스 구조

```sql
-- 사용자 프로필
profiles (
  id          UUID PRIMARY KEY,    -- auth.users.id FK
  user_name   TEXT
)

-- 분석 결과
analyses (
  aid         BIGINT PRIMARY KEY,  -- auto-increment
  user_id     UUID,                -- auth.users.id FK
  created_at  TIMESTAMP,
  result_data JSONB                -- format_result 출력 전체
)

-- Storage: videos 버킷 (public)
```

## 📂 폴더 구조
```
현재 공개 레포지토리 기준 구조입니다.

📦 2026-capstone-28
│
├── 📄 README.md                         # 프로젝트 전체 설명서
├── 📄 .gitignore
│
├── 📁 .github                           # GitHub Actions
│   └── workflows
│       └── deploy.yml                   # CI/CD 배포 워크플로우
│
├── 📁 assets                            # 정적 자산
│   └── images
│       └── poster.png                   # 프로젝트 포스터
│
├── 📁 frontend                          # 프론트엔드 (React + Vite)
│   ├── 📁 public                        # 정적 파일
│   │   ├── logo.png
│   │   └── fonts
│   │       ├── NotoSansKR-Bold.ttf
│   │       └── NotoSansKR-Regular.ttf
│   │
│   ├── 📁 src
│   │   ├── 📁 pages                     # 페이지 컴포넌트
│   │   │   ├── Login.jsx                # 로그인/회원가입
│   │   │   ├── home_page.jsx            # 영상 업로드
│   │   │   ├── loading_page.jsx         # 분석 대기
│   │   │   ├── result_page.jsx          # 분석 결과
│   │   │   ├── profile_page.jsx         # 사용자 프로필
│   │   │   └── about_us_page.jsx        # 서비스 소개
│   │   │
│   │   ├── 📁 hooks                     # Custom Hooks
│   │   │   └── useIsMobile.js
│   │   │
│   │   ├── 📁 lib                       # 외부 라이브러리
│   │   │   └── supabaseClient.js
│   │   │
│   │   ├── 📁 utils                     # 유틸리티
│   │   │   └── generatePDF.jsx          # PDF 보고서 생성
│   │   │
│   │   ├── 📁 assets                    # 이미지 자산
│   │   │   ├── background.png
│   │   │   ├── pdf-cover-bg.png
│   │   │   └── pdf-body-bg.png
│   │   │
│   │   ├── App.jsx                      # 메인 앱 컴포넌트
│   │   └── main.jsx                     # React 진입점
│   │
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
│
├── 📁 backend                           # 백엔드 (FastAPI + PyTorch)
│   ├── 📁 api                           # REST API
│   │   ├── router.py                    # API 라우터
│   │   └── video_upload.py              # 영상 업로드 처리
│   │
│   ├── 📁 core                          # 핵심 설정
│   │   ├── config.py                    # 환경 설정
│   │   └── model_loader.py              # 모델 로더
│   │
│   ├── 📁 models                        # AI 모델
│   │   ├── 📁 yolo
│   │   │   └── detector.py              # YOLOv8 인물 검출
│   │   ├── 📁 HRnet
│   │   │   └── HRnet_loader.py          # HRNet-W48 포즈 추출
│   │   ├── 📁 motion_bert
│   │   │   ├── architecture.py          # MotionBERT 구조
│   │   │   └── embedder.py              # 3D 임베딩 생성
│   │   └── 📁 gcn_mlp
│   │       ├── lightweight_gcn.py       # ST-GCN
│   │       ├── siamese_mlp.py           # Siamese MLP
│   │       └── inferencer.py            # 유사도 추론
│   │
│   ├── 📁 model_pipeline                # AI 파이프라인
│   │   ├── analyze.py                   # 메인 분석 로직
│   │   ├── object_extractor.py          # YOLO 객체 추출
│   │   ├── object_processor.py          # HRNet 포즈 처리
│   │   ├── bert_3d_lifting.py           # 2D→3D 변환
│   │   ├── bert_embedder.py             # MotionBERT 임베딩
│   │   ├── feature_extractor.py         # 특징 추출
│   │   ├── stgcn_pose_encoder.py        # ST-GCN 인코더
│   │   ├── pose_tag.py                  # Pose+Tag 멀티모달
│   │   ├── tag_extractor.py             # Tag Feature 추출
│   │   ├── inferrence.py                # 유사도 추론
│   │   ├── report.py                    # LLM 보고서 생성
│   │   └── result_formatter.py          # 결과 포맷팅
│   │
│   ├── 📁 repository                    # 데이터 레포지토리
│   │   └── video_repository.py
│   │
│   ├── 📁 schemas                       # API 스키마
│   │   ├── analyze_schemas.py
│   │   └── video.py
│   │
│   ├── 📁 utils                         # 유틸리티
│   │   ├── ffmpeg_utils.py              # 영상 처리
│   │   ├── supabase_client.py           # Supabase 클라이언트
│   │   └── validation.py                # 입력 검증
│   │
│   ├── main.py                          # FastAPI 진입점
│   └── requirements.txt                 # Python 의존성
```
\```

### Frontend Architecture
프론트엔드는 React 18 + Vite 5 기반 SPA 구조입니다.

| 디렉터리 | 역할 |
|----------|------|
| `pages/` | 라우트 단위 페이지 (Login, Home, Result 등) |
| `hooks/` | Custom React Hooks (모바일 감지 등) |
| `lib/` | 외부 라이브러리 클라이언트 (Supabase) |
| `utils/` | 유틸리티 함수 (PDF 생성, 포맷팅) |

### Backend Architecture
백엔드는 7단계 AI 파이프라인 중심으로 구성됩니다.

| 디렉터리 | 역할 |
|----------|------|
| `api/` | REST API 엔드포인트 |
| `models/` | AI 모델 구현 (YOLO, HRNet, MotionBERT, GCN) |
| `model_pipeline/` | 7단계 처리 로직 (추출→임베딩→추론→보고서) |
| `utils/` | 영상 처리, DB 연결, 검증 |

---

## ☁️ AWS 배포 아키텍처
 
```
┌──────────────────────────────────────────────────────────────────────┐
│                           AWS Cloud                                  │
│                                                                      │
│  ┌─────────────────────┐         ┌─────────────────────┐            │
│  │  EC2 — Frontend     │         │  EC2 — Backend       │            │
│  │  ┌───────┐ ┌──────┐ │         │  ┌────────┐ ┌──────┐ │            │
│  │  │ React │ │ Vite │ │  POST   │  │FastAPI │ │Docker│ │            │
│  │  └───────┘ └──────┘ │ ──────→ │  │Python  │ └──────┘ │            │
│  │       Docker         │/analyze │  └────────┘          │            │
│  └──────────┬──────────┘         └──────────┬───────────┘            │
│             │                               │                        │
└─────────────┼───────────────────────────────┼────────────────────────┘
              │ HTTPS                         │
              │                               ├──→ Supabase DB
              │                               ├──→ Supabase Storage
              │                               └──→ OpenAI API (Report)
              │
    ┌─────────┼──────────────────────────────────────┐
    │         ▼                                      │
    │  ┌─────────────┐                               │
    │  │Supabase Auth│  Login / Create Account       │
    │  └─────────────┘                               │
    │                      Supabase                  │
    └────────────────────────────────────────────────┘
 
┌──────────────────────────────────────────────────────────────────────┐
│                         CI/CD Pipeline                               │
│                                                                      │
│  Developer → GitHub → GitHub Actions → Docker Build → ECR Push      │
│                                            │                         │
│                                            └──→ EC2 자동 배포        │
└──────────────────────────────────────────────────────────────────────┘
```
 
### 인프라 구성
 
| 구성 요소 | 서비스 | 역할 |
|:---:|------|------|
| 🖥 | **EC2 (Frontend)** | React + Vite 정적 파일 서빙, Docker 컨테이너 |
| 🧠 | **EC2 (Backend)** | FastAPI + PyTorch ML 파이프라인, Docker 컨테이너 |
| 📦 | **ECR** | Frontend Image, Backend Image 저장소 |
| 🔐 | **Supabase Auth** | 사용자 인증 (이메일/비밀번호, Google OAuth) |
| 🗄 | **Supabase DB** | PostgreSQL — 분석 결과, 사용자 프로필 저장 |
| 📁 | **Supabase Storage** | 업로드 영상 파일 관리 (videos 버킷) |
| 🤖 | **OpenAI API** | GPT-5.1 기반 분석 보고서 생성 |
 
### 배포 흐름
 
```
1. 개발자가 main 브랜치에 push
2. GitHub Actions 트리거
3. Docker 이미지 빌드 (Frontend / Backend)
4. ECR에 이미지 Push
5. EC2에서 최신 이미지 Pull + 컨테이너 재시작
```

---

## 📖 연구 성과

### KICS(한국통신학회) 26년 학술대회 발표예정
#### 멀티모달 기반 안무 유사도 검출 기술, 안무 유사도 분석 시스템 구축
<div align="center">
  <img width="45%" src="https://github.com/user-attachments/assets/0fa97d8e-9502-4786-809c-429765cbcf98" />
  <img width="45%" src="https://github.com/user-attachments/assets/8f8be960-d398-4e10-9eb5-227086c61558" />
</div>


<div align="center">

**Tenein** — K-pop Visual Studio

2026 국민대학교 소프트웨어융합대학 캡스톤디자인
<br/>
산학협력 : 한국콘텐츠진흥원

© 2026 Tenein Team

</div>
