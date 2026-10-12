# 원문 설명 전체

list-up 수집 당시의 원문 설명 전문. 기준일: 2026-10-12.

## 워크스페이스 스킬 (132개)

| # | 스킬 | 출처 | 원문 설명 |
|---|---|---|---|
| 1 | 3d-intro-build | banker | 스크롤 위치에 맞춰 3D 플라이스루 영상이 움직이는 브랜드 인트로를 만듦. media.generate_image로 씬 스틸을, media.generate_video로 dive-in 클립을 만들고(외부 API·키 불필요), 단계별 검토 페이지 판정 뒤에만 다음 단계로 진행. 결과는 엄격한 CSP에서도 도는 페이지. 사용자가 '3d-intro-build 해줘'/'3D 인트로 만들어줘'/'스크롤 fly-through'/'인트로 영상 사이트'라고 요청하면 사용. |
| 2 | 3d-intro-setup | banker | `3d-intro-build` 에 필요한 실행 환경(ffmpeg, Node, Playwright/Chromium)을 점검한다. 이미지·영상 생성은 내장 media 파이프라인을 쓰므로 API 키·크레덴셜이 필요 없다. 'setup-3d-intro'/'3d-intro-setup'/'3D 인트로 설정'/'인트로 제작 환경 준비해줘' 라고 요청하면 사용. |
| 3 | agent-doc-discipline | oh-my-claudecode | 에이전트가 읽고 바로 실행할 수 있는 문서(CLAUDE.md·CONTEXT.md·docs/standards/·스펙·티켓·스킬 파일)를 작성·수정할 때 적용하는 글쓰기 규율: 규칙마다 why 첨부, 한 의미는 한 곳에, lookup 재기술 금지. 사용자가 '문서 다듬어줘', '스펙 검토해줘', '에이전트용 문서 작성해줘'라고 요청하면 사용. |
| 4 | ai-slop-cleaner | oh-my-claudecode | AI 생성 코드의 슬롭(중복·데드코드·불필요 추상화·경계 위반·약한 테스트)을 회귀 안전·삭제 우선 워크플로로 정리하는 스킬. 사용자가 'deslop 해줘', 'AI 슬롭 정리해줘', 'anti-slop', '슬롭 청소해줘'라고 요청하거나 구현 후속에 중복 로직·데드코드·래퍼 층이 남았을 때 사용. 새 기능 개발·대규모 재설계에는 부적합. |
| 5 | all-in-one | banker | (banker) 한 요청으로 합의 계획→검증 구현→독립 테스트 게이트를 연쇄(계획→구현→QA). 코딩 작업을 계획부터 통과까지 최대 rigor로 한 번에. 사용자가 'all-in-one 해줘'/'all in one'이라고 요청하면 사용(한 줄 수정은 직접 처리, 아이디어 확장은 제외). |
| 6 | append_wiki | banker | (banker) 새로 배운 비자명 지식을 프로젝트 wiki(.omc/wiki)에 구조화 적재·병합. 사용자가 'append_wiki 해줘'/'위키 기록해줘'/'wiki에 정리해줘'/'알게 된 내용 기록해줘'라고 요청하면 사용. |
| 7 | arch-diagram | banker | (banker) 시스템 아키텍처 구성도를 PlantUML과 편집 가능 PPTX로 산출. 사용자가 '아키텍처 다이어그램 만들어줘'/'plantuml'/'pptx 다이어그램'/'구성도 그려줘'라고 요청하면 사용. |
| 8 | architecture-survey | oh-my-claudecode | 사용자가 "아키텍처 서베이 해줘", "어디가 바꾸기 어려워졌는지 찾아줘", "architecture-survey 해줘"라고 요청하면 발동. 모듈 그래프를 스캔해 깊어져야 할 후보(얕은 모듈·가설적 경계·잘못된 경계 뒤 로직)를 증거와 함께 순위 보고하는 스킬. 코드 수정은 하지 않음. |
| 9 | ask | oh-my-claudecode | 외부 CLI(Claude/Codex/Gemini/Grok/Cursor) 관점의 어드바이저 요청을 처리. 이 환경에서는 외부 모델 CLI 연동이 불가하므로 병렬 서브에이전트 관점 검토로 대체한다. 사용자가 'codex 관점에서 리뷰해줘', 'gemini 관점으로 UX 제안해줘'처럼 외부 모델 관점의 답변을 요청하면 사용. |
| 10 | ask-navigator | oh-my-claudecode | 안개(fog) 낀 작업을 결정 티켓 지도로 차트화하고, 세션당 티켓 하나씩 해소한 뒤 길이 열리면 launch 미션 브리프로 넘긴다. 결정만 생산하고 절대 빌드하지 않는다. 사용자가 'ask-navigator', '이건 fog가 있어', '결정 지도 그려줘'라고 요청하면 사용. |
| 11 | audit-mock | banker | (banker) 하드코딩·mock/stub·열거형을 read-only 정적 감사로 검출. 사용자가 'audit-mock 해줘'/'하드코딩 검출해줘'/'mock·stub 감사'/'SQL 없이 하드코딩 반환하는 api 찾아줘'라고 요청하면 사용. |
| 12 | audit-security | banker | (banker) 의존성 CVE(SCA)·SAST·시크릿을 멀티툴 교차검증으로 read-only 보안 진단. 사용자가 'audit-security 해줘'/'보안 진단해줘'/'CVE 스캔'/'SCA·SAST·secret 스캔해줘'라고 요청하면 사용. |
| 13 | audit-web-page | banker | 가동 중인 웹페이지를 playwright로 라이브 점검한다: 버튼·DOM·콘솔 에러 + WebGL/Canvas 스크린샷 육안 판정. 사용자가 'audit-web-page 해줘', '라이브로 페이지 점검해줘', 'playwright로 화면 확인해줘', '캔버스·WebGL 렌더 확인해줘'라고 요청하면 사용. |
| 14 | autopilot | oh-my-claudecode | 간단한 아이디어 설명부터 요구사항 분석, 설계, 계획, 병렬 구현, QA 사이클, 다각도 검증까지 자율적으로 수행해 동작하는 코드를 만들어준다. 사용자가 "autopilot 해줘", "이거 알아서 다 만들어줘", "아이디어를 완성된 코드로 만들어줘"라고 요청하면 사용. |
| 15 | autoresearch | oh-my-claudecode | 사용자가 "autoresearch 해줘", "미션 반복 개선 루프 돌려줘"라고 요청하면 발동. 단일 미션을 평가자(JSON pass/score) 주도로 반복 개선하며, 이터레이션별 평가 JSON과 마크다운 결정 로그를 남기고 max-runtime에 정지하는 상태 유지 루프 스킬. |
| 16 | brainstorming | superpowers | 창작 작업 전 반드시 사용 - 새 기능·컴포넌트·동작 추가·변경, 또는 새로운 기획(소프트웨어든 아니든)을 시작하기 전 |
| 17 | cancel | oh-my-claudecode | 진행 중 작업 취소·상태 정리 — 사용자가 "취소해줘", "지금 돌고 있는 거 멈춰줘", "cancel 해줘"라고 요청하면 사용. [--force] [--all] 플래그 지원. 현재 세션의 진행 중 작업을 안전하게 중단하고 상태를 정리한다. |
| 18 | cleansing-memory | banker | 에이전트 메모리 파일(MEMORY.md·CLAUDE.md·AGENTS.md)을 문서화된 threshold 안으로 정리한다: 중복 최신본화, 무손실 간결화, append→replace 판별. 사용자가 'cleansing-memory 해줘', '메모리 정리해줘', 'MEMORY.md 정리해줘', 'CLAUDE.md 압축해줘'라고 요청하면 사용. |
| 19 | compact-copy | banker | ready-compact의 resume 프롬프트에서 코드펜스 본문만 뽑아 최종 메시지를 '프롬프트-only'로 출력한다. 사용자가 'compact-copy 해줘', '프롬프트만 복사해줘', 'resume 프롬프트만 줘'라고 요청하면 사용. |
| 20 | compact-wiki | banker | .omc/wiki 페이지를 무손실로 중복 제거·supersede·병합 정리한다. 사용자가 'compact-wiki 해줘', '위키 정리·압축해줘', 'wiki 중복 제거해줘', '위키 병합해줘'라고 요청하면 사용. |
| 21 | configure-notifications | oh-my-claudecode | 작업 완료·입력 필요 알림을 Telegram·Discord·Slack·웹훅으로 받도록 설정하는 스킬: 제공자별 토큰·웹훅 수집 → 설정 파일 기록 → 테스트 발송. 사용자가 '알림 설정해줘', '텔레그램 알림 연결해줘', '디스코드 웹훅 설정해줘', '슬랙 알림 설정해줘', '웹훅 알림 설정해줘'라고 요청하면 사용. |
| 22 | curation | banker | 의사결정을 선택지·권고안·근거·확신수준(0.00~1.00)·확신근거로 구조화해 제시한다. --perf는 결과물 품질·완성도를 효율보다 우선. --deep은 --perf에 더해 확신 0.80 이하인 결정을 더 조사·검토해 0.80을 넘긴 뒤 제시한다. 사용자가 'curation 해줘', '큐레이션해줘', '결정 정리해줘', '선택지 정리해줘'라고 요청하면 사용. |
| 23 | debug | oh-my-claudecode | 현재 세션/레포 상태의 문제를 로그·상태·테스트 증거로 진단하는 디버그 스킬. 사용자가 '디버그 해줘', '왜 안 되지', '어디서 깨졌어'라고 요청하거나 세션·워크플로우·에이전트 동작이 이상할 때 사용. |
| 24 | deep-init | banker | 코드베이스 전체에 계층형 AGENTS.md 문서를 생성·갱신한다(부모 역참조·MANUAL 섹션 보존). 사용자가 'deep-init 해줘', 'deepinit 해줘', 'AGENTS.md 생성해줘', '코드베이스 문서화해줘'라고 요청하면 사용. |
| 25 | deep-interview | oh-my-claudecode | 소크라테스식 심층 인터뷰 — 모호한 아이디어를 차원별 모호도 점수로 측정하며 한 번에 한 질문씩 물어 스펙으로 결정화한다. 사용자가 'deep interview', '인터뷰해줘', '제대로 이해하고 질문 다 해줘', '가정하지 말고 물어봐'라고 요청하면 사용. |
| 26 | deep-research | banker | 다중 소스 웹 리서치를 팬아웃해 주장을 적대적으로 팩트체크하고 확신순 인용 리포트로 합성한다. 사용자가 'deep-research 해줘', '딥리서치해줘', '심층 조사해줘', '출처 검증 리서치해줘'라고 요청하면 사용. |
| 27 | deepinit | oh-my-claudecode | 사용자가 "deepinit 해줘", "코드베이스 초기화 문서 만들어줘", "디렉토리별 AGENTS.md 생성해줘"라고 요청하면 발동. 코드베이스를 계층적으로 스캔해 디렉토리마다 AI 가독 문서(AGENTS.md)를 생성·갱신하는 스킬. |
| 28 | diagnosing-superpowers | superpowers | superpowers 세션이 잘못됐고 상대방이 이유를 알고 싶을 때 사용 - 반복 작업, 계획 무시, 비틀거림, 저조한 결과, 발동 안 한 스킬, '너무 오래 걸려', '왜 이렇게 비싸', '지금 뭘 하고 있어' - 또는 superpowers 메인테이너용 버그 리포트를 만들 때 |
| 29 | diagram | oh-my-claudecode | 제어 흐름·호출 깊이·모듈 소유권·변경 형태 같은 구조를 가장 작은 시각(의사코드·호출 트리·컴포넌트/파일 트리·Mermaid·diff)으로 보여주는 스킬. 사용자가 '다이어그램 그려줘', '구조를 보여줘'라고 요청하거나 문장만으로 전체 형태를 붙잡기 어려울 때 사용. 문장으로 충분하면 생략한다. |
| 30 | dispatching-parallel-agents | superpowers | 공유 상태·순차 의존 없이 작업 가능한 2개 이상의 독립 태스크가 있을 때 사용 |
| 31 | docs-setup | banker | arch-diagram·pdf-vision-extract 의존성(python-pptx·pymupdf·plantuml)을 python 환경 감지/선택 후 설치. 사용자가 '문서 툴 설치'/'pptx·pymupdf·plantuml 설치'/'docs-setup'이라고 요청하면 사용. |
| 32 | drydock | oh-my-claudecode | 어떤 레포든 shipyard 하네스(4 pillars × 5 surfaces)의 용골을 깐다 — 한 번 실행하고, 이후에는 --check로 드리프트 감사. 사용자가 'drydock 해줘', '하네스 깔아줘', 'drydock --check 해줘'라고 요청하면 사용. |
| 33 | evolve | harness | 하네스 진화 스킬. 사용 중인 하네스의 실행 결과에 대한 피드백을 수집·일반화하여 에이전트/스킬/오케스트레이터에 반영하고, 초기 구성 대비 델타를 포착해 변경 이력을 갱신한다. '하네스 회고', '하네스 진화', '하네스 피드백 반영', '하네스 개선', '결과가 아쉬웠어 하네스 고쳐줘', '이 피드백 하네스에 반영해줘', '하네스 레슨 정리' 등 기존 하네스의 실행 경험을 바탕으로 한 개선 요청 시 반드시 이 스킬을 사용. 하네스 신규 구축·구조 재설계·에이전트 추가는 harness 스킬이 담당. |
| 34 | execute | oh-my-claudecode | 합의된 작업을 동작하는 검증된 코드까지 수행하는 표준 실행 워크플로. 사용자가 "execute 해줘", "구현해줘", "만든 거 동작하게 해줘"라고 요청하면 사용. |
| 35 | executing-plans | superpowers | 구현 계획을 이 세션에서 직접 구현자로 실행할 때 사용 - 상대방이 인라인 실행을 선택했거나 서브에이전트 도구가 없을 때 |
| 36 | external-context | oh-my-claudecode | 사용자가 "external-context 해줘", "외부 문서 찾아줘", "<주제> 관련 최신 공식 문서 조사해줘"라고 요청하면 발동. 질의를 2–5개 파셋으로 분해해 document-specialist 서브에이전트를 병렬 실행하고, 출처 인용과 함께 종합하는 스킬. |
| 37 | finishing-a-development-branch | superpowers | 구현이 끝나고 모든 테스트가 통과한 뒤, 작업을 어떻게 통합할지 정할 때 사용 |
| 38 | front-qa | custom | 스펙(note 파일) 기반 프론트엔드 구현 + 레퍼런스 대비 엄격 parity QA 워크플로(계획→구현 루프→게이트). 사용자가 'front-qa 해줘', '스펙대로 프론트 구현해줘', '레퍼런스 parity QA해줘'라고 요청하면 사용. |
| 39 | graph | oh-my-claudecode | 선언적 JSON 디스크립터로 반복 가능한 다단계 파이프라인(DAG)을 기술·실행하는 오케스트레이션 스킬. 사용자가 '파이프라인 돌려줘', '단계별로 실행해줘', '중단해도 재개되게 해줘'라고 요청하고 작업이 반복 가능하며 의존성이 명확할 때 사용. 탐험적 일회성 작업이나 중간 재설계가 필요한 작업에는 부적합. |
| 40 | harbor | oh-my-claudecode | 외부 작업 인테이크 — 들어오는 이슈·PR을 훑어 주장을 검증하고, 이미 내려진 결정을 재사용해, maintainer가 서명할 안건을 정리한 docket을 만든다. captain은 미해결 결정만 다룬다. 사용자가 'harbor sweep 해줘', 'harbor #123 봐줘', 'harbor sign 해줘', '뭐가 준비됐어'라고 요청하면 사용. |
| 41 | harness | harness | 프로젝트에 맞는 하네스를 설계하고, 전문 에이전트와 각 에이전트가 사용할 스킬을 만든다. 사용자가 '하네스 구성해줘', '하네스 구축해줘', '하네스 설계', '하네스 엔지니어링', '에이전트 팀 만들어줘'라고 요청할 때 사용한다. 새로운 분야나 프로젝트의 자동화 체계를 구축하거나 기존 하네스를 재구성·확장할 때도 사용한다. '하네스 점검', '하네스 감사', '하네스 현황', '에이전트/스킬 동기화'처럼 기존 하네스를 운영하거나 유지 보수하는 요청에도 사용한다. 실행 결과를 회고하고 피드백을 반영하는 작업에는 evolve 스킬을 사용한다. |
| 42 | harness-factory | custom | (banker) 에이전트 팀 아키텍처(전문 서브에이전트 팀) 설계·스폰·운용 방법론. 사용자가 '에이전트팀 만들어줘'/'하네스 팩토리'/'전문 에이전트 팀 생성'/'harness-factory'라고 요청하면 사용. |
| 43 | hud | oh-my-claudecode | HUD(상태 표시줄) 표시 옵션 설정 — 레이아웃, 프리셋(minimal/focused/full), 표시 요소. 사용자가 'hud 해줘', 'hud setup 해줘', 'hud minimal 해줘', 'hud focused 해줘', 'hud full 해줘', 'hud status 해줘'라고 요청하면 사용. |
| 44 | humanizer | banker | AI가 쓴 듯한 영문 글의 흔적을 제거해 자연스러운 문체로 윤문. 사용자가 'humanizer'/'자연스럽게 다듬어줘'/'AI 티 나지 않게'/'sound more human'이라고 요청하면 사용. |
| 45 | intent | oh-my-claudecode | 지원/운영 담당자처럼 스펙을 못 쓰는 사람이 붙여넣은 채팅 로그나 구두 문제 보고를, 번호 매기기 배치 질문과 완료 게이트를 거쳐 5개 섹션의 intent.md 문서로 만드는 요구사항 인테이크. 사용자가 "intent 해줘", "이 문의를 정리해줘", "요구사항 문서로 만들어줘"라고 요청하면 사용. |
| 46 | interval-report | banker | 장기 수행의 중간 보고를 docs/intermission.md로 만들고 계획된 작업이 끝날 때까지 갱신. 시작 시각은 date로 실측해 파일에 영속하고, ETA는 단일 숫자 대신 범위+확신 라벨로 낸다. 사용자가 '중간 보고'/'진행 상황 보고'/'interval-report'/'intermission'이라고 요청하면 사용. |
| 47 | launch | oh-my-claudecode | 통제된 딜리버리 파이프라인 — 사용자가 "launch 해줘", "이 미션을 끝까지 밀어줘", "기획부터 검증까지 실행해줘"라고 요청하면 사용. 미션 브리프 수렴→스펙 합성→티켓 분해→병렬 실행→검증→완료 보고의 5단계를 사람 체크포인트와 함께 진행한다. |
| 48 | lineage | banker | 현재 세션(들)의 대화를 카카오톡 스타일 단일 HTML로 export. Muse 답변=1줄 요약+클릭 펼침(마크다운 렌더), 하네스 노이즈 자동 필터, 다중 세션 병합, secret 자동 redaction. 기본은 세션 모델 검토(요약·턴 선별), --rulebase는 규칙만. 사용자가 '대화 export'/'카톡 스타일 html'/'lineage'라고 요청하면 사용. |
| 49 | list-up | custom | 보유 스킬·도구 전체 목록을 표 형태의 웹 아티팩트로 만든다. 워크스페이스 스킬(~/workspace/skills) + 연결 제품 스킬(/opt/hatch/skills) + 도구 네임스페이스를 수집해 research_dir 리포트로 넘기고 artifact.create_web_static으로 빌드. 'list-up'/'스킬 목록 보여줘'/'도구 목록 보여줘'/'카탈로그 만들어줘' 시 사용. |
| 50 | loft | oh-my-claudecode | 말로 안 풀리는 디자인 질문을 버려도 되는(throwaway) 아티팩트로 확인 — 순수 로직 모듈+클릭 가능한 셸, 또는 한 라우트 뒤의 구조가 다른 UI 변형 3종. captain의 반응이 곧 결정이다. 사용자가 'loft 해줘', '직접 봐야 알 것 같아', navigator 지도에 loft 티켓이 있으면 사용. |
| 51 | make-notion-guide | banker | 실제 API/인터페이스를 노션 토글 양식의 개발자 호출 가이드로 작성. 사용자가 '노션 가이드'/'API 호출 문서를 노션 양식'/'make-notion-guide'라고 요청하면 사용. |
| 52 | map | oh-my-claudecode | 해야 할 일은 알겠는데 어떤 스킬이 맡는지 모를 때 보는 스킬 지도 — 딜리버리 루프 순서대로 라우팅만 하고 실행하지 않는다. 사용자가 'map 해줘', '어떤 스킬 써야 해'라고 직접 요청할 때 사용. |
| 53 | minimal-code-discipline | oh-my-claudecode | 코드 변경을 최소 diff로 유지하는 YAGNI 사다리 규율: 존재 우선·재사용 우선·의존성 사다리·짧고 올바른 diff, 절대 줄이지 않는 non-negotiable 포함. 사용자가 '최소한으로 구현해줘', 'YAGNI로 해줘', '가장 작게 바꿔줘'라고 요청하거나 변경 범위가 요청을 벗어나 커질 때, diff 크기 검토 시 사용. |
| 54 | minimal-prose-discipline | oh-my-claudecode | 에이전트가 사람에게 말하는 답글·보고서 문체 규율: 보호 코어(코드·명령·경로·에러·숫자·부정어)는 절대 고치지 않고, 군더더기·내레이션·장식을 제거하며, 안전이 걸리면 자동으로 풀어쓴다. 답글이 길어지거나 군더더기가 섞일 때, 보고서를 다듬기 전에 사용. |
| 55 | motion-graphic-make | banker | 10초 내외 내레이션 없는 모션 그래픽(킨네틱 타이포·통계·차트·로고·하단자막·지도)을 만듦. 텍스트 정밀형은 로컬 HTML+CSS → headless 캡처 → ffmpeg 인코딩, 시네마틱형은 media.generate_video. 배경음악+효과음 포함(무음 금지). 사용자가 '모션 그래픽 만들어줘'/'모션 그래픽 제작'/'motion graphics'라고 요청하면 사용. |
| 56 | motion-graphic-setup | banker | 모션 그래픽 제작의 전제조건(ffmpeg, headless Chromium) 확보·검증. 영상 생성 자체는 내장 media 파이프라인을 쓰므로 별도 CLI 설치가 필요 없다. 사용자가 '모션 그래픽 설치해줘'/'motion-graphic-setup'이라고 요청하면 사용. |
| 57 | nothing-design | banker | Nothing 브랜드 스타일(미니멀·도트매트릭스·모노크롬) UI 디자인 시스템 적용. 사용자가 'Nothing 스타일로 디자인해줘', 'Nothing design 적용해줘'라고 명시적으로 요청하면 사용. 일반 UI 작업에는 자동 트리거하지 않는다. |
| 58 | obsidizer | banker | AI 생성 마크다운 위키를 의미 보존한 채 Obsidian 지식그래프로 정규화·상호링크·백링크(결정적 캐노니컬라이저 obsidize.mjs). 사용자가 '옵시디언화 해줘', '위키 그래프 정리해줘', 'obsidian 최적화해줘'라고 요청하면 사용. 기본 dry-run. |
| 59 | omc-doctor | oh-my-claudecode | 워크스페이스 환경 진단·수정 — 사용자가 "환경 점검해줘", "doctor 실행해줘", "스킬 환경에 문제 있어"라고 요청하면 사용. ~/workspace/skills 정합성, git·python3·node 등 필수 도구를 점검하고 사용자 확인 후 자동 수정한다. |
| 60 | omc-patch | banker | OMC 플러그인이 자동 업데이트된 뒤 사라진 훅 패치를 활성 버전에 다시 적용하고 OMC 마켓플레이스 자동 업데이트를 막음. 진단, 적용, 검증, 되돌리기. 'omc-patch'/'OMC 패치'/'OMC 업데이트 뒤 패치'/'훅 timed out'/'훅 프로세스 누적'/'PC 느려짐' 시 사용. |
| 61 | omc-reference | banker | OMC(oh-my-claudecode) 에이전트·툴·팀·커밋·스킬 레지스트리 레퍼런스. 에이전트 위임·팀 오케스트레이션·커밋 규칙을 쓸 때 자동 참조한다. |
| 62 | omc-review | custom | 완성된 작업물을 출고 전 결함·리스크·단순화 관점으로 평가하는 코드 리뷰 스킬. 사용자가 '리뷰해줘', '검토해줘', '머지해도 돼?'라고 요청하면 사용. ai-slop-cleaner는 이 리뷰 안의 opt-in 정리 레인이다. |
| 63 | omc-setup | oh-my-claudecode | 이식된 OMC 스킬 모음 안내·관리 — 사용자가 "OMC 스킬 목록 보여줘", "OMC 스킬이 뭐가 있어", "OMC 스킬 추가해줘", "OMC 스킬 업데이트해줘"라고 요청하면 사용. 이식된 스킬 목록 안내와 새 스킬 추가 방법을 제공한다. |
| 64 | payload-mon | banker | OMC HUD 상태표시줄의 `ctx` 옆에, 현재 세션이 보내는 API 요청의 페이로드 추정치를 32MB 한도 대비로 표시하는 기능을 켜고 끔. 8MB 부터 표시. 'payload-mon'/'payload 모니터 켜/꺼'/'상태표시줄 payload 표시'/'요청 크기 경고'/'32MB 한도 경고'/'payload 표시가 안 보여' 시 사용. |
| 65 | pdf-vision-extract | banker | 비주얼 위주 PDF를 고해상도 per-page PNG로 변환해 레이아웃 손실 없이 비전 입력으로 읽기. 사용자가 'PDF를 이미지로 읽어줘', '디자인 PDF 추출해줘', 'pdf-vision-extract'라고 요청하면 사용. |
| 66 | plan | oh-my-claudecode | 요구사항 수집부터 다관점 합의까지, 코딩 전에 실행 가능한 작업 계획을 만든다. 사용자가 "plan 해줘", "계획 짜줘", "이 계획 리뷰해줘", "합의 계획 만들어줘"라고 요청하면 사용. |
| 67 | play-qa | banker | Godot HTML5 웹게임을 실제 브라우저에서 직접 플레이하며 렌더·입력·시작 결함을 QA(playwright). 사용자가 '게임 직접 플레이해서 QA해줘', '네가 직접 플레이해봐', 'play-qa'라고 요청하면 사용. |
| 68 | pr | oh-my-claudecode | 작업의 paper trail(verify 증거·ADR·스펙)에서 PR 본문을 조립하는 스킬 — 증명하는 최소 시각, 재수집 없는 증거, diff에 대한 ADR 테스트 기반 복구 가능성. PR을 열거나 실질적으로 업데이트할 때 사용. |
| 69 | project-session-manager | oh-my-claudecode | git worktree 기반 격리 개발 환경 관리(psm): 이슈·PR·기능별 워크트리 생성, 세션 목록·정리·상태 확인. 부속 CLI(psm.sh·lib/·templates/·tests/) 동봉. 사용자가 'psm 해줘', '워크트리 세션 만들어줘', 'PR 리뷰 환경 만들어줘', '이슈 수정 환경 만들어줘', '워크트리 정리해줘'라고 요청하면 사용. 'psm'은 이 스킬의 별칭. |
| 70 | ralph | oh-my-claudecode | 작업이 끝났다고 선언하지 않고, PRD의 모든 사용자 스토리가 검증될 때까지 반복 실행하는 끈질긴 완성 루프. 사용자가 "ralph 해줘", "끝까지 해줘", "멈추지 말고 완성해줘"라고 요청하면 사용. |
| 71 | ralph-qa | banker | 작업 결과를 자기채점하지 않게 독립 검증·개선 반복: 백본 서브에이전트(N개, 가장 강한 가용 모델)가 항상 돌고, 프로브로 유효성이 관측된 외부 LLM만 추가 좌석으로 합류. 사용자가 '교차검증해줘', '다른 LLM으로 검증해줘', '독립 QA해줘', 'ralph-qa'라고 요청하면 사용. |
| 72 | ralplan | oh-my-claudecode | 모호한 실행 요청을 받으면 바로 실행하지 않고 Planner·Architect·Critic 3자 합의 계획 루프를 먼저 돌려 확정된 계획을 만드는 실행 전 게이트. 사용자가 "ralplan 해줘", "실행 전에 계획부터 잡아줘", 또는 모호한 ralph/autopilot 요청을 보내면 사용. |
| 73 | ready-compact | banker | 컨텍스트 compaction 직전 진행 상태를 저장하고 이어갈 resume 프롬프트를 생성한다. 사용자가 'compact 준비해줘', '이어서 할 수 있게 준비해줘', '이어갈 프롬프트 만들어줘'라고 요청하거나 컨텍스트가 한계에 가까울 때 사용. |
| 74 | receiving-code-review | superpowers | 코드 리뷰 피드백을 받았을 때, 제안 구현 전 사용 - 특히 피드백이 불분명하거나 기술적으로 의심스러울 때. 수행적 동의·맹목적 구현이 아닌 기술적 엄밀함과 검증 요구 |
| 75 | refit | oh-my-claudecode | 세션을 넘나드는 환경 회고 — 대화·로그·실행 기록에서 드러난 마찰을 읽어, 수정이 속한 표면(결정적 검사·조향·도구·정보)에 사용자 승인 하에 반영한다. 'refit 해줘'라고 직접 요청할 때 사용. |
| 76 | refresh-git-ignore | banker | repo의 .gitignore를 비파괴·반복가능하게 갱신한다(런타임/빌드 아티팩트만 추가, 추적 파일 보호). 사용자가 'gitignore 갱신해줘', '.gitignore 정리해줘', 'git status 잡음 줄여줘'라고 요청하거나 새 도구가 남긴 런타임 아티팩트로 git status가 지저분해질 때 사용. |
| 77 | refresh-readme | banker | 코드가 움직인 뒤 뒤처진 README를 현재 프로젝트에 맞게 갱신한다. 산문 주장을 매니페스트·소스 트리와 대조해 드리프트를 잡고, 코드펜스·URL·플래그를 보호하며 간결하게 고쳐 쓴다. 사용자가 'README 갱신해줘', 'README 최신화', 'README가 코드와 안 맞아', 'README 드리프트'라고 요청하거나 릴리스 직전 산문 주장이 실제와 맞는지 확인할 때 사용. |
| 78 | release | oh-my-claudecode | 레포 릴리스 규칙을 분석해 .omc/RELEASE_RULE.md에 캐시하고 릴리스를 안내하는 얇은 어시스턴트. 사용자가 'release 해줘', 'release minor 해줘', '버전 올려줘'라고 요청하면 사용. |
| 79 | remains | banker | 남은 버그, 하자, 미검증 항목을 찾아 표로 보여 줌. 테스트박스가 등록돼 있으면 각 OS 에서 시험을 돌려 확인함. 읽기와 시험 실행만 하고 고치지 않음. 'remains'/'남은 버그'/'남은 하자'/'미검증 항목'/'뭐가 남았어' 시 사용. |
| 80 | remember | oh-my-claudecode | 사용자가 "이거 기억해줘", "remember 해줘", "세션 지식 정리해줘"라고 요청하면 발동. 세션 중 발견한 재사용 가능한 지식을 적절한 메모리 표면에 분류·승격시키는 스킬. |
| 81 | requesting-code-review | superpowers | 태스크 완료·주요 기능 구현·머지 전, 작업이 요구사항을 만족하는지 검증할 때 사용 |
| 82 | research | oh-my-claudecode | 사용자가 "리서치해줘", "조사해줘", "이거 알아봐줘"라고 요청하면 발동. 열린 질문을 근거·출처 기반으로 조사하고 불확실한 부분을 명시해 보고하는 표준 리서치 레인 스킬. |
| 83 | rfp-author | banker | 소프트웨어 외주 제안요청서(RFP)를 한국 공공/금융 + 국제 + AI/LLM 골격으로 저작한다. 사용자가 'RFP 작성해줘', '제안요청서 만들어줘', '외주 RFP'라고 요청하거나 기존 RFP 초안의 인용·반증경계·규제 currency를 검증할 때 사용. |
| 84 | scroll-world | scroll-world | 스크롤-스크럽 'fly through the world' 랜딩 페이지 제작. media.generate_image로 씬 스틸을, media.generate_video(시작 프레임 지정)로 dive-in/connector 클립을 만들고(외부 API·키 불필요), 벤더링 scrub-engine.js를 mountScrollWorld로 배선. 인터뷰 → 승인 게이트 → 씬 스틸 → 클립 → 스크롤 배선. 사용자가 'scroll-world 해줘'/'스크롤 fly-through'/'3D 월드'/'다이오라마 랜딩'이라고 요청하면 사용. |
| 85 | self-improve | oh-my-claudecode | 자율 진화형 코드 개선 엔진 — 사용자가 "self-improve 실행해줘", "이 레포를 자동으로 개선해줘", "벤치마크 기준으로 코드를 진화시켜줘"라고 요청하면 사용. 연구→계획→실행→토너먼트 선발→기록 루프를 정지 조건까지 자율 반복한다. |
| 86 | session-flow | oh-my-claudecode | 현재 세션에서 방향을 다시 잡는 증거 기반 흐름 지도 — 목표·전환·결과·현재 단계·열린 결정을 15줄 안에 압축. 세션 전환·압축 후 재정렬이 필요할 때 'session-flow 해줘'라고 직접 요청. |
| 87 | setup | custom | 구성요소·의존성을 골라 설치하는 오케스트레이터(런타임 node·python·java, LSP, tmux, MCP, sandbox, playwright 등 설치 스킬 묶음). 사용자가 'setup 해줘', '개발환경 설치해줘', 'node 설치해줘', 'playwright 설치해줘'처럼 구성요소 설치를 요청하면 사용. |
| 88 | setup-bypass-permissions | banker | 경고: 켜면 모든 Claude Code 세션에서 Claude 가 파일 수정, 셸 명령, 네트워크 도구를 묻지 않고 실행함. 격리된 환경에서만 사용. 기본 권한 모드를 `bypassPermissions` 로 바꾸며, 사용자가 직접 입력할 때만 실행하고 경고 뒤 동의를 받아 적용. `off` 는 권한 설정만 되돌림. |
| 89 | setup-harness-factory | banker | 도메인 한 줄로 전문 에이전트 팀을 만들어 주는 `revfactory/harness` 방법론을 로컬 원본(~/workspace/skills-upstream/harness)에서 읽어 쓰고 사용법을 안내. 마켓플레이스 설치는 Muse 환경에서 불가. 'setup-harness-factory'/'하네스 팩토리 설치'/'에이전트팀 생성' 시 사용. 기존 harness-factory 스킬과는 별개. |
| 90 | setup-insane-search | banker | 차단·봇방어 사이트 우회 검색·페치 플러그인 insane-search 설치(Claude Code=gptaku_plugins, Codex=gptaku-codex). 사용자가 'insane-search 설치해줘', 'setup-insane-search'라고 요청하거나 차단 사이트(WAF·봇방어) 검색·페치가 필요해지면 사용. |
| 91 | setup-java | banker | JDK 21 + JAVA_HOME 설치(alternatives로 java·javac 비대칭 방지, Debian은 Adoptium 전용). jdtls 등 Java LSP의 전제조건. 사용자가 'JDK 설치해줘', 'Java 21 설치해줘', 'setup-java'라고 요청하거나 Java 도구가 JDK 21을 요구할 때 사용. |
| 92 | setup-lsp | banker | 언어별 LSP 서버(vtsls·basedpyright·bash·jdtls·spring)와 lsp-mcp 브리지 설치·연동. symbol/type/reference 기반 코드 탐색(grep 대체) 기반을 마련한다. 사용자가 'LSP 설치해줘', '언어 서버 설치', 'setup-lsp'라고 요청하거나 코드 탐색 도구가 LSP 서버를 요구할 때 사용. |
| 93 | setup-mcp | banker | context7·sequential-thinking·filesystem·git·fetch(+선택 tavily) 범용 MCP 서버를 Claude Code·Codex CLI에 배선. 사용자가 'MCP 서버 설치해줘'·'context7 설치해줘'·'sequential-thinking 설치해줘'라고 요청하거나 전체 개발환경 세팅을 요청하면 사용. serena·lsp_bridge는 별도 스킬 소관. |
| 94 | setup-node | banker | nvm + Node 22(LTS) 런타임 설치(Windows는 winget 또는 nvm-windows). npx 기반 MCP 서버·npm 전역 패키지의 공통 전제 조건. 사용자가 'Node 설치해줘'·'nvm 설치해줘'라고 요청하거나 전체 개발환경 세팅을 요청하면 사용. |
| 95 | setup-omc | banker | `all-in-one`, `ultra-init`, `front-qa` 가 의존하는 oh-my-claudecode(OMC)를 설치하거나 갱신. Codex 에서는 oh-my-codex(OMX)가 대상. 'setup-omc'/'OMC 설치'/'oh-my-claudecode 설치' 또는 `/banker:setup` 시 사용. |
| 96 | setup-omc-hud | banker | Claude Code 의 상태표시줄 omc_hud 를 OS별 적용 스크립트로 설치하고, Claude Code 갱신 안내를 줄 맨 끝으로 옮김. Codex 는 OMX 의 `hud` 스킬을 씀. 'setup-omc-hud'/'omc_hud 설치'/'Claude 갱신 안내 위치' 또는 `/banker:setup` 시 사용. |
| 97 | setup-playwright | banker | Playwright + headless 브라우저를 OS·권한·conda 감지 후 설치(RHEL8/Rocky8·non-root·no-conda·xvfb 폴백). 사용자가 'Playwright 설치해줘'라고 요청하거나 전체 개발환경 세팅을 요청하면 사용. |
| 98 | setup-pwsh | banker | Windows PowerShell 7 + Git + $PROFILE(UTF-8 무BOM) 환경을 winget으로 설치·검증(비-Windows는 감지 후 no-op). 사용자가 'PowerShell 설치해줘'·'pwsh 환경 설정해줘'라고 요청하거나 전체 개발환경 세팅을 요청하면 사용. |
| 99 | setup-python | banker | Python 3.11+ 런타임 + pipx·uv 설치(OS별 PEP668·RHEL8 3.6 회피). 문서 라이브러리(pptx·pymupdf)는 별도 스킬 소관, 본 스킬은 런타임만. 사용자가 'Python 설치해줘'·'pipx·uv 설치해줘'라고 요청하거나 전체 개발환경 세팅을 요청하면 사용. |
| 100 | setup-sandbox | banker | OS 를 감지해 에이전트 샌드박스의 공통 기반을 설치. Linux 는 bubblewrap, socat, userns 설정, macOS 는 Seatbelt, Windows 는 AppContainer. rust 와 cargo 도 설치하고 git 의 `safe.directory` 를 설정. 'setup-sandbox'/'샌드박스 설치'/'bubblewrap 설치' 또는 `/banker:setup` 시 사용. |
| 101 | setup-stitch | banker | Google 의 디자인 생성 서비스인 Stitch 의 MCP 프록시를 `claude mcp add`(Codex 는 `codex mcp add`)로 등록. 시크릿은 커밋하지 않음. 'setup-stitch'/'stitch 설치'/'stitch mcp' 또는 `/banker:setup` 시 사용. |
| 102 | setup-tmux | banker | OMC 의 `team` 과 worktree 세션, OMX 의 `$team` 과 HUD 에 필요한 tmux 를 OS 에 맞춰 설치(Windows 는 psmux). Rocky8 은 3.6a 를 소스에서 빌드. 'setup-tmux'/'tmux 설치'/'psmux 설치' 또는 `/banker:setup` 시 사용. |
| 103 | skill | oh-my-claudecode | 워크스페이스 스킬 관리 — 사용자가 "스킬 목록 보여줘", "스킬 추가해줘", "스킬 삭제해줘", "스킬 검색해줘", "스킬 수정해줘", "스킬 설정해줘", "스킬 정보 보여줘"라고 요청하면 사용. 목록·추가·삭제·검색·수정·정보 조회·설정 마법사를 지원한다. |
| 104 | skill-up | custom | 업스트림 플러그인 5종 최신판을 받아 실사용 스킬에 이식·갱신하는 전체 워크플로. git clone/pull → ~/workspace/skills-upstream/ 스테이징 → diff 병합 이식 → 미디어 스킬을 내장 media 파이프라인 기준으로 정정 → 검증 → 백업 정리. 사용자가 'skill-up 해줘'/'스킬 업데이트해줘'/'플러그인 최신판으로 갱신해줘'라고 요청하면 사용. |
| 105 | skillify | oh-my-claudecode | 반복 가능한 워크플로를 재사용 가능한 스킬 초안으로 변환 — 사용자가 "스킬로 만들어줘", "이 작업을 스킬로 추출해줘", "skillify 해줘"라고 요청하면 사용. 현재 세션에서 발견한 반복 워크플로를 SKILL.md 초안으로 만든다. |
| 106 | smart-compact | banker | 컨텍스트 사용률이 임계(기본 50%)를 넘으면 `append_wiki` 와 `ready-compact` 를 자동 실행해 마지막 메시지에 resume 프롬프트만 남김. `/copy`, `/compact`, 붙여 넣기는 사용자가 직접 함. 'smart-compact' 로 켜고 `--cancel` 로 끔. |
| 107 | subagent-driven-development | superpowers | 독립적인 태스크들로 된 구현 계획을 이 세션에서 실행할 때 사용 |
| 108 | summary-wiki | banker | 위키 페이지 전량을 docs/ 아래 단일 파일로 개조식 요약. 사용자가 '위키 요약해줘', 'summary-wiki', '위키 지식 동기화', '위키 digest'라고 요청하면 사용. |
| 109 | systematic-debugging | superpowers | 버그·테스트 실패·예상 밖 동작을 만났을 때, 수정안을 제안하기 전에 사용 |
| 110 | tdd | oh-my-claudecode | 사전 합의된 seam에서의 테스트 우선 규율 — 테스트 하나·구현 하나, tracer-bullet red/green. 기대값은 독립 출처에서, 대체는 seam 경계 클래스에서만. 'tdd 해줘', '테스트 먼저'라고 요청하면 사용. |
| 111 | team | oh-my-claudecode | 사용자가 "팀으로 작업해줘", "N명의 에이전트로 병렬 작업해줘", "에이전트 여러 개로 나눠서 작업해줘"라고 요청하면 발동. 공유 작업 리스트 위에서 N명의 조정된 서브에이전트를 단계별 파이프라인(plan→prd→exec→verify→fix)으로 병렬 실행하는 팀 오케스트레이션 스킬. |
| 112 | test-driven-development | superpowers | 기능·버그수정을 구현할 때, 구현 코드를 쓰기 전에 사용 |
| 113 | tone-compact | banker | 답변과 새 문서를 ASD-STE100 에 기반한 한글 개조식으로 간결하게 쓰는 문체 규칙을 켜고 끔. 표와 목록, 원어 발음 표기를 쓰고 장식 기호는 금지. 인자가 없으면 `on`. `off` 할 때까지 모든 세션에 유지. 'tone-compact'/'간결체 켜'/'개조식으로 답해'/'문체 규칙 켜/꺼' 시 사용. |
| 114 | trace | oh-my-claudecode | 사용자가 "trace 해줘", "원인 추적해줘", "왜 이런 결과가 나왔는지 추적해줘"라고 요청하면 발동. 모호하고 인과적인 질문에 대해 경쟁 가설을 병렬 tracer 레인으로 세우고, 증거 기반으로 원인을 설명하는 스킬. |
| 115 | trouble-shooting | banker | 문제를 조사해 현상, 문제점, 원인, 해결방법, 조치계획을 세우고 표로 간결히 보고함. `--no-plan` 이면 해결방법까지만 함. 원인은 근거로 확인하고, 고치지 않고 보고만 함. 'trouble-shooting'/'트러블슈팅'/'원인 분석'/'장애 분석'/'문제 해결 보고' 시 사용. |
| 116 | ultra-chain | custom | 조사→인터뷰→계획 합의→목업→구현→독립 QA→비주얼 QA→과정 시각화→공유의 9단계 풀 체인. deep-research, deep-interview, ralplan --deliberate, loft, ralph, ralph-qa, visual-ralph을 순서대로 엮어 한 번의 지시로 끝까지 민다. 사용자가 'ultra-chain'/'울트라 체인'/'풀 체인으로 해줘'라고 요청하면 사용. |
| 117 | ultra-init | banker | 아이디어·러프 브리프·그린필드를 계획→구현→QA 통과까지 핸즈오프 1회 자율 실행하는 풀사이클 오케스트레이터. 사용자가 'ultra-init', '알아서 만들어줘', '핸즈오프 빌드'라고 요청하면 사용. |
| 118 | ultra-interview | banker | 리서치를 선행해 질문을 최소화하면서 이산 체크리스트로 모호성이 3% 이하가 될 때까지 인터뷰 반복. 사용자가 'ultra-interview', '울트라 인터뷰', '리서치 선행 인터뷰', '요구사항 확정해줘'라고 요청하면 사용. |
| 119 | ultra-ui-qa | banker | 웹 UI를 실제 브라우저로 렌더해 디자인 SoT(PDF/스펙)와 1:1 대조하고 내부개념 텍스트 누출을 점검하는 엄격 UI QA. 사용자가 'ultra ui qa 해줘', 'UI 대조해줘', '디자인 PDF와 대조해줘', '어색한 내용 점검해줘'라고 요청하면 사용. |
| 120 | ultragoal | oh-my-claudecode | 간단한 브리프를 순서가 있는 목표들의 집합으로 쪼개, 추가 전용 장부에 시작/체크포인트/차단/실패 이벤트를 기록하며 장기 이니셔티브를 여러 세션에 걸쳐 추적한다. 사용자가 "ultragoal 해줘", "이 큰 일을 장기로 추적해줘"라고 요청하면 사용. |
| 121 | update-banker | banker | 설치된 banker 를 최신 배포본으로 갱신. 세 채널(Claude Code 플러그인, npm 전역 CLI, Codex)은 따로 드리프트함. npm 전역 CLI 를 먼저 올려 최신 버전과 같을 때만 나머지 채널을 갱신하고, 채널마다 검증. 'update-banker'/'banker 업데이트'/'banker 최신화'/'banker 드리프트' 시 사용. |
| 122 | using-git-worktrees | superpowers | 현재 워크스페이스와 격리가 필요한 기능 작업을 시작할 때, 또는 구현 계획 실행 전 사용 - 격리된 워크스페이스 확보 |
| 123 | using-superpowers | superpowers | 대화 시작 시 사용 - 스킬을 찾고 사용하는 방식을 정립하며, 확인 질문을 포함한 모든 응답 전 스킬 호출을 요구 |
| 124 | verification-before-completion | superpowers | 작업 완료·수정·통과를 주장하기 전, 커밋·PR 생성 전 사용 - 성공 주장을 하기 전에 검증 명령을 실행하고 출력을 확인해야 함. 항상 증거가 주장보다 먼저 |
| 125 | verify | oh-my-claudecode | 기능·수정·리팩터링이 정말 동작하는지 완료를 주장하기 전에 증거로 검증한다. 사용자가 "verify 해줘", "이거 진짜 동작하는지 확인해줘", "검증해줘"라고 요청하면 사용. |
| 126 | vertical-pptx | banker | A4 세로(210x297mm) 규격 PPTX 생성·점검·수리와 16:9 덱의 A4 세로 변환. 사용자가 'A4 세로 pptx 만들어줘', '세로형 슬라이드', '인쇄용 pptx', 'vertical-pptx'라고 요청하면 사용. |
| 127 | vertical-pptx-setup | banker | vertical-pptx 의존성(pptxgenjs·python-pptx)과 시각 검증용 LibreOffice를 OS·권한 감지 후 설치(root 없으면 홈 프리픽스 추출). 사용자가 'vertical-pptx-setup 해줘', 'LibreOffice 설치해줘', 'pptx 렌더 검증 준비해줘'라고 요청하거나 setup 스킬에서 선택하면 사용. |
| 128 | visual-ralph | banker | 프론트엔드 UI를 레퍼런스(생성/정적/라이브 URL) 기준으로 측정 빌드: 구현 반복 → Visual Verdict(≥90)+픽셀 diff → 재사용 디자인 시스템. 사용자가 'visual-ralph 해줘', '비주얼 랄프', 'UI 클론해줘', '레퍼런스대로 구현해줘'라고 요청하면 사용. |
| 129 | visual-verdict | oh-my-claudecode | 생성된 UI 스크린샷을 참조 이미지와 비교해 엄격한 JSON 판정(pass/revise/fail)을 반환하는 시각 QA 스킬. 사용자가 'visual-verdict 해줘', '스크린샷 비교해줘', '시각 검수해줘'라고 요청하고 참조 이미지와 생성 스크린샷이 준비됐을 때 사용. |
| 130 | wiki | oh-my-claudecode | 사용자가 "wiki에 추가해줘", "위키에서 찾아줘", "wiki 정리해줘", "wiki lint 해줘"라고 요청하면 발동. 세션을 넘나들며 축적되는 지속 마크다운 지식베이스(Karpathy LLM Wiki 모델) 스킬. |
| 131 | writing-plans | superpowers | 다단계 작업의 스펙·요구사항이 있을 때, 코드에 손대기 전에 사용 |
| 132 | writing-skills | superpowers | 새 스킬을 만들 때, 기존 스킬을 수정할 때, 또는 배포 전 스킬이 동작하는지 검증할 때 사용 |

