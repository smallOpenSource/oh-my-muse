# oh-my-muse

뮤씨(개인 AI 에이전트)의 스킬·도구 전체를 모아 관리하는 저장소.

- 기준일: 2026-10-12
- 전체 249개: 워크스페이스 스킬 132 · 연결 제품 스킬 84 · 도구 네임스페이스 33
- 요약은 단어 중심 개조식 한글. 원문 설명 전체는 [descriptions-full.md](descriptions-full.md)

## 저장소 구성

- `skills/` — 워크스페이스 스킬 132개
- `product-skills/` — 연결 제품 스킬 84개 (`node_modules`·`*.node` 제외)
- `tools.md` — 도구 네임스페이스 33개

## 워크스페이스 스킬 (132개)

| # | 스킬 | 출처 | 요약 |
|---|---|---|---|
| 1 | 3d-intro-build | banker | 스크롤 연동 3D 플라이스루 인트로 제작 |
| 2 | 3d-intro-setup | banker | 3D 인트로 제작 환경 점검 |
| 3 | agent-doc-discipline | oh-my-claudecode | 에이전트용 문서 작성 규율 |
| 4 | ai-slop-cleaner | oh-my-claudecode | AI 생성 코드 슬롭 정리 |
| 5 | all-in-one | banker | 계획·구현·QA 일괄 연쇄 실행 |
| 6 | append_wiki | banker | 신규 지식 위키 적재·병합 |
| 7 | arch-diagram | banker | 아키텍처 구성도 PlantUML·PPTX 산출 |
| 8 | architecture-survey | oh-my-claudecode | 모듈 구조 취약 후보 순위 보고 |
| 9 | ask | oh-my-claudecode | 외부 관점 어드바이저 요청 처리 |
| 10 | ask-navigator | oh-my-claudecode | 결정 티켓 지도 차트화 |
| 11 | audit-mock | banker | 하드코딩·목·스텁 정적 감사 |
| 12 | audit-security | banker | 의존성 CVE·시크릿 보안 진단 |
| 13 | audit-web-page | banker | 가동 웹페이지 라이브 점검 |
| 14 | autopilot | oh-my-claudecode | 아이디어→동작 코드 자율 구현 |
| 15 | autoresearch | oh-my-claudecode | 평가자 주도 미션 반복 개선 |
| 16 | brainstorming | superpowers | 창작 전 아이디어 발상 |
| 17 | cancel | oh-my-claudecode | 진행 중 작업 취소·정리 |
| 18 | cleansing-memory | banker | 메모리 파일 중복 정리·간결화 |
| 19 | compact-copy | banker | 이어가기 프롬프트 본문 추출 |
| 20 | compact-wiki | banker | 위키 페이지 중복 제거·병합 |
| 21 | configure-notifications | oh-my-claudecode | 완료·입력 알림 채널 설정 |
| 22 | curation | banker | 의사결정 선택지·근거 구조화 |
| 23 | debug | oh-my-claudecode | 로그·테스트 증거 기반 진단 |
| 24 | deep-init | banker | 계층형 AGENTS.md 생성·갱신 |
| 25 | deep-interview | oh-my-claudecode | 심층 인터뷰 스펙 결정화 |
| 26 | deep-research | banker | 적대적 팩트체크 리서치 리포트 |
| 27 | deepinit | oh-my-claudecode | 디렉토리별 AGENTS.md 생성 |
| 28 | diagnosing-superpowers | superpowers | superpowers 세션 오동작 진단 |
| 29 | diagram | oh-my-claudecode | 구조 최소 시각화 표시 |
| 30 | dispatching-parallel-agents | superpowers | 독립 태스크 병렬 실행 |
| 31 | docs-setup | banker | 문서 툴 의존성 설치 |
| 32 | drydock | oh-my-claudecode | 하네스 용골 설치·드리프트 감사 |
| 33 | evolve | harness | 하네스 피드백 반영·진화 |
| 34 | execute | oh-my-claudecode | 합의 작업 검증 코드까지 수행 |
| 35 | executing-plans | superpowers | 구현 계획 직접 실행 |
| 36 | external-context | oh-my-claudecode | 파셋 분해 병렬 문서 조사 |
| 37 | finishing-a-development-branch | superpowers | 구현 완료 후 통합 방식 결정 |
| 38 | front-qa | custom | 스펙 기반 프론트 구현·QA |
| 39 | graph | oh-my-claudecode | 선언적 DAG 파이프라인 실행 |
| 40 | harbor | oh-my-claudecode | 이슈·PR 검증·안건 정리 |
| 41 | harness | harness | 전문 에이전트 팀 하네스 설계 |
| 42 | harness-factory | custom | 에이전트 팀 설계·스폰·운용 |
| 43 | hud | oh-my-claudecode | 상태표시줄 표시 옵션 설정 |
| 44 | humanizer | banker | AI 티 제거 영문 윤문 |
| 45 | intent | oh-my-claudecode | 문의 로그 요구사항 문서화 |
| 46 | interval-report | banker | 장기 작업 중간 보고 작성 |
| 47 | launch | oh-my-claudecode | 기획→검증 딜리버리 파이프라인 |
| 48 | lineage | banker | 대화 카톡 스타일 HTML 추출 |
| 49 | list-up | custom | 스킬·도구 목록 웹 카탈로그 |
| 50 | loft | oh-my-claudecode | 디자인 질문 목업으로 확인 |
| 51 | make-notion-guide | banker | API 노션 토글 호출 가이드 |
| 52 | map | oh-my-claudecode | 스킬 라우팅 지도 조회 |
| 53 | minimal-code-discipline | oh-my-claudecode | 최소 diff YAGNI 규율 |
| 54 | minimal-prose-discipline | oh-my-claudecode | 답글 군더더기 제거 문체 규율 |
| 55 | motion-graphic-make | banker | 10초 모션 그래픽 제작 |
| 56 | motion-graphic-setup | banker | 모션 그래픽 제작 환경 확보 |
| 57 | nothing-design | banker | Nothing 스타일 UI 디자인 |
| 58 | obsidizer | banker | 위키 Obsidian 그래프 정규화 |
| 59 | omc-doctor | oh-my-claudecode | 워크스페이스 환경 진단·수정 |
| 60 | omc-patch | banker | OMC 훅 패치 재적용·고정 |
| 61 | omc-reference | banker | OMC 레지스트리 참조 |
| 62 | omc-review | custom | 출고 전 결함·리스크 리뷰 |
| 63 | omc-setup | oh-my-claudecode | OMC 스킬 모음 안내·관리 |
| 64 | payload-mon | banker | API 페이로드 추정치 표시 |
| 65 | pdf-vision-extract | banker | PDF 고해상도 이미지 변환 읽기 |
| 66 | plan | oh-my-claudecode | 코딩 전 실행 계획 수립 |
| 67 | play-qa | banker | 웹게임 직접 플레이 QA |
| 68 | pr | oh-my-claudecode | 증거 기반 PR 본문 조립 |
| 69 | project-session-manager | oh-my-claudecode | worktree 격리 개발 환경 관리 |
| 70 | ralph | oh-my-claudecode | PRD 스토리 검증 완성 루프 |
| 71 | ralph-qa | banker | 독립 검증·개선 반복 |
| 72 | ralplan | oh-my-claudecode | 3자 합의 계획 루프 |
| 73 | ready-compact | banker | 이어가기 프롬프트 생성 |
| 74 | receiving-code-review | superpowers | 리뷰 피드백 엄밀 검증 |
| 75 | refit | oh-my-claudecode | 세션 회고 환경 마찰 반영 |
| 76 | refresh-git-ignore | banker | .gitignore 비파괴 갱신 |
| 77 | refresh-readme | banker | 뒤처진 README 현행화 |
| 78 | release | oh-my-claudecode | 릴리스 규칙 분석·안내 |
| 79 | remains | banker | 잔여 버그·하자 표 표시 |
| 80 | remember | oh-my-claudecode | 세션 지식 메모리 승격 |
| 81 | requesting-code-review | superpowers | 요구사항 만족 검증 요청 |
| 82 | research | oh-my-claudecode | 근거·출처 기반 조사 보고 |
| 83 | rfp-author | banker | 외주 제안요청서 저작 |
| 84 | scroll-world | scroll-world | 스크롤 스크럽 랜딩 제작 |
| 85 | self-improve | oh-my-claudecode | 자율 진화 코드 개선 |
| 86 | session-flow | oh-my-claudecode | 세션 흐름 15줄 압축 |
| 87 | setup | custom | 런타임·도구 설치 총괄 |
| 88 | setup-bypass-permissions | banker | 권한 우회 모드 설정 |
| 89 | setup-harness-factory | banker | 하네스 방법론 로컬 적용 |
| 90 | setup-insane-search | banker | 우회 검색 플러그인 설치 |
| 91 | setup-java | banker | JDK 21 설치 |
| 92 | setup-lsp | banker | LSP 서버 설치·연동 |
| 93 | setup-mcp | banker | 범용 MCP 서버 배선 |
| 94 | setup-node | banker | Node 22 LTS 설치 |
| 95 | setup-omc | banker | OMC 설치·갱신 |
| 96 | setup-omc-hud | banker | OMC 상태 표시줄 설치 |
| 97 | setup-playwright | banker | Playwright·브라우저 설치 |
| 98 | setup-pwsh | banker | PowerShell 7 설치 |
| 99 | setup-python | banker | Python 3.11+ 런타임 설치 |
| 100 | setup-sandbox | banker | 샌드박스 기반 설치 |
| 101 | setup-stitch | banker | Stitch MCP 프록시 등록 |
| 102 | setup-tmux | banker | tmux 설치 |
| 103 | skill | oh-my-claudecode | 스킬 목록·추가·삭제·수정 |
| 104 | skill-up | custom | 업스트림 스킬 이식·갱신 |
| 105 | skillify | oh-my-claudecode | 워크플로 스킬 초안 변환 |
| 106 | smart-compact | banker | 컨텍스트 임계 자동 압축 |
| 107 | subagent-driven-development | superpowers | 독립 태스크 계획 실행 |
| 108 | summary-wiki | banker | 위키 전량 단일 파일 요약 |
| 109 | systematic-debugging | superpowers | 수정 전 체계적 디버깅 |
| 110 | tdd | oh-my-claudecode | 테스트 우선 red/green 규율 |
| 111 | team | oh-my-claudecode | N명 에이전트 병렬 작업 |
| 112 | test-driven-development | superpowers | 구현 전 테스트 작성 |
| 113 | tone-compact | banker | 한글 개조식 문체 규칙 |
| 114 | trace | oh-my-claudecode | 경쟁 가설 병렬 원인 추적 |
| 115 | trouble-shooting | banker | 현상·원인·조치 표 보고 |
| 116 | ultra-chain | custom | 9단계 조사→공유 풀 체인 |
| 117 | ultra-init | banker | 핸즈오프 1회 풀사이클 실행 |
| 118 | ultra-interview | banker | 리서치 선행 모호성 제거 인터뷰 |
| 119 | ultra-ui-qa | banker | 렌더 UI·SoT 1:1 대조 QA |
| 120 | ultragoal | oh-my-claudecode | 장기 목표 분해·추적 |
| 121 | update-banker | banker | banker 최신 배포본 갱신 |
| 122 | using-git-worktrees | superpowers | 격리 워크스페이스 확보 |
| 123 | using-superpowers | superpowers | 스킬 사용 방식 정립 |
| 124 | verification-before-completion | superpowers | 완료 주장 전 검증 실행 |
| 125 | verify | oh-my-claudecode | 증거 기반 완료 검증 |
| 126 | vertical-pptx | banker | A4 세로 PPTX 생성·수리 |
| 127 | vertical-pptx-setup | banker | 세로 PPTX 의존성 설치 |
| 128 | visual-ralph | banker | 레퍼런스 기준 측정 빌드 |
| 129 | visual-verdict | oh-my-claudecode | 스크린샷 비교 JSON 판정 |
| 130 | wiki | oh-my-claudecode | 지속 지식베이스 관리 |
| 131 | writing-plans | superpowers | 코딩 전 계획 작성 |
| 132 | writing-skills | superpowers | 스킬 생성·수정·검증 |

