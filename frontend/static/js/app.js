const $ = (id) => document.getElementById(id);

let analysisTimer = null;

function badgeClass(score) {
  if (score <= 20) return "bad";
  if (score <= 40) return "warn";
  if (score <= 60) return "warn";
  return "good";
}

function renderAnalysis(data) {
  $("score").textContent = data.score;
  $("classification").textContent = data.classification;
  $("classification").className = `badge ${badgeClass(data.score)}`;
  $("meterFill").style.width = `${data.score}%`;
  $("lengthBand").textContent = `Length: ${data.metrics.length} (${data.metrics.band})`;

  $("findings").innerHTML = data.findings.length
    ? data.findings.map(f => `<li><strong>${escapeHtml(f.severity.toUpperCase())}</strong>: ${escapeHtml(f.description)}</li>`).join("")
    : "<li>No major pattern findings detected.</li>";

  $("suggestions").innerHTML = data.suggestions.map(s => `<li>${escapeHtml(s)}</li>`).join("");

  const m = data.metrics;
  $("metrics").innerHTML = [
    ["Unique characters", m.unique_character_count],
    ["Character types", m.character_type_count],
    ["Unique ratio", m.unique_character_ratio],
    ["Entropy estimate", `${m.theoretical_entropy_bits} bits`],
    ["Sequences", m.sequence_count],
    ["Keyboard patterns", m.keyboard_pattern_count],
    ["Repetition findings", m.repetition_count],
    ["Common password", m.common_password ? "Yes" : "No"],
  ].map(([k,v]) => `<div class="metric"><span>${escapeHtml(k)}</span><strong>${escapeHtml(String(v))}</strong></div>`).join("");
}

async function analyze() {
  const password = $("password").value;
  if (!password) {
    $("score").textContent = "0";
    $("classification").textContent = "READY";
    $("classification").className = "badge neutral";
    $("meterFill").style.width = "0%";
    $("findings").innerHTML = "";
    $("suggestions").innerHTML = "";
    $("metrics").innerHTML = "";
    return;
  }

  const body = {
    password,
    context: {
      first_name: $("firstName").value,
      birth_year: $("birthYear").value,
      company_college: $("companyCollege").value
    }
  };

  const res = await fetch("/api/analyze", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(body)
  });
  const data = await res.json();
  if (!res.ok) {
    alert(data.error || "Analysis failed.");
    return;
  }
  renderAnalysis(data);
  loadDashboard();
}

$("password").addEventListener("input", () => {
  clearTimeout(analysisTimer);
  analysisTimer = setTimeout(analyze, 120);
});
["firstName", "birthYear", "companyCollege"].forEach(id => $(id).addEventListener("input", analyze));

$("togglePassword").addEventListener("click", () => {
  const field = $("password");
  field.type = field.type === "password" ? "text" : "password";
  $("togglePassword").textContent = field.type === "password" ? "Show" : "Hide";
});

$("generateBtn").addEventListener("click", async () => {
  const payload = {
    length: Number($("genLength").value),
    uppercase: $("genUpper").checked,
    lowercase: $("genLower").checked,
    digits: $("genDigits").checked,
    symbols: $("genSymbols").checked
  };
  const res = await fetch("/api/generate-password", {
    method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(payload)
  });
  const data = await res.json();
  if (!res.ok) return alert(data.error || "Generation failed.");
  $("generatedPassword").value = data.password;
});

$("copyGenerated").addEventListener("click", async () => {
  if ($("generatedPassword").value) {
    await navigator.clipboard.writeText($("generatedPassword").value);
  }
});

$("policyBtn").addEventListener("click", async () => {
  const password = $("password").value;
  if (!password) return alert("Enter a synthetic/demo password first.");
  const res = await fetch("/api/policy/check", {
    method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({password})
  });
  const data = await res.json();
  $("policyStatus").textContent = data.status;
  $("policyStatus").className = `badge ${data.policy_pass ? "good" : "bad"}`;
  $("policyFailures").innerHTML = data.failures.length
    ? data.failures.map(x => `<li>${escapeHtml(x)}</li>`).join("")
    : "<li>All configured policy checks passed.</li>";
});

function renderBars(containerId, rows, labelKey, maxValue) {
  const el = $(containerId);
  if (!rows.length) {
    el.innerHTML = "<p class='privacy-note'>No aggregate data yet.</p>";
    return;
  }
  el.innerHTML = rows.map(r => {
    const value = Number(r.count);
    const width = Math.max(3, (value / maxValue) * 100);
    return `<div class="bar-row"><span>${escapeHtml(String(r[labelKey]))}</span><div class="bar"><i style="width:${width}%"></i></div><strong>${value}</strong></div>`;
  }).join("");
}

async function loadDashboard() {
  const [statsRes, weakRes] = await Promise.all([
    fetch("/api/dashboard/stats"),
    fetch("/api/analytics/weaknesses")
  ]);
  const stats = await statsRes.json();
  const weaknesses = await weakRes.json();

  $("totalAnalyses").textContent = stats.total_analyses;
  $("averageScore").textContent = stats.average_score;
  $("veryWeak").textContent = stats.strength_distribution["VERY WEAK"] || 0;
  $("strongPlus").textContent =
    (stats.strength_distribution["STRONG"] || 0) +
    (stats.strength_distribution["VERY STRONG"] || 0);

  const dist = Object.entries(stats.strength_distribution).map(([classification,count]) => ({classification,count}));
  renderBars("strengthChart", dist, "classification", Math.max(1, ...dist.map(x => x.count)));
  renderBars("weaknessChart", weaknesses, "finding_type", Math.max(1, ...weaknesses.map(x => x.count)));
}

$("refreshDashboard").addEventListener("click", loadDashboard);
loadDashboard();

function escapeHtml(value) {
  return value.replace(/[&<>"']/g, ch => ({
    "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#039;"
  }[ch]));
}
