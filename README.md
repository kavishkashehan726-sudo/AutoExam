# AutoExam LK

AI-assisted model exam papers and marking schemes for Sri Lankan examinations, starting with
the Grade 5 Scholarship Examination (English medium, mathematics).

- Requirements: `docs/SRS.md` · Decisions: `docs/DECISIONS.md` · Diary: `docs/DIARY.md`
- Deploying to the VPS: `docs/DEPLOY.md`
- Rules for contributors (and Claude): `CLAUDE.md`

## Local development

```bash
cp .env.example .env        # fill in GEMINI_API_KEY and LLM_MODEL
docker compose up --build
```

- Frontend: http://localhost:3000
- API: http://localhost:8000/api/health (docs at http://localhost:8000/docs)

Without Docker, run Postgres 17 + pgvector and Redis yourself, then:

```bash
cd backend && uv venv -p 3.13 .venv && uv pip install -p .venv -e ".[dev]"
.venv/bin/alembic upgrade head && .venv/bin/uvicorn app.main:app --reload
.venv/bin/python -m app.worker          # in another terminal
cd frontend && npm install && npm run dev
```

## Checks

```bash
cd backend && .venv/bin/ruff check . && .venv/bin/ruff format --check . && .venv/bin/pytest
cd frontend && npm run lint && npm run format:check && npm run typecheck
```
