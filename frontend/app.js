document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("jobForm");
  const submitBtn = document.getElementById("submitBtn");
  const taskTypeSelect = document.getElementById("taskType");
  const queryInput = document.getElementById("queryInput");
  const terminalBody = document.getElementById("terminalBody");
  const progressBar = document.getElementById("progressBar");
  const jobStatus = document.getElementById("jobStatus");

  function appendLog(text, className = "") {
    const line = document.createElement("div");
    line.className = `log-line ${className}`;
    const timestamp = new Date().toISOString().split("T")[1].slice(0, 8);
    line.textContent = `[${timestamp}] ${text}`;
    terminalBody.appendChild(line);
    terminalBody.scrollTop = terminalBody.scrollHeight;
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    submitBtn.disabled = true;
    submitBtn.textContent = "Dispatching Job...";
    jobStatus.textContent = "ENQUEUEING";
    jobStatus.style.color = "var(--accent-amber)";
    progressBar.style.width = "5%";

    const payload = {
      task_type: taskTypeSelect.value,
      payload: { query: queryInput.value }
    };

    try {
      appendLog(`POST /api/v1/jobs/render -> Task: ${payload.task_type}`, "system");
      const res = await fetch("/api/v1/jobs/render", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!res.ok) throw new Error(`HTTP error ${res.status}`);

      const data = await res.json();
      const jobId = data.data.job_id;
      appendLog(`Job successfully enqueued. Tracking ID: ${jobId}`, "system");

      // Subscribe to Server-Sent Events (SSE)
      subscribeToSSE(jobId);

    } catch (err) {
      appendLog(`Error submitting job: ${err.message}`, "log-line");
      submitBtn.disabled = false;
      submitBtn.textContent = "Execute Workflow";
      jobStatus.textContent = "ERROR";
      jobStatus.style.color = "var(--accent-rose)";
    }
  });

  function subscribeToSSE(jobId) {
    jobStatus.textContent = "STREAMING SSE";
    jobStatus.style.color = "var(--accent-blue)";
    const eventSource = new EventSource(`/api/v1/jobs/${jobId}/stream`);

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        progressBar.style.width = `${data.percent}%`;
        appendLog(`[${data.percent}%] ${data.log}`, data.percent === 100 ? "success" : "");

        if (data.status === "completed") {
          jobStatus.textContent = "COMPLETED";
          jobStatus.style.color = "var(--accent-emerald)";
          if (data.result) {
            appendLog(`Final Result: ${JSON.stringify(data.result)}`, "success");
          }
          eventSource.close();
          submitBtn.disabled = false;
          submitBtn.textContent = "Execute Workflow";
        } else if (data.status === "failed") {
          jobStatus.textContent = "FAILED";
          jobStatus.style.color = "var(--accent-rose)";
          eventSource.close();
          submitBtn.disabled = false;
          submitBtn.textContent = "Execute Workflow";
        }
      } catch (e) {
        appendLog(event.data);
      }
    };

    eventSource.onerror = () => {
      appendLog("SSE connection closed or completed.", "system");
      eventSource.close();
      submitBtn.disabled = false;
      submitBtn.textContent = "Execute Workflow";
    };
  }
});
