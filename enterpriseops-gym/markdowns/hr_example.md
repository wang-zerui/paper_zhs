# Case Study: HR — ``Wrap Up James Hill's Portal Access Case" *(claude-sonnet-4-5, 1/3 verifiers passed)*

## Task (condensed)
Karen Watkins (admin) is told that James Hill's 'Access issue with HR portal account' has been resolved. She must wrap up his case and add a follow-up technical issue survey using the first task to gather his feedback.

\medskip

**Relevant policy (condensed):**
- **§3.2 Closure Constraint:** *``A case cannot move to a closed status until all mandatory tasks are inactive (`active=false`)."*
- **§3.3 Lifecycle:** *``Valid transition: `awaiting_approval` → `closed_complete` (if approved)."*
- **§3.4 Approvals:** *``The approval record request\\_status transitions: `requested` → `approved` / `rejected`."*
- **§1 General Constraint:** *``Do not ask for any information or confirmation from the user. Never assume or fabricate IDs."*

## Hidden Challenge: Two Simultaneous Closure Prerequisites

"Wrap up" maps to three ordered system operations — none stated literally in the prompt:

| Step | Action | Policy Source |
|---|---|---|
| 1 | Deactivate all active tasks (`active=false`) | §3.2 — prerequisite to closure |
| 2 | Set `status='closed_complete'` | §3.3 — valid closure status for resolved cases |
| 3 | Set `request_status='approved'` | §3.4 — clears the pending approval gate |

\medskip
The case seed state has `status='awaiting_approval'` and `request_status='requested'` with two active tasks (ids 6 and 7). Steps 1–3 must all complete; failing any leaves the verifier returning COUNT=0.

## Gold Trajectory
1. `get_user_using_name("James", "Hill")` → `user_id=8`
2. `list_hr_cases(opened_for="James Hill")` → `hr_case_id=3`, `status='awaiting_approval'`, `request_status='requested'`
3. `list_hr_case_tasks(parent_case="3")` → Tasks 6 (`url`, active=True) and 7 (`checklist`, active=True)
4. `list_surveys(question_1="technical issue")` → `survey_id=4`
5. `update_hr_case_task(hr_case_task_id="6", active=false)` → Task 6 deactivated
6. `update_hr_case_task(hr_case_task_id="7", active=false)` → Task 7 deactivated
7. `update_hr_case(hr_case_id="3",` `status="closed_complete", request_status="approved")` → Case closed and approved
8. `create_survey_instance(survey_id=4, case_task_id=6, assigned_to=8)` → Survey instance created ✓

## Agent Behavior
The agent completed all four lookup steps correctly and created the survey instance with the right parameters (V3 passes). It then called `update_hr_case_task` on task 6 — but passed `task_type="survey"` and a new `short_description` instead of `active=false`. It never called `update_hr_case`. The agent declared completion after six turns, summarising the survey as something James Hill would complete in the future.

## Failure Analysis

**Failure 1 — Wrong parameters on `update_hr_case_task`.** The agent read ``add the appropriate follow-up technical issue survey \textit{using the first task}" as a directive to convert task 6 into a survey-type task. It therefore called `update_hr_case_task(task_type="survey", short_description=...)` rather than  `update_hr_case_task(active=false)`. The §3.2 Closure Constraint — visible in the system prompt and signalled by `update_hr_case_task`'s presence in the tool set — requires deactivation, not type conversion. Task 6 remained `active=true`; the verifier checks `active=false` → **fail**.

\medskip

**Failure 2 — `update_hr_case` never called.** The agent reframed ``wrap up his case" as a future activity for James Hill (completing the survey) rather than an immediate system closure. Its final summary reads: ``James can complete the survey as part of the case wrap-up process." The agent stopped at survey creation and declared success. `update_hr_case` was present in the tool set (a planning signal), §3.3 specifies `awaiting_approval → closed_complete` as the valid transition, and `request_status='requested'` was visible in the `list_hr_cases` response. The case remained in `awaiting_approval`; the verifier checks `status='closed_complete' AND request_status='approved'` → **fail**.

## Summary

| | Expected | Agent | Impact |
|---|---|---|---|
| Task 6 `active` | `false` | wrong params passed | V1 fails |
| Case `status` | `closed_complete` | tool never called | V2 fails |
| Case `request_status` | `approved` | tool never called | V2 fails |
| Survey instance | correct params | correct | V3 passes |

\medskip

Both failures stem from the same root: **natural-language business verbs (``wrap up", ``using the first task") misread as content directives rather than lifecycle commands**, causing the agent to act on a plausible surface reading while ignoring the policy-defined closure sequence.
