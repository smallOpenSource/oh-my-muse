# Humanizer — AI Writing Pattern Reference

이 문서는 [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)(WikiProject AI Cleanup 유지)의 패턴 목록을
윤문용으로 정리한 것이다. 사용법은 SKILL.md의 Process를 따른다.

핵심 통찰: "LLM은 다음에 올 가장 통계적으로 그럴듯한 결과를 내놓는다. 결과는 가장 넓은 경우에 적용되는 평균적인 표현으로 수렴한다."

## CONTENT PATTERNS (의미/내용)

### 1. Undue Emphasis on Significance, Legacy, and Broader Trends (중요성·유산 과장)

**주시할 말:** stands/serves as, is a testament/reminder, a vital/significant/crucial/pivotal/key role/moment, underscores/highlights its importance/significance, reflects broader, symbolizing its ongoing/enduring/lasting, contributing to the, setting the stage for, marking/shaping the, represents/marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted

**문제:** 임의의 사실에 "더 넓은 주제에 기여한다"는 식의 중요성 부풀리기를 덧붙인다.

> Before: The Statistical Institute of Catalonia was officially established in 1989, marking a pivotal moment in the evolution of regional statistics in Spain. This initiative was part of a broader movement across Spain to decentralize administrative functions and enhance regional governance.
> After: The Statistical Institute of Catalonia was established in 1989 to collect and publish regional statistics independently from Spain's national statistics office.

### 2. Undue Emphasis on Notability and Media Coverage (주목도 과장)

**주시할 말:** independent coverage, local/regional/national media outlets, written by a leading expert, active social media presence

> Before: Her views have been cited in The New York Times, BBC, Financial Times, and The Hindu. She maintains an active social media presence with over 500,000 followers.
> After: In a 2024 New York Times interview, she argued that AI regulation should focus on outcomes rather than methods.

### 3. Superficial Analyses with -ing Endings (-ing 덧붙이기)

**주시할 말:** highlighting/underscoring/emphasizing..., ensuring..., reflecting/symbolizing..., contributing to..., cultivating/fostering..., encompassing..., showcasing...

> Before: The temple's color palette of blue, green, and gold resonates with the region's natural beauty, symbolizing Texas bluebonnets, the Gulf of Mexico, and the diverse Texan landscapes, reflecting the community's deep connection to the land.
> After: The temple uses blue, green, and gold colors. The architect said these were chosen to reference local bluebonnets and the Gulf coast.

### 4. Promotional and Advertisement-like Language (홍보 어조)

**주시할 말:** boasts a, vibrant, rich (비유적), profound, enhancing its, showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking (비유적), renowned, breathtaking, must-visit, stunning

> Before: Nestled within the breathtaking region of Gonder in Ethiopia, Alamata Raya Kobo stands as a vibrant town with a rich cultural heritage and stunning natural beauty.
> After: Alamata Raya Kobo is a town in the Gonder region of Ethiopia, known for its weekly market and 18th-century church.

### 5. Vague Attributions and Weasel Words (막연한 출처)

**주시할 말:** Industry reports, Observers have cited, Experts argue, Some critics argue, several sources/publications (실제 인용이 적을 때)

> Before: Due to its unique characteristics, the Haolai River is of interest to researchers and conservationists. Experts believe it plays a crucial role in the regional ecosystem.
> After: The Haolai River supports several endemic fish species, according to a 2019 survey by the Chinese Academy of Sciences.

### 6. Outline-like "Challenges and Future Prospects" Sections (정형화된 Challenges 절)

**주시할 말:** Despite its... faces several challenges..., Despite these challenges, Challenges and Legacy, Future Outlook

> Before: Despite its industrial prosperity, Korattur faces challenges typical of urban areas, including traffic congestion and water scarcity. Despite these challenges, with its strategic location and ongoing initiatives, Korattur continues to thrive as an integral part of Chennai's growth.
> After: Traffic congestion increased after 2015 when three new IT parks opened. The municipal corporation began a stormwater drainage project in 2022 to address recurring floods.

## LANGUAGE AND GRAMMAR PATTERNS (어휘/문법)

### 7. Overused "AI Vocabulary" Words (AI 고빈도 어휘)

**고빈도 단어:** Actually, additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (동사), interplay, intricate/intricacies, key (형용사), landscape (추상명사), pivotal, showcase, tapestry (추상명사), testament, underscore (동사), valuable, vibrant

> Before: Additionally, a distinctive feature of Somali cuisine is the incorporation of camel meat. An enduring testament to Italian colonial influence is the widespread adoption of pasta in the local culinary landscape, showcasing how these dishes have integrated into the traditional diet.
> After: Somali cuisine also includes camel meat, which is considered a delicacy. Pasta dishes, introduced during Italian colonization, remain common, especially in the south.

### 8. Avoidance of "is"/"are" (Copula Avoidance)

**주시할 말:** serves as/stands as/marks/represents [a], boasts/features/offers [a]

