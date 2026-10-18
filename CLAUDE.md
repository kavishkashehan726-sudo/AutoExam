# CLAUDE.md — AutoExam LK

This file is the project's memory. Claude Code reads it at the start of every session.
Keep it up to date: when a decision changes, update this file in the same commit.

---

## 1. Project summary

**AutoExam LK** is an AI-powered system that generates model exam papers and marking
schemes for Sri Lankan examinations, following the NIE syllabus and Department of
Examinations standards, using Retrieval-Augmented Generation (RAG).

- **MVP:** Grade 5 Scholarship Examination, English medium, text-only mathematics questions.
- **Phase 2:** diagram/IQ-type questions, more Grade 5 content.
- **Future:** Grades 6–13, more subjects, Sinhala/Tamil medium.
- **Users:** Students/Parents, Teachers/Tutors, System Administrators.

The full requirements are in `docs/SRS.md`. Read it before starting any feature.

---

## 2. Working rules (follow these every session)

### 2.1 Ask before you build
- Before starting the project, and before starting any new major feature, **ask me every
  open question first**. Do not write code until I have answered them.
- Group questions in one message, numbered, with your recommended answer for each.
- If something is unclear mid-task, stop and ask rather than guessing.
- Record every answer in `docs/DECISIONS.md` (see 2.3).

### 2.2 Project diary
- Maintain `docs/DIARY.md` for the whole project.
- Add an entry at the end of **every** working session, newest at the top:

  ```
  ## YYYY-MM-DD — <short title>
  **Done:** what was built or changed
  **Decisions:** anything decided (also copy to DECISIONS.md)
  **Problems:** bugs, blockers, things that didn't work
  **Next:** what to do next session
  ```
- Commit the diary with the session's work.

### 2.3 Memory files (inside the project folder)
- `CLAUDE.md` (this file) — rules, stack, architecture, conventions. Keep it short and current.
- `docs/DECISIONS.md` — every decision with date and reason (one line each is fine).
- `docs/DIARY.md` — session log (2.2).
- At the start of each session, read `CLAUDE.md`, the latest 3 diary entries, and
  `docs/DECISIONS.md` before doing anything else.

### 2.4 Git and GitHub
- GitHub account: `github.com/kavishkashehan726-sudo`
- Repository: `github.com/kavishkashehan726-sudo/AutoExam` (public, MIT, until Shehan says otherwise).
- Branches: `main` (always deployable), `dev` (integration), feature branches `feat/<name>`,
  fixes `fix/<name>`. Merge into `dev` via pull request; `dev` → `main` for releases.
- Commit messages: Conventional Commits — `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`.
- Commit small and often. Push at the end of every session.
- **Never commit secrets.** `.env` files are in `.gitignore`; keep `.env.example` updated
  with every variable (no real values).

---

## 3. Tech stack

| Layer | Choice |
|---|---|
| Frontend | Next.js (React), TypeScript |
| Backend | Python, FastAPI |
| Database | PostgreSQL with `pgvector` (relational data + vector search in one DB) |
| Migrations | Alembic |
| Background jobs | RQ with Redis for batch question generation |
| LLM | Google Gemini API behind a pluggable provider layer (`backend/app/llm/`) — model names come from config, never hard-coded |
| Embeddings | Gemini embeddings through the same provider layer, stored in pgvector |
| Export | python-docx (Word), WeasyPrint or ReportLab (PDF) |
| Dev environment | Docker + Docker Compose |
| Production | OVH VPS (Debian, 8 GB), processes managed by PM2 |
| Versions | Python 3.13, Node.js 24 LTS, PostgreSQL 17 + pgvector, Redis 8 — same in dev and prod |

---

## 4. Environments

### 4.1 Development — Docker
- Everything runs with `docker compose up`: `db` (Postgres + pgvector), `redis`,
  `backend` (FastAPI with reload), `worker`, `frontend` (Next.js dev server).
- Use the `pgvector/pgvector` Postgres image so the extension is available.
- Source code is mounted as volumes for hot reload.
- Config comes from `.env`; document every variable in `.env.example`.

### 4.2 Production — VPS with PM2
- PM2 manages the app processes via `ecosystem.config.js`:
  - `frontend` — `next start`
  - `backend` — `uvicorn` (or `gunicorn` with uvicorn workers) run from the Python virtualenv
    (set `interpreter` to the venv's python, or use the venv's `uvicorn` as the script)
  - `worker` — the job-queue worker
- PostgreSQL and Redis run as native system services on the VPS (no Docker in production).
- Nginx as reverse proxy with HTTPS (Let's Encrypt).
- Keep a `docs/DEPLOY.md` with exact step-by-step deploy and rollback instructions.
- Keep dev and prod the same in Postgres version, Python version and Node version.

---

## 5. Architecture principles

1. **Question bank first.** Generate questions offline → validate → teacher review →
   store in the bank → assemble papers from the bank. Live generation is a secondary feature,
   and its questions are marked `unreviewed`.
2. **Validate every generated question:**
   - answer verified by code for numeric questions (the LLM returns a `calc` expression),
   - similarity check against past papers (reject near-copies),
   - syllabus and number-range checks.
3. **Traceability:** every question stores model, prompt version, retrieved example IDs,
   validation results and review status.
4. **Structured LLM output:** always request JSON and validate it with Pydantic.
5. **Prompts are versioned files** in `backend/prompts/`, not strings buried in code.
6. **Schema built for expansion:** grade, subject, medium, unit, competency level are data,
   not hard-coded, so Grades 6–13 can be added without schema redesign.
7. **Never show past-paper questions verbatim to users.**
8. **Children's data:** students are minors — parent-managed accounts, collect the minimum data.

---

## 6. Code conventions

- Python: type hints everywhere, `ruff` for lint/format, `pytest` for tests.
- TypeScript: strict mode, ESLint + Prettier.
- Tests required for: answer validation, paper assembly, marking scheme generation, API endpoints.
- Run tests before every commit; don't commit failing tests.
- Keep functions small; no business logic inside route handlers.

---

## 7. Open questions

The kickoff questions were answered on 2026-10-18; see `docs/DECISIONS.md`.
Still open: business model details (DECISIONS.md #19), marks per question (#6), LLM budget (#14),
domain name (#21).

---

## 8. Project structure

```
AutoExam/
├── CLAUDE.md
├── docker-compose.yml
├── ecosystem.config.js        # PM2 (production)
├── .env.example
├── docs/
│   ├── SRS.md
│   ├── SRS_REVIEW.md
│   ├── DIARY.md
│   ├── DECISIONS.md
│   └── DEPLOY.md
├── .github/workflows/ci.yml   # lint, tests, migrations, frontend build
├── backend/
│   ├── app/                   # FastAPI app (api, core, db, llm, worker; later models, services, validation)
│   ├── prompts/
│   ├── alembic/
│   └── tests/
└── frontend/
    └── (Next.js app)
```