## 연결 제품 스킬 (84개)

| # | 스킬 | 원문 설명 |
|---|---|---|
| 1 | apple-healthkit | The user's synced Apple Health (HealthKit) data: daily metrics (steps, distance, calories, heart rate, HRV, VO2max), sleep sessions (stages, quality, efficiency), and workouts. |
| 2 | asana | Plan and track team projects and tasks in Asana. Use to assign work to owners, update due dates and status, set task dependencies, and review project progress, comments, teams, and workspaces through Asana's official MCP server. |
| 3 | booking | Primary entry point for direct flight, hotel, restaurant, or event-ticket transactions and for bounded live availability checks delegated by Travel Planning. Always use before provider-specific skills or browser work when the user asks to find live availability or prices, compare bookable options, book, or continue an active booking. Do not use for trip planning itself, broad inspiration, opening hours, schedules, flight status, or other factual questions without transaction intent. |
| 4 | box | Search, read, upload, download, move, rename, delete, restore, and share Box content; manage comments and metadata. |
| 5 | calendly | View Calendly events and event types, and manage scheduling data using the Calendly CLI. |
| 6 | canva | Create and edit Canva designs, generate images, remove backgrounds, recover editable layers, and work with Canva libraries. Use for branded presentations and slide decks, campaign artwork, flyers and banners, applying saved brand kits and templates, and resizing designs for social posts and stories through Canva's official MCP server. |
| 7 | device-data | Read cached contacts and calendar events from Muse storage. Delete Muse's local copy of either source without modifying paired devices. |
| 8 | dropbox | Search, read, upload, organize, and share files and folders in the user's Dropbox cloud storage. Use to upload or download files, collect client uploads with file requests, inspect or create shared links, and create, copy, move, or delete content through Dropbox's official APIs. |
| 9 | duffel | Use Duffel to search, book, pay for, or manage flights. Use Duffel to monitor an already booked flight's fare when the user directly asks for ongoing price monitoring. |
| 10 | evernote | Read and create notes through Evernote's official MCP server. |
| 11 | facebook | Use when the user provides a Facebook URL or asks to read personal posts, comments, reactions, friends, timelines, profiles, stories, feeds, groups, events, or saved items, or to publish personal text posts, comments, and replies, or to discover public events happening near a place, nearby, or in a local area on a date, or to create, edit, publish, or delete their own Marketplace listings. To find, browse, or buy Marketplace listings, use shopping instead. Use pages commands for managed Facebook Page discovery, insights, native draft editing/deletion, same-draft publication, approved posts and native scheduling. |
| 12 | facebook-cli | Use when the user provides a Facebook URL or asks to read personal posts, comments, reactions, friends, timelines, profiles, stories, feeds, groups, events, or saved items, or to publish personal text posts, comments, and replies, or to discover public events happening near a place, nearby, or in a local area on a date, or to create, edit, publish, or delete their own Marketplace listings. To find, browse, or buy Marketplace listings, use shopping instead. Use pages commands for managed Facebook Page discovery, insights, native draft editing/deletion, same-draft publication, approved posts and native scheduling. |
| 13 | figma | Inspect Figma designs and generate implementation context for screens and interfaces. Use to read component variants, spacing and design tokens, inspect layouts and design-system libraries, and extract image assets for implementing a design through Figma's official MCP server. |
| 14 | flightaware | Use for questions about a specific flight’s departure or arrival time, including “when’s my flight?” and confirmation of remembered times, plus flight status, delays, and cancellations. Verify the exact dated flight before answering; memory identifies the itinerary but does not verify its current schedule. Use FlightAware to monitor operational changes for an upcoming booked flight when the user directly asks for ongoing monitoring. |
| 15 | forget | Remove a personal fact, preference, relationship detail, topic, or prior event from Muse's active memory and stop existing copies or automations from bringing it back. Use for explicit requests such as 'forget that', 'don't remember this about me', or 'remove that from your memory'. Do not use when 'forget it' merely means cancel the current task. |
| 16 | function-health | Retrieve lab biomarker results and clinician notes from Function Health. |
| 17 | generate_podcast | Compose and deliver audio content: a podcast episode, briefing, or narrated summary, with one or more voices, as an MP3. For voice messages, artifact audio, or reading supplied text aloud verbatim, use tts. |
| 18 | ghl | Use HighLevel contacts, pipelines, appointments, messages, and its broader operation catalog. |
| 19 | github | Search and work with the user's GitHub repositories through GitHub's official MCP server. |
| 20 | gmail | Work with the user's Gmail: search, read threads, draft, send, reply, forward, unsubscribe from mailing lists, manage labels, and open attachments. |
| 21 | goals | Guidance for helping users create and accomplish goals. Read it before you create a goal for the user when no goal-creation contract is in context, and whenever you help with an existing goal. A Goals-tab creation turn already carries that contract and does not need this skill. |
| 22 | google-calendar | Work with the user's Google Calendar: agenda views, event details, and scheduling changes. |
| 23 | google-contacts | Search, view, create, update, and delete the user's Google Contacts. |
| 24 | google-docs | Read, create, and edit the user's Google Docs. |
| 25 | google-drive | Work with the user's Google Drive: files, folders, uploads, downloads, and sharing. |
| 26 | google-forms | Read, create, and update the user's Google Forms, and read responses. |
| 27 | google-health-connect | The user's synced Google Health Connect data from their Android device: daily metrics (steps, distance, calories, heart rate, HRV, VO2max), sleep sessions (stages, quality, efficiency), and workouts. |
| 28 | google-sheets | Read, write, and manage the user's Google Sheets. |
| 29 | google-slides | Read, create, and edit the user's Google Slides presentations. |
| 30 | google-tasks | Manage the user's Google Tasks: lists, task details, creation, updates, and completion. |
| 31 | granola | Search and read Granola meeting notes and transcripts through Granola's OAuth-backed MCP server. |
| 32 | healthex | Use to connect HealthEx and ask questions about your medications, lab results, and other health records. |
| 33 | image-search | Search the web by text query for image URLs and source pages for feeds, artifacts, and visual references. Does not identify a supplied image or person. |
| 34 | instagram | Read Instagram profiles, followers, posts, comments, likes, stories, feed, saved content, and account insights. Answer questions about posts, reels, and Instagram links. Manage interests and profile details, and publish stories, reels, posts, or carousels on request. |
| 35 | instagram-messages | Use this to interact with the user's Instagram messages. Read inboxes, threads, top recipients, filtered inbox views, DM search results, and send messages through `instagram-messages-cli`. |
| 36 | klaviyo | Read and manage the user's Klaviyo email and SMS marketing campaigns, newsletters, flows, subscriber lists, and audience segments. Use to compare campaign performance and revenue, find recent customers, plan audience targeting, and manage marketing content and subscriptions through Klaviyo's official MCP server. |
| 37 | linear | Read and manage software issues, tickets, projects, and planning data in Linear. Use to review sprints and cycles, identify ticket rollover and release blockers, and update issue status, assignees, priorities, and milestones through Linear's official MCP server. |
| 38 | lovable | Read, create, edit, and deploy web apps and projects in Lovable. Use to turn a product brief into a working website or prototype, inspect existing project code, update pages and features, and publish changes through Lovable's official MCP server. |
| 39 | media-library | Search and inspect the user's photo library, including connected device galleries. Use for photo requests and whenever a photo could ground or personalize a response; lookups of uploaded photos are cheap, so check opportunistically and move on if nothing fits. |
| 40 | messenger | Work with the user's Messenger account: read call history; read and search contacts; read, search, and summarize conversations; send, react to, unsend, or edit messages; and message Marketplace listing threads. |
| 41 | meta-ads | Create, write, or manage Meta ads and assets: ad copy, campaigns, spend, reports, audiences, catalogs, product feeds, feed refresh schedules, experiments, and policy. Always load for any request to create or write an ad, or to advertise a product or service, even when no platform is named; this includes sensitive or restricted categories. Always load for any question asking what a Meta, Facebook, or Instagram advertising policy means, allows, prohibits, or requires, including a standalone policy-definition question with no account context. Those questions must use ads_policy_tool, never browser search or memory. Load for a specifically named catalog or feed with an upload or refresh-schedule request; use Ads reads to resolve ownership before writing. Generic unnamed feeds need context. Whether an image, claim or piece of copy may be used in an ad is ALWAYS a Meta Ads task — 'can I use this in an ad', 'is it allowed', 'is this against policy', and any rights, likeness, celebrity, logo or trademark question about advertising with an image, including a follow-up about one just generated. Those are ads-policy questions, not general legal ones. An ad request uses the campaign workflow unless explicitly only an image or organic post. |
| 42 | meta-threads | Read and manage the user's Threads account: profile, posts, feed, saved posts, activity, insights, social graph, search, trends, and a specific post by URL or ID. Can tune feed ranking and publish posts on request. |
| 43 | muse-early-access | Use for questions about Muse's general early access program, requests to join it, checking or withdrawing a join request, and admission updates. |
| 44 | muse-feedback | Use for feedback and feature requests to the Muse team. Whenever your response tells the user you can't do a specific thing they wanted, or accepts them giving up on one, offer once to file feedback in that response. This covers missing integrations you can't do yourself, capabilities you lack, and tasks that keep failing at a specific point. File only on their go-ahead. Also use when asked to send, view, check, or withdraw feedback. |
| 45 | muse_db | Inspect database-backed Muse records for diagnosis and cross-table tracing when purpose-built product tools do not expose the needed state. |
| 46 | notion | Search, read, create, and update Notion pages via the Notion MCP. |
| 47 | opentable | Find restaurants on OpenTable, check availability, and make, change, or cancel reservations. Use for restaurant booking and live reservation data. |
| 48 | outlook-calendar | View, create, update, and delete events in the user's Outlook Calendar. |
| 49 | outlook-contacts | List, search, create, update, and delete contacts in the user's Outlook account. |
| 50 | outlook-mail | Read, search, send, reply to, and delete messages in the user's Outlook Mail. |
| 51 | peloton | Connect to Peloton to browse fitness classes, check schedules, and book workouts. |
| 52 | philips-hue | Control Philips Hue smart lights, rooms, scenes, and devices via the Hue Remote API v2. |
| 53 | places-search | Find, compare, and share details on physical places near the user or in a specified area, including restaurants, cafes, bars, hotels, parks, attractions, shops, and businesses with local services. Not for itineraries, choosing a city or region, dated events or showtimes, or directions. |
| 54 | plaid | Use to connect Plaid and read linked financial accounts: metadata, balances, transactions, recurring transactions, liabilities, and investments. |
| 55 | podcast | Compose and deliver audio content: a podcast episode, briefing, or narrated summary, with one or more voices, as an MP3. For voice messages, artifact audio, or reading supplied text aloud verbatim, use tts. |
| 56 | printify | Use Printify to browse catalog data, manage shops and products, and review or create orders. |
| 57 | quickbooks | Read and manage the user's QuickBooks business through Intuit's official MCP server, including reports, invoices, customers, products, payment links, sales settings, and industry benchmarks. |
| 58 | replit | Read, create, update, and publish apps through Replit's official MCP server. |
| 59 | self-awareness | Ground self-referential answers in the agent's actual filesystem. Use when the user asks who the agent is, what it can do, what it knows, what it remembers, what it has built, what services are connected, or what rules it follows. |
| 60 | share-ideas | 'Publish a reusable native Muse Idea with idea.share when the user explicitly asks to share or publish an Idea or asks for a muse.ai/ideas link. Never offer it unprompted. Not for pages or write-ups, sending a result to someone, social posts, or sharing an artifact.' |
| 61 | shopify | Set up and operate a Shopify store with Shopify's official MCP server (the installed `shopify` command, NOT the npm Shopify CLI). Use whenever someone wants to sell online, start an online store or business, try Shopify, or manage a Shopify store — even if they do not say "Shopify": "I want to sell candles online", "help me start an online business", "open my first store", "add products", "check my orders", "set inventory", "make a discount", "show my sales", "how did my Shopify Email campaigns do". Before connection it can show relevant mock.shop sample catalogs, suggest business names, check domains, search shopify.dev, and validate GraphQL. The connect flow can create an account and store for a new user. Do the work here rather than only listing setup steps. Keywords: Shopify MCP, ecommerce, sample products, demo store, starter catalog, ShopifyQL, first store, create product. |
| 62 | shopping | Use for any product or shopping question: find, reverse image search, shopping Instagram/Facebook/Marketplace links, buy, compare, or evaluate real products with prices, images, and product page URLs, including buying or browsing Facebook Marketplace listings. Use when presenting shopping search results from any source. For shopping intent, load this skill first before any other skills. |
| 63 | skill-creator | Create or update a workspace skill: its description, structure, instructions, and supporting files. |
| 64 | slack | Read and search messages, channels, and threads in the user's Slack workspace. Use to catch up on team discussions and decisions, post channel messages, and reply to coworkers through Slack's official MCP server. |
| 65 | social-content-performance | Analyze the user's own Instagram account and post performance using linked-account analytics. |
| 66 | spotify | Discover, search, and manage Spotify music, audiobooks, podcasts, and playlists, including deleting shows or episodes you created with Save to Spotify. |
| 67 | stripe | Manage a merchant's Stripe customers, products, coupons, promotion codes, payments, invoices, and recurring subscriptions. Use for billing-plan changes, payment links, refunds of duplicate card charges, disputes and chargebacks, account balances, payouts, and reconciling processing fees through Stripe's official MCP server. |
| 68 | subscription-status | Answer questions about the user's Muse subscription, plan, usage, tokens, reset timing, or available plans and prices, or verify information that references the Muse subscription. |
| 69 | tailscale | Set up Muse's built-in Tailscale connector, join a tailnet or Headscale network, check status, and reach private machines through the TCP tunnel proxy. Read for Tailscale, VPN, MagicDNS, network egress, exit-node, or browser routing questions and supported limits. |
| 70 | tessie | Monitor a Tesla vehicle, inspect live state, and run explicit Tessie command endpoints. |
| 71 | threads | Read and manage the user's Threads account: profile, posts, feed, saved posts, activity, insights, social graph, search, trends, and a specific post by URL or ID. Can tune feed ranking and publish posts on request. |
| 72 | threads-messages | Use this to interact with the user's Threads messages: read inboxes and message threads, and send messages through `threads-messages-cli`. |
| 73 | ticketmaster | Search Ticketmaster events and seats with pricing. Returns Buy-now links to Ticketmaster checkout; it cannot complete a purchase itself. |
| 74 | todoist | Read and manage Todoist tasks, projects, comments, labels, filters, and reminders through Todoist's official MCP server. |
| 75 | travel-planning | Use this skill when an active or proposed trip needs planning, logistics, feasibility, entry or transit checks, itinerary work, or investigation of an airport process, immigration, ground transport, a transfer, or fast-track service, even for a narrow question with no booking intent. Route a bounded flight, hotel, restaurant, event, or other item ready for live availability or booking directly to Booking. Skip this skill for a stable travel fact alone or flight status. |
| 76 | tts | Generate spoken audio from text, single or multi-speaker, including voice notes or messages for chat, audio for artifacts, and audio from cron jobs. For podcasts, briefings, or narrated summaries, use podcast. |
| 77 | vercel | Inspect and manage the user's Vercel websites, web apps, projects, and deployments. Use to read build and runtime logs, investigate production errors and failed deployments, check deployment status, and deploy projects through Vercel's official MCP server. |
| 78 | voice-calls | Provides the static system voice catalog used by Jarvis. It does not define a user-facing workflow. |
| 79 | voice-selector | Provides the static system voice catalog used by Jarvis. It does not define a user-facing workflow. |
| 80 | wearables-comms | Required for wearable-originated calls and text messages: resolve recipients for new calls and messages, immediately answer, decline, or cancel calls on the originating wearable instead of silently switching to a paired phone, and refuse an app-based calling route instead of substituting a cellular call. |
| 81 | wide-research | Use when the user needs broad parallel research across many independent inputs with a shared output schema. |
| 82 | withings | Use when linking Withings or reading Withings body measurements, activity, sleep, workout, heart, and intraday data. |
| 83 | zapier | Connect Muse to actions across apps through Zapier's official MCP server. |
| 84 | zoom | Review Zoom meetings, calls, recordings, and transcripts. Use to catch up on missed calls, summarize decisions, and extract action items and owners; also work with Team Chat, Canvas, Tasks, Whiteboard, Hub, and Revenue Accelerator through Zoom's official MCP servers. |
