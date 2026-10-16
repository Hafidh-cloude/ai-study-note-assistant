
import { useEffect, useState } from "react";
import {
  getNotes,
  createNote,
  updateNote,
  deleteNote,
  askNote,
  summarizeNote,
} from "./services/api";
import "./App.css";

function normalizeNote(row) {
  if (Array.isArray(row)) {
    return {
      id: row[0],
      title: row[1],
      content: row[2],
      createdAt: row[3],
      updatedAt: row[4],
    };
  }

  return {
    id: row.id ?? row.note_id,
    title: row.title ?? "",
    content: row.content ?? "",
    createdAt: row.created_at,
    updatedAt: row.updated_at,
  };
}

function normalizeNotes(data) {
  if (!Array.isArray(data)) {
    throw new Error("Format respons GET /notes tidak sesuai.");
  }

  const rows =
    data.length > 0 &&
    !Array.isArray(data[0]) &&
    (typeof data[0] !== "object" || data[0] === null)
      ? [data]
      : data;

  return rows.map(normalizeNote);
}

function App() {
  const [notes, setNotes] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [isNewNote, setIsNewNote] = useState(false);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [mode, setMode] = useState("ask");

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [aiLoading, setAiLoading] = useState(false);
  const [apiError, setApiError] = useState("");

  const selectedNote = notes.find(
    (note) => String(note.id) === String(selectedId),
  );

  const hasUnsavedChanges =
    isNewNote ||
    (selectedNote && content !== selectedNote.content);

  useEffect(() => {
    let cancelled = false;

    async function loadInitialNotes() {
      setLoading(true);

      try {
        const data = await getNotes();
        const loadedNotes = normalizeNotes(data);

        if (cancelled) return;

        setNotes(loadedNotes);

        if (loadedNotes.length > 0) {
          const firstNote = loadedNotes[0];

          setSelectedId(firstNote.id);
          setIsNewNote(false);
          setTitle(firstNote.title);
          setContent(firstNote.content);
        }
      } catch (error) {
        if (!cancelled) {
          setApiError(`Gagal memuat catatan: ${error.message}`);
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    loadInitialNotes();

    return () => {
      cancelled = true;
    };
  }, []);

  async function refreshNotes() {
    const data = await getNotes();
    const refreshedNotes = normalizeNotes(data);
    setNotes(refreshedNotes);
    return refreshedNotes;
  }

  function selectNote(note) {
    setSelectedId(note.id);
    setIsNewNote(false);
    setTitle(note.title);
    setContent(note.content);
    setMessages([]);
    setQuestion("");
    setApiError("");
  }

  function createNoteDraft() {
    setSelectedId(null);
    setIsNewNote(true);
    setTitle("");
    setContent("");
    setMessages([]);
    setQuestion("");
    setApiError("");
  }

  async function saveNote() {
    if (!title.trim()) {
      setApiError("Judul catatan tidak boleh kosong.");
      return;
    }

    setSaving(true);
    setApiError("");

    try {
      if (isNewNote) {
        await createNote(title.trim(), content);

        const refreshedNotes = await refreshNotes();
        const matches = refreshedNotes.filter(
          (note) =>
            note.title === title.trim() &&
            note.content === content,
        );

        const savedNote = matches[matches.length - 1];

        if (savedNote) {
          selectNote(savedNote);
        } else {
          setApiError(
            "Catatan terkirim, tetapi tidak ditemukan dalam daftar. Periksa respons GET /notes.",
          );
        }
      } else {
        if (selectedId == null) {
          throw new Error("ID catatan tidak tersedia.");
        }

        await updateNote(selectedId, content);

        const refreshedNotes = await refreshNotes();
        const updatedNote = refreshedNotes.find(
          (note) => String(note.id) === String(selectedId),
        );

        if (updatedNote) {
          selectNote(updatedNote);
        } else {
          setApiError(
            "Catatan tidak ditemukan setelah diperbarui.",
          );
        }
      }
    } catch (error) {
      setApiError(`Gagal menyimpan catatan: ${error.message}`);
    } finally {
      setSaving(false);
    }
  }

  async function removeNote() {
    if (isNewNote || selectedId == null || !selectedNote) {
      return;
    }

    if (
      !window.confirm(
        `Hapus "${selectedNote.title}" secara permanen?`,
      )
    ) {
      return;
    }

    setSaving(true);
    setApiError("");

    try {
      await deleteNote(selectedId);
      const refreshedNotes = await refreshNotes();

      if (refreshedNotes.length > 0) {
        selectNote(refreshedNotes[0]);
      } else {
        createNoteDraft();
      }
    } catch (error) {
      setApiError(`Gagal menghapus catatan: ${error.message}`);
    } finally {
      setSaving(false);
    }
  }

  async function handleAIAction(event) {
    event.preventDefault();

    if (isNewNote || selectedId == null || !selectedNote) {
      setApiError(
        "Simpan catatan terlebih dahulu sebelum menggunakan AI.",
      );
      return;
    }

    if (hasUnsavedChanges) {
      setApiError(
        "Simpan perubahan isi catatan terlebih dahulu agar AI menggunakan konten terbaru.",
      );
      return;
    }

    if (!content.trim()) {
      setApiError("Isi catatan masih kosong.");
      return;
    }

    if (mode === "ask" && !question.trim()) {
      setApiError("Masukkan pertanyaan terlebih dahulu.");
      return;
    }

    setAiLoading(true);
    setApiError("");

    try {
      let result;
      let responseText;
      let messageText;

      if (mode === "summary") {
        result = await summarizeNote(selectedId);
        responseText = result?.summary;
        messageText = "Ringkasan catatan";
      } else {
        const submittedQuestion = question.trim();

        result = await askNote(selectedId, submittedQuestion);
        responseText = result?.answer;
        messageText = submittedQuestion;
      }

      if (typeof responseText !== "string" || !responseText.trim()) {
        throw new Error(
          "Respons AI tidak memiliki field summary atau answer yang valid.",
        );
      }

      setMessages((currentMessages) => [
        ...currentMessages,
        {
          id: `${Date.now()}-${currentMessages.length}`,
          type: mode,
          text: messageText,
          response: responseText,
        },
      ]);

      if (mode === "ask") setQuestion("");
    } catch (error) {
      setApiError(`Gagal memproses AI: ${error.message}`);
    } finally {
      setAiLoading(false);
    }
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">✳</div>
          <div>
            <strong>StudyNotes AI</strong>
            <span>Your learning workspace</span>
          </div>
        </div>

        <button
          className="new-note-button"
          onClick={createNoteDraft}
          disabled={saving || aiLoading}
        >
          <span>＋</span> New note
        </button>

        <p className="section-label">
          YOUR NOTES · {notes.length}
        </p>

        <div className="notes-list">
          {notes.map((note) => (
            <button
              key={note.id}
              className={`note-item ${
                !isNewNote && selectedId === note.id ? "active" : ""
              }`}
              onClick={() => selectNote(note)}
              disabled={saving || aiLoading}
            >
              <span className="note-icon">▤</span>
              <span className="note-item-text">
                <strong>{note.title || "Untitled note"}</strong>
                <small>
                  {note.content.slice(0, 38) || "Empty note"}
                </small>
              </span>
            </button>
          ))}
        </div>

        <div className="sidebar-footer">
          <div className="avatar">H</div>
          <div>
            <strong>My Workspace</strong>
            <span>Personal study space</span>
          </div>
        </div>
      </aside>

      <main className="workspace">
        <header className="topbar">
          <div className="breadcrumb">
            Workspace <span>/</span> Notes
          </div>
          <div className="demo-badge">
            <span />
            {loading ? "Connecting..." : "API mode"}
          </div>
        </header>

        {apiError && (
          <div className="api-error" role="alert">
            {apiError}
          </div>
        )}

        {loading ? (
          <div className="empty-workspace">
            <h2>Loading notes...</h2>
            <p>Mengambil catatan dari FastAPI.</p>
          </div>
        ) : (
          <div className="content-layout">
            <section className="editor-panel">
              <div className="editor-toolbar">
                <span className="document-label">
                  ▤ &nbsp; STUDY NOTE
                </span>
                <div className="editor-actions">
                  <button
                    className="button-secondary"
                    onClick={removeNote}
                    disabled={
                      saving || aiLoading || isNewNote || !selectedNote
                    }
                  >
                    Delete
                  </button>
                  <button
                    className="button-primary"
                    onClick={saveNote}
                    disabled={saving || aiLoading}
                  >
                    {saving
                      ? "Saving..."
                      : isNewNote
                        ? "Create note"
                        : "Save content"}
                  </button>
                </div>
              </div>

              <input
                className="title-input"
                value={title}
                onChange={(event) => setTitle(event.target.value)}
                placeholder="Give your note a title..."
                readOnly={!isNewNote}
              />

              <div className="editor-meta">
                <span>
                  {isNewNote
                    ? "New note · belum tersimpan"
                    : hasUnsavedChanges
                      ? "Ada perubahan yang belum disimpan"
                      : "Personal knowledge base"}
                </span>
                <span>
                  {content.trim()
                    ? content.trim().split(/\s+/).length
                    : 0}{" "}
                  words
                </span>
              </div>

              <textarea
                className="content-input"
                value={content}
                onChange={(event) => setContent(event.target.value)}
                placeholder="Start writing your study notes here..."
              />

              <div className="editor-footer">
                <span>✎ &nbsp; Edit your knowledge</span>
                <span>
                  {saving ? "Saving..." : "Remember to save changes"}
                </span>
              </div>
            </section>

            <aside className="ai-panel">
              <div className="ai-heading">
                <div className="ai-icon">✳</div>
                <div>
                  <h2>AI Assistant</h2>
                  <p>Learn smarter with your notes</p>
                </div>
              </div>

              <div className="mode-switch">
                <button
                  className={mode === "ask" ? "selected" : ""}
                  onClick={() => setMode("ask")}
                  disabled={aiLoading}
                >
                  Ask AI
                </button>
                <button
                  className={mode === "summary" ? "selected" : ""}
                  onClick={() => setMode("summary")}
                  disabled={aiLoading}
                >
                  Summarize
                </button>
              </div>

              <div className="ai-context">
                <span className="context-icon">▤</span>
                <div>
                  <strong>Current context</strong>
                  <p>{title || "Untitled note"}</p>
                </div>
                <span className="context-status">●</span>
              </div>

              <div className="ai-messages">
                {messages.length === 0 && !aiLoading ? (
                  <div className="empty-ai">
                    <div className="empty-ai-icon">✳</div>
                    <h3>
                      {mode === "ask"
                        ? "Ask your notes"
                        : "Understand faster"}
                    </h3>
                    <p>
                      {mode === "ask"
                        ? "Ask a question about this note and explore the concepts in more depth."
                        : "Turn your study notes into a concise summary with the key ideas."}
                    </p>
                  </div>
                ) : (
                  <>
                    {messages.map((message) => (
                      <div className="message" key={message.id}>
                        <span className="message-label">
                          {message.type === "summary"
                            ? "SUMMARY"
                            : "YOUR QUESTION"}
                        </span>
                        <p className="message-question">
                          {message.text}
                        </p>
                        <div className="message-answer">
                          {message.response}
                        </div>
                      </div>
                    ))}
                    {aiLoading && (
                      <div className="message">
                        <span className="message-label">AI ASSISTANT</span>
                        <p className="message-answer">
                          Sedang memproses permintaan...
                        </p>
                      </div>
                    )}
                  </>
                )}
              </div>

              <form className="ai-form" onSubmit={handleAIAction}>
                {mode === "ask" && (
                  <textarea
                    value={question}
                    onChange={(event) => setQuestion(event.target.value)}
                    placeholder="Ask anything about this note..."
                    rows={3}
                    disabled={aiLoading}
                  />
                )}

                <button
                  className="button-primary ai-submit"
                  type="submit"
                  disabled={aiLoading || saving || loading}
                >
                  {aiLoading
                    ? "Processing..."
                    : mode === "summary"
                      ? "✳ Generate summary"
                      : "Ask AI ↗"}
                </button>

                <p className="ai-disclaimer">
                  Responses are generated by your AI backend.
                </p>
              </form>
            </aside>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
