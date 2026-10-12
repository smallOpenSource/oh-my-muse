---
name: setup-harness-factory
description: "도메인 한 줄로 전문 에이전트 팀을 만들어 주는 `revfactory/harness` 방법론을 로컬 원본(~/workspace/skills-upstream/harness)에서 읽어 쓰고 사용법을 안내. 마켓플레이스 설치는 Muse 환경에서 불가. 'setup-harness-factory'/'하네스 팩토리 설치'/'에이전트팀 생성' 시 사용. 기존 harness-factory 스킬과는 별개."
---

# setup-harness-factory: revfactory/harness 팀 아키텍처 팩토리 설치·구성

> **Muse 환경 적응**: `harness` 원본은 `~/workspace/skills-upstream/harness` 에 이미 clone돼 있다. Claude Code 마켓플레이스 명령(`/plugin marketplace add`, `/plugin install harness@harness-marketplace`)은 Muse 환경에서 동작하지 않는다. Muse에는 네이티브 팀 프리미티브·플러그인 마켓플레이스가 없으므로, **설치 대신 방법론을 직접 읽어 쓰는 방식**으로 적응한다. 실사용 대안은 이미 설치된 별개 스킬 `harness-factory`(에이전트 팀 방법론, Muse 네이티브)다. 이 디렉터리와 혼동하지 말 것.

`harness`는 도메인을 한 줄로 받아 `.claude/agents/`+`.claude/skills/`(전문 에이전트팀 + 그 에이전트가 쓸
스킬)를 생성하는 **메타 스킬**이다. 이 플러그인의 본체는 설치물이 아니라 **방법론**이다. 따라서 이
스킬은 설치에서 그치지 않고 구성(experimental flag 영속화)과 사용 안내(모드·패턴·비용 가드)까지
책임진다. 이미 설치돼 있으면 갱신·재확인만 한다(멱등). 답변은 한글.

## 런타임 배선
- **Claude Code** = `revfactory/harness` 플러그인(마켓플레이스 설치, 네이티브 팀 프리미티브 사용). Muse 환경에서는 마켓플레이스가 없어 이 경로를 쓸 수 없다.
- **Codex** = `SaehwanPark/meta-harness`(별개 레포·Python 인스톨러·파일 handoff). Muse 환경에서 해당 없다.
- **Muse** = 로컬 원본(`~/workspace/skills-upstream/harness`)의 `skills/harness/SKILL.md` 와 `references/` 를 방법론으로 직접 읽고, 팀 실행은 서브에이전트 병렬 호출로 구현한다. 플러그인 설치 과정이 필요 없다.

## 0. 감지 (먼저, 추정 금지)
```bash
command -v claude >/dev/null && claude --version || echo "claude: 미설치"
ls -la .claude/agents .claude/skills 2>/dev/null   # 기존 harness 산출물 흔적 감사
```
- **v2.1.178 경계 주의**: 그 이후 버전은 `TeamCreate`/`TeamDelete` 도구가 제거되고 팀이 세션 시작 시
  자동 구성된다. harness SKILL.md·OMC 문서의 `TeamCreate` 호출 예시가 현행 CLI와 어긋날 수 있다.
  버전을 확인하고 **불일치 가능성을 사용자에게 정직히 고지**한다(가짜 확신 금지).
- 기존 `.claude/agents/`·`.claude/skills/`·`CLAUDE.md`에 harness 흔적이 있으면 신규 생성이 아니라
  확장·유지보수로 다룬다(harness 자신의 Phase 0 감사 원칙).

