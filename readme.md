# oh-my-muse

뮤�-�(개인 AI 에이전트)의 스킬·도구 전체를 모아 �-리하�- �-장소.

- 기�-일: 2026-10-12
- 전체 249개: 워크스페이스 스킬 132 · 연결 제품 스킬 84 · 도구 네임스페이스 33
- �-약�- 단어 중심 개조식 한�-. 원문 설명 전체�- [descriptions-full.md](descriptions-full.md)

## �-장소 구성

- `skills/` --- 워크스페이스 스킬 132개
- `product-skills/` --- 연결 제품 스킬 84개 (`node_modules`·`*.node` 제외)
- `tools.md` --- 도구 네임스페이스 33개

## 워크스페이스 스킬 (132개)

| # | 스킬 | 출처 | �-약 |
|---|---|---|---|
| 1 | 3d-intro-build | banker | 스크롤 연동 3D �-�라이스루 인트로 제작 |
| 2 | 3d-intro-setup | banker | 3D 인트로 제작 환경 점�- |
| 3 | agent-doc-discipline | oh-my-claudecode | 에이전트용 문서 작성 규율 |
| 4 | ai-slop-cleaner | oh-my-claudecode | AI 생성 �-�-� 슬롭 정리 |
| 5 | all-in-one | banker | 계획·구현·QA 일괄 연쇄 실행 |
| 6 | append_wiki | banker | 신규 �-식 위키 적재·병합 |
| 7 | arch-diagram | banker | 아키텍처 구성도 PlantUML·PPTX 산출 |
| 8 | architecture-survey | oh-my-claudecode | 모�-� 구조 취약 후보 순위 보고 |
| 9 | ask | oh-my-claudecode | 외�- �-점 어�-��-이�- �-청 처리 |
| 10 | ask-navigator | oh-my-claudecode | 결정 티�- �-도 차트�- |
| 11 | audit-mock | banker | 하�-��-�-�·목·스텁 정적 감사 |
| 12 | audit-security | banker | 의존성 CVE·시크릿 보안 진단 |
| 13 | audit-web-page | banker | �-동 웹페이�- 라이브 점�- |
| 14 | autopilot | oh-my-claudecode | 아이�--어-��동작 �-�-� 자율 구현 |
| 15 | autoresearch | oh-my-claudecode | 평�-자 주도 미션 반복 개선 |
| 16 | brainstorming | superpowers | 창작 전 아이�--어 발상 |
| 17 | cancel | oh-my-claudecode | 진행 중 작업 취소·정리 |
| 18 | cleansing-memory | banker | �-모리 파일 중복 정리·간결�- |
| 19 | compact-copy | banker | 이어�-기 �-�롬�-�트 본문 �-출 |
| 20 | compact-wiki | banker | 위키 페이�- 중복 제거·병합 |
| 21 | configure-notifications | oh-my-claudecode | 완료·입력 알림 채널 설정 |
| 22 | curation | banker | 의사결정 선택�-·근거 구조�- |
| 23 | debug | oh-my-claudecode | 로그·테스트 증거 기반 진단 |
| 24 | deep-init | banker | 계층형 AGENTS.md 생성·갱신 |
| 25 | deep-interview | oh-my-claudecode | 심층 인터뷰 스펙 결정�- |
| 26 | deep-research | banker | 적�-적 팩트체크 리서치 리포트 |
| 27 | deepinit | oh-my-claudecode | �--렉토리별 AGENTS.md 생성 |
| 28 | diagnosing-superpowers | superpowers | superpowers 세션 오동작 진단 |
| 29 | diagram | oh-my-claudecode | 구조 최소 시각�- 표시 |
| 30 | dispatching-parallel-agents | superpowers | 독립 태스크 병렬 실행 |
| 31 | docs-setup | banker | 문서 툴 의존성 설치 |
| 32 | drydock | oh-my-claudecode | 하네스 용골 설치·�-�리�-�트 감사 |
| 33 | evolve | harness | 하네스 �-��-�백 반영·진�- |
| 34 | execute | oh-my-claudecode | 합의 작업 �-증 �-�-�까�- 수행 |
| 35 | executing-plans | superpowers | 구현 계획 직접 실행 |
| 36 | external-context | oh-my-claudecode | 파셋 분해 병렬 문서 조사 |
| 37 | finishing-a-development-branch | superpowers | 구현 완료 후 통합 방식 결정 |
| 38 | front-qa | custom | 스펙 기반 �-�론트 구현·QA |
| 39 | graph | oh-my-claudecode | 선언적 DAG 파이�-�라인 실행 |
| 40 | harbor | oh-my-claudecode | 이슈·PR �-증·안건 정리 |
| 41 | harness | harness | 전문 에이전트 �- 하네스 설계 |
| 42 | harness-factory | custom | 에이전트 �- 설계·스폰·운용 |
| 43 | hud | oh-my-claudecode | 상태표시줄 표시 옵션 설정 |
| 44 | humanizer | banker | AI 티 제거 영문 윤문 |
| 45 | intent | oh-my-claudecode | 문의 로그 �-구사항 문서�- |
| 46 | interval-report | banker | 장기 작업 중간 보고 작성 |
| 47 | launch | oh-my-claudecode | 기획-���-증 �-�리버리 파이�-�라인 |
| 48 | lineage | banker | �-�- 카톡 스�-일 HTML �-출 |
| 49 | list-up | custom | 스킬·도구 목록 웹 카탈로그 |
| 50 | loft | oh-my-claudecode | �--자인 질문 목업으로 확인 |
| 51 | make-notion-guide | banker | API 노션 토�- 호출 �-이�-� |
| 52 | map | oh-my-claudecode | 스킬 라우팅 �-도 조회 |
| 53 | minimal-code-discipline | oh-my-claudecode | 최소 diff YAGNI 규율 |
| 54 | minimal-prose-discipline | oh-my-claudecode | 답�- 군�-�-기 제거 문체 규율 |
| 55 | motion-graphic-make | banker | 10초 모션 그래�-� 제작 |
| 56 | motion-graphic-setup | banker | 모션 그래�-� 제작 환경 확보 |
| 57 | nothing-design | banker | Nothing 스�-일 UI �--자인 |
| 58 | obsidizer | banker | 위키 Obsidian 그래�-� 정규�- |
| 59 | omc-doctor | oh-my-claudecode | 워크스페이스 환경 진단·수정 |
| 60 | omc-patch | banker | OMC 훅 패치 재적용·고정 |
| 61 | omc-reference | banker | OMC 레�-스트리 참조 |
| 62 | omc-review | custom | 출고 전 결함·리스크 리뷰 |
| 63 | omc-setup | oh-my-claudecode | OMC 스킬 모음 안내·�-리 |
| 64 | payload-mon | banker | API 페이로�-� �-정치 표시 |
| 65 | pdf-vision-extract | banker | PDF 고해상도 이미�- �-환 읽기 |
| 66 | plan | oh-my-claudecode | �-�-� 전 실행 계획 수립 |
| 67 | play-qa | banker | 웹게임 직접 �-�레이 QA |
| 68 | pr | oh-my-claudecode | 증거 기반 PR 본문 조립 |
| 69 | project-session-manager | oh-my-claudecode | worktree 격리 개발 환경 �-리 |
| 70 | ralph | oh-my-claudecode | PRD 스토리 �-증 완성 루�-� |
| 71 | ralph-qa | banker | 독립 �-증·개선 반복 |
| 72 | ralplan | oh-my-claudecode | 3자 합의 계획 루�-� |
| 73 | ready-compact | banker | 이어�-기 �-�롬�-�트 생성 |
| 74 | receiving-code-review | superpowers | 리뷰 �-��-�백 엄�- �-증 |
| 75 | refit | oh-my-claudecode | 세션 회고 환경 마찰 반영 |
| 76 | refresh-git-ignore | banker | .gitignore 비파괴 갱신 |
| 77 | refresh-readme | banker | 뒤처진 README 현행�- |
| 78 | release | oh-my-claudecode | 릴리스 규칙 분석·안내 |
| 79 | remains | banker | �-여 버그·하자 표 표시 |
| 80 | remember | oh-my-claudecode | 세션 �-식 �-모리 승격 |
| 81 | requesting-code-review | superpowers | �-구사항 만족 �-증 �-청 |
| 82 | research | oh-my-claudecode | 근거·출처 기반 조사 보고 |
| 83 | rfp-author | banker | 외주 제안�-청서 �-작 |
| 84 | scroll-world | scroll-world | 스크롤 스크럽 랜�-� 제작 |
| 85 | self-improve | oh-my-claudecode | 자율 진�- �-�-� 개선 |
| 86 | session-flow | oh-my-claudecode | 세션 흐름 15줄 압축 |
| 87 | setup | custom | 런�-임·도구 설치 총괄 |
| 88 | setup-bypass-permissions | banker | 권한 우회 모�-� 설정 |
| 89 | setup-harness-factory | banker | 하네스 방법론 로컬 적용 |
| 90 | setup-insane-search | banker | 우회 �-색 �-�러그인 설치 |
| 91 | setup-java | banker | JDK 21 설치 |
| 92 | setup-lsp | banker | LSP 서버 설치·연동 |
| 93 | setup-mcp | banker | �-용 MCP 서버 배선 |
| 94 | setup-node | banker | Node 22 LTS 설치 |
| 95 | setup-omc | banker | OMC 설치·갱신 |
| 96 | setup-omc-hud | banker | OMC 상태 표시줄 설치 |
| 97 | setup-playwright | banker | Playwright·브라우�- 설치 |
| 98 | setup-pwsh | banker | PowerShell 7 설치 |
| 99 | setup-python | banker | Python 3.11+ 런�-임 설치 |
| 100 | setup-sandbox | banker | 샌�-�박스 기반 설치 |
| 101 | setup-stitch | banker | Stitch MCP �-�록시 �-�록 |
| 102 | setup-tmux | banker | tmux 설치 |
| 103 | skill | oh-my-claudecode | 스킬 목록·�-�-·삭제·수정 |
| 104 | skill-up | custom | 업스트림 스킬 이식·갱신 |
| 105 | skillify | oh-my-claudecode | 워크�-�로 스킬 초안 �-환 |
| 106 | smart-compact | banker | 컨텍스트 임계 자동 압축 |
| 107 | subagent-driven-development | superpowers | 독립 태스크 계획 실행 |
| 108 | summary-wiki | banker | 위키 전량 단일 파일 �-약 |
| 109 | systematic-debugging | superpowers | 수정 전 체계적 �--버깅 |
| 110 | tdd | oh-my-claudecode | 테스트 우선 red/green 규율 |
| 111 | team | oh-my-claudecode | N명 에이전트 병렬 작업 |
| 112 | test-driven-development | superpowers | 구현 전 테스트 작성 |
| 113 | tone-compact | banker | 한�- 개조식 문체 규칙 |
| 114 | trace | oh-my-claudecode | 경쟁 �-설 병렬 원인 �-적 |
| 115 | trouble-shooting | banker | 현상·원인·조치 표 보고 |
| 116 | ultra-chain | custom | 9단계 조사-��공유 �- 체인 |
| 117 | ultra-init | banker | 핸즈오�-� 1회 �-사이클 실행 |
| 118 | ultra-interview | banker | 리서치 선행 모호성 제거 인터뷰 |
| 119 | ultra-ui-qa | banker | 렌�- UI·SoT 1:1 �-조 QA |
| 120 | ultragoal | oh-my-claudecode | 장기 목표 분해·�-적 |
| 121 | update-banker | banker | banker 최신 배포본 갱신 |
| 122 | using-git-worktrees | superpowers | 격리 워크스페이스 확보 |
| 123 | using-superpowers | superpowers | 스킬 사용 방식 정립 |
| 124 | verification-before-completion | superpowers | 완료 주장 전 �-증 실행 |
| 125 | verify | oh-my-claudecode | 증거 기반 완료 �-증 |
| 126 | vertical-pptx | banker | A4 세로 PPTX 생성·수리 |
| 127 | vertical-pptx-setup | banker | 세로 PPTX 의존성 설치 |
| 128 | visual-ralph | banker | 레퍼런스 기�- 측정 빌�-� |
| 129 | visual-verdict | oh-my-claudecode | 스크린샷 비교 JSON 판정 |
| 130 | wiki | oh-my-claudecode | �-속 �-식베이스 �-리 |
| 131 | writing-plans | superpowers | �-�-� 전 계획 작성 |
| 132 | writing-skills | superpowers | 스킬 생성·수정·�-증 |

