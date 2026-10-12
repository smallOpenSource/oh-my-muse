---
name: setup
description: "구성요소·의존성을 골라 설치하는 오케스트레이터(런타임 node·python·java, LSP, tmux, MCP, sandbox, playwright 등 설치 스킬 묶음). 사용자가 'setup 해줘', '개발환경 설치해줘', 'node 설치해줘', 'playwright 설치해줘'처럼 구성요소 설치를 요청하면 사용."
---

# setup — 구성요소 설치 오케스트레이터

## Purpose
설치 스킬들(setup-node, setup-python, setup-java, setup-lsp, setup-tmux, setup-pwsh, setup-mcp, setup-sandbox, setup-omc, harness-factory, setup-insane-search, setup-omc-hud, setup-stitch, setup-playwright, docs-setup, motion-graphic-setup, 3d-intro-setup)을 **골라서 실행**하는 오케스트레이터. 답변은 한글(기술 토큰 영문).

**원천**: banker 플러그인의 `/banker:setup` 커맨드를 Muse 환경용 스킬로 이식. 원본의 `AskUserQuestion`(multi-select)·Claude Code `Skill("banker:<name>")` 호출은 아래 환경 매핑으로 대체한다.

### Muse 환경 매핑
| 원본 | 이 환경에서의 대체 |
|---|---|
| `AskUserQuestion`(multiSelect) | 사용자에게 설치할 컴포넌트를 직접 묻는다(목록 제시 후 선택 수신). `$ARGUMENTS`에 컴포넌트명이 명시돼 있으면 질문 생략하고 그것만 실행 |
| `Skill("banker:<name>")` | 해당 이름의 스킬을 호출한다(예: `setup-node`) |
| Codex 런타임 분기 | 생략 (이 환경 전용) |
| `claude mcp list` / `codex mcp list` 확인 | MCP 서버 추가 후에는 세션 갱신 뒤 연결을 확인한다(확인 수단이 없으면 사용자에게 확인 요청) |

## Workflow

### 1. 선택 받기
인자에 컴포넌트명이 명시돼 있으면 그것만 실행(질문 생략). 비어 있으면 아래 목록을 제시하고 설치할 항목을 사용자에게 물어 받는다. 항목은 **계층/의존 순서**로 묶여 있으니, 뒤 계층을 고르면 앞 계층 전제를 먼저 채운다.

**런타임 (기반 — 먼저)**
- **setup-node** — nvm + Node 22(winget/nvm-windows). npx 기반 MCP·CLI 전제.
- **setup-python** — Python 3.11 + pipx + uv(PEP668). `setup-lsp`·`setup-mcp`·`docs-setup` 전제.
- **setup-java** — JDK 21 + JAVA_HOME(Debian=Adoptium). `setup-lsp`의 jdtls 요구.

**개발도구**
- **setup-lsp** — 언어별 LSP(vtsls·basedpyright·bash·jdtls·spring) + lsp-mcp 브리지. (의존: node·python·java)
- **setup-tmux** — tmux(Rocky8 3.6a 소스빌드)/psmux(Windows). 장기 실행 세션 전제.
- **setup-pwsh** — Windows PowerShell 7 환경($PROFILE UTF-8·Terminal·Git). 비-Windows는 no-op.
- **setup-mcp** — 공통 MCP 서버(context7·seq-thinking·filesystem·git·fetch). (의존: node·python)
- **setup-sandbox** — OS별 샌드박스(bubblewrap+userns / AppContainer / Seatbelt) + rust + git safe.directory.

**프레임워크·플러그인**
- **setup-omc** — oh-my-claudecode(OMC) 설치/갱신. `all-in-one`·`ultra-init`·`front-qa` 의존성.
- **harness-factory** — revfactory/harness(팀 아키텍처 팩토리) 설치+구성+안내.
- **setup-insane-search** — insane-search 플러그인(차단 사이트 우회).
- **setup-omc-hud** — omc_hud 상태표시줄(OS별).
- **setup-stitch** — Stitch(디자인 생성) MCP 프록시 등록(RockyLinux8 proxy-script, API key 필요).

**의존성 라이브러리**
- **setup-playwright** — Playwright + 브라우저 + Xvfb(RHEL8/Rocky8 폴백). (`ultra-ui-qa`·`audit-web-page`·`play-qa` 의존성)
- **docs-setup** — arch-diagram·pdf-vision-extract 의존성(python-pptx·pymupdf·plantuml). (의존: python)
- **motion-graphic-setup** — hyperframes(무료 모션 그래픽 CLI) 전제조건(Node≥22 + ffmpeg → `npx hyperframes`). (`motion-graphic-make` 의존성)
- **3d-intro-setup** — Azure Sora-2/gpt-image-2 3D 인트로용 크레덴셜·의존성(Node/ffmpeg) + 무과금 프리플라이트. (`3d-intro-build` 의존성)

### 2. 실행
선택된 각 항목을 호출한다(미선택은 건드리지 않음).
- **의존 순서 강제**: 뒤 계층을 고르면 전제 스킬을 먼저 실행한다 — `setup-lsp` 전에 setup-node·setup-python·setup-java; `setup-mcp` 전에 setup-node·setup-python; `docs-setup` 전에 setup-python. 이미 설치돼 있으면 각 스킬이 감지해 skip(멱등).
- 각 스킬이 OS를 감지해 알맞은 절차로 설치하고 끝에 검증한다. 한 항목이 실패해도 정직히 보고하고 다음 항목 진행.

### 3. 마무리 보고(한글)
설치된 항목·검증 결과·**재시작/reload 필요 여부**.
- 플러그인 설치(insane-search 등)는 런타임 재시작/reload 후 반영될 수 있다.
- MCP 추가(stitch 등)는 세션 갱신 후 연결 확인.

## Output Contract
- 설치된 항목별: 실행한 스킬 / 검증 결과(각 스킬의 검증 출력) / 재시작 필요 여부.
- 실패 항목은 정직히 보고(원인·다음 단계)하고 다음 항목을 계속 진행.
- 선택받지 않은 항목은 건드리지 않는다.

## Operating Rules
1. 각 설치는 **비파괴·멱등**(이미 설치면 skip).
2. 시크릿(API key 등)은 사용자 입력/환경변수로만 — 출력·커밋 금지.
3. root 불가/conda 부재 등은 각 스킬의 폴백 경로로 처리(추정 금지, 감지 기반).
4. 인자에 컴포넌트명이 있으면 질문을 생략한다. 없으면 목록을 제시하고 선택을 받는다.
5. 이 환경의 한계: 목록의 설치 스킬 중 스킬 목록에 없는 것이 있으면 해당 항목은 실행하지 않고 "미이식/부재"로 보고한다. OMC/OMX 전용 전제(`setup-tmux`의 OMC team 등)는 해당 스킬의 Operating Rules 한계를 따른다.
6. 이 VM은 Linux다. Windows/macOS 전용 분기(setup-pwsh, winget 등)는 다른 머신에서 이 스킬을 쓸 때를 위한 것이며 이 VM에서는 no-op 또는 Linux 분기만 실행된다.
