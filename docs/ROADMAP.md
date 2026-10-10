# Roadmap

Each milestone ends with something that works. Write the code yourself first, then ask Claude to review it. You'll learn much more than by having it generated.

## Milestone 1: Working MVP ✅

- [x] FastAPI backend with `/health`, `/documents`, `/chat`
- [x] Character-based chunking with overlap (`services/chunking.py`)
- [x] In-memory keyword search (`services/store.py`)
- [x] Prompt that forces cited answers (`services/llm.py`)
- [x] React UI with upload, chat, and expandable sources

**Try this:** read every file in `backend/app/`. Run it, upload a document, ask questions, and watch the terminal logs. Then ask a question using *different words* than the document uses. Keyword search will miss it. That failure is the reason for Milestone 2.

## Milestone 2: Embeddings + pgvector

- [ ] Start Postgres with `docker compose up -d`
- [ ] Learn what an embedding is; embed each chunk and each question
- [ ] Store vectors in Postgres with the pgvector extension
- [ ] Replace keyword search with cosine-similarity search
- [ ] Add PDF uploads (`pypdf`)
- [ ] Improve chunking: split on paragraphs and sentences
- [ ] Data survives a restart

**Concepts:** vector similarity, indexes (HNSW), SQL migrations.

## Milestone 3: Streaming + chat history

- [ ] Stream answers token by token (server-sent events)
- [ ] Keep conversation history so follow-up questions work
- [ ] Delete documents

## Milestone 4: Evaluation

- [ ] Write 20 question/expected-answer pairs about a test document
- [ ] Script that scores retrieval (was the right chunk found?) and answers
- [ ] Use it to compare chunk sizes and `top_k` values; record the results

**Why:** this is what separates AI engineering from demos. You can't improve what you don't measure.

## Milestone 5: Deploy to AWS

- [ ] Set a billing alarm and a monthly budget **first**
- [ ] Dockerfile for the backend
- [ ] Uploads go to **S3**; database moves to **RDS for PostgreSQL**
- [ ] API key moves to **Secrets Manager**; switch the LLM call to **Amazon Bedrock**
- [ ] Run the backend on **ECS Fargate** behind an **Application Load Balancer**
- [ ] Serve the frontend from **S3 + CloudFront**
- [ ] Define it all with **Terraform** so it can be destroyed and rebuilt; keep state in an S3 backend
- [ ] Draw the architecture: VPC, public/private subnets, security groups

**Exam link:** almost every service here is core Solutions Architect material. Write down *why* you chose each one.

## Milestone 6: Users + production polish

- [ ] Sign-up and login with **Cognito**; each user sees only their documents
- [ ] Logs, metrics, and alarms in **CloudWatch**
- [ ] Rate limiting and per-user cost tracking
- [ ] GitHub Actions: run tests on every push; `terraform plan` on pull requests and `apply` on merge, using OIDC instead of stored AWS keys

## Milestone 7: Kubernetes

- [ ] Run Paper Trail on a local cluster with kind
- [ ] Settings in a ConfigMap, the API key in a Secret
- [ ] Postgres with a PersistentVolumeClaim
- [ ] Expose the app through an Ingress; restrict traffic with a NetworkPolicy
- [ ] Package it as a Helm chart
- [ ] Deploy to **Amazon EKS**, with the cluster defined in Terraform

**Exam link:** this milestone is your CKA lab. Do it with `kubectl` from the terminal, not a GUI.
