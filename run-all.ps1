<#
run-all.ps1
Universal PowerShell script to run frontend (Next.js) and backend (Django) locally.
Usage:
  .\run-all.ps1            - runs frontend and backend (by default installs dependencies if needed)
  .\run-all.ps1 -NoInstall - runs without npm/pnpm / pip install
  .\run-all.ps1 -Docker    - if docker-compose.yml is present, runs docker-compose up --build
  .\run-all.ps1 -Stop      - stops processes started by the previous run (reads .run-all-pids.json)

Operation principle:
- Checks for the presence of `backend` and `front` folders.
- Checks availability of python and npm/pnpm.
- If needed, creates a virtual environment in `backend/.venv` and installs dependencies.
- Installs frontend dependencies via pnpm (if available and lock file is present) or npm.
- Starts backend and frontend in separate PowerShell windows (Start-Process) and writes PID to `.run-all-pids.json`.
- Supports safe stopping with the -Stop flag (stops PID and removes the file).

Limitations and assumptions:
- The script is designed to run in Windows PowerShell (by default in your environment).
- For the virtual environment, `python -m venv` is used followed by the full path to `...\.venv\Scripts\python.exe`.
- If you prefer to run inside a single window (so-called "attached"), you can later adapt the script.
#>

param(
    [switch]$Stop,
    [switch]$Docker,
    [switch]$NoInstall
)

$root = Get-Location
$scriptDir = $root.Path
$pidFile = Join-Path $scriptDir '.run-all-pids.json'

function ExitWithError([string]$msg) {
    Write-Host "ERROR: $msg" -ForegroundColor Red
    exit 1
}

if ($Stop) {
    if (-not (Test-Path $pidFile)) {
        Write-Host "PID file not found: $pidFile. Nothing to stop." -ForegroundColor Yellow
        exit 0
    }
    try {
        $data = Get-Content $pidFile -Raw | ConvertFrom-Json
        foreach ($k in $data.PSObject.Properties.Name) {
            $pid = $data.$k
            if ($pid -and (Get-Process -Id $pid -ErrorAction SilentlyContinue)) {
                Write-Host "Stopping process $k (PID $pid) ..."
                Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
            } else {
                Write-Host "Process $k (PID $pid) not found or already stopped." -ForegroundColor Yellow
            }
        }
        Remove-Item $pidFile -ErrorAction SilentlyContinue
        Write-Host "Stopped and removed $pidFile" -ForegroundColor Green
    } catch {
        ExitWithError "Failed to stop processes: $_"
    }
    exit 0
}

if ($Docker) {
    if (Test-Path (Join-Path $scriptDir 'docker-compose.yml')) {
        Write-Host "Running docker-compose up --build (may require elevated privileges)..." -ForegroundColor Cyan
        docker-compose up --build
        exit 0
    } else {
        ExitWithError "docker-compose.yml not found in project root."
    }
}

# Check project structure
if (-not (Test-Path (Join-Path $scriptDir 'backend'))) { ExitWithError "Folder 'backend' not found in project root." }
if (-not (Test-Path (Join-Path $scriptDir 'front')))   { ExitWithError "Folder 'front' not found in project root." }

# Check python
$pyCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pyCmd) { ExitWithError "Python not found in PATH. Install Python and retry." }

# Prepare backend venv and dependencies
$backendRoot = (Resolve-Path (Join-Path $scriptDir 'backend')).Path
$venvPath = Join-Path $backendRoot 'venv'
$pythonVenvExe = Join-Path $venvPath 'Scripts\python.exe'
$activateScript = Join-Path $venvPath 'Scripts\Activate.ps1'
$requirements = Join-Path $backendRoot 'requirements.txt'