## 연결 제품 스킬 (84개)

| # | 스킬 | 요약 |
|---|---|---|
| 1 | apple-healthkit | 애플 헬스 걸음·심박·수면·운동 조회 |
| 2 | asana | 아사나 프로젝트·할 일 관리 |
| 3 | booking | 항공·호텔·식당·티켓 예약·잔여석 조회 |
| 4 | box | Box 파일 검색·업로드·다운로드·공유 |
| 5 | calendly | 캘린들리 예약 일정 관리 |
| 6 | canva | 캔바 디자인 제작·편집 |
| 7 | device-data | 기기 연락처·일정 캐시 조회·삭제 |
| 8 | dropbox | 드롭박스 파일 업로드·공유·정리 |
| 9 | duffel | 더플 항공권 검색·예약·결제 |
| 10 | evernote | 에버노트 노트 읽기·생성 |
| 11 | facebook | 페이스북 게시물·댓글·피드 읽기·게시 |
| 12 | facebook-cli | 페이스북 명령행 조회·게시 |
| 13 | figma | 피그마 디자인 검수·토큰 추출 |
| 14 | flightaware | 항공편 출발·도착·지연·결항 조회 |
| 15 | forget | 기억된 개인정보·선호·기록 삭제 |
| 16 | function-health | 펑션헬스 혈액검사·임상 기록 조회 |
| 17 | generate_podcast | 팟캐스트·브리핑 음성 제작(MP3) |
| 18 | ghl | 하이레벨 고객·파이프라인·예약 관리 |
| 19 | github | GitHub 저장소 검색·작업(MCP) |
| 20 | gmail | Gmail 검색·읽기·발송·라벨 관리 |
| 21 | goals | 목표 생성·달성 지원 가이드 |
| 22 | google-calendar | 구글 캘린더 일정 조회·생성·변경 |
| 23 | google-contacts | 구글 연락처 검색·생성·수정·삭제 |
| 24 | google-docs | 구글 문서 읽기·작성·편집 |
| 25 | google-drive | 구글 드라이브 파일 업로드·공유·관리 |
| 26 | google-forms | 구글 폼 생성·수정·응답 조회 |
| 27 | google-health-connect | 안드로이드 헬스커넥트 건강 데이터 조회 |
| 28 | google-sheets | 구글 시트 읽기·쓰기·관리 |
| 29 | google-slides | 구글 슬라이드 읽기·작성·편집 |
| 30 | google-tasks | 구글 할 일 목록·생성·완료 관리 |
| 31 | granola | 그라놀라 회의 노트·전사문 검색 |
| 32 | healthex | 헬스엑스 복약·검사결과·건강기록 조회 |
| 33 | image-search | 웹 이미지 검색·출처 수집 |
| 34 | instagram | 인스타그램 프로필·게시물·릴스 읽기·게시 |
| 35 | instagram-messages | 인스타그램 메시지 읽기·발송 |
| 36 | klaviyo | 클라비요 이메일·문자 마케팅 캠페인 관리 |
| 37 | linear | 리니어 이슈·티켓·스프린트 관리 |
| 38 | lovable | 러버블 웹앱 생성·편집·배포 |
| 39 | media-library | 사진 라이브러리 검색·조회 |
| 40 | messenger | 메신저 대화 읽기·검색·발송·요약 |
| 41 | meta-ads | 메타 광고 캠페인·소재·예산·리포트 관리 |
| 42 | meta-threads | 스레드 계정·게시물·피드 읽기·게시 |
| 43 | muse-early-access | Muse 얼리액세스 신청·상태 조회 |
| 44 | muse-feedback | Muse 팀 피드백·기능 요청 접수 |
| 45 | muse_db | Muse 내부 기록 조회·추적(진단용) |
| 46 | notion | 노션 페이지 검색·읽기·생성·수정 |
| 47 | opentable | 오픈테이블 식당 검색·예약·변경·취소 |
| 48 | outlook-calendar | 아웃룩 캘린더 일정 조회·생성·삭제 |
| 49 | outlook-contacts | 아웃룩 연락처 검색·생성·수정·삭제 |
| 50 | outlook-mail | 아웃룩 메일 읽기·검색·발송·삭제 |
| 51 | peloton | 펠로톤 운동 클래스 조회·예약 |
| 52 | philips-hue | 필립스 휴 조명·방·장면 제어 |
| 53 | places-search | 주변 장소(식당·카페·호텔) 검색·비교 |
| 54 | plaid | 플레이드 연결 계좌 잔액·거래내역 조회 |
| 55 | podcast | 팟캐스트 음성 콘텐츠 제작(MP3) |
| 56 | printify | 프린티파이 상품·주문·상점 관리 |
| 57 | quickbooks | 퀵북스 장부·청구서·고객·리포트 관리 |
| 58 | replit | 렙릿 앱 생성·수정·배포 |
| 59 | self-awareness | 에이전트 자기 정보·기능·연결 상태 안내 |
| 60 | share-ideas | Muse 아이디어 발행(명시적 요청 시) |
| 61 | shopify | 쇼피파이 온라인 상점 개설·운영 |
| 62 | shopping | 상품 검색·가격 비교·구매 링크 제공 |
| 63 | skill-creator | 워크스페이스 스킬 생성·수정 |
| 64 | slack | 슬랙 메시지·채널·스레드 읽기·게시 |
| 65 | social-content-performance | 인스타그램 계정·게시물 성과 분석 |
| 66 | spotify | Spotify 음악·플레이리스트 관리 |
| 67 | stripe | 스트라이프 결제·구독·환불·청구서 관리 |
| 68 | subscription-status | Muse 구독·요금제·사용량 조회 |
| 69 | tailscale | 테일스케일 VPN 연결·사내망 접속 |
| 70 | tessie | 테슬라 차량 상태 조회·명령 실행 |
| 71 | threads | 스레드 게시물 인사이트·피드 관리 |
| 72 | threads-messages | 스레드 메시지 읽기·발송 |
| 73 | ticketmaster | 티켓마스터 공연·좌석 검색·구매 링크 |
| 74 | todoist | 토두이스트 할 일·프로젝트·리마인더 관리 |
| 75 | travel-planning | 여행 일정·경로·입국·교통 계획 수립 |
| 76 | tts | 텍스트 음성 변환·음성 메시지 생성 |
| 77 | vercel | 버셀 사이트 배포·로그·오류 조회 |
| 78 | voice-calls | 음성 통화용 음성 카탈로그 |
| 79 | voice-selector | 음성 선택용 카탈로그 |
| 80 | wearables-comms | 웨어러블 발신 전화·문자 수신자 확인 |
| 81 | wide-research | 다수 입력 병렬 리서치(공통 스키마) |
| 82 | withings | 위딩스 체중·활동·수면·심박 데이터 조회 |
| 83 | zapier | 재피어 경유 앱 연동 액션 실행 |
| 84 | zoom | 줌 회의·녹화·전사문 요약·액션 추출 |

