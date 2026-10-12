---
name: finishing-a-development-branch
description: "구현이 끝나고 모든 테스트가 통과한 뒤, 작업을 어떻게 통합할지 정할 때 사용"
---

# 개발 브랜치 마무리

## 개요

**핵심 원칙:** 테스트 검증 → 환경 감지 → 옵션 제시 → 선택 실행 → 정리.

**시작 시 알린다:** "finishing-a-development-branch 스킬을 사용해 작업을 마무리합니다."

## 1단계: 테스트 검증

프로젝트 전체 테스트 스위트 실행 (`npm test` / `cargo test` / `pytest` / `go test ./...`).

**테스트가 실패하면** 실패를 보고하고 멈춘다 — 메뉴는 그린 스위트 뒤에 나온다.

**테스트가 통과하면** 2단계로.

## 2단계: 환경 감지

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
WORKTREE_PATH=$(git rev-parse --show-toplevel)
```

어떤 메뉴를 보여줄지와 정리 방식을 결정한다:

| 상태 | 메뉴 | 정리 |
|------|------|------|
| `GIT_DIR == GIT_COMMON` (일반 레포) | 표준 3개 옵션 | 워크트리 없음 |
| `GIT_DIR != GIT_COMMON`, 이름 있는 브랜치 | 표준 3개 옵션 | 출처 기반 (6단계) |
| `GIT_DIR != GIT_COMMON`, detached HEAD | 축소 2개 옵션 (머지 없음) | 외부 관리 — 그대로 둔다 |

## 3단계: 베이스 브랜치 확정

베이스 브랜치는 이 작업이 갈라진 곳 — 보통 계획서·대화·브랜치 upstream에 있다.
모르면 묻는다: "이 브랜치는 <최선 추측>에서 갈라진 게 맞나요?" 머지 전에 확인한다.
잘못된 베이스에 머지하면 되돌리기 비싸다.

## 4단계: 옵션 제시

**일반 레포와 이름 있는 브랜치 워크트리 — 정확히 이 3개 옵션:**

```
구현 완료. 어떻게 할까요?

1. <base-branch>에 로컬로 머지
2. 푸시하고 Pull Request 생성
3. 브랜치 그대로 두기 (나중에 직접 처리)

어느 쪽인가요?
```

**Detached HEAD — 정확히 이 2개 옵션:**

```
구현 완료. detached HEAD입니다 (외부 관리 워크스페이스).

1. 새 브랜치로 푸시하고 Pull Request 생성
2. 그대로 두기 (나중에 직접 처리)

어느 쪽인가요?
```

메뉴는 쓴 그대로, 간결하게, 위 목록의 옵션으로만 제시한다. 작업 폐기는
상대방이 명시적으로 요청할 때만 다룬다 (아래 참조). 답을 기다린다 — 통합 결정은
상대방의 몫이다.

## 5단계: 선택 실행

### 옵션 1: 로컬 머지

```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"

git checkout <base-branch>
git pull
git merge <feature-branch>

# 머지 결과에 테스트 실행
<test command>
```

머지 결과가 빨간색이면: 멈추고, 워크트리·브랜치를 그대로 두고 조사한다 — 푸시된
게 없으니 머지는 로컬이고 복구 가능하다.

머지 결과가 그린색이면: 워크트리 정리 (6단계), 브랜치 삭제:

```bash
git branch -d <feature-branch>
```

### 옵션 2: 푸시하고 PR 생성

```bash
git push -u origin <feature-branch>
# detached HEAD에서는 원격에 새 브랜치 이름 지정:
# git push origin HEAD:refs/heads/<new-branch>
```

그 다음 <base-branch>를 대상으로 pull/merge request 생성 — 사용 가능한 forge CLI,
또는 푸시 시 출력되는 생성 URL. 레포의 PR 템플릿·관례가 있으면 따르고, URL을
상대방에게 보고한다.

워크트리는 유지한다 — PR 피드백을 그곳에서 반영한다.

### 옵션 3: 그대로 두기

보고: "브랜치 <name> 유지. 워크트리 <path> 보존."

### 상대방이 작업 폐기를 요청하면

이 경로는 작업을 버리라고 명시적으로 요청했을 때만 존재한다. 먼저 확인한다:

```
아래를 영구 삭제합니다:
- 브랜치 <name>
- 모든 커밋: <commit-list>
- 워크트리 <path>

