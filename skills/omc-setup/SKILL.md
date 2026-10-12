---
name: omc-setup
description: 이식된 OMC 스킬 모음 안내·관리 — 사용자가 "OMC 스킬 목록 보여줘", "OMC 스킬이 뭐가 있어", "OMC 스킬 추가해줘", "OMC 스킬 업데이트해줘"라고 요청하면 사용. 이식된 스킬 목록 안내와 새 스킬 추가 방법을 제공한다.
---

# OMC Setup (메타 스킬)

## Purpose

이 환경에 이식된 oh-my-claudecode(OMC) 스킬 모음을 안내·관리한다. 원본의 Claude Code 설치 마법사가 아니라, **이미 이식된 스킬들의 사용 안내와 확장(새 스킬 추가) 관리**가 목적이다.

## Workflow

### 1. 이식된 OMC 스킬 목록 안내

사용자가 "OMC 스킬 목록 보여줘"라고 요청하면 `~/workspace/skills/`에서 OMC에서 이식된 스킬을 확인하고 이름·설명을 표로 안내한다. 현재 이식 목록:

| 스킬 | 용도 |
|---|---|
| `skill` | 스킬 목록·추가·삭제·검색·수정 |
| `skillify` | 반복 워크플로 → 스킬 초안 추출 |
| `self-improve` | 자율 진화형 코드 개선 루프 |
| `omc-setup` | 이 스킬 (OMC 스킬 모음 안내·관리) |
| `omc-doctor` | 워크스페이스 환경 점검·자동 수정 |
| `cancel` | 진행 중 작업 취소·상태 정리 |
| `launch` | 미션 브리프 → 스펙 → 티켓 → 병렬 실행 → 검증 파이프라인 |

각 스킬의 상세 내용은 해당 스킬의 SKILL.md를 읽어 안내한다.

### 2. 새 OMC 스킬 추가

사용자가 "OMC 스킬 추가해줘 <이름>"이라고 요청하면:

1. 원본 경로 `/tmp/plugin_import/oh-my-claudecode/skills/<이름>/`에 해당 스킬이 있는지 확인한다.
2. 있으면 이식 규칙(아래 Operating Rules)에 따라 `~/workspace/skills/<이름>/`로 이식한다.
3. 없으면 `skill_creator` 스킬을 사용해 새로 작성하는 방향을 제안한다.
4. 복잡한 이식은 `skill` 스킬의 "스킬 추가해줘" 흐름이나 `skill_creator`에 위임한다.

### 3. OMC 스킬 업데이트·점검

- "OMC 스킬 업데이트해줘": 각 이식 스킬의 SKILL.md가 최신 이식 규칙(프론트매터 `name`/`description`, Purpose/Workflow/Output Contract/Operating Rules 구조)을 따르는지 점검하고 어긋난 부분을 수정한다.
- 환경 자체의 점검·수정은 `omc-doctor` 스킬에 위임한다 ("환경 점검해줘").

## Output Contract

- 목록 안내: 스킬 이름·한 줄 설명 표 + 각 스킬 호출 트리거 문구.
- 추가: 이식된 스킬의 경로(`~/workspace/skills/<이름>/SKILL.md`)와 적용된 이식 규칙 요약.
- 업데이트: 점검 결과와 수정 내역.

## Operating Rules

- 이 스킬은 Claude Code에 OMC를 설치하는 원본 `omc-setup`의 설치 마법사가 아니다. 이 환경에는 설치할 Claude Code 플러그인이 없으므로 설치 플로우는 제공하지 않는다.
- 비고: 원본의 `phases/` 설치 플로우 파일(01-install-claude-md.md, 02-configure.md, 03-integrations.md, 04-welcome.md)은 Claude Code 전용 설치 단계(CLAUDE.md 설치·HUD 설정·통합 연동)라 이 환경에 불필요하므로 복사하지 않았다.
- 원본의 슬래시 커맨드(`/omc-setup --local/--global/--force/--help`)는 채팅 요청("OMC 스킬 목록 보여줘" 등)으로 대체된다.
- 원본의 `scripts/setup-claude-md.sh`, `scripts/setup-progress.sh` 호출은 이 환경에 해당 스크립트가 없으므로 수행하지 않는다. 요구받으면 불가함을 명시한다.
- 새 스킬 추가 시 이식 규칙: 프론트매터 `name` 유지·`description`만 한국어 트리거 문구로 작성, 불필요 메타(level/aliases/argument-hint) 제거, Task tool → `subagent.spawn`, `~/.claude/` → `~/workspace/`, 외부 모델·hooks 불가 항목은 Operating Rules에 한계 명시.