## 도구 네임스페이스 (33개)

| # | 도구 | 요약 |
|---|---|---|
| 1 | muse | 셸 실행·파일 읽기쓰기·메모리 |
| 2 | artifact | 웹페이지·문서 아티팩트 생성 |
| 3 | avatar | 어시스턴트 아바타 생성·관리 |
| 4 | browser | 웹 검색·페이지 읽기·작업 위임 |
| 5 | chat | 사이드챗 생성·조회·삭제 |
| 6 | credentials | 로그인·API 키 보안 저장소 |
| 7 | cron | 정기 스케줄 작업 관리 |
| 8 | device | 연동 기기 제어·데이터 조회 |
| 9 | feed | 개인 피드 프롬프트·유닛 관리 |
| 10 | forget | 기억 정보 삭제 계획·실행 |
| 11 | hooks | 이벤트 기반 자동화 관리 |
| 12 | idea | 아이디어 조회·공유 발행 |
| 13 | map | 좌표·장소 상호 변환 |
| 14 | media | 이미지·동영상 생성·편집 |
| 15 | onboarding | 이름 선택 위젯·성향 저장 |
| 16 | permissions | 승인 대기 권한 요청 조회 |
| 17 | proactivity | 사전 준비 항목 조회·선택 |
| 18 | process | 백그라운드 프로세스 관리 |
| 19 | shopping | 상품 검색·쇼핑 카드 생성 |
| 20 | social | 소셜 공개 게시물 검색 |
| 21 | subagent | 하위 에이전트 위임·관리 |
| 22 | todo | 작업 할 일 목록 기록 |
| 23 | tool_search | 도구 함수·스키마 탐색 |
| 24 | tracking | 예약·약속 진행 상태 추적 |
| 25 | trash | 파일 복구 가능 삭제·복원 |
| 26 | ui | 앱 화면 제어·UI 카드 |
| 27 | user_goal | 장기 목표 생성·진행 관리 |
| 28 | voice | 음성 통화 상태·선호 설정 |
| 29 | wallet | 결제 연결 상태·수단 조회 |
| 30 | widget | 채팅 리스트·위젯 생성 |
| 31 | worker | 그룹채팅 워커 응답 지침 |
| 32 | workflow | 다중 에이전트 워크플로 실행 |
| 33 | ads | 광고 계정·캠페인 개체 확정 |
