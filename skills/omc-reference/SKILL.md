---
name: omc-reference
description: "OMC(oh-my-claudecode) 에이전트·툴·팀·커밋·스킬 레지스트리 레퍼런스. 에이전트 위임·팀 오케스트레이션·커밋 규칙을 쓸 때 자동 참조한다."
user-invocable: false
---

# OMC Reference

에이전트/툴/스킬 카탈로그 상세가 필요할 때 참조하는 내장 레퍼런스. 세션 상시 지침에는 두지 않고
필요할 때 이 스킬을 읽는다.

**런타임**: 이 문서는 OMC(oh-my-claudecode, Claude Code용) **5.6.1** 기준이다. **OMC 5.0.0은 워크플로 17개를 별칭 없이 삭제했다**(아래 §Retired in OMC 5). 삭제된 이름을 부르면 실패한다. 원본 banker 스킬은
Codex CLI용 대응 프레임워크 OMX(oh-my-codex) 카탈로그도 병기했으나, 이식본에서는 참고 수준으로
축소한다(말미 §OMX note). 설치 환경 기준으로 확인하라 — 이 Muse 환경에서는 `~/workspace/skills/`.

## Agent Catalog

OMC 에이전트 프롬프트 카탈로그. `subagent.spawn` 위임 시 렌즈 선택의 어휘로 쓴다.

- `explore` (haiku) — fast codebase search and mapping
- `analyst` (opus) — requirements clarity and hidden constraints
- `planner` (opus) — sequencing and execution plans
- `architect` (opus) — system design, boundaries, and long-horizon tradeoffs
- `debugger` (sonnet) — root-cause analysis and failure diagnosis
- `executor` (sonnet) — implementation and refactoring
- `verifier` (sonnet) — completion evidence and validation
- `tracer` (sonnet) — trace gathering and evidence capture
- `security-reviewer` (opus) — trust boundaries and vulnerabilities
- `code-reviewer` (opus) — comprehensive code review
- `test-engineer` (sonnet) — testing strategy and regression coverage
- `designer` (sonnet) — UX and interaction design
- `writer` (haiku) — documentation and concise content work
- `qa-tester` (sonnet) — runtime/manual validation
- `scientist` (sonnet) — data analysis and statistical reasoning
- `document-specialist` (sonnet) — SDK/API/framework documentation lookup
- `git-master` (sonnet) — commit strategy and history hygiene
- `code-simplifier` (opus) — behavior-preserving simplification
- `critic` (opus) — plan/design challenge and review

## Model Routing

- `haiku` — quick lookups, lightweight inspection, narrow docs work
- `sonnet` — standard implementation, debugging, and review
- `opus` — architecture, deep analysis, consensus planning, and high-risk review
- `fable` — Claude Fable 5, above Opus, when passed explicitly

## Tools Reference

### OMC 상태·팀·메모 (OMC 런타임 전용 MCP/슬래시)

- **외부 AI/오케스트레이션**: `/team N:executor "task"`(worker type: executor, debugger, designer, codex, gemini, antigravity), `omc team N:codex|gemini "..."`, `omc ask <claude|codex|gemini|antigravity|grok|cursor>`. 멀티모델 합성(구 `/ccg`, 5.0.0에서 삭제): `/oh-my-claudecode:ask codex` + `/oh-my-claudecode:ask antigravity` 후 합성, 또는 `/team`.
- **OMC CLI (OMC 5)**: `omc ralph verify [--write-baseline] [--session <id>]` — ralph가 자체 실행하는 피드백 베이스라인·게이트. 전역 CLI가 플러그인과 맞아야 한다(4.x CLI엔 없어 ralph가 멈춘다). `omc ultragoal create-goals|complete-goals|checkpoint|record-review-blockers|status` — `.omc/ultragoal/` 아래 내구 목표 원장.
- **OMC state**: `state_read`, `state_write`, `state_clear`, `state_list_active`, `state_get_status`, `state_migrate_non_git`
- **Wiki·공유 메모리·트레이스**: `wiki_ingest`, `wiki_query`, `wiki_list`, `wiki_read`, `wiki_lint`, `wiki_add`, `wiki_delete` · `shared_memory_read`, `shared_memory_write`, `shared_memory_list`, `shared_memory_delete`, `shared_memory_cleanup` · `trace_timeline`, `trace_summary`, `session_search`
- **팀 런타임**: Claude Code 2.1.178+부터 네이티브 `TeamCreate`/`TeamDelete` 제거. `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`이면 세션당 암시적 팀 1개: `SendMessage`와 공유 태스크 리스트(`TaskCreate`, `TaskList`, `TaskGet`, `TaskUpdate`)로 조정.
- **Notepad**: `notepad_read`, `notepad_write_priority`, `notepad_write_working`, `notepad_write_manual`
- **Project memory**: `project_memory_read`, `project_memory_write`, `project_memory_add_note`, `project_memory_add_directive`