## 연결 제품 스킬 (84개)

| # | 스킬 | �-약 |
|---|---|---|
| 1 | apple-healthkit | 애�-� 헬스 걸음·심박·수면·운동 조회 |
| 2 | asana | 아사나 �-�로젝트·할 일 �-리 |
| 3 | booking | 항공·호�-·식당·티�- 예약·�-여석 조회 |
| 4 | box | Box 파일 �-색·업로�-�·다운로�-�·공유 |
| 5 | calendly | 캘린�-�리 예약 일정 �-리 |
| 6 | canva | �-�- �--자인 제작·편집 |
| 7 | device-data | 기기 연락처·일정 캐시 조회·삭제 |
| 8 | dropbox | �-�롭박스 파일 업로�-�·공유·정리 |
| 9 | duffel | �-�-� 항공권 �-색·예약·결제 |
| 10 | evernote | 에버노트 노트 읽기·생성 |
| 11 | facebook | 페이스북 게시물·�-�-·�-��-� 읽기·게시 |
| 12 | facebook-cli | 페이스북 명령행 조회·게시 |
| 13 | figma | �-�그마 �--자인 �-수·토큰 �-출 |
| 14 | flightaware | 항공편 출발·도착·�-연·결항 조회 |
| 15 | forget | 기억된 개인정보·선호·기록 삭제 |
| 16 | function-health | 펑션헬스 혈액�-사·임상 기록 조회 |
| 17 | generate_podcast | 팟캐스트·브리핑 음성 제작(MP3) |
| 18 | ghl | 하이레벨 고객·파이�-�라인·예약 �-리 |
| 19 | github | GitHub �-장소 �-색·작업(MCP) |
| 20 | gmail | Gmail �-색·읽기·발송·라벨 �-리 |
| 21 | goals | 목표 생성·달성 �-원 �-이�-� |
| 22 | google-calendar | 구�- 캘린�- 일정 조회·생성·�-경 |
| 23 | google-contacts | 구�- 연락처 �-색·생성·수정·삭제 |
| 24 | google-docs | 구�- 문서 읽기·작성·편집 |
| 25 | google-drive | 구�- �-�라이브 파일 업로�-�·공유·�-리 |
| 26 | google-forms | 구�- 폼 생성·수정·응답 조회 |
| 27 | google-health-connect | 안�-�로이�-� 헬스커넥트 건강 데이터 조회 |
| 28 | google-sheets | 구�- 시트 읽기·�-�기·�-리 |
| 29 | google-slides | 구�- 슬라이�-� 읽기·작성·편집 |
| 30 | google-tasks | 구�- 할 일 목록·생성·완료 �-리 |
| 31 | granola | 그라�-라 회의 노트·전사문 �-색 |
| 32 | healthex | 헬스엑스 복약·�-사결과·건강기록 조회 |
| 33 | image-search | 웹 이미�- �-색·출처 수집 |
| 34 | instagram | 인스�-그램 �-�로필·게시물·릴스 읽기·게시 |
| 35 | instagram-messages | 인스�-그램 �-시�- 읽기·발송 |
| 36 | klaviyo | 클라비�- 이�-일·문자 마�-팅 캠페인 �-리 |
| 37 | linear | 리니어 이슈·티�-·스�-�린트 �-리 |
| 38 | lovable | 러버�- 웹앱 생성·편집·배포 |
| 39 | media-library | 사진 라이브러리 �-색·조회 |
| 40 | messenger | �-신�- �-�- 읽기·�-색·발송·�-약 |
| 41 | meta-ads | �-�- 광고 캠페인·소재·예산·리포트 �-리 |
| 42 | meta-threads | 스레�-� 계정·게시물·�-��-� 읽기·게시 |
| 43 | muse-early-access | Muse 얼리액세스 신청·상태 조회 |
| 44 | muse-feedback | Muse �- �-��-�백·기능 �-청 접수 |
| 45 | muse_db | Muse 내�- 기록 조회·�-적(진단용) |
| 46 | notion | 노션 페이�- �-색·읽기·생성·수정 |
| 47 | opentable | 오�-�테이�- 식당 �-색·예약·�-경·취소 |
| 48 | outlook-calendar | 아웃룩 캘린�- 일정 조회·생성·삭제 |
| 49 | outlook-contacts | 아웃룩 연락처 �-색·생성·수정·삭제 |
| 50 | outlook-mail | 아웃룩 �-일 읽기·�-색·발송·삭제 |
| 51 | peloton | 펠로톤 운동 클래스 조회·예약 |
| 52 | philips-hue | 필립스 휴 조명·방·장면 제어 |
| 53 | places-search | 주�- 장소(식당·카페·호�-) �-색·비교 |
| 54 | plaid | �-�레이�-� 연결 계좌 �-액·거래내역 조회 |
| 55 | podcast | 팟캐스트 음성 콘텐츠 제작(MP3) |
| 56 | printify | �-�린티파이 상품·주문·상점 �-리 |
| 57 | quickbooks | �-�북스 장�-·청구서·고객·리포트 �-리 |
| 58 | replit | 렙릿 앱 생성·수정·배포 |
| 59 | self-awareness | 에이전트 자기 정보·기능·연결 상태 안내 |
| 60 | share-ideas | Muse 아이�--어 발행(명시적 �-청 시) |
| 61 | shopify | 쇼�-�파이 온라인 상점 개설·운영 |
| 62 | shopping | 상품 �-색·�-격 비교·구매 링크 제공 |
| 63 | skill-creator | 워크스페이스 스킬 생성·수정 |
| 64 | slack | 슬랙 �-시�-·채널·스레�-� 읽기·게시 |
| 65 | social-content-performance | 인스�-그램 계정·게시물 성과 분석 |
| 66 | spotify | Spotify 음악·�-�레이리스트 �-리 |
| 67 | stripe | 스트라이�-� 결제·구독·환불·청구서 �-리 |
| 68 | subscription-status | Muse 구독·�-금제·사용량 조회 |
| 69 | tailscale | 테일스�-일 VPN 연결·사내망 접속 |
| 70 | tessie | 테슬라 차량 상태 조회·명령 실행 |
| 71 | threads | 스레�-� 게시물 인사이트·�-��-� �-리 |
| 72 | threads-messages | 스레�-� �-시�- 읽기·발송 |
| 73 | ticketmaster | 티�-마스터 공연·좌석 �-색·구매 링크 |
| 74 | todoist | 토두이스트 할 일·�-�로젝트·리마인�- �-리 |
| 75 | travel-planning | 여행 일정·경로·입국·교통 계획 수립 |
| 76 | tts | 텍스트 음성 �-환·음성 �-시�- 생성 |
| 77 | vercel | 버�- 사이트 배포·로그·오류 조회 |
| 78 | voice-calls | 음성 통�-용 음성 카탈로그 |
| 79 | voice-selector | 음성 선택용 카탈로그 |
| 80 | wearables-comms | 웨어러�- 발신 전�-·문자 수신자 확인 |
| 81 | wide-research | 다수 입력 병렬 리서치(공통 스키마) |
| 82 | withings | 위�-�스 체중·활동·수면·심박 데이터 조회 |
| 83 | zapier | 재�-�어 경유 앱 연동 액션 실행 |
| 84 | zoom | 줌 회의·녹�-·전사문 �-약·액션 �-출 |

