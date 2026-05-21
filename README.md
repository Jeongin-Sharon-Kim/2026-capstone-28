<div align="center">

# 🎵 Tenein — K-pop 안무 유사도 분석 시스템

**AI 기반 K-pop 안무 영상 비교 · 분석 · 보고서 자동 생성 웹 서비스**
<img width="1200" height="700" alt="image" src="https://github.com/user-attachments/assets/c7d712bf-b262-4aec-ba73-295095736013" />


<br/>

*두 K-pop 안무 영상을 업로드하면 AI가 유사 구간을 탐지하고,*
*신체 부위별 유사도를 분석하여 PDF 보고서를 자동 생성합니다.*

</div>

---

## 📋 목차

- [프로젝트 소개](#-프로젝트-소개)
- [팀 소개](#-팀-소개)
- [기술 스택](#-기술-스택)
- [서비스 플로우](#-서비스-플로우)
- [웹 서비스](#-웹-서비스)
- [AWS 배포 아키텍처](#-aws-배포-아키텍처)
- [연구 성과](#-연구-성과)

---

## 🎬 프로젝트 소개

K-pop 안무 영상 간 유사도를 자동으로 분석하는 풀스택 AI 웹 서비스입니다.
두 영상을 업로드하면 딥러닝 파이프라인이 동작을 추출하고, 구간별 유사도를 계산한 뒤, LLM이 자연어 분석 보고서를 생성합니다.

### 주요 기능

| 기능 | 설명 |
|:---:|------|
| 🎯 **전체 유사도 분석** | 두 안무 영상의 전체 유사도 점수 산출 |
| 🔍 **구간별 탐지** | 시간 구간별 유사 안무 구간 자동 탐지 |
| 🦴 **부위별 분석** | 왼팔, 오른팔, 왼다리, 오른다리, 몸통 부위별 유사도 |
| 📊 **AI 보고서** | GPT-5.1 기반 자연어 분석 보고서 자동 생성 |
| 📄 **PDF 내보내기** | 분석 결과를 PDF 보고서로 다운로드 |
| 👤 **분석 히스토리** | 과거 분석 기록 조회 및 상세 보기 |

프로젝트 시연 및 소개 영상 링크 : https://youtu.be/C7zSym6TCzI

---
## 👥 Team : Tenein
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
---

<div align="center">

**Tenein** — K-pop Visual Studio

2026 국민대학교 소프트웨어융합대학 캡스톤디자인

© 2026 Tenein Team

</div>
