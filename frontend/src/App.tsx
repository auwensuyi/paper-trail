import { FormEvent, useEffect, useState } from "react";
import { ask, ChatResponse, Doc, listDocuments, uploadDocument } from "./api";

type Turn = { question: string; response?: ChatResponse; error?: string };

export default function App() {
  const [docs, setDocs] = useState<Doc[]>([]);
  const [turns, setTurns] = useState<Turn[]>([]);
  const [question, setQuestion] = useState("");
  const [busy, setBusy] = useState(false);
  const [uploadError, setUploadError] = useState("");

  useEffect(() => {
    listDocuments().then(setDocs).catch(() => setDocs([]));
  }, []);

  async function onUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploadError("");
    try {
      const doc = await uploadDocument(file);
      setDocs((d) => [...d, doc]);
    } catch (err) {
      setUploadError((err as Error).message);
    }
    e.target.value = "";
  }

  async function onAsk(e: FormEvent) {
    e.preventDefault();
    const q = question.trim();
    if (!q || busy) return;
    setQuestion("");
    setBusy(true);
    setTurns((t) => [...t, { question: q }]);
    try {
      const response = await ask(q);
      setTurns((t) => t.map((turn, i) => (i === t.length - 1 ? { ...turn, response } : turn)));
    } catch (err) {
      const error = (err as Error).message;
      setTurns((t) => t.map((turn, i) => (i === t.length - 1 ? { ...turn, error } : turn)));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="layout">
      <aside>
        <h1>Paper Trail</h1>
        <p className="muted">Upload .txt or .md files, then ask questions.</p>
        <label className="upload">
          Upload a document
          <input type="file" accept=".txt,.md" onChange={onUpload} />
        </label>
        {uploadError && <p className="error">{uploadError}</p>}
        <ul className="docs">
          {docs.map((d) => (
            <li key={d.id}>
              {d.filename} <span className="muted">· {d.chunks} chunks</span>
            </li>
          ))}
        </ul>
      </aside>

      <main>
        <div className="turns">
          {turns.length === 0 && <p className="muted">Ask something about your documents.</p>}
          {turns.map((t, i) => (
            <div key={i} className="turn">
              <p className="question">{t.question}</p>
              {t.error && <p className="error">{t.error}</p>}
              {!t.response && !t.error && <p className="muted">Thinking…</p>}
              {t.response && (
                <>
                  <p className="answer">{t.response.answer}</p>
                  {t.response.sources.length > 0 && (
                    <details>
                      <summary>Sources ({t.response.sources.length})</summary>
                      {t.response.sources.map((s) => (
                        <blockquote key={s.number}>
                          <strong>
                            [{s.number}] {s.filename}, part {s.part}
                          </strong>
                          <p>{s.text}</p>
                        </blockquote>
                      ))}
                    </details>
                  )}
                </>
              )}
            </div>
          ))}
        </div>
        <form onSubmit={onAsk}>
          <input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask a question…"
            aria-label="Question"
          />
          <button disabled={busy || !question.trim()}>Ask</button>
        </form>
      </main>
    </div>
  );
}
