---
name: deepinit
description: 사용자가 "deepinit 해줘", "코드베이스 초기화 문서 만들어줘", "디렉토리별 AGENTS.md 생성해줘"라고 요청하면 발동. 코드베이스를 계층적으로 스캔해 디렉토리마다 AI 가독 문서(AGENTS.md)를 생성·갱신하는 스킬.
---

# Deepinit

## Purpose

- 코드베이스 전체에 계층적 `AGENTS.md` 문서를 생성한다. 각 `AGENTS.md`는 해당 디렉토리의 내용, 컴포넌트 간 관계, 작업 시 특별 지침, 의존성을 AI가 읽기 쉽게 정리한 문서다.
- 계층 태깅: 루트를 제외한 모든 `AGENTS.md`는 본문 맨 위에 가시 문구로 부모 참조를 포함한다.
  `**Parent context:** `../AGENTS.md``
  (HTML 주석 금지 — 주석은 메모리 파일이 모델에 전달되기 전에 제거되므로 보이지 않는다.)

## Workflow

### 1. 디렉토리 구조 매핑

- `subagent.spawn`으로 탐색 에이전트를 실행해 모든 디렉토리를 재귀 나열한다. 제외: `node_modules`, `.git`, `dist`, `build`, `__pycache__`, `.venv`, `coverage`, `.next`, `.nuxt`.

### 2. 레벨별 작업 계획

- 깊이 레벨별로 todo 목록을 만든다: Level 0 = `/` (루트), Level 1 = `/src`, `/docs` …

### 3. 레벨 단위로 생성 (부모 먼저)

**중요: 부모 레벨을 자식보다 먼저 생성** — 부모 참조 경로가 유효해야 한다.

디렉토리마다:
1. 디렉토리 내 모든 파일을 읽는다.
2. 목적과 관계를 분석한다.
3. 아래 템플릿으로 `AGENTS.md`를 생성한다.

```markdown
# {디렉토리 이름}

**Parent context:** `{상대경로}/AGENTS.md`
**Generated:** {타임스탬프} · **Updated:** {타임스탬프}

## Purpose
{디렉토리의 내용과 역할을 한 단락으로}

## Key Files
| File | Description |
|------|-------------|
| `file.ts` | 한 줄 설명 |

## Subdirectories
| Directory | Purpose |
|-----------|---------|
| `subdir/` | 내용 (see `subdir/AGENTS.md`) |

## For AI Agents
### Working In This Directory
{이곳에서 파일을 수정할 때의 특별 지침}
### Testing Requirements
{테스트 방법}
### Common Patterns
{코드 패턴·컨벤션}

## Dependencies
### Internal
{코드베이스 내부 의존}
### External
{주요 외부 패키지·라이브러리}

## Manual Notes
{사람이 쓴 메모 — 재생성 시 보존}
```

- 빈 디렉토리 처리: 파일도 없고 서브디렉토리도 없으면 **스킵**. 서브디렉토리만 있으면 서브디렉토리 목록만 담은 최소 `AGENTS.md` 생성. 생성물(`*.min.js`, `*.map`)만 있으면 스킵 또는 최소 문서. 설정 파일만 있으면 설정 목적 설명 문서 생성.

### 4. 업데이트 모드 (기존 AGENTS.md가 있을 때)

1. 기존 내용을 읽는다. `## Manual Notes` 이하(사람 메모)는 **절대 건드리지 않는다**.
2. 추가·삭제·구조 변경을 비교해 자동 생성 섹션만 갱신하고, 타임스탬프를 업데이트한다.

### 5. 계층 검증

- `find . -name "AGENTS.md" -type f`로 전체 목록을 뽑고, 각 파일의 `**Parent context:**` 경로가 실제로 존재하는지 확인한다.
- 고아(부모가 없는 참조, 디렉토리 구조와 맞지 않는) 파일은 경로를 수정하거나 삭제한다.
- 누락된 디렉토리는 생성한다.

### 병렬화 규칙

- 같은 레벨의 디렉토리: `subagent.spawn`으로 **병렬** 처리.
- 다른 레벨: 순차 (부모 먼저).
- 큰 디렉토리: 디렉토리당 전용 에이전트. 작은 디렉토리: 하나로 묶어 배치 처리.
- 역할 매핑: 디렉토리 매핑→`explore`, 파일 분석→`architect`, 문서 생성·작성→`writer` (역할 프롬프트는 `~/workspace/skills/team/references/agents/` 재사용).

## Output Contract

- 생성·갱신된 `AGENTS.md` 파일 목록 (경로).
- 계층 검증 결과: 부모 참조 오류·고아 파일·누락 디렉토리 처리 내역.
- 스킵된 디렉토리와 사유.
- 품질 기준: 정확한 파일 설명, 올바른 부모 참조, 서브디렉토리 링크, AI 작업 지침 포함. 상투적 문구·잘못된 파일명·깨진 참조 금지.

## Operating Rules

1. **OMC PostToolUse 디렉토리 컨텍스트 인젝터 없음** — 원본은 접근한 파일에서 위로 올라가며 가장 가까운 `AGENTS.md`를 주입하는 OMC hooks에 의존한다. 이 환경에는 해당 hooks가 없다. 대안: 루트에 `CLAUDE.md` 심링크 또는 `@AGENTS.md` import를 추가해 루트 문서가 로드되도록 하고, 중첩 파일은 자동 로드되지 않을 수 있음을 사용자에게 알린다.
2. **부모 참조는 가시 prose로** — HTML 주석(`<!-- Parent: ... -->` 등)은 절대 사용하지 않는다.
3. **Manual Notes 보존** — 재생성 시 사람이 쓴 섹션은 항상 유지한다.
4. **디렉토리 스캔 캐시** — 같은 디렉토리를 중복 스캔하지 않는다. 변경 없는 디렉토리는 재생성을 스킵한다.
5. **명령어 흡수**: 원본 `/oh-my-claudecode:deepinit` 슬래시 커맨드는 단순 디스패치 래퍼였으므로, 이 스킬의 채팅 트리거("deepinit 해줘" 등)로 대체된다.
