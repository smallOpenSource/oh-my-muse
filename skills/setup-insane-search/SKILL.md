---
name: setup-insane-search
description: "차단·봇방어 사이트 우회 검색·페치 플러그인 insane-search 설치(Claude Code=gptaku_plugins, Codex=gptaku-codex). 사용자가 'insane-search 설치해줘', 'setup-insane-search'라고 요청하거나 차단 사이트(WAF·봇방어) 검색·페치가 필요해지면 사용."
---

# setup-insane-search: insane-search 플러그인 설치

## Purpose

차단 사이트 우회(WAF·봇방어; X·Reddit·YouTube·GitHub 등) 검색·페치를 제공하는 `insane-search` 플러그인을 설치한다. 현재 도구(Claude Code / Codex)를 감지해 알맞은 경로로 진행하고, 이미 설치돼 있으면 skip(멱등). 답변은 한글.

## Workflow

### Claude Code 경로

세션 안(슬래시 커맨드):

```
/plugin marketplace add https://github.com/fivetaku/gptaku_plugins.git
/plugin install insane-search@gptaku-plugins
/reload-plugins
```

CLI(비대화형):

```bash
claude plugin marketplace add https://github.com/fivetaku/gptaku_plugins.git
claude plugin install insane-search@gptaku-plugins
# 반영엔 /reload-plugins 또는 재시작 필요
```

### Codex CLI 경로

Codex는 마켓플레이스명(`gptaku-codex`)과 플러그인명(`insane-research-codex`)이 Claude와 다르다.

```bash
codex plugin marketplace list            # gptaku-codex 가 이미 있으면 다음 add 는 skip
codex plugin marketplace add https://github.com/fivetaku/insane-search.git
codex plugin add insane-research-codex@gptaku-codex
codex plugin list                        # STATUS=installed 확인
```

- `gptaku-codex` 마켓플레이스가 `marketplace list`에 없을 때만 add 한다.
- add 후 등록된 마켓플레이스명을 `marketplace list`로 확인한다. 이름이 `gptaku-codex`가 아니면 `codex plugin add insane-research-codex@<실제이름>`으로 맞춘다.

## Output Contract

검증·보고: Claude는 `claude plugin list`에 `insane-search` 표시(반영엔 `/reload-plugins`·재시작). Codex는 `codex plugin list`에서 `insane-research-codex`가 `STATUS=installed`. 이미 설치면 skip. 실패는 정직 보고(가짜 성공 금지).

## Operating Rules

- **도구별 이름이 다르다**: Claude=`insane-search@gptaku-plugins`, Codex=`insane-research-codex@gptaku-codex`.
- 설치는 `<plugin>@<marketplace>` 형식. 마켓플레이스명은 add 후 `marketplace list`로 확인.
- 깃·네트워크 접근 필요(사설망이면 프록시 확인).
- **이 환경 참고:** 이 VM에는 `codex` CLI가 있고 `claude` CLI는 없다. Codex 경로는 이 VM에서 그대로 동작하고, Claude Code 경로는 `claude` CLI가 있는 머신에서 실행하는 참고용이다. 이 스킬이 설치하는 것은 claude/codex CLI용 플러그인이며, 이 Muse 에이전트 자체의 검색 능력과는 별개다.
