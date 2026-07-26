# Case Study: ITSM — ``Create KB and Link" *(claude-sonnet-4-5, 0/2 verifiers passed)*

## Task (condensed)
Kenji Tanaka (agent, Acme Corp) resolved incident INC0000004 (VPN connection failure) without referencing a knowledge article. He must draft a new internal KB article titled "VPN Connection Failure Guide" and link it to the incident.

**Relevant policy (excerpts):**
- **§7 Knowledge Creation:** *``…the Agent must create and link a new **knowledge draft** before final closure."*
- **§1 General Constraint:** *``Never assume or fabricate IDs … rely solely on verified API results. The same is the case for optional or default arguments."*

## Hidden Challenge: Duplicate Incident Numbers
Two incidents share external ID `INC0000004` across different tenants:

| Internal ID | Org | Description | Status | Assignee |
|---|---|---|---|---|
| `INC_004` | TechCorp | Network connectivity issues | **new** | Elena Petrov |
| `INC_011` | Acme Corp | VPN connection failure | **resolved** | **Kenji Tanaka** ✓ |
\medskip
`find_incident_by_number("INC0000004")` returns `INC_004` (first DB hit). Recovery requires a follow-up: `list_incidents(number="INC0000004", status="resolved", assigned_to="USER_009")` → `INC_011`.

## Gold Trajectory
1. `get_user_using_name("Kenji", "Tanaka")` → `USER_009`
2. `find_incident_by_number("INC0000004")` → `INC_004` → **detect mismatch** (wrong status, description, assignee)
3. `list_incidents(number=..., status="resolved", assigned_to="USER_009")` → `INC_011` ✓
4. `find_incident_knowledge_links("INC_011")` → no existing links
5. `create_knowledge_article(..., state=`\textbf{``draft"}`, visibility="internal", owner_id="USER_009")`
6. `link_knowledge_to_incident("INC_011", "KB_006", used_as="resolution")`

## Agent Behavior
The agent called `find_incident_by_number`, received `INC_004`, and accepted it without validation. It never called `list_incidents` to explore the difference. It then created the KB article with `state="published"` (the tool default) and linked it to `INC_004`.

## Failure Analysis

**Failure 1 — Wrong incident.** `INC_004` contradicted the task on three observable signals: wrong status (`new` vs. *resolved*), wrong description, and wrong assignee. The agent treated number-match as identity-confirmation and never cross-validated. Verifier checks `incident_id = "INC_011"` in the link table → **fail**.

**Failure 2 — Wrong KB state.** The tool's default is `state="published"`. Both §7 and the user's verb ("*drafts*") mandate `state="draft"`. §1 explicitly prohibits accepting defaults without policy verification. The agent applied the default silently. Verifier checks `state = "draft"` → **fail**.

## Summary

| | Expected | Agent | Impact |
|---|---|---|---|
| Incident ID | `INC_011` | `INC_004` | KB link verifier fails |
| KB state | `draft` | `published` | New KB verifier fails |
| Disambiguation step | `list_incidents(...)` called | Never called | Root cause of wrong incident |

\medskip

Both failures share the same pattern: **accepting the first plausible result without cross-validating against task context or policy constraints.**