Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendDir = Resolve-Path -LiteralPath (Join-Path $scriptDir "..")
Set-Location $backendDir

if (-not (Test-Path -LiteralPath ".\.venv\Scripts\python.exe")) {
    throw "Python virtual environment not found: backend\.venv"
}

.\.venv\Scripts\python.exe -m alembic upgrade head