if (-not (Test-Path $pythonVenvExe)) {
    if ($NoInstall) {
        ExitWithError "Virtual environment not found ($pythonVenvExe) and installation is disabled by -NoInstall."
    }
    $create = Read-Host "Virtual environment not found in backend/venv. Create and install dependencies? [Y/n]"
    if ($create -eq '' -or $create.ToLower() -in @('y','yes')) {
        Write-Host "Creating virtual environment at $venvPath ..."
        & python -m venv $venvPath
        if (-not (Test-Path $pythonVenvExe)) { ExitWithError "Failed to create virtual environment." }
        Write-Host "Upgrading pip and installing requirements from requirements.txt ..."
        & $pythonVenvExe -m pip install --upgrade pip
        if (Test-Path $requirements) {
            & $pythonVenvExe -m pip install -r $requirements
        } else {
            Write-Host "requirements.txt not found at $requirements. Skipping pip dependency installation." -ForegroundColor Yellow
        }
    } else {
        ExitWithError "Aborted by user choice."
    }
} else {
    if (-not $NoInstall -and (Test-Path $requirements)) {
        $installDeps = Read-Host "Virtual environment found. Run 'pip install -r requirements.txt'? [Y/n]"
        if ($installDeps -eq '' -or $installDeps.ToLower() -in @('y','yes')) {
            Write-Host "Installing/updating pip dependencies..."
            & $pythonVenvExe -m pip install -r $requirements
        }
    }
}

# Frontend package manager (use npm per user request)
$frontRoot = (Resolve-Path (Join-Path $scriptDir 'front')).Path
$npmCmd = Get-Command npm -ErrorAction SilentlyContinue
if (-not $npmCmd) { ExitWithError "npm not found in PATH. Install Node.js/npm and retry." }

if (-not $NoInstall) {
    $doInstall = Read-Host "Install frontend dependencies in 'front/' (npm install)? [Y/n]"
    if ($doInstall -eq '' -or $doInstall.ToLower() -in @('y','yes')) {
        Write-Host "Using npm to install frontend dependencies."
        Push-Location $frontRoot
        npm install
        Pop-Location
    } else {
        Write-Host "Skipping frontend dependency installation (NoInstall or user choice)." -ForegroundColor Yellow
    }
}

# Run commands
$pythonExeToUse = $pythonVenvExe
if (-not (Test-Path $pythonExeToUse)) { # fallback to system python
    $pythonExeToUse = (Get-Command python).Source
}

# Backend: activate venv via Activate.ps1 and run manage.py
$backendCommand = ". `"$activateScript`"; python manage.py runserver 0.0.0.0:8000"
# Frontend: npm run dev as requested by user
$frontendCommand = 'npm run dev'

Write-Host "Starting backend and frontend in separate PowerShell windows..." -ForegroundColor Cyan

# Start backend in new window
$backendFull = $backendRoot
$backendArgs = "-NoProfile -NoExit -Command Set-Location -LiteralPath `"$backendFull`"; $backendCommand"
$backendProc = Start-Process -FilePath "powershell" -ArgumentList $backendArgs -WorkingDirectory $backendFull -PassThru

# Start frontend in new window
$frontFull = $frontRoot
$frontArgs = "-NoProfile -NoExit -Command Set-Location -LiteralPath `"$frontFull`"; $frontendCommand"
$frontProc = Start-Process -FilePath "powershell" -ArgumentList $frontArgs -WorkingDirectory $frontFull -PassThru

# Save PIDs for later stop
$pids = @{ backend = $backendProc.Id; frontend = $frontProc.Id } | ConvertTo-Json
Set-Content -Path $pidFile -Value $pids

Write-Host "Backend PID: $($backendProc.Id)" -ForegroundColor Green
Write-Host "Frontend PID: $($frontProc.Id)" -ForegroundColor Green
Write-Host "PIDs saved to $pidFile" -ForegroundColor Green

Write-Host "Open browser: backend -> http://localhost:8000, frontend -> http://localhost:3000 (or the port your frontend uses)." -ForegroundColor Cyan
Write-Host "To stop both later: .\run-all.ps1 -Stop" -ForegroundColor Cyan

# End
