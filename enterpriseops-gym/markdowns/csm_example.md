# Case Study: CSM — ``KB Remediation and Case Setup" *(claude-sonnet-4-6, 4/5 verifiers passed)*

## Task (condensed)
An agent must link a relevant knowledge article to case CS-0000002 and set up the assignee. The case involves a NetApp FAS2750 product issue. Joanne Simpson will handle the case under a new "Case Management" support group.

**Relevant policy (excerpts):**
- **KB Linking:** *``Articles must be in state = published … when the knowledge is found through automated search it should be linked as `suggested`."*
- **Case State:** *``Once case linked to a knowledge article marked the state = `pending`."*
- **Assignment:** *``assigned\\_to must … be member of assignment\\_group\\_id."*

## Hidden Challenges
Three compounding complexities are not stated in the user prompt and needs to be inferred from system policy:

- **KB state remediation:** KB-0000197 is `retired`; must be updated to `published` before linking.
- **Group creation:** ``Case Management" does not exist; must be created with `type="support"`.
- **Lifecycle transition:** KB linkage unconditionally requires `update_case(state="pending")`.

## Gold Trajectory
1. `search_cases(number="CS-0000002")` → `case_id=2`, `product_id=130`
2. `retrieve_knowledge(product_id=130)` → `knowledge_id=197`, `state="retired"`
3. `update_knowledge(knowledge_id=197, state="published")` → KB now usable
4. `link_case_knowledge(case_id=2, knowledge_id=197, used_as="suggested")` → link created
5. `find_user(name="Joanne Simpson")` → `user_id=4`, `role="manager"`, `active=1`
6. `find_user_group(name="Case Management")` → `{}` (absent)
7. `add_new_user_group(name="Case Management", type="support", active=true)` → `group_id=81`
8. `add_new_group_member(group_id=81, user_id=4)` → membership created
9. `update_case(case_id=2, assignment_group_id=81, assigned_to=4,` **`state="pending"`**`)` → case closed

## Agent Behavior
The agent executed a near-perfect 5-turn trajectory. In Turn 1 it issued three parallel lookups (case, user, group). In Turn 2–3 it correctly pivoted from a text-based KB search (which returned wrong product variants) to a `product_id=130` filter, finding the retired KB-0000197. In Turn 4 it published the KB and created the group in parallel. In Turn 5 it added Joanne to the group, linked the KB article, and updated the case assignment — but omitted `state="pending"` from the `update_case` call.

## Failure Analysis

**Single failure — missing state transition.** The agent's `update_case` call set `case_id`, `assignment_group_id`, and `assigned_to` correctly, but did not include `state="pending"`. The case remained in `state="new"`. The policy rule is explicit and unconditional: any KB linkage event requires a transition to `pending`. The agent's Turn 5 reasoning focused on "update the case assignment" without revisiting the lifecycle rules — a classic lifecycle-truncation failure (Pattern \#4). The `state` parameter and the `pending` enum value are both present in the tool schema; no tool error or ambiguity blocked the correct call.

## Summary

| | Expected | Agent | Impact |
|---|---|---|---|
| `update_case.state` | `"pending"` | omitted (`"new"`) | V5 fail |
| KB remediation | `update_knowledge(state="published")` | correct | V1 pass |
| KB linkage | `used_as="suggested"` | correct | V2 pass |
| Group creation | `type="support"` | correct | V3 pass |
| Membership check | `add_new_group_member` before assignment | correct | V4 pass |

\medskip

The failure isolates to a single omitted parameter on an otherwise correct trajectory: **the agent completed the assignment but did not apply the KB-linkage-triggered lifecycle rule.**
