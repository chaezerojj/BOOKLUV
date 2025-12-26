# 📖BOOKLUV

## 프로젝트 개요
- 설명 : AI API 기반 도서 추천 및 실시간 모임 서비스
- 기간 : 2025.12.19 - 2025.12.26

- 목표 서비스 : 카카오 api 기반 로그인+ AI API 기반 도서 추천 기능 + 실시간 채팅+실시간 알림 + 자유게시판 및 댓글알라딘 api 기반의 양질 데이터셋
실제 구현 정도
- 추가적인 성과 : Netlify+Railway 기반의 풀스택 배포 / SQLite에서 PostgreSQL로 마이그레이션해서 DB 안정성 높임

## 서비스 특징
- Kakao API 기반 소셜 로그인 
- ChatGPT 4o mini 기반 도서 추천 
- WebSocket 및 Django Channels, Redis 기반 실시간 채팅 
- WebSocket, Django Channels, Django Selery 기반 알림

## 주요 기능
- Kakao API 기반 소셜 로그인 
- ChatGPT 4o mini 기반 도서 및 모임 추천
- WebSocket 및 Django Channels, Redis 기반 실시간 채팅 
- WebSocket, Django Channels, Django Selery 기반 알림 및 채팅방 생성
- 자유 게시판 및 댓글 CRUD

## 팀 소개
| 이름 | 역할 | 맡은 기능 |
|--------|--------|--------|
| ![145894536](https://github.com/user-attachments/assets/5901db01-81cb-40d6-a588-d3f77ccfbf42) | Frontend | - 와이어 프레임 및 UXUI 설계 / 프론트엔드(Vue) 전반 / Netlify 배포 |
| ![김수미](https://github.com/user-attachments/assets/3f2322b3-12be-4ce0-b268-69a7c2f13c62) | Backend | - OAuth 2.0 기반 Kakao 소셜 로그인 인증 시스템 구현 / 마이페이지, 자유게시판 및 댓글 구현 |
| ![엄송현](https://github.com/user-attachments/assets/ad19a243-e8d1-4cc6-bcf2-7ec4c3cb8db7) | Backend | - GPT-4o-mini API 기반 추천 서비스 구현 / WebSocket, Redis 기반 실시간 채팅 구현 / WebSocket, Celery 기반 실시간 알림 구현 / Railway 배포 |

## 커밋 규칙 및 이행 화면
### 📌 Git rules

- `feat` : 새로운 기능 추가
- `fix` : 버그 수정
- `refactor` : 코드 리팩터링 (기능 변경 없음)
- `style` : CSS, UI 스타일 작업
- `docs` : 문서 수정(README 등)
- `test` : 테스트 코드 수정
- `chore` :	빌드/의존성/기타 작업
<img width="623" height="406" alt="스크린샷 2025-12-25 오후 7 21 33" src="https://github.com/user-attachments/assets/3e2fa48b-ee2e-4263-82f3-1a3b909a8ad3" />

## 기술스택
### Frontend
<img src="https://img.shields.io/badge/vue.js-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white"> <img src="https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white"> <img src="https://img.shields.io/badge/pinia-3B82F6?style=for-the-badge&logo=vue.js&logoColor=white"> <img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=white"> 
### Backend
<img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white"> <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/websocket-010101?style=for-the-badge&logo=socket.io&logoColor=white"> <img src="https://img.shields.io/badge/redis-DC382D?style=for-the-badge&logo=redis&logoColor=white"> <img src="https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white"> <img src="https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=Celery&logoColor=white"> <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white"> 
### DevOps
<img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white"> <img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white"> <img src="https://img.shields.io/badge/Netlify-00C7B7?style=for-the-badge&logo=netlify&logoColor=white"> <img src="https://img.shields.io/badge/Railway-131415?style=for-the-badge&logo=railway&logoColor=white">
### Tools
<img src="https://img.shields.io/badge/notion-000000?style=for-the-badge&logo=notion&logoColor=white"> <img src="https://img.shields.io/badge/vscode-0078d4?style=for-the-badge&logo=visual-studio-code&logoColor=white"> <img src="https://img.shields.io/badge/figma-F24E1E?style=for-the-badge&logo=figma&logoColor=white">
### 전체 서비스 구조
<img width="1805" height="1009" alt="image" src="https://github.com/user-attachments/assets/91f563ba-092f-46af-bd6a-a308d3d867ac" />



## 개발환경
### Frontend
- vue.js 3.5.25
- vite 7.2.7
- vue-router 4.6.3
- pinia 3.0.4
- pinia-plugin-persistedstate 4.7.1
- axios 1.13.2
- swiper 12.0.3
- @vitejs/plugin-vue 6.0.2
- vite-plugin-vue-devtools 8.0.5
- Netlify
### Backend
- django 4.2.27
- WebSocket 25.5.0
- Redis 5.0.1
- Daphne 4.0.0
- docker 29.1.3
- docker compose 2.40.3
## 프로젝트 폴더 구조
### Frontend - Vue.js
```
frontend/
├── node_modules/
├── public/
├── App.vue
├── main.js
└── src/                     # 프론트엔드 메인 소스 디렉터리
    ├── api/                 # 백엔드 API 통신 모듈
    ├── assets/              # 이미지, 스타일 등 정적 리소스
    ├── components/          # 공통 컴포넌트
    ├── router/              # Vue Router 설정
    ├── stores/              # 상태 관리 (Pinia/Vuex)
    └── views/               # 페이지 단위 컴포넌트
```
### Backend - Django
```
backend/
├── klub_chat/ # 채팅 기능 관련 앱
├── klub_talk/ # 도서 관련 기능 앱
├── klub_user/ # 사용자 관리 기능 앱
├── klub_recommend/ # 추천 시스템 관련 앱
└── manage.py # Django 관리 명령어 실행을 위한 파일
```

## 사용 API
```
1. Kakao 소셜 로그인/회원가입 API
- 인가 요청 및 토큰 발급을 통한 소셜 로그인 API
2. 알라딘 도서 검색 API
- 알라딘 베스트셀러 검색을 통한 DB 구축
3. GPT 4o mini API
- 도서 추천 기능을 위한 소형 멀티모달 AI API 
```

## ERD
https://dbdiagram.io/d/69323b5dd6676488baac0293

## 기능 상세 설명 및 화면
### 1. 메인 페이지
### 2. 카카오 API 기반의 소셜 로그인 / 회원가입
- 카카오 소셜 로그인 API 기반의 토큰 인증 로그인 기능

### 2. AI 기반 도서 추천 기능
- GPT-4o-mini API 기반의 도서 추천 기능

### 3. 알라딘 API 기반 도서 목록
- Aladin 도서 검색 및 상품 목록 API 기반의 데이터셋 활용

### 4. 모임방 목록 및 참가 신청
- 도서 데이터셋 기반의 독서 모임 CRUD
  
### 5. 실시간 알림 및 다대다 채팅
- WebSocket, Redis, Celery 기반의 실시간 알람 및  채팅 기능

### 6. 자유게시판 및 댓글 CRUD
- 유저들의 소통을 위한 게시판 및 댓글 CRUD

### 7. 마이페이지 및 회원정보 수정
- 회원정보 수정 및 현재 참여중인 채팅방 목록