> Before: Gallery 825 serves as LAAA's exhibition space for contemporary art. The gallery features four separate spaces and boasts over 3,000 square feet.
> After: Gallery 825 is LAAA's exhibition space for contemporary art. The gallery has four rooms totaling 3,000 square feet.

### 9. Negative Parallelisms and Tailing Negations (부정 병렬·꼬리 부정)

"Not only...but...", "It's not just about..., it's..." 과용. 문장 끝에 붙는 "no guessing", "no wasted motion" 같은 잘린 꼬리 부정도 마찬가지.

> Before: It's not just about the beat riding under the vocals; it's part of the aggression and atmosphere. It's not merely a song, it's a statement.
> After: The heavy beat adds to the aggressive tone.
> Before (꼬리 부정): The options come from the selected item, no guessing.
> After: The options come from the selected item without forcing the user to guess.

### 10. Rule of Three Overuse (3개 묶음 강박)

> Before: The event features keynote sessions, panel discussions, and networking opportunities. Attendees can expect innovation, inspiration, and industry insights.
> After: The event includes talks and panels. There's also time for informal networking between sessions.

### 11. Elegant Variation (유의어 순환)

반복 회피 코드 때문에 같은 대상을 계속 다른 말로 부른다.

> Before: The protagonist faces many challenges. The main character must overcome obstacles. The central figure eventually triumphs. The hero returns home.
> After: The protagonist faces many challenges but eventually triumphs and returns home.

### 12. False Ranges (가짜 범위)

의미 있는 척도가 아닌데 "from X to Y" 구성을 쓴다.

> Before: Our journey through the universe has taken us from the singularity of the Big Bang to the grand cosmic web, from the birth and death of stars to the enigmatic dance of dark matter.
> After: The book covers the Big Bang, star formation, and current theories about dark matter.

### 13. Passive Voice and Subjectless Fragments (수동태·무주어 단편)

"No configuration file needed", "The results are preserved automatically" 같은 문장. 능동태가 더 명확하면 고친다.

> Before: No configuration file needed. The results are preserved automatically.
> After: You do not need a configuration file. The system preserves the results automatically.

## STYLE PATTERNS (스타일)

### 14. Em Dashes (and En Dashes): Cut Them

**최종본에 em dash(—)·en dash(–) 금지 — 하드 제약.** 치환 우선순위: 마침표(새 문장) > 쉼표(짧은 삽입) > 콜론(설명 도입) > 괄호(진짜 삽입) > 문장 재구성. ` — `(공백 em dash), `--`(이중 하이픈)도 잡는다. 최종 반환 전 `—`/`–` 스캔.

> Before: The term is primarily promoted by Dutch institutions—not by the people themselves. You don't say "Netherlands, Europe" as an address—yet this mislabeling continues—even in official documents.
> After: The term is primarily promoted by Dutch institutions, not by the people themselves. You don't say "Netherlands, Europe" as an address, yet this mislabeling continues in official documents.

### 15. Overuse of Boldface (볼드 남발)

> Before: It blends **OKRs (Objectives and Key Results)**, **KPIs (Key Performance Indicators)**, and visual strategy tools such as the **Business Model Canvas (BMC)** and **Balanced Scorecard (BSC)**.
> After: It blends OKRs, KPIs, and visual strategy tools like the Business Model Canvas and Balanced Scorecard.

### 16. Inline-Header Vertical Lists (볼드 헤더 리스트)

항목이 굵은 헤더 + 콜론으로 시작하는 리스트 → 문장으로 푼다.

> Before: - **User Experience:** The user experience has been significantly improved with a new interface. ...
> After: The update improves the interface, speeds up load times through optimized algorithms, and adds end-to-end encryption.

### 17. Title Case in Headings (헤딩 제목체)

> Before: ## Strategic Negotiations And Global Partnerships
> After: ## Strategic negotiations and global partnerships

### 18. Emojis

> Before: 🚀 **Launch Phase:** The product launches in Q3 / 💡 **Key Insight:** Users prefer simplicity
> After: The product launches in Q3. User research showed a preference for simplicity. Next step: schedule a follow-up meeting.

### 19. Curly Quotation Marks (곱슬 따옴표)

> Before: He said “the project is on track” but others disagreed.
> After: He said "the project is on track" but others disagreed.

## COMMUNICATION PATTERNS (소통 흔적)

### 20. Collaborative Communication Artifacts (챗봇 잔재)

**주시할 말:** I hope this helps, Of course!, Certainly!, You're absolutely right!, Would you like..., Want me to...?, let me know, here is a...

> Before: Here is an overview of the French Revolution. I hope this helps! Let me know if you'd like me to expand on any section.
> After: The French Revolution began in 1789 when financial crisis and food shortages led to widespread unrest.

### 21. Knowledge-Cutoff Disclaimers and Speculative Gap-Filling (컷오프 면책·추측 메우기)

**주시할 말:** as of [date], Up to my last training update, While specific details are limited/scarce..., based on available information, not publicly available, maintains a low profile, keeps personal details private, prefers to stay out of the spotlight, likely [grew up/studied/began], it is believed that