확인하려면 'discard'를 입력하세요.
```

정확한 확인을 기다린다. 도착하면:

```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
```

워크트리 정리 (6단계) 후 브랜치 강제 삭제:

```bash
git branch -D <feature-branch>
```

## 6단계: 워크스페이스 정리

**옵션 1과 확인된 폐기에서 실행.** 옵션 2·3은 항상 워크트리를 보존한다. 두 호출자
모두 이미 메인 레포 루트로 디렉토리를 옮겼다 — 워크트리 제거는 워크트리 밖에서
실행 — 2단계에서 캡처한 `GIT_DIR`/`GIT_COMMON`/`WORKTREE_PATH` 값을 사용한다.

**`GIT_DIR == GIT_COMMON`:** 일반 레포, 정리할 워크트리 없음. 끝.

**`WORKTREE_PATH`가 `.worktrees/` 또는 `worktrees/` 아래:** superpowers가 만든
워크트리 — 우리가 정리한다:

```bash
git worktree remove "$WORKTREE_PATH"
git worktree prune
```

**제거가 거부되면** (수정·untracked 파일 포함): 그 파일들은 그 워크트리에만 있다 —
커밋 안 된 계획·노트·스크래치. 내 판단으로 `--force` 금지. 무엇이 걸려 있는지
보여주고 묻는다:

```bash
git -C "$WORKTREE_PATH" status --porcelain -uall
```

```
워크트리 제거 거부 — 커밋된 적 없는 파일:

<file list>

1. 정리 전 <branch>에 커밋
2. <메인 레포 루트>로 이동
3. 삭제 (복구 불가)

어느 쪽인가요?
```

선택을 수행한 뒤 워크트리를 제거한다.

**그 외:** 호스트 환경이 이 워크스페이스를 소유한다 — 그대로 둔다.

## 빠른 참조

| 옵션 | 머지 | 푸시 | 워크트리 유지 | 브랜치 정리 |
|------|------|------|--------------|-------------|
| 1. 로컬 머지 | 예 | - | - | 예 |
| 2. PR 생성 | - | 예 | 예 | - |
| 3. 그대로 | - | - | 예 | - |
| 폐기 (명시적 요청만) | - | - | - | 예 (강제) |

## 흔한 합리화

| 변명 | 현실 |
|------|------|
| "이 세션 초에 테스트 통과했었다" | 통합하려는 그 트리에서 스위트를 실행한다. 그린 실행은 실행된 트리만 증명한다. |
| "머지하길 원하는 게 뻔하다" | 통합은 상대방의 결정이다. 메뉴를 제시하고 기다린다. |
| "폐기해달라는 듯이 말했다" | 메뉴는 쓴 그대로 완전하다. 폐기는 상대방이 말 그대로 요청할 때만. |
| "'응, 없애줘'는 확인이다" | `discard`라는 입력만이 삭제를 승인한다. |
| "PR이 떴으니 워크트리는 잡동사니다" | PR 피드백은 그 워크트리에서 고친다. 랜딩까지 유지한다. |
| "이 워크트리도 오래됐으니 같이 정리하자" | `.worktrees/`·`worktrees/` 아래만 정리한다. 나머지는 호스트의 것. |
| "제거 거부 — --force는 그냥 정리 마무리다" | 거부는 그 워크트리에만 있는 파일이 있다는 뜻이다. `--force`는 영구 삭제다. 보여주고 묻는다. |
| "베이스 브랜치는 뻔히 main이다" | 갈라진 지점을 확인하거나 묻는다. 잘못된 베이스에 머지하면 되돌리기 비싸다. |
| "푸시가 거부됐다 — force-push로 해결하자" | 거부된 푸시는 원격이 움직였다는 뜻이다. 조사한다. force-push는 상대방의 명시적 요청에만. |
