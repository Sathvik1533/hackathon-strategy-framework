document.addEventListener("DOMContentLoaded", () => {
  const refreshBtn = document.getElementById("refreshBtn");
  const faithfulnessVal = document.getElementById("faithfulnessVal");
  const relevanceVal = document.getElementById("relevanceVal");
  const latencyP95Val = document.getElementById("latencyP95Val");
  const cacheRateVal = document.getElementById("cacheRateVal");
  const p99Val = document.getElementById("p99Val");
  const totalJobsVal = document.getElementById("totalJobsVal");
  const uptimeVal = document.getElementById("uptimeVal");
  const budgetRatioText = document.getElementById("budgetRatioText");
  const budgetFill = document.getElementById("budgetFill");
  const circuitsTableBody = document.getElementById("circuitsTableBody");

  async function loadTelemetry() {
    try {
      const res = await fetch("/api/v1/analytics/telemetry");
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const json = await res.json();
      const t = json.data;

      faithfulnessVal.textContent = `${(t.ragas_faithfulness * 100).toFixed(1)}%`;
      relevanceVal.textContent = `${(t.ragas_answer_relevance * 100).toFixed(1)}%`;
      latencyP95Val.textContent = `${t.p95_latency_ms}ms`;
      cacheRateVal.textContent = `${(t.cache_hit_rate * 100).toFixed(1)}%`;
      p99Val.textContent = `${t.p99_latency_ms}ms`;
      totalJobsVal.textContent = t.total_jobs_processed;

      const hrs = Math.floor(t.uptime_seconds / 3600);
      const mins = Math.floor((t.uptime_seconds % 3600) / 60);
      uptimeVal.textContent = `${hrs}h ${mins}m (Healthy)`;

      const pct = ((t.token_budget_used / t.token_budget_limit) * 100).toFixed(1);
      budgetRatioText.textContent = `${t.token_budget_used.toLocaleString()} / ${t.token_budget_limit.toLocaleString()} (${pct}%)`;
      budgetFill.style.width = `${pct}%`;

      if (t.active_circuits && t.active_circuits.length > 0) {
        circuitsTableBody.innerHTML = t.active_circuits.map(c => `
          <tr>
            <td><code>${escapeHtml(c.name)}</code></td>
            <td><span class="status-chip ${c.state.toLowerCase().replace('_', '-')}">${c.state}</span></td>
            <td>${c.failure_count} / 5</td>
            <td>${c.recovery_timeout_sec}s</td>
          </tr>
        `).join("");
      }
    } catch (err) {
      console.warn("Using offline demo telemetry snapshot:", err);
    }
  }

  refreshBtn.addEventListener("click", () => {
    refreshBtn.textContent = "Refreshing...";
    loadTelemetry().finally(() => {
      setTimeout(() => { refreshBtn.textContent = "🔄 Refresh Telemetry"; }, 400);
    });
  });

  function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  // Initial load
  loadTelemetry();
});
