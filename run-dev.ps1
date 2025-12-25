# Скрипт запускает фронтенд и бэкенд в отдельных окнах PowerShell
# Запуск: .\run-dev.ps1

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Фронтенд
$frontCmd = "cd `"$scriptDir\front`"; npm run dev"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontCmd

# Бэкенд
$backendCmd = "cd `"$scriptDir\backend`"; if (Test-Path .\\venv) { .\\venv\\Scripts\\Activate } ; python manage.py runserver"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCmd

Write-Host "Frontend and backend started in separate PowerShell windows."
