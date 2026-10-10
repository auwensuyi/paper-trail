// All calls to the backend live here, so components stay simple.

export type Doc = { id: string; filename: string; chunks: number };
export type Source = { number: number; filename: string; part: number; text: string };
export type ChatResponse = { answer: string; sources: Source[] };

async function handle<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail ?? `Request failed (${res.status})`);
  }
  return res.json();
}

export async function listDocuments(): Promise<Doc[]> {
  return handle(await fetch("/api/documents"));
}

export async function uploadDocument(file: File): Promise<Doc> {
  const form = new FormData();
  form.append("file", file);
  return handle(await fetch("/api/documents", { method: "POST", body: form }));
}

export async function ask(question: string): Promise<ChatResponse> {
  return handle(
    await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    })
  );
}
