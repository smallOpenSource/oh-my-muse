---
name: autoresearch
description: 사용자가 "autoresearch 해줘", "미션 반복 개선 루프 돌려줘"라고 요청하면 발동. 단일 미션을 평가자(JSON pass/score) 주도로 반복 개선하며, 이터레이션별 평가 JSON과 마크다운 결정 로그를 남기고 max-runtime에 정지하는 상태 유지 루프 스킬.
---

# Autoresearch

## Purpose

- 경계가 있는(bounded), 평가자 주도 반복 개선을 위한 상태 유지(stateful) 스킬이다.
- 한 번에 **하나의 미션만** 소유한다. 통과하지 못한 결과에도 계속 반복하고, 각 평가와 결정을 내구성 있는 아티팩트로 기록한다. 명시적 max-runtime 상한(또는 다른 명시적 종료 조건)에 도달해야만 멈춘다.

## Workflow

1. **단일 미션이 존재하고 평가자 설정이 이미 준비됐는지 확인**한다. (미션·평가자 생성은 이 스킬의 범위가 아니다.)
2. 모드/상태를 `autoresearch` 활성으로 기록한다:
   - mission slug/dir, evaluator 참조, iteration count, started/updated 타임스탬프, 명시적 max-runtime 또는 deadline.
3. **매 이터레이션마다**:
   - 정확히 하나의 실험/변경 사이클 실행
   - 평가자(evaluator) 실행
   - 기계 가독 평가 JSON 저장
   - 사람이 읽는 마크다운 결정 로그에 항목 추가
   - 평가가 통과하지 않아도 **계속한다**
4. **다음 중 하나가 되면 정지**:
   - max-runtime 상한 도달
   - 사용자 명시 취소
   - 런타임이 기록한 다른 명시적 종료 조건

## Output Contract

- 영속 저장소: `~/workspace/autoresearch/<mission-slug>/` (원본 `.omc/autoresearch/` → 이 환경의 workspace 경로로 치환)
  ```text
  ~/workspace/autoresearch/<mission-slug>/
    mission.md
    evaluator.json
    runs/<run-id>/
      evaluations/
        iteration-0001.json
        iteration-0002.json
      decision-log.md
  ```
- 최소 아티팩트: mission spec, evaluator 스크립트 또는 명령 참조, 이터레이션별 평가 JSON, 마크다운 결정 로그.
- 평가자 출력은 구조화 JSON이어야 하며, 필수 boolean `pass`와 선택 numeric `score`를 포함한다.
- 주기적 재실행이 필요하면 Muse의 `cron`으로 예약한다 (잡당 하나의 미션, 같은 미션/평가자 계약 유지, 기존 실험을 덮어쓰지 않고 새 run 아티팩트 추가).

## Operating Rules

1. **단일 미션만 (v1)** — 다중 미션 오케스트레이션을 만들지 않는다.
2. **미션 설정·평가자 생성은 범위 밖** — 원본의 `/deep-interview --autoresearch` 흐름에 해당. 이 환경에는 deep-interview 스킬이 없으므로, 미션과 평가자는 사용자가 직접 제공하거나 사전 인터뷰로 확보해야 한다. 런타임에 평가자를 새로 만드는 용도로 쓰지 않는다.
3. **`omc autoresearch` CLI 흐름 사용 금지** — 구식(deprecated)이며 권위 있는 경로가 아니다.
4. **주기(cron) 연동 시** — 잡당 하나의 미션, 계약 유지, run 아티팩트는 추가(append)만.
5. **로그는 사람이 읽을 수 있게** — 기계만을 위한 로그가 아니라 사람이 이해할 수 있는 결정 로그를 남긴다.
6. **명령어 흡수**: 원본 `/oh-my-claudecode:autoresearch` 슬래시 커맨드는 단순 디스패치 래퍼였으므로, 이 스킬의 채팅 트리거("autoresearch 해줘" 등)로 대체된다.
