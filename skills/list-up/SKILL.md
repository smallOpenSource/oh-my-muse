---
name: list-up
description: "보유 스킬·도구 전체 목록을 표 형태의 웹 아티팩트로 만든다. 워크스페이스 스킬(~/workspace/skills) + 연결 제품 스킬(/opt/hatch/skills) + 도구 네임스페이스를 수집해 research_dir 리포트로 넘기고 artifact.create_web_static으로 빌드. 'list-up'/'스킬 목록 보여줘'/'도구 목록 보여줘'/'카탈로그 만들어줘' 시 사용."
argument-hint: "없음"
---

# list-up — 스킬·도구 카탈로그 아티팩트 생성

## Purpose

보유 스킬과 도구 전체를 단일 표 형태의 웹 아티팩트(검색·필터·모달 포함)로 만든다.
데이터 수집은 직접 수행하고, 표 렌더링은 `research_dir` 경유로 빌더에게 위임한다.
`verbatim_request`에는 사용자 원문을 그대로 넣고, 표시 요구사항은 리포트에 적는다.

## Step 1 — 데이터 수집

### 1a. 워크스페이스 스킬

```bash
python3 - <<'EOF'
import os, re, json
skills_dir = os.path.expanduser("~/workspace/skills")
up = os.path.expanduser("~/workspace/skills-upstream")
origins = {}
for repo, label in [("banker_plugins","banker"),("oh-my-claudecode","oh-my-claudecode"),
                    ("superpowers","superpowers"),("harness","harness"),("scroll-world","scroll-world")]:
    p = os.path.join(up, repo, "skills")
    if os.path.isdir(p):
        for n in os.listdir(p):
            origins.setdefault(n, label)
out = []
for n in sorted(os.listdir(skills_dir)):
    sp = os.path.join(skills_dir, n, "SKILL.md")
    if not os.path.isfile(sp): continue
    txt = open(sp, encoding="utf-8").read(3000)
    m = re.search(r'^name:\s*(.+)$', txt, re.M)
    name = m.group(1).strip() if m else n
    m2 = re.search(r'^description:\s*(.+)$', txt, re.M)
    desc = m2.group(1).strip().strip('"') if m2 else ""
    out.append({"name": name, "desc": desc, "origin": origins.get(n, "custom")})
json.dump(out, open("/tmp/listup_ws.json","w"), ensure_ascii=False)
print(len(out), "workspace skills")
EOF
```

- 출처 분류: 디렉터리명이 업스트림 5종의 `skills/` 아래 이름과 일치하면 해당 출처, 없으면 `custom`.
- `description` 원문 전문을 수집 (약식 설명은 빌더가 단어 중심 개조식 한글로 압축).

### 1b. 연결 제품 스킬

```bash
for d in /opt/hatch/skills/*/; do
  n=$(basename "$d"); f="$d/SKILL.md"
  [ -f "$f" ] && echo "$n | $(grep -m1 '^description:' "$f" | sed 's/^description: *//' | cut -c1-100)"
done
```

- 설명이 `>-` YAML 폴드 형태면 SKILL.md 본문 첫 문단으로 대체.

### 1c. 도구 네임스페이스

런타임 도구 목록에서 네임스페이스별 한 줄 설명을 직접 작성한다 (muse, artifact, avatar,
browser, chat, credentials, cron, device, feed, forget, hooks, idea, map, media,
onboarding, permissions, proactivity, process, shopping, social, subagent, todo,
tool_search, tracking, trash, ui, user_goal, voice, wallet, widget, worker, workflow, ads).

## Step 2 — research_dir 리포트 작성

`~/workspace/research_notes/skill-catalog/report.md`에 작성:

- 기준일, "전체 빠짐없이 포함 (요약·생략 금지)" 명시
- 섹션 1: 워크스페이스 스킬 — `| # | 스킬 | 출처 | 원문 설명 |` 표 (설명은 원문 전문)
- 섹션 2: 연결 제품 스킬 — `| # | 스킬 | 설명 |` 표
- 섹션 3: 도구 네임스페이스 — `| # | 도구 | 설명 |` 표
- 표시 요구사항 (빌더가 반드시 지킴):
  - 단일 표, 열: 번호(1~N 연속), 이름, 약식 설명(단어 중심 개조식 한글), 출처(태그), 원문설명(클릭 시 모달로 전체 표시), 비고
  - 상단: 전체 검색창, 출처·비고 필터, 개수 요약 카드
  - 라이트 테마 강제: `<meta name="color-scheme" content="light">` + `:root{color-scheme:light}` + `html,body{background:#ffffff}`
  - 모바일: 가로 스크롤 없는 반응형 행 표시
  - 한국어 UI, 표 중심, 장식 금지

## Step 3 — 아티팩트 생성

```
artifact.create_web_static
  name: "스킬·도구 카탈로그"
  icon_subject: 보유 스킬·도구 전체를 검색·필터 가능한 단일 표로 보여주는 카탈로그 페이지
  verbatim_request: 사용자의 원문 그대로 (덧붙이지 않음)
  research_dir: ~/workspace/research_notes/skill-catalog
  capabilities: {"public_web_read": false, "connectors": []}
```

- 빌드는 비동기. 시작 확인 후 턴 종료, 완료 핸드오프 수신 시 카드 present.
- 수정 요청은 `artifact.edit` + 사용자 원문 그대로.

## Step 4 — 보고

- 완료 시: 총 항목 수, 열 구성, 검증 내용(모달·검색·필터 동작, 콘솔 에러 없음)을 간결 개조식으로 보고.
- 공개 공유 제안 금지. `artifact.share`는 사용자 명시 요청 시에만.

## Gotchas

- `verbatim_request`에 요구사항을 덧붙이지 않는다 — 빌더는 요청자 원문으로 읽는다. 표 열 구성·테마 같은 요구는 리포트에 둔다.
- 업스트림 디렉터리명이 바뀌면 1a의 출처 매핑을 먼저 갱신한다.
- 제품 스킬 설명이 YAML 폴드(`>-`)면 본문에서 한 줄 요약을 직접 만든다.
