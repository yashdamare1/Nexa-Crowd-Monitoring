
const token = sessionStorage.getItem("nexaToken");
const connectionStatus = document.getElementById("connectionStatus");
const sourceMessage = document.getElementById("sourceMessage");
const sourceTableBody = document.getElementById("sourceTableBody");
const alertMessage = document.getElementById("alertMessage");
const alertTableBody = document.getElementById("alertTableBody");
const historySource = document.getElementById("historySource");
const historyMessage = document.getElementById("historyMessage");
const riskTimeline = document.getElementById("riskTimeline");
const riskTimelineMessage = document.getElementById("riskTimelineMessage");
const chartCanvas = document.getElementById("peopleCountChart");

let historyLoadedSource = "";
let historyData = [];
let sourceIds = [];
let refreshInProgress = false;

if (!token) {
    window.location.replace("/login.html");
}

document.getElementById("welcomeMessage").textContent =
    `Signed in as ${sessionStorage.getItem("nexaName") || "User"} · ` +
    `${sessionStorage.getItem("nexaRole") || "Authenticated"}`;

document.getElementById("logoutButton").addEventListener("click", () => {
    sessionStorage.removeItem("nexaToken");
    sessionStorage.removeItem("nexaName");
    sessionStorage.removeItem("nexaRole");
    window.location.replace("/login.html");
});

document.getElementById("refreshButton").addEventListener("click", refreshDashboard);

historySource.addEventListener("change", async () => {
    historyLoadedSource = "";
    await loadHistory();
});

function createStatusBadge(value, type) {
    const badge = document.createElement("span");
    const normalized = String(value ?? "").toUpperCase();
    badge.className = "status";

    if (type === "risk") {
        badge.classList.add(
            normalized === "CRITICAL" ? "status-critical" :
            normalized === "WARNING" ? "status-warning" : "status-normal"
        );
        badge.textContent = normalized || "UNKNOWN";
    } else if (type === "event") {
        badge.classList.add(
            normalized === "ESCALATED" ? "status-critical" :
            normalized === "RESOLVED" ? "status-normal" : "status-warning"
        );
        badge.textContent = normalized || "UNKNOWN";
    } else {
        badge.classList.add(value === true ? "status-online" : "status-offline");
        badge.textContent = value === true ? "ONLINE" : "OFFLINE";
    }

    return badge;
}

function addCell(row, value) {
    const cell = document.createElement("td");
    cell.textContent = value ?? "—";
    row.appendChild(cell);
    return cell;
}

function formatDate(value) {
    if (!value) return "—";
    const date = new Date(value);
    return Number.isNaN(date.getTime()) ? String(value) : date.toLocaleString();
}

async function apiGet(url) {
    const response = await fetch(url, {
        headers: { Authorization: `Bearer ${token}` },
        cache: "no-store"
    });

    if (response.status === 401 || response.status === 403) {
        sessionStorage.clear();
        window.location.replace("/login.html");
        throw new Error("Authentication expired. Please sign in again.");
    }

    if (!response.ok) {
        throw new Error(`API returned ${response.status}.`);
    }

    return response.json();
}


async function apiPost(url, body) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(body)
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
        throw new Error(
            data.detail || data.message || data.error || `HTTP ${response.status}`
        );
    }

    return data;
}


function updateSourceOptions(sources) {
    const previousValue = historySource.value;
    const newIds = sources.map(source => source.sourceId);

    const changed =
        newIds.length !== sourceIds.length ||
        newIds.some((id, index) => id !== sourceIds[index]);

    if (!changed) {
        return;
    }

    sourceIds = newIds;
    historySource.replaceChildren();

    const placeholder = document.createElement("option");
    placeholder.value = "";
    placeholder.textContent = "Select source";
    historySource.appendChild(placeholder);

    for (const sourceId of sourceIds) {
        const option = document.createElement("option");
        option.value = sourceId;
        option.textContent = sourceId;
        historySource.appendChild(option);
    }

    if (sourceIds.includes(previousValue)) {
        historySource.value = previousValue;
    } else if (sourceIds.length > 0) {
        historySource.value = sourceIds[0];
    }

    historyLoadedSource = "";
}

