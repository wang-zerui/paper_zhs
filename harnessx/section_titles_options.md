# Section 3-4-5 Title Options

## Current Titles (Problems)

| # | Current Title | Issue |
|---|---|---|
| 3 | Foundry: The Compositional Substrate | "Name: Subtitle" pattern |
| 4 | AEGIS: Harness Evolution as RL in Symbolic Space | Same pattern but subtitle too long |
| 5 | Model-Harness Co-Evolution | No name prefix, breaks pattern |

**Structural issues:**
1. Inconsistent naming pattern (3/4 have "System: Description", 5 does not)
2. The three pillars from the abstract (composability, adaptability, evolvability) are invisible in the TOC
3. Reader cannot tell from titles alone that these form a progressive three-part method
4. Section 4 subtitle is overly specific for a TOC entry

---

## Option A: Parallel "Pillar: System" Pattern

| # | Title |
|---|---|
| 3 | Composability: The Foundry |
| 4 | Adaptability: AEGIS |
| 5 | Evolvability: Model-Harness Co-Evolution |

**Pros:** Directly mirrors the abstract's three pillars; TOC reads as a coherent progression; short and scannable.
**Cons:** Loses the descriptive subtitles that hint at technical content; "Composability" as a section title may feel abstract.

---

## Option B: "System — Description" with Consistent Length

| # | Title |
|---|---|
| 3 | Foundry: Compositional Harness Substrate |
| 4 | AEGIS: Adaptive Harness Evolution |
| 5 | Co-Evolution: Joint Model-Harness Optimization |

**Pros:** All follow "Name: Short Description"; consistent rhythm; Co-Evolution gets a name prefix.
**Cons:** Doesn't surface the three-pillar narrative; "Co-Evolution" as a system name is weaker than Foundry/AEGIS.

---

## Option C: Pillars as Lead, System in Parentheses

| # | Title |
|---|---|
| 3 | Composable Harness Architecture (Foundry) |
| 4 | Adaptive Harness Evolution (AEGIS) |
| 5 | Model-Harness Co-Evolution |

**Pros:** Adjectives (Composable, Adaptive) create visible parallel; system names are present but subordinate; Section 5 naturally has no separate system name.
**Cons:** Parenthetical system names feel demoted; breaks if reader expects "Name: Description" format.

---

## Option D: Keep Current Pattern, Fix Consistency Only

| # | Title |
|---|---|
| 3 | Foundry: The Compositional Substrate |
| 4 | AEGIS: Harness Evolution in Symbolic Space |
| 5 | COEVO: Model-Harness Co-Evolution |

**Pros:** Minimal change; all three now have "NAME: Description"; fixes the asymmetry.
**Cons:** "COEVO" is an invented acronym with no prior use in the paper; forced.

---

## Option E: Three Pillars as Numbered Subtitles (my recommendation)

| # | Title |
|---|---|
| 3 | The Foundry: Composable Harness Substrate |
| 4 | AEGIS: Adaptive Harness Evolution |
| 5 | Co-Evolution: Closing the Model-Harness Loop |

**Pros:**
- All three follow "Name: Verb/Adjective + Noun" pattern
- Adjectives (Composable, Adaptive) + verb (Closing) create a progressive narrative: build → evolve → close the loop
- Each subtitle is 3-4 words (consistent length)
- "Closing the loop" echoes the abstract ("closes the model-harness co-evolution loop")
- No invented acronyms

**Cons:** "The Foundry" vs "AEGIS" vs "Co-Evolution" — the third still lacks a proper name, but "Co-Evolution" reads naturally as a concept-name.

---

## Option F: Full Pillar Integration

| # | Title |
|---|---|
| 3 | Composability: The Foundry Substrate |
| 4 | Adaptability: The AEGIS Evolution Engine |
| 5 | Evolvability: The Co-Evolution Loop |

**Pros:** Maximum clarity on three pillars; "The X" pattern in subtitle is parallel; TOC reads like a roadmap.
**Cons:** "The AEGIS Evolution Engine" is slightly redundant; pillar words may feel heavy-handed.

---

## My Ranking

1. **Option E** — best balance of consistency, narrative, and naturalness
2. **Option A** — cleanest if you want maximum brevity
3. **Option F** — strongest if you want the three pillars front-and-center

Pick one (or mix elements), and I'll update method.tex + push.
