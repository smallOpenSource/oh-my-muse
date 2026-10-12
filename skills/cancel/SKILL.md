---
name: cancel
description: 진행 중 작업 취소·상태 정리 — 사용자가 "취소해줘", "지금 돌고 있는 거 멈춰줘", "cancel 해줘"라고 요청하면 사용. [--force] [--all] 플래그 지원. 현재 세션의 진행 중 작업을 안전하게 중단하고 상태를 정리한다.
---

# Cancel

## Purpose

현재 세션에서 진행 중인 작업(self-improve 루프, 백그라운드 프로세스 등)을 감지하고 안전하게 취소한다. 작업 중단의 표준 절차이며, `--force`는 중단의 긴급도만 바꾸고 범위·잠금·소유권 검사를 우회하지 않는다. `--all`만이 세션 간 정리를 승인한다.

## Workflow

### 취소 계약

플래그는 범위와 중단 방식을 독립적으로 제어한다:

| 호출 | 범위 | 중단 방식 |
|---|---|---|
| 플래그 없음 | 현재 세션만 | 정상 취소 (graceful 대기 포함) |
| `--force` | 현재 세션만 | 강제 취소: 정상 대기를 건너뛰되 보호된 상태 도구와 잠금/소유권은 준수 |
| `--all` | 알려진 모든 세션 (명시적 세션 id별) | 각 세션마다 안전한 정상 취소 후 전역 정리 |
| `--force --all` | 알려진 모든 세션 | 각 세션 강제 취소 후 승인된 전역 정리 |

현재 세션 식별자가 없거나 모호하면 fail-closed: 상태를 집계하거나 발견된 세션을 임의로 선택하거나 범위 없는 정리를 하지 않는다. `--all`은 세션을 열거할 수 있지만 각 id는 독립적으로 읽고·취소하고·정리한다.

### 1. 인자 파싱

`--force`, `--all`만 인식한다. 알 수 없는 인자는 무시한다(아무 것도 하지 않음).

### 2. 활성 작업 감지

이 환경의 취소 대상:

1. **self-improve 루프**: `<self-improve-root>/state/agent-settings.json`의 `status`가 `running`인지 확인. 해당하면 중단 대상.
2. **백그라운드 프로세스**: `process.list`로 현재 세션이 시작한 실행 중 프로세스를 확인.
3. **cron/hooks 작업**: `cron.*`/`hooks.*` 네임스페이스로 관리되는 예약 작업 — 이 스킬은 목록만 확인하고 실제 비활성화는 부모 에이전트에 보고한다(스킬 권한 밖의 영속 상태 변경이므로).

의존 순서: self-improve → 백그라운드 프로세스 → cron/hooks(보고만).

### 3. 각 세션 취소

**self-improve 중단**:

1. `state/agent-settings.json`을 읽는다.
2. `status`를 `"user_stopped"`로 기록하고, `iteration_state.json`에 `status: "interrupted"`, `current_step`을 기록한다.
3. 현재 라운드의 worktree를 정리한다 (`git worktree remove --force`, `git worktree prune`). 고아 worktree는 self-improve 스킬의 Step 0 로직을 따른다.
4. `iteration_state`와 `best_score` 등 재개용 아티팩트는 보존한다. 재개는 self-improve 스킬의 재개 절차를 따른다.
5. 로그: `"Self-improve stopped by user at iteration {N}, step {current_step}"`.

**백그라운드 프로세스 중단**:

1. 정상 경로: `process.poll`로 상태를 확인하고 완료를 기다린다(최대 수 초).
2. `--force` 또는 응답 없으면 `process.kill`로 종료한다.
3. 종료 후 `process.clear`로 세션을 정리한다.

**cron/hooks**: 비활성화하지 않고 목록과 작업 id를 보고서에 포함해 부모 에이전트에 전달한다.

### 4. 승인된 전역 정리 (`--all` 전용)

모든 세션의 개별 취소가 성공한 뒤에만 수행한다. 하나라도 실패·미해결이면 부분 완료로 보고하고 이 단계를 생략한다.

- self-improve의 고아 worktree 정리(모든 토픽 루트 대상).
- 빈 상태 디렉터리 정리.
- self-improve·백그라운드 프로세스의 영속 아티팩트(반복 이력, best_score, 완료 보고서)는 삭제하지 않는다.

### 취소 보고서

```
취소 범위: 현재 세션 / 전체
감지된 작업: [...]
성공: [...]
실패: [...] (사유 포함)
보존된 상태: [...] (재개용)
후속 조치 필요: [...] (예: cron 비활성화는 부모 에이전트에 요청)
```

활성 작업이 없으면 "진행 중인 작업을 찾지 못했습니다."라고 보고한다. 현재 세션 명령에서 이 결과를 조용히 확대 해석하지 않는다.

## Output Contract

- 범위·감지된 작업·성공/실패·보존된 상태·후속 조치를 보고서 형식으로 출력한다.
- 타임아웃·식별자 누락·잠금 충돌·상태 손상을 성공으로 보고하지 않는다.
- 실패한 작업은 상태를 유지하고 사유를 보고한 뒤 같은 범위에서 재시도한다.

## Operating Rules

- 원본의 OMC 모드(autopilot, ralph, ultragoal, swarm, ultrapilot, pipeline, team, plan consensus)와 `.omc/state` 기반 MCP 상태 도구(`state_clear` 등)는 이 환경에 없으므로 취소 대상에서 제외한다. 요구받으면 "이 환경에서는 해당 없음"으로 명시한다.
- 원본의 tmux 기반 워커 정리는 `process.kill`로 대체한다. tmux 세션을 직접 종료하는 원본 로직은 이 환경에 tmux 오케스트레이션이 없으므로 수행하지 않는다.
- `--force`는 대기 생략일 뿐, 상태 파일 무결성 검사나 확인 절차를 우회하지 않는다.
- cron/hooks의 비활성화·삭제는 이 스킬이 직접 수행하지 않고 부모 에이전트에 보고한다 (영속 스케줄 변경은 사용자 승인 필요).
- 긴급 폴백(원본의 bash 직접 파일 삭제 스크립트)은 현재 세션이 명확히 식별된 self-improve 상태 파일에만 사용하고, autopilot/team 같은 타 모드나 `--force`/`--all`에는 사용하지 않는다.
