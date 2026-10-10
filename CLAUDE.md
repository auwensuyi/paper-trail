# Notes for Claude

This is a **learning project**. The owner is new to AI engineering and is learning Python (then Go and Rust) and AWS, aiming for the AWS Solutions Architect Associate, Terraform Associate, AWS Data Engineer Associate, CKA, and Terraform Professional exams, and learning Linux along the way.

## How to help

- Prefer explaining and reviewing over writing large amounts of code. When asked to build a feature, outline the approach and the concepts involved first, and offer to let the owner write it.
- Keep changes small and focused on the current milestone in `docs/ROADMAP.md`. Tick off checklist items as they are completed.
- When a change involves AWS, Terraform, or Kubernetes, mention which exam topic it relates to.
- Infrastructure is defined with Terraform (not CDK or click-ops).
- Never commit secrets. Real keys live only in `backend/.env` (gitignored).

## Commands

- Backend: `cd backend && uvicorn app.main:app --reload`
- Backend tests: `cd backend && pytest` (must pass before committing)
- Frontend: `cd frontend && npm run dev`; type-check and build with `npm run build`

## Conventions

- HTTP endpoints go in `backend/app/routers/`; logic goes in `backend/app/services/`.
- All frontend calls to the backend go through `frontend/src/api.ts`.
- Add or update a test for every backend change.
