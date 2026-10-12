---
name: skill
description: 워크스페이스 스킬 관리 — 사용자가 "스킬 목록 보여줘", "스킬 추가해줘", "스킬 삭제해줘", "스킬 검색해줘", "스킬 수정해줘", "스킬 설정해줘", "스킬 정보 보여줘"라고 요청하면 사용. 목록·추가·삭제·검색·수정·정보 조회·설정 마법사를 지원한다.
---

# Skill Management

`~/workspace/skills`에 설치된 스킬을 관리하는 메타 스킬. 모든 스킬은 `<이름>/SKILL.md` 단일 파일(필요시 부속 파일 포함)이며, 프론트매터는 `name`/`description`이 필수다.

## Purpose

- 워크스페이스 스킬 목록 조회, 추가, 삭제, 검색, 수정, 정보 조회를 채팅 인터페이스로 제공한다.
- 스킬 작성 규격(SKILL.md 프론트매터 + Purpose/Workflow/Output Contract/Operating Rules 구조)을 강제해 스킬 품질을 유지한다.

## Workflow

사용자의 요청에서 하위 명령을 식별한다. 인자가 있으면 직접 실행, 없으면 대화형으로 진행한다.

### "스킬 목록 보여줘" (list / scan)

1. `~/workspace/skills/*/SKILL.md`를 스캔한다 (내장·번들 스킬은 읽기 전용으로 표시).
2. 각 파일의 프론매터(`name`, `description`)를 파싱한다.
3. 테이블로 출력한다.

```
INSTALLED SKILLS (~/workspace/skills/):
| Name        | Description          |
|-------------|----------------------|
| skillify    | 반복 워크플로→스킬 초안 |
```

없으면 "설치된 스킬이 없습니다"라고 보고한다.

### "스킬 추가해줘 <이름>" (add)

1. 이름(소문자·하이픈만), 한 줄 설명(description), 트리거 키워드를 묻는다 (인자에 이름이 있으면 생략).
2. `~/workspace/skills/<이름>/` 디렉터리를 만들고 아래 템플릿으로 `SKILL.md`를 생성한다.
3. 성공 경로를 보고하고 "스킬 수정해줘 <이름>"으로 내용을 다듬으라고 안내한다.

템플릿:

```yaml
---
name: <name>
description: <한 줄 설명 — 트리거 문구 포함>
---

# <Name>

## Purpose

[무엇을 하는 스킬인지]

## Workflow

1. [단계 1]
2. [단계 2]
3. [단계 3]

## Output Contract

[완료 시 사용자에게 전달하는 결과 형식]

## Operating Rules

[하지 말아야 할 것, 한계, 예외 처리]
```

3번 템플릿(오류 해결·워크플로·코드 패턴·통합) 같은 특화 템플릿이 필요하면 사용자에게 물어보고, 아래 ## Skill Templates에서 골라 적용한다. 새 스킬의 실제 작성은 `skill_creator` 스킬을 활용하면 편하다.

### "스킬 삭제해줘 <이름>" (remove)

1. `~/workspace/skills/<이름>/`이 있는지 확인한다.
2. 정보(이름·설명)를 보여주고 **반드시 확인을 받는다**: "'<이름>' 스킬을 삭제할까요? (예/아니오)"
3. 확인되면 디렉터리 전체를 삭제(`trash` 도구 사용 — 복구 가능)하고 보고한다.
4. 없으면 "✗ '<이름>' 스킬을 찾을 수 없습니다"라고 보고한다.

### "스킬 수정해줘 <이름>" (edit)

1. SKILL.md를 읽어 현재 값(이름·설명·구조)을 보여준다.
2. 무엇을 바꿀지 묻는다: `description` / `content` / `rename` / `cancel`.
3. 선택한 항목의 현재 값을 보여주고 새 값을 받아 파일에 반영한다.
4. 변경 요약을 보고한다.

### "스킬 검색해줘 <질의>" (search)

