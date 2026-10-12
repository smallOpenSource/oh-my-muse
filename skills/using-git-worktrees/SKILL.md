---
name: using-git-worktrees
description: "현재 워크스페이스와 격리가 필요한 기능 작업을 시작할 때, 또는 구현 계획 실행 전 사용 - 격리된 워크스페이스 확보"
---

# Git Worktree 사용

## 개요

작업이 격리된 워크스페이스에서 일어나도록 한다. 이 환경의 네이티브 워크트리
수단을 먼저 쓰고, 없으면 수동 git worktree로 폴백한다.

**핵심 원칙:** 기존 격리를 먼저 감지한다. 그 다음 네이티브 도구. 그 다음 git.
하네스와 싸우지 않는다.

**시작 시 알린다:** "using-git-worktrees 스킬을 사용해 격리된 워크스페이스를 준비합니다."

**[환경 한계]** 이 환경에는 EnterWorktree 같은 네이티브 워크트리 도구나
`/worktree` 슬래시 커맨드가 없다. 1a 단계는 건너뛰고 1b(git worktree 직접
사용)로 간다.

## 0단계: 기존 격리 감지

**무엇을 만들기 전에, 이미 격리된 워크스페이스에 있는지 확인한다.**

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

**서브모듈 가드:** `GIT_DIR != GIT_COMMON`은 git 서브모듈 안에서도 참이다.
"이미 워크트리다"라고 결론짓기 전에 서브모듈이 아닌지 확인한다:

```bash
# 경로가 나오면 서브모듈이다, 워크트리가 아니다 — 일반 레포로 취급
git rev-parse --show-superproject-working-tree 2>/dev/null
```

**`GIT_DIR != GIT_COMMON` (서브모듈 아님):** 이미 링크된 워크트리다. 2단계(프로젝트
셋업)로 건너뛴다. 워크트리를 또 만들지 않는다.

브랜치 상태와 함께 보고:
- 브랜치 위: "`<path>`의 격리된 워크스페이스, 브랜치 `<name>`."
- Detached HEAD: "`<path>`의 격리된 워크스페이스 (detached HEAD, 외부 관리). 마무리 시 브랜치 생성 필요."

**`GIT_DIR == GIT_COMMON` (또는 서브모듈):** 일반 레포 체크아웃이다.

워크트리 생성을 상대방이 이미 지시로 표명했는가? 아니라면 만들기 전에 동의를 묻는다:

> "격리된 워크트리를 만들어드릴까요? 현재 브랜치를 변경으로부터 보호합니다."

기존에 선언된 선호는 묻지 않고 따른다. 동의를 거절하면 제자리에서 작업하고
2단계로 건너뛴다.

## 1단계: 격리된 워크스페이스 생성

### 디렉토리 선택

우선순위 순. 명시적 사용자 선호가 관측된 파일시스템 상태보다 항상 우선한다.

1. **지시 파일에 선언된 워크트리 디렉토리 선호를 확인한다.** 있으면 묻지 않고 쓴다.
2. **프로젝트 로컬 워크트리 디렉토리를 확인한다:**
   ```bash
   ls -d .worktrees 2>/dev/null     # 선호 (숨김)
   ls -d worktrees 2>/dev/null      # 대안
   ```
   있으면 쓴다. 둘 다 있으면 `.worktrees`가 이긴다.
3. **다른 안내가 없으면** 기본값은 프로젝트 루트의 `.worktrees/`다.

#### 안전 검증 (프로젝트 로컬 디렉토리만)

**디렉토리가 ignored인지 반드시 검증:**

```bash
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

**ignored가 아니면:** .gitignore에 추가하고 커밋한 뒤 진행한다.

**이유가 중요:** 워크트리 내용을 레포에 커밋해버리는 사고를 막는다.

#### 워크트리 생성

```bash
# 선택된 위치 기준 경로
path="$LOCATION/$BRANCH_NAME"

git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

**샌드박스 폴백:** `git worktree add`가 권한 에러(샌드박스 거부)로 실패하면,
샌드박스가 워크트리 생성을 막았으니 현재 디렉토리에서 작업한다고 상대방에게
말한다. 그 다음 제자리에서 셋업과 베이스라인 테스트를 실행한다.

## 2단계: 프로젝트 셋업

자동 감지 후 적절한 셋업 실행:

```bash
# Node.js
if [ -f package.json ]; then npm install; fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

## 3단계: 깨끗한 베이스라인 검증

워크스페이스가 깨끗하게 시작하는지 테스트 실행:

```bash
# 프로젝트에 맞는 명령
npm test / cargo test / pytest / go test ./...
```

**테스트가 실패하면:** 실패를 보고하고, 진행할지 조사할지 묻는다.

**테스트가 통과하면:** 준비 완료를 보고한다.

### 보고

```
워크트리 준비: <전체 경로>
테스트 통과 (<N>개 테스트, 0 실패)
<기능명> 구현 준비 완료
```

## 빠른 참조

| 상황 | 행동 |
|------|------|
| 이미 링크된 워크트리 | 생성 건너뛰기 (0단계) |
| 서브모듈 안 | 일반 레포로 취급 (0단계 가드) |
| `.worktrees/` 있음 | 쓴다 (ignored 검증) |
| `worktrees/` 있음 | 쓴다 (ignored 검증) |
| 둘 다 있음 | `.worktrees/` |
| 둘 다 없음 | 지시 파일 확인, 그 다음 `.worktrees/` 기본값 |
| 디렉토리 not ignored | .gitignore에 추가 + 커밋 |
| 생성 시 권한 에러 | 샌드박스 폴백, 제자리 작업 |
| 베이스라인 테스트 실패 | 실패 보고 + 질문 |
| package.json/Cargo.toml 없음 | 의존성 설치 건너뛰기 |

## 흔한 합리화

| 변명 | 현실 |
|------|------|
| "워크트리에 아닌 게 뻔하니 확인 불필요" | 0단계를 실행한다. 하네스가 만든 격리와 서브모듈은 둘 다 눈대중을 속인다. 감지 명령이 확정한다. |
| "워크트리 디렉토리는 이미 ignored일 거야" | `git check-ignore`를 실행한다. ignored 안 된 워크트리 디렉토리는 트리 전체를 레포에 커밋한다. |
| "아무 디렉토리 이름이나 된다" | 명시적 지시가 기존 프로젝트 로컬 디렉토리보다, 그것이 `.worktrees/` 기본값보다 우선한다. |
| "워크스페이스가 새것이니 베이스라인 테스트는 나중에" | 더러운 베이스라인은 이후 모든 실패를 모호하게 한다. 지금 테스트를 돌린다. 실패를 넘기고 진행하는 것은 상대방의 몫이다. |