async function loadSources() {
    sourceMessage.textContent = "Loading monitoring data...";

    try {
        const sources = await apiGet("/api/security/monitoring/sources");

        document.getElementById("totalSources").textContent = sources.length;
        document.getElementById("onlineSources").textContent =
            sources.filter(source => source.sourceOnline === true).length;
        document.getElementById("totalPeople").textContent =
            sources.reduce((sum, source) => sum + (Number(source.personCount) || 0), 0);
        document.getElementById("criticalSources").textContent =
            sources.filter(source =>
                String(source.riskLevel).toUpperCase() === "CRITICAL"
            ).length;

        document.getElementById("normalSources").textContent =
            sources.filter(source =>
                String(source.riskLevel).toUpperCase() === "NORMAL"
            ).length;

        document.getElementById("warningSources").textContent =
            sources.filter(source =>
                String(source.riskLevel).toUpperCase() === "WARNING"
            ).length;

        document.getElementById("riskCriticalSources").textContent =
            sources.filter(source =>
                String(source.riskLevel).toUpperCase() === "CRITICAL"
            ).length;

        sourceTableBody.replaceChildren();

        for (const source of sources) {
            const row = document.createElement("tr");
            addCell(row, source.sourceId);
            addCell(row, source.personCount);

            const riskCell = document.createElement("td");
            riskCell.appendChild(createStatusBadge(source.riskLevel, "risk"));
            row.appendChild(riskCell);

            
            const onlineCell = document.createElement("td");

            const isOnline = source.sourceOnline === true;
            const statusWrapper = document.createElement("span");
            statusWrapper.className = isOnline
                ? "source-indicator source-online"
                : "source-indicator source-offline";

            const statusDot = document.createElement("span");
            statusDot.className = "source-status-dot";
            statusDot.setAttribute("aria-hidden", "true");

            const statusText = document.createElement("span");
            statusText.textContent = isOnline ? "ONLINE" : "OFFLINE";

            statusWrapper.append(statusDot, statusText);
            onlineCell.appendChild(statusWrapper);
            row.appendChild(onlineCell);


            addCell(row, formatDate(source.lastUpdated));
            sourceTableBody.appendChild(row);
        }

        sourceMessage.textContent = sources.length
            ? "" : "No monitoring sources yet. Start the AI pipeline to send updates.";

        connectionStatus.textContent = "CONNECTED";
        connectionStatus.className = "status status-online";

        document.getElementById("lastRefresh").textContent =
            `Last refreshed: ${new Date().toLocaleTimeString()}`;

        updateSourceOptions(sources);
    } catch (error) {
        connectionStatus.textContent = "API ERROR";
        connectionStatus.className = "status status-critical";
        sourceMessage.textContent = error.message;
    }
}


async function loadAlerts() {
    alertMessage.textContent = "Loading alert history...";

    try {
        const alerts = await apiGet("/api/security/alerts");
        alertTableBody.replaceChildren();

        for (const alert of alerts) {
            const row = document.createElement("tr");

            const riskLevel = String(alert.riskLevel || "").toUpperCase();
            const alertStatus = String(alert.status || "").toUpperCase();

            row.classList.add("alert-row");

            if (alertStatus === "RESOLVED") {
                row.classList.add("alert-resolved");
            } else if (riskLevel === "CRITICAL") {
                row.classList.add("alert-critical");
            } else if (riskLevel === "WARNING") {
                row.classList.add("alert-warning");
            } else {
                row.classList.add("alert-normal");
            }

            addCell(row, alert.id);
            addCell(row, alert.sourceId);

            const eventCell = document.createElement("td");
            eventCell.appendChild(createStatusBadge(alert.eventType, "event"));
            row.appendChild(eventCell);

            const riskCell = document.createElement("td");
            riskCell.appendChild(createStatusBadge(alert.riskLevel, "risk"));
            row.appendChild(riskCell);

            addCell(row, alert.message);
            addCell(row, alert.status);
            addCell(row, formatDate(alert.createdAt));
            addCell(row, formatDate(alert.resolvedAt));

            alertTableBody.appendChild(row);
        }

        alertMessage.textContent = alerts.length
            ? ""
            : "No alerts recorded yet.";

        document.getElementById("alertLastRefresh").textContent =
            `Last refreshed: ${new Date().toLocaleTimeString()}`;
    } catch (error) {
        alertMessage.textContent = error.message;
    }
}



