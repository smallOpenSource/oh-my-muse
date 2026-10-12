---
name: append_wiki
description: "(banker) 새로 배운 비자명 지식을 프로젝트 wiki(.omc/wiki)에 구조화 적재·병합. 사용자가 'append_wiki 해줘'/'위키 기록해줘'/'wiki에 정리해줘'/'알게 된 내용 기록해줘'라고 요청하면 사용."
---

# append_wiki — 작업 지식을 wiki에 적재

## Purpose
- 이번 작업에서 **새로 배운 비자명한 지식**(결정·함정·근본원인)을 프로젝트 wiki에 구조화해 남김
- 저장 위치: 대상 프로젝트의 `.omc/wiki/*.md`(프로젝트 로컬, git-ignored), 목차 `index.md`, 이력 `log.md`
- 답변·설명은 한글(도구명·경로·식별자 등 기술 토큰은 영문 유지)

## When to use
- 기능 구현/디버깅/리팩터링 등 한 덩어리 작업이 끝났을 때
- 사용자가 "append_wiki", "위키 기록", "wiki에 정리해", "알게 된 내용 기록해" 등으로 요청할 때
- 다음 세션/다른 사람이 알면 시간을 아낄 비자명한 결정·함정·근본원인이 생겼을 때

## 쓰지 않을 때
- 코드/테스트/깃 히스토리/CLAUDE.md가 그대로 담는 사실(중복)
- 이번 대화에서만 의미 있는 일회성 잡담
- 광범위한 문서 재작성(이건 기록이 아니라 별도 작업)

## Workflow

### 0) wiki 메커니즘 확인 (이 환경의 한계)
- 원본 스킬은 OMC `wiki_*` MCP 도구(`wiki_ingest`/`wiki_query`/`wiki_list`/`wiki_lint`)를 사용했으나, **이 환경에는 해당 MCP 도구가 없음**(skill_search 확인 결과 없음)
- **가장 가까운 대안: wiki 도구가 쓰던 저장 형식을 파일로 직접 에뮬레이션** — `.omc/wiki/*.md` 마크다운 파일 + `index.md` + `log.md`를 직접 읽고 씀
- 새 파일 형식(기존 MCP 출력과 호환):
  ```markdown
  ---
  title: "ThreadPool Deadlock Acquire-Before-Pool"
  tags: [threadpool, deadlock, concurrency]
  category: debugging
  confidence: high
  sources: ["path/to/file.py"]
  ---
  # ThreadPool Deadlock Acquire-Before-Pool
  ...한글 본문...
  ```
  - 슬러그 = 영문 title에서 소문자+하이픈(예: `threadpool-deadlock-acquire-before-pool`). 파일명 = `<slug>.md`
  - 동일 title에 이미 파일이 있으면 **교체가 아니라 append**(기존 본문 아래에 새 섹션 추가)

### 1) 무엇을 남길지 식별
- **아키텍처/설계 결정**과 그 이유(대안 포함) → `architecture` / `decision`
- **디버깅 근본원인 + 증상 + 재현 + 수정 + 교훈** → `debugging`
- **재사용 가능한 패턴/불변식** → `pattern`
- **환경·운영 함정**(빌드/재기동/인증/포트/로그 등) → `environment`
- **명명·구조 규칙** → `convention`. 외부 링크/티켓 → `reference`
- **범위 외 finding**(이번엔 안 고쳤지만 알아야 할 것)도 명시적으로
- "왜/어떻게 적용"이 핵심 — 코드만 봐선 모르는 맥락을 남김

### 2) 기존 페이지 확인 (중복 방지)
- `.omc/wiki/` 목차(`index.md`)를 보고, 주제 키워드로 기존 파일들을 읽어 중복 확인
- 관련 페이지가 있으면 **같은 title로 append**(교체가 아니라 추가)

### 3) 페이지 단위로 응축
- **한 페이지 = 한 주제.** 크면 여러 페이지로 쪼개고 `[[slug]]`로 상호 링크
- **title은 영문**(슬러그가 title에서 생성되므로 한글 title은 슬러그 불안정 → cross-link 깨짐 위험). 본문은 한글로 충실히
- 표·코드블록·파일경로(`path:line`)로 증거 밀도 높게. 추측 금지, 검증된 사실만

### 4) 적재
- 파일이 없으면 새로 쓰고, 있으면 기존 본문 아래에 새 섹션 append
- 본문 상단 frontmatter에 `title`·`tags`(최대 20개)·`category`·`sources`·`confidence(high|medium|low)` 포함
- 관련 페이지는 본문에 `[[related-slug]]`로 연결. 여러 페이지면 영문 title을 먼저 확정해 cross-link 슬러그 일치

### 5) 검증 (lint 직접 수행)
- `[[slug]]` 참조가 실제 파일 슬러그와 맞는지 grep으로 확인 — 깨진 링크가 있으면 슬러그를 맞춰 다시 작성
- orphan(아무 데서도 링크 안 됨)/stale(오래됨)/oversized(50KB 초과) 점검
- **environment.md 위생(정화는 이식 가능, 재생성 hook은 OMC 전용)**
  - `.omc/wiki/environment.md`에 `[object Object]`가 보이면 정화:
    - `**Frameworks:**` 줄 → `project-memory.json`의 `techStack.frameworks[].name`들을 `, `로 조인한 값으로 교체
    - `## Build Commands`의 객체형 값 줄(예: `- **scripts:**` 뒤 `[object Object]`) → 삭제(문자열 command만 남김)
  - **한계(정직히 명시)**: 원본의 이 hook 자동재생성(`hooks/wiki/session-hooks`)과 소스 근본 패치(`~/.claude/plugins` 탐색·dist .js 수정)는 OMC/Claude Code 전용 메커니즘으로 이 환경에 없음 — 해당 단계는 생략. 이 환경에서는 수동 정화가 유지됨(자동재생성 주체 자체가 없음)

### 6) 보고 (한글)
- 생성/갱신된 페이지와 슬러그 목록
- lint 결과
- environment.md 위생: `[object Object]` 정화 여부
- 저장 위치: `.omc/wiki/*.md`, 목차 `index.md`, 이력 `log.md`

## Output Contract
- 생성/갱신된 페이지 목록(슬러그 포함) + lint 결과(깨진 링크/orphan/stale/oversized) + environment.md 정화 여부
- 저장 위치 명시(`.omc/wiki/*.md`, `index.md`, `log.md`)

## Operating Rules
- **삭제보다 보존, 중복보다 병합.** 같은 주제는 새 페이지 대신 기존 페이지에 append
- **비자명성 우선.** "왜 이렇게 했나 / 어떤 함정이 있었나 / 어떻게 재현·검증했나"
- **증거 기반.** 파일:라인, 명령, 측정값, 테스트명으로 뒷받침
- **상호 링크 적극.** 아키텍처 ↔ 디버깅 ↔ 환경 페이지를 `[[slug]]`로 엮음
- wiki는 키워드+태그 검색(벡터 임베딩 없음) → **검색 가능한 tags**를 충분히 단 것
- wiki 도구는 키워드+태그 검색이므로 한글 본문에도 영문 기술 키워드를 함께 남김
- 이 환경에 `wiki_*` MCP 도구가 없으므로 파일 직접 에뮬레이션이 정식 경로. 나중에 동등한 wiki 도구/스킬이 연결되면 그 경로로 전환
