# deploy.ps1 — HARPIAN Deploy Script
# Faz push para jfdconsult/harpian-prototype (origin) E Jinstronda/harpian-front (jp)
# Uso: .\deploy.ps1 "mensagem do commit"

param([string]$msg = "")

$BASE = $PSScriptRoot
$STATIC_FILES = @(
    "terminal.html",
    "presentation-mode.html",
    "behavioral-questionnaire.html",
    "index.html",
    "styles.css",
    "harpian_perf_data.js",
    "harpian_strategies_data.js"
)
$WORKTREE = "C:\Users\jfdco\AppData\Local\Temp\harpian-front-deploy"

Set-Location $BASE

Write-Host ""
Write-Host "============================================================"
Write-Host "  HARPIAN Deploy"
Write-Host "============================================================"

# ── 1. Commit se houver mudancas ─────────────────────────────────────────────
$status = git status --porcelain
if ($status) {
    if (-not $msg) {
        $msg = Read-Host "  Mensagem do commit"
    }
    git add -A
    git commit -m $msg
    if ($LASTEXITCODE -ne 0) { Write-Host "  [ERRO] Commit falhou."; exit 1 }
}

# ── 2. Push para origin (jfdconsult/harpian-prototype) ───────────────────────
Write-Host ""
Write-Host "  [1/2] Push para jfdconsult/harpian-prototype..."
git push origin master
if ($LASTEXITCODE -ne 0) { Write-Host "  [ERRO] Push origin falhou."; exit 1 }
Write-Host "  [OK] origin/master atualizado"

# ── 3. Sync para Jinstronda/harpian-front via worktree ───────────────────────
Write-Host ""
Write-Host "  [2/2] Sincronizando com Jinstronda/harpian-front..."

git fetch jp 2>&1 | Out-Null

# Limpar worktree anterior se existir
if (Test-Path $WORKTREE) {
    git worktree remove $WORKTREE --force 2>&1 | Out-Null
    Remove-Item $WORKTREE -Recurse -Force -ErrorAction SilentlyContinue
}

git worktree add $WORKTREE jp/main 2>&1 | Out-Null
if (-not (Test-Path $WORKTREE)) {
    Write-Host "  [ERRO] Nao foi possivel criar worktree."; exit 1
}

# Copiar arquivos estaticos para public/harpian/
foreach ($f in $STATIC_FILES) {
    $src = "$BASE\$f"
    $dst = "$WORKTREE\public\harpian\$f"
    if (Test-Path $src) {
        Copy-Item $src $dst -Force
    }
}

# Commit e push no worktree
Set-Location $WORKTREE
$diff = git status --porcelain
if ($diff) {
    $deployMsg = if ($msg) { "deploy: $msg" } else { "deploy: sync static files from harpian-prototype" }
    git add public/harpian/
    git -c user.email=jfdconsult@gmail.com -c user.name=jfdconsult commit -m $deployMsg 2>&1 | Out-Null
    git push jp HEAD:main
    if ($LASTEXITCODE -ne 0) { Write-Host "  [ERRO] Push jp falhou."; Set-Location $BASE; exit 1 }
    Write-Host "  [OK] Jinstronda/harpian-front atualizado"
} else {
    Write-Host "  [OK] Jinstronda/harpian-front ja esta atualizado (sem mudancas)"
}

# Limpar worktree
Set-Location $BASE
git worktree remove $WORKTREE --force 2>&1 | Out-Null

Write-Host ""
Write-Host "============================================================"
Write-Host "  Deploy concluido!"
Write-Host "  Producao: https://harpian-front-rho.vercel.app/harpian/terminal.html"
Write-Host "============================================================"
Write-Host ""
