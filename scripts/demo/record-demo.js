#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..', '..');
const VIDEO_DIR = path.join(ROOT, 'demo');
const FIVE_MIN_MODE = process.argv.includes('--five-min');
const OUTPUT_MP4 = path.join(
  VIDEO_DIR,
  FIVE_MIN_MODE ? 'vw-digital-twin-full-demo-5min.mp4' : 'vw-digital-twin-full-demo.mp4'
);

function run(command) {
  return execSync(command, {
    cwd: ROOT,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
    maxBuffer: 20 * 1024 * 1024,
  }).trim();
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function runWithRetry(command, attempts = 30, waitMs = 1500) {
  let lastErr;
  for (let i = 0; i < attempts; i += 1) {
    try {
      return run(command);
    } catch (err) {
      lastErr = err;
      await sleep(waitMs);
    }
  }
  throw lastErr;
}

function compact(text, maxLines = 14) {
  const lines = text.split('\n').filter(Boolean);
  if (lines.length <= maxLines) return lines.join('\n');
  return ['...', ...lines.slice(lines.length - maxLines)].join('\n');
}

function line(title) {
  return `\n### ${title} ###`;
}

async function main() {
  fs.mkdirSync(VIDEO_DIR, { recursive: true });

  const composeOut = run('docker compose up --build -d');
  const composePs = run('docker compose ps --format "table {{.Name}}\\t{{.State}}\\t{{.Ports}}"');

  const healthChecks = [
    ['digital-twin-api (8000)', 'curl -s http://localhost:8000/health'],
    ['anomaly-detection (8001)', 'curl -s http://localhost:8001/health'],
    ['predictive-maintenance (8002)', 'curl -s http://localhost:8002/health'],
    ['alerting-service (8003)', 'curl -s http://localhost:8003/health'],
    ['data-aggregator (8004)', 'curl -s http://localhost:8004/health'],
  ];

  const healthOut = [];
  for (const [name, cmd] of healthChecks) {
    const out = await runWithRetry(cmd);
    healthOut.push(`${name}: ${out}`);
  }

  const telemetryOut = run(
    "curl -s -X POST http://localhost:8000/machines/CNC-001/telemetry -H 'Content-Type: application/json' -H 'x-api-key: dev-key' -d '{\"timestamp\":\"2026-02-04T10:00:00Z\",\"machine_id\":\"CNC-001\",\"data\":{\"spindle\":{\"temperature_c\":95.0,\"rpm\":12000},\"tool\":{\"wear_percent\":85}}}'"
  );
  const latestTelemetryOut = run(
    "curl -s http://localhost:8000/machines/CNC-001/telemetry -H 'x-api-key: dev-key'"
  );
  const historyOut = run(
    "curl -s http://localhost:8000/machines/CNC-001/history -H 'x-api-key: dev-key'"
  );
  const alertsOut = run(
    "curl -s -X POST http://localhost:8000/machines/CNC-001/alerts -H 'Content-Type: application/json' -H 'x-api-key: dev-key' -d '{\"severity\":\"warning\",\"message\":\"Legacy warning demo\",\"metric\":\"spindle.temperature_c\",\"value\":95}'"
  );
  const aggregateLegacyOut = run(
    "curl -s -X POST http://localhost:8000/machines/CNC-001/aggregate -H 'Content-Type: application/json' -H 'x-api-key: dev-key' -d '{\"window_minutes\":5}'"
  );
  const aggregateModernOut = run(
    "curl -s -X POST http://localhost:8000/machines/CNC-001/aggregate -H 'Content-Type: application/json' -H 'x-api-key: dev-key' -d '{\"metric\":\"spindle.temperature_c\",\"windows\":[\"1min\",\"5min\"]}'"
  );

  const anomalyDetectOut = run(
    "curl -s -X POST http://localhost:8001/detect -H 'Content-Type: application/json' -d '{\"telemetry\":[{\"timestamp\":\"2026-02-04T10:00:00Z\",\"machine_id\":\"CNC-001\",\"spindle\":{\"rpm\":12000,\"load_percent\":45,\"temperature_c\":95,\"vibration_mm_s\":7},\"axes\":{\"x\":{\"position_mm\":10,\"velocity_mm_min\":1000},\"y\":{\"position_mm\":20,\"velocity_mm_min\":1000},\"z\":{\"position_mm\":-5,\"velocity_mm_min\":500}},\"tool\":{\"id\":\"T01\",\"type\":\"end_mill\",\"diameter_mm\":10,\"wear_percent\":85,\"runtime_minutes\":120},\"coolant\":{\"flow_rate_lpm\":1,\"temperature_c\":25,\"pressure_bar\":3},\"power\":{\"total_kw\":10,\"spindle_kw\":6,\"servo_kw\":4},\"status\":{\"mode\":\"AUTO\",\"program\":\"O1234\",\"block\":\"N0100\",\"cycle_time_s\":1000}}]}'"
  );

  const predictToolOut = run(
    "curl -s -X POST http://localhost:8002/predict/tool-rul -H 'Content-Type: application/json' -d '{\"machine_id\":\"CNC-001\",\"wear_percent\":85,\"runtime_minutes\":120,\"cutting_speed_m_min\":180}'"
  );
  const predictSpindleOut = run(
    "curl -s -X POST http://localhost:8002/predict/spindle-health -H 'Content-Type: application/json' -d '{\"machine_id\":\"CNC-001\",\"vibration_mm_s\":6.5,\"temperature_c\":88,\"trend_slope\":0.2}'"
  );
  const predictScheduleOut = run(
    "curl -s -X POST http://localhost:8002/predict/maintenance-schedule -H 'Content-Type: application/json' -d '{\"machine_id\":\"CNC-001\",\"wear_percent\":85,\"runtime_minutes\":120,\"cutting_speed_m_min\":180}'"
  );

  const pytestOut = run('.venv/bin/pytest -q');

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1366, height: 768 },
    recordVideo: { dir: VIDEO_DIR, size: { width: 1366, height: 768 } },
  });
  const page = await context.newPage();

  await page.setContent(`
<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<style>
  body { margin: 0; background: #070b18; color: #d7e0ff; font-family: "Courier New", monospace; }
  .frame { padding: 24px; }
  h1 { margin: 0 0 14px 0; font-size: 44px; color: #8bd3ff; }
  .term { border: 1px solid #2a3d66; border-radius: 12px; background: #030712; }
  .bar { background: #0e1b33; padding: 10px 14px; border-bottom: 1px solid #2a3d66; color: #9ab6ff; font-size: 24px; }
  pre { margin: 0; padding: 14px; white-space: pre-wrap; line-height: 1.42; font-size: 24px; height: 620px; overflow-y: auto; }
  .ok { color: #7ee787; }
  .cmd { color: #79c0ff; }
  .sec { color: #f2cc60; }
</style>
</head>
<body>
  <div class="frame">
    <h1>VW Digital Twin - Full Functional Demo</h1>
    <div class="term">
      <div class="bar">Terminal</div>
      <pre id="out"></pre>
    </div>
  </div>
</body>
</html>
  `);

  const script = [
    line('Start Stack'),
    '$ docker compose up --build -d',
    compact(composeOut),
    '',
    '$ docker compose ps',
    composePs,
    '',
    line('Health Checks'),
    '$ curl health endpoints (8000-8004)',
    ...healthOut,
    '',
    line('Digital Twin API'),
    '$ POST /machines/CNC-001/telemetry',
    compact(telemetryOut, 8),
    '$ GET /machines/CNC-001/telemetry',
    compact(latestTelemetryOut, 8),
    '$ GET /machines/CNC-001/history',
    compact(historyOut, 8),
    '$ POST /machines/CNC-001/alerts  (legacy severity=warning)',
    compact(alertsOut, 8),
    '$ POST /machines/CNC-001/aggregate  (legacy window_minutes=5)',
    compact(aggregateLegacyOut, 8),
    '$ POST /machines/CNC-001/aggregate  (modern windows=[1min,5min])',
    compact(aggregateModernOut, 8),
    '',
    line('Anomaly Detection Service'),
    '$ POST /detect',
    compact(anomalyDetectOut, 10),
    '',
    line('Predictive Maintenance Service'),
    '$ POST /predict/tool-rul',
    compact(predictToolOut, 8),
    '$ POST /predict/spindle-health',
    compact(predictSpindleOut, 8),
    '$ POST /predict/maintenance-schedule',
    compact(predictScheduleOut, 8),
    '',
    line('Tests'),
    '$ .venv/bin/pytest -q',
    compact(pytestOut, 6),
    '',
    line('Demo Complete'),
    'All core functions verified in one run.',
  ];

  const timing = FIVE_MIN_MODE
    ? {
        cmdCharMs: 58,
        outCharMs: 17,
        cmdLinePauseMs: 5500,
        outLinePauseMs: 2400,
        finalPauseMs: 26000,
      }
    : {
        cmdCharMs: 7,
        outCharMs: 2,
        cmdLinePauseMs: 500,
        outLinePauseMs: 240,
        finalPauseMs: 5000,
      };

  await page.evaluate(async ({ lines, timing }) => {
    const out = document.getElementById('out');
    const delay = (ms) => new Promise((r) => setTimeout(r, ms));
    for (const line of lines) {
      const span = document.createElement('span');
      if (line.startsWith('$ ')) span.className = 'cmd';
      else if (line.startsWith('###')) span.className = 'sec';
      else if (line.includes('{"status":"ok"}') || line.includes('passed')) span.className = 'ok';
      out.appendChild(span);

      for (const ch of line) {
        span.textContent += ch;
        await delay(line.startsWith('$ ') ? timing.cmdCharMs : timing.outCharMs);
      }
      out.appendChild(document.createTextNode('\n'));
      await delay(line.startsWith('$ ') ? timing.cmdLinePauseMs : timing.outLinePauseMs);
      out.scrollTop = out.scrollHeight;
    }
    await delay(timing.finalPauseMs);
  }, { lines: script, timing });

  const videoPath = await page.video().path();
  await context.close();
  await browser.close();

  execSync(
    `ffmpeg -y -i "${videoPath}" -vf "format=yuv420p" -movflags +faststart "${OUTPUT_MP4}"`,
    { stdio: 'pipe' }
  );

  console.log(`Video created: ${OUTPUT_MP4}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