### 코드 인텔리전스

- LSP: `lsp_hover`, `lsp_goto_definition`, `lsp_find_references`, `lsp_diagnostics` 및 관련 헬퍼
- AST: `ast_grep_search`, `ast_grep_replace`
- 유틸: `python_repl`

## Skills Registry

내장 워크플로는 `/oh-my-claudecode:<name>`으로 호출 (OMC 5.6.1).

### Canonical workflows (Tier-0)
- `plan` → `execute` → `review` → `verify` — plan, build, review, verify. 플러그인 스킬로는 `/oh-my-claudecode:plan`·`/oh-my-claudecode:review`; 단독 설치(`omc setup`이 `~/.claude/skills/`에 복사)는 `omc-plan`·`omc-review`라 이름이 다르다(Claude Code 자체 `/plan`·`/review`와 충돌하므로)
- `ralplan` — consensus planning (Planner → Architect → Critic); `pending approval` 계획에서 멈춤
- `deep-interview` — Socratic ambiguity-gated requirements workflow

### Directly invocable workflows
- `autopilot` — full autonomous execution from idea to working code
- `ralph` — PRD-driven persistence loop with a configurable reviewer; `omc` CLI 필요(`omc ralph verify`)
- `ultragoal` — durable multi-goal plan and ledger with Claude Code `/goal` handoff
- `autoresearch` — stateful single-mission improvement loop

### Lanes and quality
- `team` — N coordinated agents on a shared task list (`team-plan` → `team-prd` → `team-exec` → `team-verify` → `team-fix`)
- `research` — grounded, sourced investigation; `external-context` — parallel external doc lookup
- `trace` — competing-hypothesis tracing; `debug` — diagnose OMC session or repo state
- `verify` — evidence before a completion claim (gathers evidence, does not fix)
- `visual-verdict` — screenshot-to-reference QA verdict
- `tdd` — test-first at agreed seams
- `ai-slop-cleaner` — regression-safe cleanup, an opt-in lane of `review`
- `minimal-code-discipline`, `minimal-prose-discipline`, `agent-doc-discipline` — writing-time disciplines for code, replies, and agent-facing docs

