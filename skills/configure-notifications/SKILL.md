---
name: configure-notifications
description: "작업 완료·입력 필요 알림을 Telegram·Discord·Slack·웹훅으로 받도록 설정하는 스킬: 제공자별 토큰·웹훅 수집 → 설정 파일 기록 → 테스트 발송. 사용자가 '알림 설정해줘', '텔레그램 알림 연결해줘', '디스코드 웹훅 설정해줘', '슬랙 알림 설정해줘', '웹훅 알림 설정해줘'라고 요청하면 사용."
---

# configure-notifications — 알림 연동 설정

## Purpose

작업 완료·입력 필요·백그라운드 작업 종료를 Telegram·Discord·Slack·커스텀 웹훅으로 알려주도록 설정한다. 설정은 `~/workspace/.omc-config.json`에 저장된다.

**원본 대비 핵심 변경**: 원본은 Claude Code hooks(Stop/Notification/PreCompact 이벤트)에 알림 발송을 배선한다. 이 환경에는 그 hooks 메커니즘이 없으므로, 본 스킬은 "연동 설정(자격증명 수집·저장·테스트)"까지만 담당하고, 실제 발송 트리거는 [Operating Rules](#operating-rules)의 대안을 따른다.

## Workflow

### Step 1 — 제공자 판별

사용자 요청에서 제공자를 판별한다: "telegram" → Telegram, "discord" → Discord, "slack" → Slack, "webhook"/"n8n"/"openclaw"/"cli" → 커스텀 연동. 제공자가 없으면 `muse.create_options`로 묻는다: "어떤 알림 서비스를 설정할까요?" (Telegram / Discord / Slack / 커스텀 웹훅).

### Step 2 — 자격증명 수집

`muse.create_options`의 자유 입력(Other)으로 값을 받고 형식을 검증한다.

**Telegram**
1. 기존 설정 확인: `jq -r '.notifications.telegram.enabled // false' ~/workspace/.omc-config.json`. 이미 있으면 현재 값을 보여주고 갱신 여부를 묻는다.
2. 봇 생성 안내: 텔레그램에서 @BotFather → `/newbot` → 이름/사용자명 → 토큰 발급 (`123456789:ABCdefGHI...` 형식).
3. 채팅 ID 안내: 봇에게 `/start` 전송 후 `https://api.telegram.org/bot<토큰>/getUpdates`에서 `chat.id` 확인 (개인=양수, 그룹=음수).
4. 수집·검증: 봇 토큰(`숫자:영숫자` 패턴), 채팅 ID(숫자), 메시지 형식(Markdown 권장 / HTML).
5. 알림 이벤트 선택(멀티): 세션 종료(권장), 입력 필요(권장), 세션 시작, 세션 유지.

**Discord**
1. 기존 설정 확인: `.notifications.discord`(웹훅) / `.notifications["discord-bot"]`(봇) enabled 여부.
2. 웹훅 방식: 서버 설정 → 연동 → 웹훅 → 새 웹훅 → URL 복사. 멘션(`<@user_id>`)은 선택. 표시 이름(username) 오버라이드 선택 가능(기본값 "OMC").
3. 봇 방식: Discord 개발자 포털에서 봇 토큰 + 채널 ID 수집.
4. 이벤트 선택(멀티): 위 Telegram과 동일.

**Slack**
1. 기존 설정 확인: `.notifications.slack.enabled`.
2. Incoming Webhook URL 수집: Slack 앱 디렉터리 → Incoming Webhooks → 채널 선택 → URL 복사.
3. 이벤트 선택(멀티): 위와 동일.

### Step 3 — 설정 저장

기존 파일을 읽어 병합 후 저장한다 (환경변수 대체도 지원: `OMC_TELEGRAM_BOT_TOKEN`, `OMC_TELEGRAM_CHAT_ID`, `OMC_DISCORD_WEBHOOK_URL`, `OMC_SLACK_WEBHOOK_URL`):

```bash
CONFIG_FILE="$HOME/workspace/.omc-config.json"
EXISTING=$(cat "$CONFIG_FILE" 2>/dev/null || echo '{}')
echo "$EXISTING" | jq \
  --arg token "$BOT_TOKEN" \
  --arg chatId "$CHAT_ID" \
  --arg parseMode "$PARSE_MODE" \
  '.notifications.enabled = true |
   .notifications.telegram = {enabled: true, botToken: $token, chatId: $chatId, parseMode: $parseMode}' \
  > "$CONFIG_FILE"
```

선택하지 않은 이벤트는 `.notifications.events["<이벤트>"] = {enabled: false}` 로 비활성화.

### Step 4 — 테스트 발송

"테스트 알림을 보낼까요?" 묻고(권장: 예), 발송 후 결과 보고:

- **Telegram**: `curl -s "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" -d chat_id=... -d parse_mode=... -d text="테스트 알림"`. 401=토큰 오류, 400 chat not found=채팅 ID 오류 또는 봇에게 `/start` 미전송.
- **Discord/Slack**: 웹훅 URL에 `curl -X POST -H "Content-Type: application/json" -d '{"text":"테스트"}'` (Slack) / `{"content":"테스트"}` (Discord).

### Step 5 — 커스텀 연동 (웹훅·n8n·CLI)

"커스텀 연동/웹훅/n8n/OpenClaw/CLI 명령"이라고 하면 이 흐름을 따른다.

1. 종류 선택: OpenClaw 게이트웨이 / n8n 웹훅 / 커스텀 에이전트 게이트웨이 / 일반 웹훅 / 일반 CLI 명령.
2. 웹훅 계열: URL(HTTPS 필수, localhost 개발 예외) → 인증(Bearer/커스텀 헤더/없음) → 이벤트 멀티선택(session-start, session-end, session-stop, session-idle, ask-user-question) → 테스트 POST(`{"event":"test", ...}`) → 저장.
3. CLI 계열: 실행할 단일 명령(공백·셸 메타문자 금지) → 인자(한 줄에 하나, `{{변수}}` 사용 가능) → 타임아웃(기본 5000ms) → 이벤트 선택 → 테스트 실행 → 저장.
4. 저장 형식(`.omc-config.json` 내 `customIntegrations.integrations[]`):

```json
{
  "id": "my-webhook", "type": "webhook", "preset": "generic",
  "enabled": true, "events": ["session-end"],
  "config": {
    "url": "https://example.com/hook", "method": "POST",
    "headers": {"Content-Type": "application/json"},
    "bodyTemplate": "{\"event\":\"{{event}}\",\"sessionId\":\"{{sessionId}}\",\"timestamp\":\"{{timestamp}}\"}",
    "timeout": 10000
  }
}
```

관리: `jq '.customIntegrations.integrations[] | {id, type, enabled, events}'` 로 목록, `enabled` 토글로 활성화/비활성화, `select(.id != "...")` 로 삭제.

**템플릿 변수**: `{{event}}`, `{{sessionId}}`, `{{projectPath}}`, `{{projectName}}`, `{{timestamp}}`, `{{duration}}`, `{{durationMs}}`, `{{reason}}`, `{{tmuxSession}}`, (session-end 전용: `{{agentsSpawned}}`, `{{agentsCompleted}}`, `{{modesUsed}}`, `{{contextSummary}}`), (ask-user-question 전용: `{{question}}`).

### Step 6 — 완료 보고

```
<제공자> 알림 설정 완료!

  대상:    <봇 사용자명 / 채널 / 웹훅>
  형식:    Markdown
  이벤트:  session-end, ask-user-question

설정 저장: ~/workspace/.omc-config.json
```

## Output Contract

완료 보고 시 제공자·대상·이벤트·설정 파일 경로를 명시한다. 테스트 발송을 했으면 성공/실패와 실패 사유(401/400 등)를 함께 보고한다. 환경변수 대체 사용 시 어떤 변수를 설정했는지도 명시한다.

## Operating Rules

- **Claude Code hooks 한계**: 원본의 자동 발송(Stop/Notification/PreCompact 이벤트 훅, `omc --telegram` 같은 세션별 활성화 플래그)은 Claude Code CLI 전용 메커니즘이라 이 환경에서 동작하지 않는다. 조용히 누락하지 않기 위해 명시한다.
- **대안 1 — 이벤트 자동화**: 이 환경의 `hooks.add`로 작업 완료 시점에 알림 스크립트를 연결한다. 예: 서브에이전트 작업 종료 후 부모 에이전트가 설정된 제공자로 결과 요약을 발송.
- **대안 2 — 주기 확인**: `cron`으로 상태 파일을 폴링해 조건 충족 시 알림 발송(예: 장시간 작업의 중간 경과 보고).
- **수동 발송**: 위 자동화가 없으면, 사용자가 요청할 때 에이전트가 저장된 설정을 읽어 `curl`로 직접 발송한다. 토큰 등 자격증명은 파일·로그·보고서에 원문 노출하지 않는다.
- **AskUserQuestion 치환**: 원본의 AskUserQuestion은 이 환경의 `muse.create_options`로 대체한다.
- **경로 치환**: 원본의 `${CLAUDE_CONFIG_DIR:-~/.claude}/.omc-config.json`·`omc_config.hook.json`·`omc_config.openclaw.json`은 모두 `~/workspace/` 아래로 읽는다. OpenClaw 레거시 설정 마이그레이션(`omc_config.openclaw.json` → `customIntegrations`)은 경로만 치환하고 절차는 원본을 따른다.
- **훅 이벤트 템플릿 축소**: 원본의 "Hook Event Templates" 섹션(플랫폼별 메시지 커스터마이징)은 핵심만 남겼다. 메시지 커스터마이징이 필요하면 커스텀 연동의 `bodyTemplate`을 사용한다.
- `configure-openclaw` 연동 언급은 원본 참조용으로만 남긴다. 별도 스킬이 없으면 커스텀 연동 흐름으로 처리한다.
