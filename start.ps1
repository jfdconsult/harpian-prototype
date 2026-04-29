# start.ps1 — HARPIAN Portfolio Engineering Terminal
# Inicializa o banco de dados, sobe a API Flask e o servidor frontend.
# Uso: .\start.ps1

$BASE = $PSScriptRoot
$VENV = "$BASE\venv"
$PORT_API = 5050
$PORT_FE  = 3131

Write-Host ""
Write-Host "============================================================"
Write-Host "  HARPIAN Portfolio Engineering Terminal"
Write-Host "============================================================"
Write-Host ""

# ── Ler .env se existir ────────────────────────────────────────────────────
$ENV_FILE = "$BASE\.env"
if (Test-Path $ENV_FILE) {
    Get-Content $ENV_FILE | ForEach-Object {
        if ($_ -match '^([^#=]+)=(.*)$') {
            [System.Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim(), "Process")
        }
    }
    Write-Host "  [ENV] Loaded from .env"
} else {
    Write-Host "  [WARN] .env not found — copy .env.example to .env and fill in values"
}

# ── Ler ANTHROPIC_API_KEY do registro Windows se não estiver no .env ───────
if (-not $env:ANTHROPIC_API_KEY) {
    try {
        $env:ANTHROPIC_API_KEY = (Get-ItemProperty "HKCU:\Environment" -Name "ANTHROPIC_API_KEY" -ErrorAction Stop).ANTHROPIC_API_KEY
        Write-Host "  [ENV] ANTHROPIC_API_KEY loaded from Windows Registry"
    } catch {
        Write-Host "  [WARN] ANTHROPIC_API_KEY not found — AI features disabled"
    }
}

# ── Ativar venv ────────────────────────────────────────────────────────────
if (-not (Test-Path "$VENV\Scripts\python.exe")) {
    Write-Host "  [SETUP] Creating virtual environment..."
    python -m venv $VENV
    Write-Host "  [SETUP] Installing dependencies..."
    & "$VENV\Scripts\pip.exe" install -r "$BASE\requirements.txt" -q
}

$PYTHON = "$VENV\Scripts\python.exe"

# ── Inicializar banco de dados ─────────────────────────────────────────────
Write-Host "  [DB] Initializing database..."
& $PYTHON "$BASE\backend\harpian_db.py" init 2>&1 | Out-Null
Write-Host "  [DB] Done"

# ── Subir API Flask (background) ──────────────────────────────────────────
Write-Host "  [API] Starting Flask API on http://localhost:$PORT_API ..."
$apiJob = Start-Job -ScriptBlock {
    param($python, $base, $port)
    $env:PORT = $port
    & $python "$base\api\server.py"
} -ArgumentList $PYTHON, $BASE, $PORT_API

Start-Sleep -Seconds 2

# Verificar se a API subiu
try {
    $health = Invoke-RestMethod "http://localhost:$PORT_API/api/health" -TimeoutSec 3
    Write-Host "  [API] Online — demo_mode=$($health.data.demo_mode)"
} catch {
    Write-Host "  [API] Starting (may take a moment)..."
}

# ── Subir frontend (background) ───────────────────────────────────────────
Write-Host "  [FE]  Starting frontend on http://localhost:$PORT_FE ..."
$feJob = Start-Job -ScriptBlock {
    param($base, $port)
    npx serve -l $port $base
} -ArgumentList $BASE, $PORT_FE

Start-Sleep -Seconds 1

Write-Host ""
Write-Host "============================================================"
Write-Host "  Terminal:  http://localhost:$PORT_FE/terminal.html"
Write-Host "  API:       http://localhost:$PORT_API/api/health"
Write-Host "  API Docs:  docs/ARCHITECTURE.md"
Write-Host "============================================================"
Write-Host ""
Write-Host "  Pressione Ctrl+C para encerrar."
Write-Host ""

# ── Abrir browser ─────────────────────────────────────────────────────────
Start-Sleep -Seconds 1
Start-Process "http://localhost:$PORT_FE/terminal.html"

# ── Aguardar ──────────────────────────────────────────────────────────────
try {
    Wait-Job $apiJob, $feJob
} finally {
    Stop-Job $apiJob, $feJob -ErrorAction SilentlyContinue
    Remove-Job $apiJob, $feJob -ErrorAction SilentlyContinue
    Write-Host "  [STOP] Servers stopped."
}