function drawPeopleCountChart(samples) {
    const canvas = chartCanvas;
    const context = canvas.getContext("2d");
    const rect = canvas.getBoundingClientRect();

    if (rect.width === 0) return;

    const pixelRatio = window.devicePixelRatio || 1;
    canvas.width = Math.floor(rect.width * pixelRatio);
    canvas.height = Math.floor(300 * pixelRatio);
    context.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);

    const width = rect.width;
    const height = 300;
    const left = 48;
    const right = 20;
    const top = 24;
    const bottom = 48;
    const plotWidth = width - left - right;
    const plotHeight = height - top - bottom;

    context.clearRect(0, 0, width, height);
    context.font = "12px Arial";

    if (!samples.length) {
        context.fillStyle = "#94a3b8";
        context.textAlign = "center";
        context.fillText(
            "No historical samples available",
            width / 2,
            height / 2
        );
        return;
    }

    const counts = samples.map(sample =>
        Math.max(0, Number(sample.personCount) || 0)
    );

    const minCount = Math.max(0, Math.floor(Math.min(...counts) - 2));
    const maxCount = Math.max(
        minCount + 4,
        Math.ceil(Math.max(...counts) + 2)
    );

    const x = index => left +
        (samples.length === 1 ? 0.5 : index / (samples.length - 1)) *
        plotWidth;

    const y = count => top +
        ((maxCount - count) / (maxCount - minCount)) * plotHeight;

    // Dark-theme grid and axis labels
    context.lineWidth = 1;
    context.strokeStyle = "#263449";
    context.fillStyle = "#94a3b8";
    context.textAlign = "right";

    for (let tick = 0; tick <= 4; tick++) {
        const value = minCount + (maxCount - minCount) * tick / 4;
        const py = y(value);

        context.beginPath();
        context.moveTo(left, py);
        context.lineTo(width - right, py);
        context.stroke();

        context.fillText(String(Math.round(value)), left - 9, py + 4);
    }

    // Filled area beneath the people-count line
    context.beginPath();

    samples.forEach((sample, index) => {
        const px = x(index);
        const py = y(Number(sample.personCount) || 0);

        if (index === 0) {
            context.moveTo(px, py);
        } else {
            context.lineTo(px, py);
        }
    });

    context.lineTo(x(samples.length - 1), top + plotHeight);
    context.lineTo(x(0), top + plotHeight);
    context.closePath();

    context.fillStyle = "rgba(34, 211, 238, 0.12)";
    context.fill();

    // Bright cyan monitoring line
    context.beginPath();

    samples.forEach((sample, index) => {
        const px = x(index);
        const py = y(Number(sample.personCount) || 0);

        if (index === 0) {
            context.moveTo(px, py);
        } else {
            context.lineTo(px, py);
        }
    });

    context.strokeStyle = "#22d3ee";
    context.lineWidth = 3;
    context.lineJoin = "round";
    context.lineCap = "round";
    context.stroke();

    // Highlight the latest reading
    const latestIndex = samples.length - 1;
    const latestX = x(latestIndex);
    const latestY = y(counts[latestIndex]);

    context.beginPath();
    context.arc(latestX, latestY, 7, 0, Math.PI * 2);
    context.fillStyle = "rgba(34, 211, 238, 0.2)";
    context.fill();

    context.beginPath();
    context.arc(latestX, latestY, 4, 0, Math.PI * 2);
    context.fillStyle = "#22d3ee";
    context.fill();

    // Time labels
    context.fillStyle = "#94a3b8";
    context.textAlign = "left";
    context.fillText(
        formatTime(samples[0].recordedAt),
        left,
        height - 18
    );

    context.textAlign = "right";
    context.fillText(
        formatTime(samples[samples.length - 1].recordedAt),
        width - right,
        height - 18
    );

    // Y-axis label
    context.save();
    context.translate(14, height / 2);
    context.rotate(-Math.PI / 2);
    context.textAlign = "center";
    context.fillStyle = "#cbd5e1";
    context.fillText("People detected", 0, 0);
    context.restore();
}