이름·설명·본문에서 대소문자 무시 매칭. 이름/설명 매치를 본문 매치보다 우선 순위로 표시한다.

### "스킬 정보 보여줘 <이름>" (info)

이름·설명·파일 경로·전체 본문을 보여준다. 없으면 search를 제안한다.

### "스킬 설정해줘" (setup)

1. `~/workspace/skills/` 존재 확인 → 없으면 생성한다.
2. list로 전체 인벤토리를 보여준다.
3. 다음 중 무엇을 할지 묻는다: 새 스킬 추가 / 대화에서 패턴 스캔(반복 해결 패턴이 보이면 skillify로 추출 제안) / 완료.

## Output Contract

- 각 작업 후: 수행한 작업 + 대상 스킬 이름 + 파일 경로를 한 줄로 보고한다.
- 삭제·이름 변경 등 파괴적 작업은 사전 확인 없이 실행하지 않는다.
- 오류 형식: `✗ 오류: <내용>` → `→ 제안: <다음 단계>`.

## Operating Rules

- Claude Code 원본의 user/project 스코프(`~/.claude/skills/omc-learned/`, `.omc/skills/`) 개념은 이 환경에 없다. 이 환경의 유일한 스킬 저장소는 `~/workspace/skills/`다 — scope 인자나 동기화(sync) 개념을 요구받으면 "이 환경은 단일 스코프"라고 안내한다.
- 슬래시 커맨드(`/skill ...`)는 이 환경에서 채팅 요청("스킬 목록 보여줘")으로 대체된다. 원래 트리거 문구는 그대로 이해한다.
- 원본의 Quality/Usage 통계(quality/usage 메타)는 이 환경에 추적 인프라가 없으므로 표시하지 않는다. 요구받으면 "지원되지 않음 — 수동으로 description에 메모 가능"이라고 안내한다.
- 파일 삭제는 `rm -rf` 대신 `trash` 도구를 사용한다(복구 가능).
- 스킬 이름 검증: 소문자·숫자·하이픈만 허용.
- AskUserQuestion 같은 대화형 도구가 이 서브에이전트 컨텍스트에 없으면 일반 질문 텍스트로 대체한다.

## Skill Templates

`스킬 추가해줘` 시 사용자가 특화 템플릿을 원하면 아래 중 하나를 선택해 적용한다. 모든 템플릿은 YAML 프론트매터(`name`, `description`, `triggers`)를 필수로 포함한다.

**오류 해결 템플릿**: The Insight / Why This Matters / Recognition Pattern(오류 메시지·파일·발생 맥락) / The Approach(파일·줄 번호 명시 단계) / Example(수정 전후 코드).

**워크플로 템플릿**: The Insight / Why This Matters / Recognition Pattern(작업 유형·파일 패턴) / The Approach / Gotchas.

**코드 패턴 템플릿**: The Insight / Why This Matters / Recognition Pattern / The Approach(원칙 기반 휴리스틱) / Example / Anti-Pattern.

**통합 템플릿**: The Insight / Why This Matters / Recognition Pattern(통합 파일·설정 위치) / The Approach / Gotchas.

## Skill Quality Guidelines

좋은 스킬은:

1. **검색으로 5분 안에 못 찾는 것** — BAD: "TypeScript에서 파일 읽기", GOOD: "이 코드베이스의 커스텀 path resolution은 fileURLToPath 필요"
2. **이 코드베이스·프로젝트 특화** — 실제 파일/오류 인용
3. **정확히 실행 가능** — WHAT과 WHERE 명시
4. **고생해서 얻은 것** — 상당한 디버깅이 필요했던 패턴

## Related Skills

- `skillify` — 현재 대화에서 반복 워크플로를 스킬 초안으로 추출 (사용자가 "스킬로 만들어줘"라고 요청하면 사용)
- `skill_creator` — 재사용 가능한 새 스킬을 정식으로 만들 때 사용
