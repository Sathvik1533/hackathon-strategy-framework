document.addEventListener("DOMContentLoaded", () => {
  const ingestForm = document.getElementById("ingestForm");
  const ingestBtn = document.getElementById("ingestBtn");
  const ingestNotice = document.getElementById("ingestNotice");

  const searchForm = document.getElementById("searchForm");
  const searchBtn = document.getElementById("searchBtn");
  const searchQuery = document.getElementById("searchQuery");
  const topK = document.getElementById("topK");
  const useRerank = document.getElementById("useRerank");
  const searchResultsList = document.getElementById("searchResultsList");
  const resultCount = document.getElementById("resultCount");

  // Ingest chunk submission
  ingestForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    ingestBtn.disabled = true;
    ingestBtn.textContent = "Indexing Vector...";

    const payload = {
      title: document.getElementById("chunkTitle").value,
      source: document.getElementById("chunkSource").value,
      content: document.getElementById("chunkContent").value
    };

    try {
      const res = await fetch("/api/v1/documents/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      ingestNotice.style.display = "block";
      ingestNotice.textContent = `✔ Successfully indexed chunk #${data.data.id} ("${data.data.title}")`;
      ingestForm.reset();
      document.getElementById("chunkSource").value = "manual";
    } catch (err) {
      ingestNotice.style.display = "block";
      ingestNotice.style.color = "var(--accent-rose)";
      ingestNotice.textContent = `Error indexing: ${err.message}`;
    } finally {
      ingestBtn.disabled = false;
      ingestBtn.textContent = "Index Chunk into pgvector";
    }
  });

  // Hybrid search execution
  searchForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    searchBtn.disabled = true;
    searchBtn.textContent = "Searching Vectors & Reranking...";

    const payload = {
      query: searchQuery.value,
      top_k: parseInt(topK.value, 10) || 3,
      use_rerank: useRerank.checked
    };

    try {
      const res = await fetch("/api/v1/documents/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const json = await res.json();
      const results = json.data || [];
      resultCount.textContent = results.length;
      renderResults(results);
    } catch (err) {
      searchResultsList.innerHTML = `<div style="color: var(--accent-rose); font-size: 0.85rem;">Search error: ${err.message}</div>`;
    } finally {
      searchBtn.disabled = false;
      searchBtn.textContent = "Execute Hybrid Search";
    }
  });

  function renderResults(items) {
    if (!items.length) {
      searchResultsList.innerHTML = `<div style="color: var(--text-muted); font-size: 0.85rem;">No matching documents found.</div>`;
      return;
    }

    searchResultsList.innerHTML = items.map(item => `
      <div class="doc-item">
        <div class="doc-header">
          <span class="doc-title">#${item.rank} ${escapeHtml(item.title || 'Untitled Chunk')}</span>
          <span class="doc-badge">RRF Score: ${item.score}</span>
        </div>
        <p class="doc-snippet">${escapeHtml(item.content)}</p>
        <div style="margin-top: 6px; font-size: 0.75rem; color: var(--text-muted); font-family: var(--font-mono);">
          Source: ${escapeHtml(item.source || 'unknown')}
        </div>
      </div>
    `).join("");
  }

  function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }
});