function formatTime(value) {
    const date = new Date(value);
    return Number.isNaN(date.getTime())
        ? String(value ?? "")
        : date.toLocaleTimeString();
}


function renderRiskTimeline(samples) {
    riskTimeline.replaceChildren();

    if (!samples.length) {
        riskTimelineMessage.textContent =
            "No risk history available for this source.";
        return;
    }

    // Samples are expected in chronological order.
    const events = [];
    let previousRisk = null;

    for (const sample of samples) {
        const riskLevel = String(
            sample.riskLevel || "UNKNOWN"
        ).toUpperCase();

        if (riskLevel !== previousRisk) {
            events.push({
                ...sample,
                riskLevel,
                eventType: previousRisk === null
                    ? "INITIAL STATE"
                    : "RISK CHANGED",
                previousRisk
            });

            previousRisk = riskLevel;
        }
    }

    // Always include the latest sample, even if its risk did not change.
    const latest = samples[samples.length - 1];
    const latestRisk = String(
        latest.riskLevel || "UNKNOWN"
    ).toUpperCase();

    const lastEvent = events[events.length - 1];

    if (
        !lastEvent ||
        lastEvent.recordedAt !== latest.recordedAt
    ) {
        events.push({
            ...latest,
            riskLevel: latestRisk,
            eventType: "LATEST STATUS",
            previousRisk: null
        });
    }

    riskTimelineMessage.textContent =
        `${events.length} important events from ${samples.length} historical samples.`;

    for (const event of events.slice(-20).reverse()) {
        const item = document.createElement("article");
        const riskLevel = event.riskLevel;

        item.className = "risk-timeline-item";
        item.classList.add(
            "risk-" + riskLevel.toLowerCase()
        );

        const badge = createStatusBadge(riskLevel, "risk");
        const details = document.createElement("div");
        details.className = "risk-timeline-details";

        const heading = document.createElement("strong");

        if (event.eventType === "RISK CHANGED") {
            heading.textContent =
                `${event.previousRisk} → ${riskLevel}`;
        } else {
            heading.textContent =
                `${event.eventType}: ${riskLevel}`;
        }

        const metadata = document.createElement("p");
        metadata.textContent =
            `${Number(event.personCount) || 0} people · ${formatDate(event.recordedAt)}`;

        details.append(heading, metadata);
        item.append(badge, details);
        riskTimeline.appendChild(item);
    }
}

async function loadHistory(force = false) {
    const sourceId = historySource.value;

    if (!sourceId) {
        historyData = [];
        drawPeopleCountChart([]);
        riskTimeline.replaceChildren();
        historyMessage.textContent = "No monitoring source available.";
        riskTimelineMessage.textContent = "No source selected.";
        return;
    }

    if (!force && historyLoadedSource === sourceId) {
        // Continue refreshing the history periodically.
    }

    historyMessage.textContent = `Loading history for ${sourceId}...`;

    try {
        const samples = await apiGet(
            `/api/security/monitoring/sources/${encodeURIComponent(sourceId)}/history`
        );

        historyData = samples;
        historyLoadedSource = sourceId;

        drawPeopleCountChart(historyData);
        renderRiskTimeline(historyData);

        historyMessage.textContent =
            `${historyData.length} samples loaded for ${sourceId}.`;
    } catch (error) {
        historyMessage.textContent = error.message;
        riskTimelineMessage.textContent = "Could not load risk history.";
    }
}