## 1. 설치
### Muse (이 환경)
플러그인 마켓플레이스가 없으므로 설치 과정이 없다. 로컬 원본을 방법론 소스로 쓴다.
```bash
ls ~/workspace/skills-upstream/harness/skills/harness/          # SKILL.md + references/
ls ~/workspace/skills-upstream/harness/skills/harness/references/
```
- `skills/harness/SKILL.md` 를 읽고, 심층 패턴은 `references/` 6종(패턴 카탈로그·오케스트레이터 템플릿·팀 예시·skill writing/testing·QA)에 위임한다.
- 상류 문서를 verbatim 복사하지 않고, 설치된 원본 자체를 가리킨다(Apache-2.0).
- 이미 `~/workspace/skills/harness-factory/` 가 설치돼 있으면 그 스킬(Muse 네이티브 방법론)을 우선 검토한다. 이 스킬 디렉터리는 건드리지 않는다.

### Claude Code (참고 - Muse에서 실행 불가)
세션 안(슬래시 커맨드):
```
/plugin marketplace add revfactory/harness
/plugin install harness@harness-marketplace
/reload-plugins
```
- **정답 슬러그는 `harness@harness-marketplace` 하나뿐이다.** 저장소 문서가 3-way로 어긋나 있으니(KO/JA README=`harness-marketplace`[`harness@` 접두 누락], quickstart=`harness@harness`[마켓플레이스 접미 오류]) 그대로 복붙하지 말 것. Muse 환경에서는 이 명령들이 동작하지 않는다.
- 대안(마켓플레이스 없이 글로벌 스킬 직접 설치): `cp -r skills/harness ~/.claude/skills/harness`.

### Codex CLI (Muse 환경에서 해당 없음)
원본의 meta-harness 설치 안내는 Codex 전용이라 생략한다.

## 2. 구성 (핵심)
팀 프리미티브는 Claude Code에서 **experimental flag로 게이트**된다. 셸 세션이 아니라 `settings.json`에 영속화한다:
```json
{ "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" } }
```
- 셸 `export`는 **그 셸에서 띄운 claude에만** 적용되어 재시작 후 유실된다. 반드시 `settings.json`
  `env`에 기록해야 영속한다(Claude Code 환경 기준).
- 미설정 시 **에러 없이 조용히 단일 에이전트로 폴백**되어 Pipeline/Fan-out-in/Supervisor/Hierarchical
  패턴이 소리 없이 깨진다(harness 관리자가 `docs/experimental-dependency.md`에 공식 인정). Claude Code
  v2.x+ 필요.
- **Muse 환경에서는 이 flag가 필요 없다.** Muse의 팀 실행은 서브에이전트 병렬 호출이라 실험 플래그 게이트가 존재하지 않는다. 무증상 폴백 리스크도 해당 없다.

## 3. 사용 안내 (요약; 심층은 설치된 플러그인 references/ 위임)
> harness 자신이 6종 references/(패턴 카탈로그·오케스트레이터 템플릿·팀 예시·skill writing/testing·QA)로
> Progressive Disclosure한다. 여기서는 요약만 담고, 깊이는 설치된 플러그인의 references/를 읽게 위임한다
> (상류 문서를 verbatim 복사하지 않는다).

**(a) 모드 결정트리** (team / subagent / hybrid):
- 2+ 에이전트 + 실시간 상호통신(교차검증·발견 공유)이 가치를 더하면 → **team**.
- 단일 작업·독립 병렬·결과만 반환이면 → **subagent**(경량·토큰효율).
- 공식 비용지침: **순차·동일 파일 편집·의존성 많은 작업은 subagent/단일세션이 유리**하다. harness의
  "2+면 팀 기본"과 어긋날 수 있으니, 팀이 정말 필요한지 재확인하는 게이트를 둔다.

**(b) 6개 아키텍처 패턴**(1줄):
- **Pipeline** (순차 의존): n 출력이 n+1 입력.
- **Fan-out/Fan-in** (병렬+집계): 팀모드가 가장 자연스럽다.
- **Expert Pool** (라우팅 택1): 라우터가 입력 분류 후 전문가 하나 호출, subagent 적합.
- **Producer-Reviewer** (생성·검증): 재시도 캡 2-3(무한루프 방지).
- **Supervisor** (동적 분배): 중앙이 런타임 조건으로 워커 배정.
- **Hierarchical** (재귀 위임): 깊이 ≤ 2(3+는 지연·컨텍스트 손실).

