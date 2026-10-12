---
name: omc-doctor
description: 워크스페이스 환경 진단·수정 — 사용자가 "환경 점검해줘", "doctor 실행해줘", "스킬 환경에 문제 있어"라고 요청하면 사용. ~/workspace/skills 정합성, git·python3·node 등 필수 도구를 점검하고 사용자 확인 후 자동 수정한다.
---

# Doctor

## Purpose

이 워크스페이스(특히 `~/workspace/skills`)의 설치·설정 문제를 진단하고, 사용자 확인 후 자동으로 수정한다.

## Workflow

### Step 1 — 스킬 디렉터리 점검

```bash
ls -la ~/workspace/skills/ 2>/dev/null || echo "SKILLS DIR MISSING"
```

- 디렉터리 없으면 CRITICAL — 스킬 저장소 자체가 없음.

### Step 2 — SKILL.md 정합성 점검

각 `~/workspace/skills/*/SKILL.md`에 대해:

```bash
for f in ~/workspace/skills/*/SKILL.md; do
  echo "== $f"
  head -5 "$f" | grep -q "^name:" && echo "  name: OK" || echo "  name: MISSING (CRITICAL)"
  head -8 "$f" | grep -q "^description:" && echo "  description: OK" || echo "  description: MISSING (WARN)"
done
```

- `name` 누락: CRITICAL — 스킬로 인식되지 않음.
- `description` 누락: WARN — 트리거 매칭이 안 됨.
- 프론트매터에 `level`/`aliases` 등 이 환경에서 쓰지 않는 메타가 있으면 WARN — 정리 권장.

### Step 3 — 필수 도구 점검

```bash
for t in git python3 node; do command -v $t >/dev/null && echo "$t: $($t --version 2>&1 | head -1)" || echo "$t: MISSING"; done
```

- `git` 없음: WARN — self-improve의 worktree/브랜치 전략이 동작하지 않음.
- `python3` 없음: WARN — self-improve의 `plot_progress.py`가 동작하지 않음.
- `node` 없음: WARN — `resolve-paths.mjs`가 동작하지 않음.

### Step 4 — self-improve 상태 정합성 점검

`~/workspace/self-improve/topics/`가 존재하면 각 토픽 루트에 대해:

- `config/settings.json`, `config/goal.md`, `state/agent-settings.json` 존재 여부.
- `agent-settings.json`의 `status`가 `running`인데 실제 루프가 돌고 있지 않으면 WARN — 크래시 잔여 상태(재개 또는 정리 필요).
- 고아 worktree 확인: 대상 레포에서 `git worktree list`에 `worktrees/round_*` 잔재가 있으면 WARN.

### Step 5 — 보고서 출력

```
## Doctor Report

### Summary
[HEALTHY / ISSUES FOUND]

### Checks
| Check | Status | Details |
|-------|--------|---------|
| Skills 디렉터리 | OK/CRITICAL | ... |
| SKILL.md 정합성 | OK/WARN/CRITICAL | ... |
| 필수 도구 (git/python3/node) | OK/WARN | ... |
| self-improve 상태 | OK/WARN | ... |

### Issues Found
1. [문제 설명]

### Recommended Fixes
[문제별 수정 방안]
```

### Step 6 — 자동 수정 (사용자 확인 후)

"이 문제들을 자동으로 수정할까요?"라고 묻고, 확인받으면 적용한다.

- **SKILL.md 프론트매터 누락**: `name`(디렉터리명), `description`(빈 값 또는 파일 첫 제목에서 도출)을 보완. 기존 본문은 건드리지 않는다.
- **불필요 메타 정리**: `level`, `aliases`, `argument-hint` 등 이 환경 미사용 키 제거(값은 유지 목적이므로 삭제 전 사용자에게 알린다).
- **self-improve 크래시 잔여 상태**: `agent-settings.json`의 `status`를 `idle`로 되돌리거나(사용자 선택) 고아 worktree를 `git worktree remove --force`로 정리.
- **수정 후 보고**: "수정 완료. 변경 사항: ..."

## Output Contract

- 점검 후 위 보고서 형식으로 출력한다. 상태를 OK/WARN/CRITICAL로 구분한다.
- 수정은 반드시 사전 확인 후에만 수행하고, 수행 내역을 보고한다.
- 문제를 성공으로 포장하지 않는다. 미해결 항목은 남았다고 명시한다.

## Operating Rules

- Claude Code 전용 점검 항목(원본 Step 1 플러그인 버전, Step 2~3 레거시 hooks, Step 4 CLAUDE.md OMC 마커, Step 6 플러그인 캐시, Step 7 curl 설치 잔재)은 이 환경에 해당 개념이 없으므로 점검하지 않는다. 요구받으면 "이 환경에서는 해당 없음"으로 명시한다.
- 파괴적 수정(파일 삭제, 상태 초기화)은 확인 없이 실행하지 않는다. 파일 삭제 시 `trash` 도구 사용을 우선한다.
- `npm view` 같은 네트워크 조회는 필요시에만 수행하고, 실패하면 "(조회 불가)"로 표기한다.
- self-improve 상태 파일을 고칠 때는 JSON 구조를 보존하고, 백업(`agent-settings.json.bak`)을 먼저 만든다.