async function refreshDashboard() {
    if (!token || refreshInProgress) {
        return;
    }

    refreshInProgress = true;

    try {
        await Promise.all([loadSources(), loadAlerts()]);
        await loadHistory();
    } finally {
        refreshInProgress = false;
    }
}

refreshDashboard();
setInterval(refreshDashboard, 5000);

window.addEventListener("resize", () => {
    drawPeopleCountChart(historyData);
});




const videoSelector = document.getElementById("videoSelector");
const pipelineEmail = document.getElementById("pipelineEmail");
const pipelinePassword = document.getElementById("pipelinePassword");
const pipelineStatus = document.getElementById("pipelineStatus");
const pipelineMessage = document.getElementById("pipelineMessage");
const startPipelineButton = document.getElementById("startPipelineButton");
const stopPipelineButton = document.getElementById("stopPipelineButton");
const refreshVideosButton = document.getElementById("refreshVideosButton");

async function refreshVideoList() {
    try {
        const videos = await apiGet("/api/security/video/videos");
        const previousValue = videoSelector.value;

        videoSelector.replaceChildren();

        if (!videos.length) {
            videoSelector.add(new Option("No supported videos found", ""));
            pipelineMessage.textContent =
                "Add an MP4, AVI, MOV or MKV file to ai/video.";
            return;
        }

        videoSelector.add(new Option("Select a video", ""));

        videos.forEach(filename => {
            videoSelector.add(new Option(filename, filename));
        });

        if (videos.includes(previousValue)) {
            videoSelector.value = previousValue;
        }

        pipelineMessage.textContent =
            `${videos.length} video(s) available.`;
    } catch (error) {
        pipelineMessage.textContent =
            `Could not load videos: ${error.message}`;
    }
}

async function refreshPipelineStatus() {
    try {
        const status = await apiGet("/api/security/video/status");
        const running = status.status === "RUNNING";

        pipelineStatus.textContent = running
            ? `RUNNING — ${status.filename}`
            : "STOPPED";

        pipelineStatus.classList.toggle("running", running);
        pipelineStatus.classList.toggle("stopped", !running);

        startPipelineButton.disabled = running;
        stopPipelineButton.disabled = !running;
        videoSelector.disabled = running;

        if (!running) {
            pipelinePassword.value = "";
        }
    } catch (error) {
        pipelineMessage.textContent =
            `Could not read pipeline status: ${error.message}`;
    }
}

startPipelineButton.addEventListener("click", async () => {
    const filename = videoSelector.value;
    const email = pipelineEmail.value.trim();
    const password = pipelinePassword.value;

    if (!filename || !email || !password) {
        pipelineMessage.textContent =
            "Select a video and enter your Nexa email and password.";
        return;
    }

    startPipelineButton.disabled = true;
    pipelineMessage.textContent = "Starting AI monitoring...";

    try {
        const result = await apiPost("/api/security/video/start", {
            filename,
            email,
            password
        });

        pipelineMessage.textContent =
            `Pipeline started for ${result.filename}. The AI video window should open shortly.`;

        await refreshPipelineStatus();
    } catch (error) {
        pipelineMessage.textContent =
            `Could not start monitoring: ${error.message}`;
        await refreshPipelineStatus();
    } finally {
        pipelinePassword.value = "";
    }
});

stopPipelineButton.addEventListener("click", async () => {
    stopPipelineButton.disabled = true;
    pipelineMessage.textContent = "Stopping AI monitoring...";

    try {
        const result = await apiPost("/api/security/video/stop", {});

        pipelineMessage.textContent =
            result.status === "STOPPED"
                ? "Monitoring stopped."
                : "No pipeline was running.";

        await refreshPipelineStatus();
    } catch (error) {
        pipelineMessage.textContent =
            `Could not stop monitoring: ${error.message}`;
        await refreshPipelineStatus();
    }
});

refreshVideosButton.addEventListener("click", refreshVideoList);

refreshVideoList();
refreshPipelineStatus();