**(c) 비용 가드**: 팀 실행은 단일세션 대비 **약 7× 토큰**(공식). 그러므로:
- 팀 규모 **3-5명**(집중된 3명 > 분산된 5명).
- 워커 모델은 **Sonnet** 기본.
- 작업 완료 즉시 종료. spawn 프롬프트는 간결하게.

## 4. 리스크 고지
harness는 실험적 팀 API에 의존한다. `docs/experimental-dependency.md`가 3시나리오를 자체 정의한다:
- **A** 플래그 제거(GA 승격) / **B** Managed Agents 서버사이드 실행으로 대체 / **C** 하위호환 없는
  시그니처 변경.
- **C는 v2.1.178에서 사실상 현실화된 정황이다**(`TeamCreate`/`TeamDelete` 제거). 설치 시 "실험적 기능
  의존"이라는 사실을 반드시 드러낸다.
- **부작용(read-only 아님)**: 실행 시 사용자 프로젝트에 파일을 직접 생성한다(`.claude/agents/`·
  `.claude/skills/`·중간산출물 `_workspace/`). 기존 파일 충돌 처리·CLAUDE.md 포인터 등록을 안내한다.

## 검증 (보고 의무)
1. **산출물**: `~/workspace/skills-upstream/harness/skills/harness/` 에 SKILL.md·references/ 가 실제 있는지.
2. **flag 영속**: Muse 환경에서는 해당 없음(서브에이전트 방식이라 게이트가 없다). Claude Code에서 쓸 때만 `settings.json`에 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 기록을 확인한다.
3. **팀 스폰**: 간단한 샘플 태스크로 서브에이전트 병렬 호출이 실제로 동작하는지.
4. **Codex**: Muse 환경에서 해당 없음.

보고는 4필드로 한다: **감지(버전·기존흔적) · 설치(로컬 원본 or 마켓플레이스) · 구성(flag 영속, Muse는 불필요) ·
검증(산출물·팀스폰)**. 실패·불명확은 정직 보고(가짜 성공 금지).

## 함정
- **마켓플레이스 명령 불가**: `/plugin marketplace add`, `/plugin install harness@harness-marketplace` 는 Muse 환경에서 동작하지 않는다. 로컬 원본(`~/workspace/skills-upstream/harness`)을 직접 읽는 방식으로 대체한다.
- **3-way 설치명령 버그**: (Claude Code 참고) 유일 정답은 `harness@harness-marketplace`. KO/JA README·quickstart는 틀림.
- **무증상 폴백**: (Claude Code 참고) flag 없으면 팀 패턴이 조용히 단일 에이전트로 저하(에러 안 남). Muse 환경에서는 해당 없음.
- **비용 7×**: 팀은 고토큰. 규모·모델·종료 가드 없이 돌리지 말 것.
- **버전 drift**: v2.1.178에서 `TeamCreate`/`TeamDelete` 제거. 상류 문서의 팀 호출 예시가 현행과 어긋남.
- **릴리스/태그 0건**: GitHub Releases·Tags 모두 없음. 버전 근거는 오직 `plugin.json`의 `1.2.0`.
- **라이선스 Apache-2.0**: 연동·참조이지 banker 재배포가 아니다. 상류 references/를 verbatim 복사하지
  않고 로컬 원본 자체를 가리킨다.
- **`~/workspace/skills/harness-factory/` 는 별개 스킬**: 이 스킬과 이름이 비슷하지만 Muse 네이티브 에이전트 팀 방법론 스킬이다. 절대 건드리지 않는다.

ARGUMENTS: `[--scope user|project]` (원본의 Codex meta-harness 설치 범위 인자. Muse 환경에서는 해당 없음)