모르면 모른다고 쓰거나 문장을 자른다. 추측을 사실처럼 꾸미지 않는다.

> Before (면책): While specific details about the company's founding are not extensively documented in readily available sources, it appears to have been established sometime in the 1990s.
> After: The company was founded in 1994, according to its registration documents.
> Before (추측 메우기): Information about her early life is not publicly available, suggesting she maintains a low profile and keeps personal details private. She likely grew up in a middle-class household, which shaped her later interest in education reform.
> After: Her early life is not documented in the available sources. (또는 해당 절 삭제.)

### 22. Sycophantic/Servile Tone (아첨 어조)

> Before: Great question! You're absolutely right that this is a complex topic. That's an excellent point about the economic factors.
> After: The economic factors you mentioned are relevant here.

## FILLER AND HEDGING (군더더기·완곡)

### 23. Filler Phrases

- "In order to achieve this goal" → "To achieve this"
- "Due to the fact that it was raining" → "Because it was raining"
- "At this point in time" → "Now"
- "In the event that you need help" → "If you need help"
- "The system has the ability to process" → "The system can process"
- "It is important to note that the data shows" → "The data shows"

### 24. Excessive Hedging (과도한 완곡)

> Before: It could potentially possibly be argued that the policy might have some effect on outcomes.
> After: The policy may affect outcomes.

### 25. Generic Positive Conclusions (막연한 낙관 결말)

> Before: The future looks bright for the company. Exciting times lie ahead as they continue their journey toward excellence. This represents a major step in the right direction.
> After: The company plans to open two more locations next year.

### 26. Hyphenated Word Pair Overuse (하이픈 쌍 남발)

**주시할 말:** third-party, cross-functional, client-facing, data-driven, decision-making, well-known, high-quality, real-time, long-term, end-to-end.

AI는 서술어 위치에서도 하이픈을 붙인다(`the report is high-quality`). 사람은 대개 수식 위치에서만 붙인다(`a high-quality report`).

> Before: The cross-functional team delivered a high-quality, data-driven report. The team is cross-functional, the report is high-quality, and the methodology is data-driven.
> After: The cross-functional team delivered a high-quality, data-driven report. The team is cross functional, the report is high quality, and the methodology is data driven.

### 27. Persuasive Authority Tropes (권위 행세 문구)

**주시할 말:** The real question is, at its core, in reality, what really matters, fundamentally, the deeper issue, the heart of the matter

> Before: The real question is whether teams can adapt. At its core, what really matters is organizational readiness.
> After: The question is whether teams can adapt. That mostly depends on whether the organization is ready to change its habits.

### 28. Signposting and Announcements (예고 멘트)

**주시할 말:** Let's dive in, let's explore, let's break this down, here's what you need to know, now let's look at, without further ado

> Before: Let's dive into how caching works in Next.js. Here's what you need to know.
> After: Next.js caches data at multiple layers, including request memoization, the data cache, and the router cache.

### 29. Fragmented Headers (헤딩 앵무새 문장)

헤딩 뒤에 헤딩을 되풀이하는 한 줄짜리 워밍업 문장 → 삭제.

> Before: ## Performance / Speed matters. / When users hit a slow page, they leave.
> After: ## Performance / When users hit a slow page, they leave.

### 30. Diff-Anchored Writing (변경 서술)

changelog·릴리스 노트·마이그레이션 가이드가 아니면, "이전에는 ~였는데" 식의 변경 서술이 아니라 현재 상태를 서술한다.

> Before: This function was added to replace the previous approach of iterating through all items, which caused O(n²) performance.
> After: This function uses a hash map for O(1) lookups, avoiding the O(n²) cost of naive iteration.

### 31. Manufactured Punchlines and Staccato Drama (조작된 펀치라인)

짧은 단문 하나는 강조로 괜찮다. 연달아 쌓이면 조작처럼 들린다.

> Before: Then AlphaEvolve arrived. It had no preference for symmetry. No aesthetic prior. No nostalgia for human taste. The old rules were gone.
> After: AlphaEvolve changed the search because it did not favor symmetry or human-looking designs. That made some of the older assumptions less useful.

### 32. Aphorism Formulas (격언 공식)

**주시할 말:** X is the Y of Z, X becomes a trap, X is not a tool but a mirror, the language of, the currency of, the architecture of

> Before: Symmetry is the language of trust. Efficiency becomes a trap when teams forget the human layer.
> After: Symmetric layouts often feel more predictable to users. Teams can over-optimize workflows and miss how people actually use them.

### 33. Conversational Rhetorical Openers (가짜 솔직 오프너)

**주시할 말:** Honestly?, Look, Here's the thing, The thing is, Let's be honest, Real talk (독립된 훅으로 쓸 때)

> Before: Is it worth the price? Honestly? It depends on how often you'll use it.
> After: Whether it's worth the price depends on how often you'll use it.
