const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  const responseText = await response.text();
  let data = null;

  if (responseText) {
    try {
      data = JSON.parse(responseText);
    } catch {
      data = responseText;
    }
  }

  if (!response.ok) {
    const detail = typeof data === 'object' && data !== null ? data.detail || data.message : data;

    throw new Error(detail || `Request gagal dengan status ${response.status}`);
  }

  return data;
}

export function getNotes() {
  return request('/notes');
}

export function createNote(title, content) {
  return request('/notes', {
    method: 'POST',
    body: JSON.stringify({ title, content }),
  });
}

export function updateNote(noteId, content) {
  return request(`/notes/${noteId}`, {
    method: 'PUT',
    body: JSON.stringify({ content }),
  });
}

export function deleteNote(noteId) {
  return request(`/notes/${noteId}`, {
    method: 'DELETE',
  });
}

export function askNote(noteId, question) {
  return request(`/notes/${noteId}/ask`, {
    method: 'POST',
    body: JSON.stringify({ question }),
  });
}

export function summarizeNote(noteId) {
  return request(`/notes/${noteId}/summary`, {
    method: 'POST',
  });
}
