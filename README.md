# Paper Trail

AI-powered document chat app: upload files and ask questions with cited answers. Built with Python, FastAPI, React, and AWS.

This is a learning project for AI engineering (RAG: retrieval-augmented generation) and the AWS Solutions Architect Associate exam. It starts simple and grows one milestone at a time.

## How it works

```
 Upload file ──► split into chunks ──► store chunks
                                            │
 Ask question ──► find relevant chunks ◄────┘
                        │
                        ▼
          send question + chunks to the LLM ──► answer with [1] [2] citations
```

## Project layout

```
paper-trail/
├── backend/                 FastAPI app (Python)
│   ├── app/
│   │   ├── main.py          creates the app, wires up routes
│   │   ├── config.py        settings from environment / .env
│   │   ├── routers/         HTTP endpoints: /health, /documents, /chat
│   │   └── services/        the real logic: chunking, storage/search, LLM calls
│   └── tests/               pytest tests
├── frontend/                React + TypeScript (Vite)
│   └── src/
│       ├── App.tsx          the whole UI
│       └── api.ts           every call to the backend
├── docs/ROADMAP.md          milestones with learning goals
└── docker-compose.yml       local Postgres + pgvector (Milestone 2)
```

## Run it locally

You need **Python 3.11+**, **Node.js 20+**, and an **Anthropic API key**.

**1. Backend** (terminal 1)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # then put your API key in .env
uvicorn app.main:app --reload
```

The API runs at http://localhost:8000. Interactive docs are at http://localhost:8000/docs.

**2. Frontend** (terminal 2)

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173, upload a `.txt` or `.md` file, and ask a question about it.

**3. Tests**

```bash
cd backend
pytest
```

## Roadmap

| # | Milestone | You learn | AWS / exam topics |
|---|-----------|-----------|-------------------|
| 1 | **Working MVP** (done) | FastAPI, React, prompts, citations | — |
| 2 | Embeddings + pgvector | Embeddings, vector search, PDF parsing | RDS for PostgreSQL |
| 3 | Streaming + chat history | Server-sent events, conversation state | — |
| 4 | Evaluation | Measuring answer quality, regression tests | — |
| 5 | Deploy to AWS | Containers, IaC, secrets | S3, ECS Fargate, ALB, RDS, Secrets Manager, Bedrock, IAM, VPC |
| 6 | Users + production polish | Auth, monitoring, cost control | Cognito, CloudWatch, CloudFront, Budgets |

Details and checklists are in [docs/ROADMAP.md](docs/ROADMAP.md).

## License

MIT. See [LICENSE](LICENSE).
