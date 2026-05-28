# CLAUDE.md — Frontend (React + Vite)

## 개요

React 18 + Vite 5 기반 SPA. 영상 업로드, 분석 결과 표시, PDF 보고서 생성을 담당한다.

## 실행 방법

```bash
cd frontend
npm install
npm run dev       # localhost:5173
npm run build     # dist/ 생성
```

### 환경 변수 (.env)
```
VITE_SUPABASE_URL=https://xxx.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhb...
```

## 디자인 시스템: "Emerald Luxe"

### 컬러 토큰
```javascript
const C = {
  deep: "#0B3B2E",          // 딥 포레스트 (텍스트, 버튼 배경)
  forest: "#13513F",        // 포레스트 그린 (그라디언트 중간)
  emerald: "#2E8B57",       // 에메랄드 (액센트, 아이콘)
  emeraldLight: "#3CB371",  // 라이트 에메랄드 (그라디언트 끝)
  mint: "#7FE3B5",          // 민트 (글로우, 배지, 프로그레스)
  mintSoft: "#C8F2DC",      // 소프트 민트 (배경 틴트)
  text: "#0E2A20",          // 본문 텍스트
  textSoft: "#3B5A4B",      // 보조 텍스트
};
```

### 스타일 패턴
- **Glassmorphism**: `backdrop-filter: blur(28px~36px) saturate(170%~180%)`, 반투명 그라디언트 배경
- **카드**: `border-radius: 20px~36px`, `border: 1px solid rgba(255,255,255,0.8)`, 다층 box-shadow
- **Sheen**: 카드 상단 1px 하이라이트 라인 (`linear-gradient 90deg`)
- **Glow**: 카드 뒤 `radial-gradient` + `filter: blur(40px~60px)`
- **버튼**: `border-radius: 999px`, deep→forest→emerald 그라디언트, inset 하이라이트
- **타이포**: Chakra Petch (제목, 700), Rajdhani (본문, 500/700)
- **배경**: 페이지별 배경 이미지 (`background.png`, `profile_background.png`) + radial-gradient 오버레이

### 스타일 구현
- CSS-in-JS (인라인 스타일 객체 `styles = { ... }`)
- CSS 모듈/Tailwind 미사용
- Google Fonts는 `<link>` 태그로 컴포넌트 내 직접 삽입

## 페이지 구조

### App.jsx — 라우팅
- state 기반 페이지 전환 (`useState("login")`)
- `navigate(target)`: "home" → login, 나머지 → 해당 페이지
- `handleAnalyze(videoAId, videoBId)`: `/api/analyze` 호출 → loading → result

### 페이지 컴포넌트

| 페이지 | 파일 | 주요 props |
|--------|------|-----------|
| Login | `Login.jsx` | `onLogin` |
| Home (분석) | `home_page.jsx` | `onNavigate`, `onAnalyze` |
| Loading | `loading_page.jsx` | (없음) |
| Result | `result_page.jsx` | `onNavigate`, `result` |
| Profile | `profile_page.jsx` | `onNavigate` |
| About | `about_us_page.jsx` | `onNavigate` |

### 네비게이션
- 모든 페이지에 공통 `<nav>` (Home, About us, Analyse, Profile)
- `activeNav` state로 현재 활성 탭 표시
- `onNavigate(key)` 콜백으로 App.jsx에 페이지 전환 위임

## 핵심 유틸리티

### generatePDF.jsx

@react-pdf/renderer를 사용한 브라우저 내 PDF 생성.

**구조:**
1. 폰트 등록 (NotoSansKR, `/public/fonts/` 로컬 서빙)
2. 영상 프레임 순차 캡처 (`captureFramesFromVideo`)
3. 데이터 정규화 (`normalizeData` — 듀얼 경로)
4. PDF 페이지 조합: CoverPage → SummaryPage → SegmentsPage → FooterPage
5. Blob 생성 → 자동 다운로드

**normalizeData 듀얼 경로:**
- `raw.overall` 존재 시: ResultPage에서 호출 (API 응답 직접 소비)
- `raw.overall` 없을 시: ProfilePage 히스토리에서 호출 (저장된 result_data 소비)
- **두 경로 모두에 `parseTimeStr` 등 변환 로직 적용 필요**

**알려진 제약:**
- Yoga 레이아웃 엔진: absolute Image는 흐름 공간을 차지함 → `height: 0, overflow: visible` 래퍼 사용
- Google Fonts CORS 차단 → NotoSansKR TTF를 `public/fonts/`에 로컬 배치
- `Buffer is not defined` → `main.jsx`에 폴리필 필요 (buffer 패키지)
- 영상 스크린샷: 단일 video 엘리먼트로 순차 처리 (병렬 시 동일 프레임 반환)

### supabaseClient.js

```javascript
import { createClient } from "@supabase/supabase-js";
const supabase = createClient(VITE_SUPABASE_URL, VITE_SUPABASE_ANON_KEY);
```

## 주요 의존성

```json
{
  "@react-pdf/renderer": "^4.5.1",
  "@supabase/supabase-js": "^2.103.0",
  "buffer": "^6.0.3",
  "react": "^19.2.4",
  "react-dom": "^19.2.4"
}
```

## 주의사항

- Backend URL은 `App.jsx`에 하드코딩 (`http://localhost:8000`) — 배포 시 변경 필요
- `home_page.jsx`의 `handleAnalyze`에 `|| True` 오타 존재 (Python 구문)
- `result_page.jsx`에 `RESULT.metrics` / `RESULT.segments` 미정의 변수 참조 존재 (mock 제거 불완전)
- PDF 배경 이미지: `assets/pdf-cover-bg.png`, `assets/pdf-body-bg.png`
- 모바일 반응형: `useIsMobile` 훅 사용
