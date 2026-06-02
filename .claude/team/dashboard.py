#!/usr/bin/env python3
"""
Agent Team Dashboard
Usage: python3 .claude/team/dashboard.py
Open:  http://localhost:5765
"""

import http.server
import json
import socketserver
import time
from pathlib import Path

PORT = 5766
TEAM_DIR = Path(".claude/team")
AGENTS_DIR = TEAM_DIR / "agents"
APPROVAL_REQ  = TEAM_DIR / "approval.json"
APPROVAL_RESP = TEAM_DIR / "approval-response.json"
AUDIT_LOG = Path.home() / ".claude/logs/audit.log"
PIPELINE = ["coordinator", "researcher", "architect", "implementer", "reviewer"]


def get_agent_status(name):
    f = AGENTS_DIR / f"{name}.json"
    if not f.exists():
        return {"name": name, "status": "waiting", "step": "", "result": None}
    try:
        return json.loads(f.read_text())
    except Exception:
        return {"name": name, "status": "error", "step": "Could not read status file", "result": None}


def get_approval():
    if not APPROVAL_REQ.exists():
        return None
    try:
        return json.loads(APPROVAL_REQ.read_text())
    except Exception:
        return None


def get_recent_logs(n=20):
    if not AUDIT_LOG.exists():
        return []
    lines = AUDIT_LOG.read_text(errors="replace").splitlines()
    return lines[-n:]


def get_data():
    return {
        "agents":   [get_agent_status(name) for name in PIPELINE],
        "logs":     get_recent_logs(),
        "approval": get_approval(),
        "timestamp": time.strftime("%H:%M:%S"),
    }


HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Agent Team</title>
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:#0d1117;color:#c9d1d9;font-family:'Segoe UI',system-ui,sans-serif;padding:24px;min-height:100vh}
  h1{color:#58a6ff;font-size:1.3rem;font-weight:600;letter-spacing:-.3px}
  .sub{color:#6e7681;font-size:.8rem;margin-top:3px;margin-bottom:28px}

  .pipeline{display:flex;align-items:stretch;gap:0;margin-bottom:28px;overflow-x:auto;padding-bottom:4px}
  .arrow{display:flex;align-items:center;color:#30363d;font-size:1.1rem;padding:0 6px;flex-shrink:0}

  .card{background:#161b22;border:1px solid #30363d;border-radius:10px;padding:16px 18px;min-width:155px;flex:1;transition:border-color .25s,background .25s}
  .card.waiting{opacity:.45}
  .card.running{border-color:#9e6a03;background:#1c1a0f}
  .card.done   {border-color:#1f6feb;background:#0d1b2a}
  .card.approval{border-color:#bc8cff;background:#1a0f2e;animation:glow 1.5s ease-in-out infinite}
  .card.error  {border-color:#da3633;background:#1b0e0d}
  @keyframes glow{0%,100%{box-shadow:0 0 0 0 #bc8cff00}50%{box-shadow:0 0 12px 2px #bc8cff44}}

  .card-top{display:flex;align-items:center;gap:8px;margin-bottom:10px}
  .dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
  .dot.waiting {background:#484f58}
  .dot.running {background:#e3b341;animation:pulse 1.4s ease-in-out infinite}
  .dot.done    {background:#58a6ff}
  .dot.approval{background:#bc8cff;animation:pulse 1.4s ease-in-out infinite}
  .dot.error   {background:#f85149}
  @keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}

  .card-name{font-size:.9rem;font-weight:600;color:#c9d1d9;flex:1}
  .badge{font-size:.65rem;padding:2px 7px;border-radius:10px;font-weight:500;flex-shrink:0}
  .badge.waiting {background:#21262d;color:#6e7681}
  .badge.running {background:#3d2300;color:#e3b341}
  .badge.done    {background:#0c2d6b;color:#79c0ff}
  .badge.approval{background:#2d1a4a;color:#d2a8ff}
  .badge.error   {background:#2d0f0f;color:#f85149}

  .card-step{font-size:.78rem;color:#8b949e;line-height:1.45;min-height:34px}
  .card-result{font-size:.75rem;color:#3fb950;margin-top:8px;padding-top:8px;border-top:1px solid #21262d;line-height:1.4}

  .progress-wrap{margin-top:10px;background:#21262d;border-radius:4px;height:3px;overflow:hidden}
  .progress-bar{height:100%;border-radius:4px;transition:width .5s ease}
  .progress-bar.running {background:#e3b341}
  .progress-bar.approval{background:#bc8cff}
  .progress-bar.done    {background:#58a6ff;width:100%!important}

  /* ── Approval Modal ─────────────────────────────── */
  .overlay{position:fixed;inset:0;background:#00000099;display:flex;align-items:center;justify-content:center;z-index:100;backdrop-filter:blur(3px)}
  .overlay.hidden{display:none}
  .modal{background:#161b22;border:1px solid #bc8cff;border-radius:14px;padding:28px 32px;max-width:480px;width:90%;box-shadow:0 0 40px #bc8cff33}
  .modal-header{display:flex;align-items:center;gap:10px;margin-bottom:6px}
  .modal-icon{font-size:1.4rem}
  .modal-title{font-size:1rem;font-weight:600;color:#d2a8ff}
  .modal-from{font-size:.78rem;color:#6e7681;margin-bottom:16px}
  .modal-question{font-size:.95rem;color:#e6edf3;line-height:1.55;margin-bottom:8px}
  .modal-context{font-size:.75rem;color:#6e7681;margin-bottom:20px;font-style:italic}
  .modal-actions{display:flex;gap:10px;flex-wrap:wrap}
  .modal-btn{flex:1;padding:9px 16px;border-radius:8px;border:none;font-size:.85rem;font-weight:500;cursor:pointer;transition:opacity .15s,transform .1s}
  .modal-btn:hover{opacity:.85;transform:translateY(-1px)}
  .modal-btn:active{transform:translateY(0)}
  .modal-btn.primary{background:#238636;color:#fff}
  .modal-btn.secondary{background:#21262d;color:#c9d1d9;border:1px solid #30363d}
  .modal-btn.danger{background:#da3633;color:#fff}

  /* ── Logs ───────────────────────────────────────── */
  .logs-section h2{font-size:.8rem;color:#6e7681;text-transform:uppercase;letter-spacing:.8px;margin-bottom:8px}
  .logs{background:#010409;border:1px solid #21262d;border-radius:8px;padding:12px 14px;font-family:'Cascadia Code','Fira Code',monospace;font-size:.73rem;color:#6e7681;max-height:220px;overflow-y:auto}
  .log-line{padding:1px 0;white-space:pre}
  .log-line:hover{color:#c9d1d9}
  .footer{margin-top:14px;font-size:.72rem;color:#30363d;display:flex;justify-content:space-between}
</style>
</head>
<body>

<!-- Approval Modal -->
<div class="overlay hidden" id="overlay">
  <div class="modal">
    <div class="modal-header">
      <span class="modal-icon">🔔</span>
      <span class="modal-title">Agent cần xác nhận</span>
    </div>
    <div class="modal-from" id="modal-from">—</div>
    <div class="modal-question" id="modal-question">—</div>
    <div class="modal-context" id="modal-context"></div>
    <div class="modal-actions" id="modal-actions"></div>
  </div>
</div>

<h1>🤖 Agent Team</h1>
<p class="sub">Monitoring · Auto-refresh every 2s · <span id="ts">—</span></p>

<div class="pipeline" id="pipeline"><div style="color:#6e7681;padding:20px">Loading...</div></div>

<div class="logs-section">
  <h2>Audit Log</h2>
  <div class="logs" id="logs"><div class="log-line">Waiting for events...</div></div>
</div>

<div class="footer">
  <span>Watching <code>.claude/team/agents/</code> + <code>~/.claude/logs/audit.log</code></span>
  <span>port <strong>5765</strong></span>
</div>

<script>
const BADGE_TEXT = {waiting:"waiting", running:"● running", done:"✓ done", approval:"⏸ waiting you", error:"✗ error"};

function pct(a) {
  const m = (a.step||"").match(/step\s*(\d+)\s*\/\s*(\d+)/i);
  if (m) return Math.round((+m[1] / +m[2]) * 100);
  if (a.status === "done") return 100;
  if (a.status === "running" || a.status === "approval") return 50;
  return 0;
}

function card(a) {
  const s = a.status || "waiting";
  const p = pct(a);
  const showBar = ["running","done","approval"].includes(s);
  return `
<div class="card ${s}">
  <div class="card-top">
    <div class="dot ${s}"></div>
    <span class="card-name">${a.name}</span>
    <span class="badge ${s}">${BADGE_TEXT[s]||s}</span>
  </div>
  <div class="card-step">${a.step || (s==="waiting"?"Idle":"")}</div>
  ${showBar ? `<div class="progress-wrap"><div class="progress-bar ${s}" style="width:${p}%"></div></div>` : ""}
  ${a.result ? `<div class="card-result">↳ ${a.result}</div>` : ""}
</div>`;
}

// ── Approval modal ───────────────────────────────────
let currentApprovalId = null;

function showApproval(ap) {
  if (!ap || ap.id === currentApprovalId) return;  // already showing same request
  currentApprovalId = ap.id;

  document.getElementById("modal-from").textContent    = `From: ${ap.from}`;
  document.getElementById("modal-question").textContent = ap.question;
  document.getElementById("modal-context").textContent  = ap.context || "";

  const actions = document.getElementById("modal-actions");
  actions.innerHTML = "";
  (ap.options || ["Yes, proceed", "No, stop"]).forEach((opt, i) => {
    const btn = document.createElement("button");
    btn.textContent = opt;
    btn.className = "modal-btn " + (i === 0 ? "primary" : i === ap.options.length-1 && ap.options.length > 1 ? "danger" : "secondary");
    btn.onclick = () => respond(ap.id, opt);
    actions.appendChild(btn);
  });

  document.getElementById("overlay").classList.remove("hidden");
}

function hideModal() {
  document.getElementById("overlay").classList.add("hidden");
}

async function respond(id, answer) {
  // Ẩn modal ngay, GIỮ currentApprovalId để poll tiếp theo không mở lại
  hideModal();
  try {
    await fetch("/respond", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({id, answer})
    });
  } catch(e) { console.error("respond failed", e); }
}

// ── Main render ──────────────────────────────────────
function render(data) {
  // Pipeline cards
  let html = "";
  data.agents.forEach((a, i) => {
    html += card(a);
    if (i < data.agents.length - 1) html += '<div class="arrow">→</div>';
  });
  document.getElementById("pipeline").innerHTML = html;

  // Logs
  const logEl = document.getElementById("logs");
  const atBottom = logEl.scrollHeight - logEl.scrollTop - logEl.clientHeight < 30;
  logEl.innerHTML = data.logs.length
    ? data.logs.map(l => `<div class="log-line">${l}</div>`).join("")
    : '<div class="log-line" style="color:#484f58">No events yet.</div>';
  if (atBottom) logEl.scrollTop = logEl.scrollHeight;

  document.getElementById("ts").textContent = data.timestamp;

  // Approval: chỉ clear currentApprovalId khi server confirm xóa file
  if (data.approval) {
    showApproval(data.approval);
  } else {
    currentApprovalId = null;  // server đã xóa → an toàn reset
    hideModal();
  }
}

async function poll() {
  try {
    const r = await fetch("/data");
    render(await r.json());
  } catch(e) {}
}

poll();
setInterval(poll, 2000);
</script>
</body>
</html>"""


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            body = HTML.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif self.path == "/data":
            body = json.dumps(get_data()).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/respond":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body)
                APPROVAL_RESP.write_text(json.dumps(data, ensure_ascii=False))
                APPROVAL_REQ.unlink(missing_ok=True)   # clear the request
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"ok":true}')
            except Exception as e:
                self.send_response(500)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, *_):
        pass


if __name__ == "__main__":
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"  Agent Team Dashboard")
    print(f"  → http://localhost:{PORT}")
    print(f"  → Watching: {TEAM_DIR.resolve()}")
    print(f"  → Ctrl+C to stop\n")
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.allow_reuse_address = True
        httpd.serve_forever()
