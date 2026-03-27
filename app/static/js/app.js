function clearResults() {
  const results = document.getElementById("results");
  results.replaceChildren();
  return results;
}

function showMessage(message) {
  const results = clearResults();
  const p = document.createElement("p");
  p.textContent = message;
  results.appendChild(p);
}

function clearFileInput() {
  const fileInput = document.getElementById("file-input");
  fileInput.value = "";
  return fileInput;
}

document.addEventListener("DOMContentLoaded", () => {
  const uploadButton = document.getElementById("upload-button");
  const searchButton = document.getElementById("search-button");
  const fileInput = document.getElementById("file-input");
  const searchInput = document.getElementById("search-input");
  const deleteButton = document.getElementById("delete-button")

  uploadButton.addEventListener("click", async () => {
    const file = fileInput.files[0];
    if (!file) {
      showMessage("Please choose a file to upload.");
      return;
    }

    const form = new FormData();
    form.append("file", file);

    showMessage("Uploading and ingesting…");
    const res = await fetch("/ingest", { method: "POST", body: form });
    const data = await res.json().catch(() => null);

    if (!res.ok) {
      showMessage(`Ingest failed: ${data?.detail ?? "Unknown error"}`);
      return;
    }

    showMessage(`Ingested: ${data.filename}`);
  });

  deleteButton.addEventListener("click", async () => {
    clearFileInput();
    clearResults();
    showMessage("File cleared");
  });

  searchButton.addEventListener("click", async () => {
    const q = searchInput.value.trim();
    if (!q) {
      showMessage("Please enter a search query.");
      return;
    }

    showMessage("Searching…");
    const res = await fetch(`/search?query=${encodeURIComponent(q)}&top_k=5`);
    const data = await res.json().catch(() => null);

    if (!res.ok) {
      showMessage(`Search failed: ${data?.detail ?? "Unknown error"}`);
      return;
    }

    const resultsEl = clearResults();
    const list = document.createElement("ol");

    const items = Array.isArray(data?.results) ? data.results : [];
    if (items.length === 0) {
      const li = document.createElement("li");
      li.textContent = "No results";
      list.appendChild(li);
    } else {
      for (const r of items) {
        const li = document.createElement("li");

        const title = document.createElement("div");
        const source = r?.metadata?.source ? ` (${r.metadata.source})` : "";
        title.textContent = `#${r.rank}${source}`;

        const pre = document.createElement("pre");
        pre.classList.add("result-text");
        pre.textContent = r?.text ?? "";

        li.appendChild(title);
        li.appendChild(pre);
        list.appendChild(li);
      }
    }

    resultsEl.appendChild(list);
  });
});