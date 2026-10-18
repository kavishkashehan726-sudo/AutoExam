# Decisions

One line per decision: date, decision, reason. Newest at the bottom of each section.

## Kickoff question round (answered by Shehan, 2026-10-18)

| # | Topic | Decision |
|---|---|---|
| 1 | Repository | Use the existing `kavishkashehan726-sudo/AutoExam` repo, not a new `autoexam-lk`. |
| 2 | Visibility / licence | Repo stays **public** with the MIT licence until Shehan says otherwise. |
| 3 | Layout | Monorepo: `backend/`, `frontend/`, `docs/` at the root. |
| 4 | Branches | `main` (deployable), `dev` (integration), feature PRs into `dev`, `dev` → `main` for releases. |
| 5 | SRS | Full SRS not added yet; it will be expanded later. `docs/SRS.md` holds the agreed MVP scope until then; the review is in `docs/SRS_REVIEW.md`. |
| 6 | Exam format | Support **both** MCQ and structured (short-answer) questions. Marks per question still to be confirmed. |
| 7 | Student mode | MVP **generates papers and marking schemes for download** only; no online answering or auto-marking. |
| 8 | Marking schemes | Follow the **published** Department of Examinations marking schemes. |
| 9 | Difficulty | Easy = 1 step, Medium = 2 steps, Hard = 3+ steps, plus number-range limits per level; calibrate later. |
| 10 | UI language | English only for the MVP. |
| 11 | Source data | The admin team uploads sample papers, textbooks and other material through the app. The system uses them by **retrieval (RAG)**, not by training a model. |
| 12 | Data rights | Source material is stored inside the software for retrieval only; past-paper questions are never shown verbatim. |
| 13 | Reviewers | Shehan is the only reviewer of generated questions for now. |
| 14 | LLM | **Google Gemini API** behind the pluggable provider layer; model name set in config. Budget not set. |
| 15 | Embeddings | Gemini embeddings through the same provider layer; model name in config. |
| 16 | Job queue | **RQ** with Redis for now. |
| 17 | Versions | Current LTS/stable: **Python 3.13, Node.js 24 LTS, PostgreSQL 17 + pgvector, Redis 8** (same versions in dev and prod). |
| 18 | Auth | Email + password for teachers/parents/admins; student profiles managed by the parent account. |
| 19 | Business model | Free for the MVP, no payment gateway. Shehan's answer was "for the ease of admin"; read as: limits are admin-configurable. **To confirm.** |
| 20 | Production | OVH VPS, Debian, 8 GB RAM. **PM2** in production (Postgres and Redis as native services); Docker only for local development. |
| 21 | Domain | Decide later. |
| 22 | MVP date | No target date. |

## Later decisions

- 2026-10-18: First PR (project skeleton) targets `dev`. Reason: decision 4.
- 2026-10-18: Production installs Python 3.13 with `uv` and Postgres 17 from the PGDG apt repo, so versions match dev on any Debian release. Reason: decision 17.