### Shipyard and repo workflows
- `drydock` (harness seed), `launch` (governed delivery pipeline), `harbor` (intake of issues and PRs), `intent` (requirements intake), `ask-navigator` (decision map), `map` (which skill owns which job), `loft` (throwaway design artifact), `refit` (environment retrospective), `architecture-survey`
- `graph` (declarative DAG runtime), `diagram`, `pr` (PR body from OMC's paper trail), `release`, `deepinit`, `self-improve`

### Utility skills
- `ask`, `cancel`, `remember`, `skillify`, `skill`, `wiki`, `omc-setup`, `omc-doctor`, `hud`, `project-session-manager` (alias `psm`), `configure-notifications`

### Retired in OMC 5 (removed, no alias)

| Removed | Use instead |
|---|---|
| `ultrawork`, `pipeline` | `execute` (or `team` for coordinated parallel workers) |
| `ultraqa` | `verify` |
| `ultrapilot`, `swarm`, `omc-teams` | `team` (or `omc team`) |
| `merge-readiness`, `understanding-gate` | `review` |
| `deep-dive`, `sciomc` | `research` |
| `ccg` | `ask` + `team` |
| `setup` | `omc-setup` |
| `mcp-setup` | `claude mcp add <name> ...` |
| `omc-reference` | `wiki` |
| `learner`, `writer-memory` | `remember` |
| `local-build-reminder` | none |

### Keyword triggers
- `"autopilot"`→autopilot · `"ralplan"`→ralplan · `"deep interview"`→deep-interview
- `"deslop"`/`"anti-slop"`→ai-slop-cleaner (opt-in lane of review)
- `"deep-analyze"`→analysis mode · `"tdd"`→TDD mode · `"deepsearch"`→codebase search
- `"ultrathink"`→deep reasoning · `"cancelomc"`→cancel
- 팀 오케스트레이션은 `/team`으로 명시적 호출.

## Team Pipeline

Stages: `team-plan` → `team-prd` → `team-exec` → `team-verify` → `team-fix` (loop).

- `team-fix`는 bounded remediation loop에 사용.
- `team ralph`는 팀 파이프라인과 Ralph식 순차 검증을 연결한다.
- 독립 병렬 레인이 조정 오버헤드를 정당화할 때 team mode를 선호한다.

## Commit Protocol

모든 커밋 메시지에 git trailer로 결정 맥락을 보존한다.

### Format

- Intent line first: 왜 바꿨는지
- Optional body: 맥락과 근거
- 해당 시 structured trailer

### Common trailers

- `Constraint:` — 결정을 빚은 활성 제약
- `Rejected:` — 고려한 대안 | 기각 이유
- `Directive:` — 전향적 경고·지시
- `Confidence:` — `high` | `medium` | `low`
- `Scope-risk:` — `narrow` | `moderate` | `broad`
- `Not-tested:` — 알려진 검증 공백

### Example

```text
feat(docs): reduce always-loaded OMC instruction footprint

Move reference-only orchestration content into a native skill so
session-start guidance stays small while detailed OMC reference remains available.

Constraint: Preserve CLAUDE.md marker-based installation flow
Rejected: Sync all built-in skills in legacy install | broader behavior change than issue requires
Confidence: high
Scope-risk: narrow
Not-tested: End-to-end plugin marketplace install in a fresh profile
```

## OMX note (참고 수준 — Codex CLI 전용)

원본은 OMX(oh-my-codex) 카탈로그를 실측 병기했다: 에이전트 프롬프트(`~/.codex/prompts/*.md`,
`analyst`·`architect`·`critic`·`debugger`·`executor`·`verifier` 외 Codex 확장 다수),
스킬 레지스트리(`$<name>` 호출 — `ralph`·`ralplan`·`ultraqa`·`ultrawork`·`autopilot`·`team`·`swarm` 등),
인터페이스(`~/.codex/skills/<name>/`, `codex mcp add`, `/copy` 등 TUI 내장 슬래시).
OMC↔OMX는 대체로 대칭이나 1:1은 아니다. 이 Muse 환경에서 Codex CLI를 쓸 일이 생기면 원본
`banker_plugins/skills/omc-reference/SKILL.md`의 §OMX (Codex) Catalog를 직접 참조하라.

## Operating Rules

- 이 스킬은 레퍼런스다. 사용자가 직접 호출하는 용도가 아니다(`user-invocable: false`).
- 에이전트 위임·팀 오케스트레이션·커밋 메시지 작성 시 필요한 카탈로그 정보를 여기서 가져오고,
  세션 상시 지침(CLAUDE.md/AGENTS.md급)에는 키워드 트리거 수준으로만 둔다.
- 한계: OMC MCP 도구(state/notepad/project memory 등)와 `/team`·`omc` CLI는 OMC 런타임(Claude Code +
  oh-my-claudecode 플러그인)에 종속된다. 이 Muse 환경에 해당 런타임이 없으면 그 항목은 어휘·개념
  참조용으로만 쓰고, 실행은 `subagent.spawn`·`workflow`·내 cron/hooks 등 이 환경의 메커니즘으로 대체한다.
