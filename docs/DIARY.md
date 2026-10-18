# Diary

Newest entry at the top.

## 2026-10-18 — Kickoff and project skeleton
**Done:** Asked the kickoff questions and recorded the answers. Added the monorepo skeleton:
FastAPI backend (config, health endpoint, LLM provider registry, RQ worker, Alembic with a
pgvector migration, tests), Next.js 16 frontend (TypeScript strict, ESLint + Prettier),
Docker Compose for development, PM2 `ecosystem.config.js` and `docs/DEPLOY.md` for the VPS,
`.env.example`, and a CI workflow.
**Decisions:** See the kickoff table in DECISIONS.md (Gemini, RQ, PM2 on OVH Debian, MCQ +
structured questions, download-only MVP, published marking schemes).
**Problems:** Docker Hub rate-limited the cloud dev box, so `docker compose up` was not run
end to end; the migration, API and worker were tested against native Postgres 16 + pgvector
and Redis instead. The full SRS is not in the repo yet. Q19 (business model) needs confirming.
**Next:** Design the question-bank data model (grade, subject, medium, unit, competency,
difficulty, review status, traceability fields) and its migration.
