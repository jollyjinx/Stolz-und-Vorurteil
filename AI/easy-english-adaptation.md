---
title: Easy English - Editorial and Adaptation Rules
description: Binding standard for the complete accessible-English adaptation of Pride and Prejudice.
doc_type: agent-guidance
status: active
scope: easy-english-chapters
source_of_truth:
  english: source-chapters
  terminology: easy-english-glossary.json
  notes: easy-english-notes.json
---

# Purpose of the Edition

This edition tells the complete novel in clear, present-day English. It is for readers who find long sentences, rare words, or unstated historical customs difficult. It is **not an abridged retelling** and does not claim compliance with a formally regulated Easy Read standard.

# Binding Rules

1. Adapt directly from the matching chapter in `source-chapters/`. Do not use another adaptation, summary, translation, or external rewriting service.
2. Preserve every source paragraph as exactly one Easy English paragraph. Long source sentences should be divided into shorter sentences inside that paragraph.
3. Omit no action, observation, judgment, joke, letter passage, or turn in a conversation. Add no new event or interpretation.
4. Aim broadly at accessible B1 English. Prefer common, concrete words and one main idea per sentence. Most sentences should be no longer than about 15 to 18 words, with some variation so the prose remains literary.
5. Avoid nested clauses, distant subjects and verbs, double negatives, abstract noun-heavy phrasing, and unclear pronouns. Repeat a person's name when `he`, `she`, or `they` could be unclear.
6. Preserve Jane Austen's irony. Make it understandable through clear wording and sentence order, but do not explain the joke inside the novel.
7. Preserve point of view, the characters' current knowledge, and genuine ambiguity. Never reveal a motive or later discovery before the source does.
8. Dialogue should sound natural and current without slang. Use English curly quotation marks (`“…”`) and an em dash (`—`) for abrupt interruptions.
9. Keep names, place names, and English titles exactly: `Mr.`, `Mrs.`, `Miss`, `Lady`, `Sir`, and `Colonel`. The forms in `easy-english-glossary.json` are binding.
10. Replace difficult historical wording with the clear term required by the glossary. Put additional explanation in the generated first-use note and reader glossary, not in repeated parenthetical explanations.
11. Preserve every amount of money and the phrase `a year` where the source uses it. Write the currency as `pounds`; do not add modern currency conversions to the novel.
12. Letters keep their internal paragraph divisions and Markdown italics. Every completed file begins with `# Chapter <Roman numeral>` and then contains only the adapted novel text.
13. Do not retain the source edition's decorative all-caps opening word. Use ordinary English capitalization at every chapter opening.

# Workflow for Each Chapter

1. Read the full source chapter and the relevant glossary entries before writing.
2. Adapt paragraph by paragraph directly from the source.
3. Check paragraph count and order against the source.
4. Read the Easy English chapter alone. Shorten nested sentences and replace needlessly rare words.
5. Compare again with the source. Content, irony, speakers, names, numbers, and italics must remain present.
6. Keep chapter files free of footnote markup. The book builder adds notes from `easy-english-notes.json` after the chapter set has been reviewed.

# Style Examples

- Avoid: `In consequence of her having formed this determination …`
  Prefer: `She had made this decision. Because of it …`
- Avoid: `She was unable to understand his motives.`
  Prefer: `She could not understand his reasons.`
- Avoid: `Having read the letter while in a state of great agitation, she …`
  Prefer: `She was very upset. Then she read the letter and …`
- Allowed: an unusual word when it is important to rank, character, or a joke. Its meaning must be clear from the context, note, or glossary.
