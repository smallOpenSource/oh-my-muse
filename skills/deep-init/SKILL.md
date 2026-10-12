---
name: deep-init
description: "코드베이스 전체에 계층형 AGENTS.md 문서를 생성·갱신한다(부모 역참조·MANUAL 섹션 보존). 사용자가 'deep-init 해줘', 'deepinit 해줘', 'AGENTS.md 생성해줘', '코드베이스 문서화해줘'라고 요청하면 사용."
---

# deep-init — 계층형 AGENTS.md 초기화

## Purpose

코드베이스 전 디렉터리에 **AI가 읽는 문서** `AGENTS.md`를 계층형으로 생성한다.
각 파일은 상위로 역참조(`<!-- Parent: ../AGENTS.md -->`)해 내비게이션 가능한 트리를 이룬다.
(자율 풀사이클 빌드 스킬인 `ultra-init`과는 별개다.)

**핵심 로직은 런타임 무관**이다(순수 fs + 문서 생성). 병렬 탐색·분석·문서 작성을
서브에이전트에 위임할 때는 `subagent.spawn`을 사용한다. 위임이 불가능하면
**직접**(Read/Write/exec + `find`/`grep`) 수행 — 성능만 저하되고 결과는 동일하다.

## Workflow

### 핵심 개념

`AGENTS.md`는 에이전트가 다음을 이해하게 돕는다: 각 디렉터리의 내용, 컴포넌트 관계,
그 영역 작업 시 특수 지침, 의존성. 루트를 제외한 모든 `AGENTS.md`는 상위 참조 태그를 포함한다:

```
/AGENTS.md                       ← 루트(부모 태그 없음)
├── src/AGENTS.md                ← <!-- Parent: ../AGENTS.md -->
│   └── src/utils/AGENTS.md      ← <!-- Parent: ../AGENTS.md -->
└── docs/AGENTS.md               ← <!-- Parent: ../AGENTS.md -->
```

### Step 1 — 디렉터리 구조 매핑

`subagent.spawn`으로 병렬 탐색 에이전트를 띄우거나(불가하면 `find`) 재귀 나열.
제외: `node_modules · .git · dist · build · __pycache__ · .venv · coverage · .next · .nuxt`.

### Step 2 — 작업 계획(depth 순)

디렉터리별 todo를 깊이 레벨로 조직: Level 0 `/` → Level 1 `/src`,`/docs` → Level 2 … .

### Step 3 — 레벨별 생성 (부모 먼저)

**부모 레벨을 자식보다 먼저** 생성해 부모 참조가 유효하게 한다.
각 디렉터리: 파일 읽기 → 목적·관계 분석 → AGENTS.md 생성 → 올바른 부모 참조로 쓰기.
큰 디렉터리는 전용 서브에이전트(`subagent.spawn`)에, 작은 디렉터리는 여러 개를 한 에이전트에 배치.

### Step 4 — 기존 파일 비교·갱신

이미 있으면: 기존 읽기 → 자동생성 섹션 vs `<!-- MANUAL -->` 섹션 식별 → 파일 추가/삭제/구조변경
비교 → **자동 섹션만 갱신, MANUAL 보존**, timestamp 갱신.

### Step 5 — 계층 검증

| 검사 | 방법 | 조치 |
|------|------|------|
| 부모 참조 해석 | 각 `<!-- Parent: -->` 경로 존재 확인 | 경로 수정/고아 제거 |
| 고아 AGENTS.md 없음 | 파일 위치 ↔ 디렉터리 구조 대조 | 고아 삭제 |
| 완전성 | 전 디렉터리에 AGENTS.md 유무 | 누락 생성 |
| timestamp 최신 | `<!-- Generated: -->` 확인 | 오래된 것 재생성 |

검증 스크립트: `find . -name AGENTS.md -type f` / `grep -r "<!-- Parent:" --include=AGENTS.md .`

### 빈 디렉터리 처리

| 조건 | 조치 |
|------|------|
| 파일·하위 없음 | **건너뜀** (생성 안 함) |
| 파일 없고 하위 있음 | 하위 목록만 담은 최소 AGENTS.md |
| 생성물만(*.min.js,*.map) | 건너뜀/최소 |
| 설정 파일만 | 설정 목적 기술 AGENTS.md |

### 병렬화 규칙

1. 같은 레벨 디렉터리 → 병렬. 2. 다른 레벨 → 순차(부모 먼저). 3. 큰 디렉터리 → 전용 에이전트.
4. 작은 디렉터리 → 여러 개를 한 에이전트에 배치.

## Output Contract

### AGENTS.md 템플릿

```markdown
<!-- Parent: {상위_상대경로}/AGENTS.md -->
<!-- Generated: {timestamp} | Updated: {timestamp} -->

# {Directory Name}

## Purpose
{이 디렉터리가 담는 것과 역할, 한 문단}

## Key Files
| File | Description |
|------|-------------|
| `file.ts` | 목적 한 줄 |

## Subdirectories
| Directory | Purpose |
|-----------|---------|
| `subdir/` | 내용 (see `subdir/AGENTS.md`) |

## For AI Agents
### Working In This Directory
{이 영역 수정 시 특수 지침}
### Testing Requirements
{변경 검증 방법}
### Common Patterns
{여기서 쓰는 코드 패턴/규약}

## Dependencies
### Internal
{의존하는 코드베이스 다른 부분}
### External
{핵심 외부 패키지}

<!-- MANUAL: 이 줄 아래 수동 추가 노트는 재생성 시 보존된다 -->
```

### 품질 기준

- **포함**: 정확한 파일 설명·올바른 부모 참조·하위 링크·AI 에이전트 지침.
- **회피**: 일반 보일러플레이트·틀린 파일명·깨진 부모 참조·중요 파일 누락.

## Operating Rules

### 함정

- **부모 먼저** 생성하지 않으면 자식의 부모 참조가 깨진다(Step 3 순서 엄수).
- `<!-- MANUAL -->` 아래를 재생성이 덮으면 수동 지식 소실 — Step 4 병합 필수.
- 대량 디렉터리 재스캔 반복 금지(디렉터리 목록 캐시, 변경 없으면 skip).

### 한계 (Muse 환경)

- 원본의 Claude Code 전용 서브에이전트 타입(oh-my-claudecode:explore / architect / writer)과 Codex(OMX) worker/explore는 이 환경에 없다. `subagent.spawn`의 일반 스폰으로 대체하며, 역할(explore/architect/writer)은 스폰 시 프롬프트에 명시한다.
- 위임 없이 직접 수행하는 폴백 경로는 그대로 유지한다.
