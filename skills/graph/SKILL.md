---
name: graph
description: "선언적 JSON 디스크립터로 반복 가능한 다단계 파이프라인(DAG)을 기술·실행하는 오케스트레이션 스킬. 사용자가 '파이프라인 돌려줘', '단계별로 실행해줘', '중단해도 재개되게 해줘'라고 요청하고 작업이 반복 가능하며 의존성이 명확할 때 사용. 탐험적 일회성 작업이나 중간 재설계가 필요한 작업에는 부적합."
---

# Graph

## Purpose

선언적 JSON 디스크립터로 기술된 결정적 오케스트레이션 그래프(DAG 파이프라인)를 실행한다. 사용 시점: 의존성이 명시된 반복 가능한 다단계 파이프라인, 중단 후 재개가 필요한 작업, 감사 가능한 실행 기록이 필요한 경우.

## Workflow

1. **디스크립터가 주어지면** → 3으로.
2. **파이프라인 설명이 주어지면** → 디스크립터 JSON(아래 스키마 최소형)을 작성해 프로젝트 옆(권장 `.omc/graphs/<name>.json`)에 쓰고, 실행 전 사용자에게 보여준다. `run_id`는 논리적 파이프라인당 유일해야 하며, 같은 `run_id`로 재실행하면 **재개(resume)** 되지 처음부터가 아니다.
3. **승인 노드**: 디스크립터에 `"kind": "human-approval"` 노드가 있으면 백그라운드·비대화형 실행을 하지 않는다(표준 입력이 대화형이 아니면 EOF가 denied로 fail-closed). 사용자에게 대화형 실행을 요청한다.
4. 실행하고 진행 상황을 중계한다. 종료 코드(규범): 0 성공 | 1 최종 실패 | 19 다른 작성자가 실행 중(busy) | 20 손상/변조된 저널(fail-closed) | 21 재개 시 디스크립터 변경 | 70 런타임 크래시.
5. **재개**: 크래시 후 같은 명령을 재실행하면 커밋된 전이를 리플레이하고 계속한다. 완료된 노드는 재실행되지 않는다.

## Output Contract (디스크립터 스키마 최소형)

```json
{
  "descriptor_version": 1,
  "run_id": "unique-pipeline-id",
  "revision_id": "rev-1",
  "goal": "one line",
  "nodes": [
    { "id": "n1", "kind": "command", "title": "...", "timeout_ms": 60000,
      "max_attempts": 2, "effect_policy": { "policy": "side_effect_free" },
      "command": "npm test" },
    { "id": "a1", "kind": "agent", "title": "...", "timeout_ms": 300000,
      "max_attempts": 1, "effect_policy": { "policy": "side_effect_free" },
      "instructions": "..." },
    { "id": "gate", "kind": "human-approval", "title": "...",
      "prompt": "Proceed?" }
  ],
  "edges": [ { "id": "e1", "kind": "fixed", "from": "n1", "to": "a1" } ],
  "entry_node_ids": ["n1"],
  "concurrency_limit": 2,
  "terminal_verification_node_id": "a1"
}
```

엣지 종류: `fixed` | `conditional` | `fan_out`/`join` 쌍 | `back_edge`(max_traversals로 제한된 재시도).

## Operating Rules

- **한계와 대안**: 원본의 `omc graph run` CLI와 저널 기반 크래시 복구 런타임은 이 Muse 환경에 설치되어 있지 않다. 가장 가까운 대안은 위 디스크립터 형식을 **실행 계획 스펙**으로 유지하고, 노드를 순서대로 직접 실행하는 것이다: `command` 노드는 `muse.exec`로(단, 신뢰할 수 있는 디스크립터만), `agent` 노드는 심층 세션에서 `subagent.spawn` 병렬 실행으로, `human-approval` 노드는 사용자에게 확인을 받는다. 진행 상황은 `~/workspace/` 상태 파일에 기록해 재개를 흉내낸다.
- `conditional`/`back_edge` 라우팅은 원본 런타임 계약상 커스텀 실행자가 `route`를 방출해야 하며, 기본 실행자는 라우트를 만들지 않으므로 해당 그래프는 fail-fast(`route_required`)로 중단한다. `reconcile` 실행자는 기본 지원에서 거부한다 — 실제 외부 조정 권한을 가진 커스텀 실행자가 필요하다. 원본 동작 그대로 유지.
- 크래시 복구 보장은 **at-least-once**(command 노드): 외부 부작용과 저널 기록 사이에 크래시가 나면 재개 시 해당 노드가 재실행된다. `idempotent` 명령에는 시작 전 `GRAPH_IDEMPOTENCY_KEY` 환경 변수가 주어지며 다운스트림 중복 제거에 기록한다. 외부 부작용의 exactly-once는 범위 밖이다.
- command 노드는 현재 작업 디렉터리에서 실행되는 임의 셸 라인이다. 직접 작성했거나 신뢰하는 디스크립터만 실행한다. 실행 자식은 호스트 비밀 전체가 아닌 허용 환경만 상속받으며, 파일시스템/프로세스 샌드박스는 없다.
- agent 노드는 원본에서 명시적으로 읽기 전용이다(쓰기·외부 효과 필요 시 별도 실행 경로를 설계한다). `.omc/graph-runs/<run_id>/descriptor.json` 상당 파일은 실행 가능 콘텐츠로 취급한다.
- 진행 라인은 `[run]`, `[node]`, `[ok]`, `[fail]`, `[join]`, `[done]` 형식으로 스트리밍한다(계획 실행 시 그대로 중계).