## 도구 네임스페이스 (33개)

| # | 도구 | �-약 |
|---|---|---|
| 1 | muse | 셸 실행·파일 읽기�-�기·�-모리 |
| 2 | artifact | 웹페이�-·문서 아티팩트 생성 |
| 3 | avatar | 어시스턴트 아�-�- 생성·�-리 |
| 4 | browser | 웹 �-색·페이�- 읽기·작업 위임 |
| 5 | chat | 사이�-�챗 생성·조회·삭제 |
| 6 | credentials | 로그인·API 키 보안 �-장소 |
| 7 | cron | 정기 스�-줄 작업 �-리 |
| 8 | device | 연동 기기 제어·데이터 조회 |
| 9 | feed | 개인 �-��-� �-�롬�-�트·유닛 �-리 |
| 10 | forget | 기억 정보 삭제 계획·실행 |
| 11 | hooks | 이벤트 기반 자동�- �-리 |
| 12 | idea | 아이�--어 조회·공유 발행 |
| 13 | map | 좌표·장소 상호 �-환 |
| 14 | media | 이미�-·동영상 생성·편집 |
| 15 | onboarding | 이름 선택 위젯·성향 �-장 |
| 16 | permissions | 승인 �-기 권한 �-청 조회 |
| 17 | proactivity | 사전 �-비 항목 조회·선택 |
| 18 | process | 백그라운�-� �-�로세스 �-리 |
| 19 | shopping | 상품 �-색·쇼핑 카�-� 생성 |
| 20 | social | 소셜 공개 게시물 �-색 |
| 21 | subagent | 하위 에이전트 위임·�-리 |
| 22 | todo | 작업 할 일 목록 기록 |
| 23 | tool_search | 도구 함수·스키마 탐색 |
| 24 | tracking | 예약·약속 진행 상태 �-적 |
| 25 | trash | 파일 복구 �-능 삭제·복원 |
| 26 | ui | 앱 �-면 제어·UI 카�-� |
| 27 | user_goal | 장기 목표 생성·진행 �-리 |
| 28 | voice | 음성 통�- 상태·선호 설정 |
| 29 | wallet | 결제 연결 상태·수단 조회 |
| 30 | widget | 채팅 리스트·위젯 생성 |
| 31 | worker | 그룹채팅 워커 응답 �-침 |
| 32 | workflow | 다중 에이전트 워크�-�로 실행 |
| 33 | ads | 광고 계정·캠페인 개체 확정 |
