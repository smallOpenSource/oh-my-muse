---
name: hud
description: "HUD(상태 표시줄) 표시 옵션 설정 — 레이아웃, 프리셋(minimal/focused/full), 표시 요소. 사용자가 'hud 해줘', 'hud setup 해줘', 'hud minimal 해줘', 'hud focused 해줘', 'hud full 해줘', 'hud status 해줘'라고 요청하면 사용."
---

# hud: HUD 표시 설정

## Purpose

- OMC HUD(Heads-Up Display)의 표시 옵션을 설정한다 — 레이아웃·프리셋·표시 요소.
- 인자 없이 호출하면 현재 HUD 상태를 보여주고, 필요 시 설정을 안내한다.

## Workflow

### 트리거

| 요청 | 동작 |
|---|---|
| `hud` | 현재 HUD 상태 표시 (미설정이면 설정 안내) |
| `hud setup` | HUD 설치/수리 안내 |
| `hud minimal` | 최소 표시 프리셋으로 전환 |
| `hud focused` | 기본 프리셋으로 전환 (focused) |
| `hud full` | 전체 표시 프리셋으로 전환 |
| `hud status` | 상세 HUD 상태 표시 |

### 프리셋

- **minimal**: `[OMC] ralph | todos:2/5` — 최소 요소만.
- **focused** (기본): `[OMC] branch:main | ralph:3/10 | US-002 | skill:planner | ctx:67% | agents:2 | bg:3/5 | todos:2/5`.
- **full**: 전부 + 멀티라인 에이전트 상세 (`├─`, `└─` 트리).

### 표시 요소

`repo`(저장소명) · `branch` · `ralph:진행/최대` · `autopilot` · `US-번호`(PRD 스토리) · `skill`(마지막 활성 스킬) · `activeSkills` · `ctx`(컨텍스트 사용률, 70% 경고·80% 압축 제안·85% 위험) · `agents` · `bg`(백그라운드 슬롯) · `todos` · `thinking` · `effort`(dim low / cyan medium / yellow high / magenta xhigh / bold magenta max) · `permissionStatus` · `apiKeySource` · `profile` · `promptTime` · `sessionHealth` · `omcLabel` · `updateNotification`.

### 에이전트 표시 형식 (`agentsFormat`)

- `count`: `agents:2` — 개수만.
- `codes`: `agents:Oes` — 타입 코드 + 모델 티어 대소문자.
- `codes-duration`: `agents:O(2m)es` — 코드 + 실행 시간.
- `detailed`: `agents:[architect(2m),explore,exec]` — 상세 목록.
- `descriptions`: `O:analyzing code | e:searching` — 코드 + 작업 내용.
- `tasks`: `[analyzing code, searching...]` — 작업 내용만.
- `multiline`: 실행 중 에이전트를 별도 라인에 풀 상세 표시 (`├─` `└─` 트리, 에이전트 코드, 실행 시간, 작업 내용 최대 45자).

### 수동 설정

설정 파일에 아래 키로 저장한다:

```json
{
  "preset": "focused",
  "elements": { "ralph": true, "autopilot": true, "prdStory": true, "contextBar": true, "agents": true, "agentsFormat": "multiline", "backgroundTasks": true, "todos": true, "lastSkill": true, "activeSkills": true, "thinking": true, "effort": true, "useBars": true, "showCallCounts": true, "safeMode": true, "maxOutputLines": 4 },
  "thresholds": { "contextWarning": 70, "contextCompactSuggestion": 80, "contextCritical": 85, "ralphWarning": 7 },
  "staleTaskThresholdMinutes": 30,
  "contextLimitWarning": { "threshold": 80, "autoCompact": false }
}

- `safeMode: true`(기본) — ANSI 제거 + ASCII 출력으로 터미널 깨짐 방지.
- 색상: 녹색 정상 / 노랑 경고(ctx >70%, ralph >7) / 빨강 위험(ctx >85%, ralph 최대).
```

## Output Contract

- 적용된 프리셋 + 변경된 요소 + "재시작 후 적용" 안내 (해당되는 경우).

## Operating Rules

- 한계: 원본의 자동 설치(`omc-hud.mjs` 복사, `settings.json`의 `statusLine` 설정)는 **Claude Code 전용**이므로 이 환경에서 동작 불가. `~/.claude/` 경로는 `~/workspace/`로 치환한다.
- 대안: 이 환경에서는 프리셋·표시 요소 선택을 `~/workspace/hud-config.json`에 기록하고, 실제 상태줄 연동은 Claude Code를 쓰는 환경에서 수동으로 적용한다.
- 레거시: 상태줄이 문자열 형식이던 구버전 설정은 객체 형식(`{"type": "command", "command": "..."}`)으로 마이그레이션 — 원본 규칙 유지, 적용은 수동.
- 생략 항목: 설치 스크립트 7단계(node 명령)·플러그인 버전 검사·Windows 경로 규칙·트러블슈팅 진단 절차(Claude Code 전용).
- commands/hud.md 흡수: 해당 파일은 스킬 읽기로의 단순 디스패처라 본문 내용 없음. 트리거 매핑(`hud setup|minimal|focused|full|status` → 채팅)만 이 description/Workflow에 반영.
