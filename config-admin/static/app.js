// Configurations page. Viewers see a read-only table; admins can create, edit and delete.
const $ = (id) => document.getElementById(id);
let me = null;
let editingId = null;

async function api(path, options = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (res.status === 401) {
    window.location.href = "/";
    throw new Error("Not authenticated");
  }
  return res;
}

function showMessage(text) {
  $("message").textContent = text;
  $("message").hidden = !text;
}

function cell(text) {
  const td = document.createElement("td");
  td.textContent = text; // textContent, never innerHTML: config values are untrusted
  return td;
}

function renderRows(configs) {
  const tbody = $("rows");
  tbody.replaceChildren();
  for (const c of configs) {
    const tr = document.createElement("tr");
    tr.append(cell(c.key), cell(c.value), cell(c.value_type), cell(c.environment),
              cell(`${c.updated_at} by ${c.updated_by}`));
    const actions = document.createElement("td");
    if (me.role === "admin") {
      const edit = document.createElement("button");
      edit.textContent = "Edit";
      edit.className = "secondary";
      edit.addEventListener("click", () => openEditor(c));
      const del = document.createElement("button");
      del.textContent = "Delete";
      del.className = "danger";
      del.addEventListener("click", () => removeConfig(c));
      actions.append(edit, del);
    }
    tr.append(actions);
    tbody.append(tr);
  }
}

async function load() {
  const params = new URLSearchParams();
  if ($("search").value) params.set("q", $("search").value);
  if ($("env-filter").value) params.set("environment", $("env-filter").value);
  const res = await api(`/api/configs?${params}`);
  if (!res.ok) return showMessage("Could not load configurations");
  showMessage("");
  renderRows(await res.json());
}

function openEditor(config) {
  editingId = config ? config.id : null;
  $("editor-title").textContent = config ? "Edit config" : "New config";
  $("f-key").value = config ? config.key : "";
  $("f-value").value = config ? config.value : "";
  $("f-type").value = config ? config.value_type : "string";
  $("f-env").value = config ? config.environment : "dev";
  $("f-desc").value = config ? config.description : "";
  $("editor-error").hidden = true;
  $("editor").showModal();
}

async function removeConfig(config) {
  if (!confirm(`Delete ${config.key} (${config.environment})?`)) return;
  const res = await api(`/api/configs/${config.id}`, { method: "DELETE" });
  if (!res.ok) showMessage("Delete failed");
  await load();
}

$("editor-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const body = JSON.stringify({
    key: $("f-key").value,
    value: $("f-value").value,
    value_type: $("f-type").value,
    environment: $("f-env").value,
    description: $("f-desc").value,
  });
  const res = await api(editingId ? `/api/configs/${editingId}` : "/api/configs",
                        { method: editingId ? "PUT" : "POST", body });
  if (res.ok) {
    $("editor").close();
    await load();
  } else {
    const err = await res.json().catch(() => ({}));
    // 422 from pydantic returns a list of problems; our own validation returns a string
    $("editor-error").textContent = typeof err.detail === "string" ? err.detail : "Invalid input";
    $("editor-error").hidden = false;
  }
});

$("cancel").addEventListener("click", () => $("editor").close());
$("new-btn").addEventListener("click", () => openEditor(null));
$("search").addEventListener("input", load);
$("env-filter").addEventListener("change", load);
$("logout").addEventListener("click", async () => {
  await api("/api/auth/logout", { method: "POST" }).catch(() => {});
  window.location.href = "/";
});

(async () => {
  const res = await api("/api/auth/me");
  me = await res.json();
  $("who").textContent = `${me.username} (${me.role})`;
  $("new-btn").hidden = me.role !== "admin";
  await load();
})();
