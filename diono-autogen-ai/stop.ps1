# DionoAutogen AI - Stop Script for Windows PowerShell
# This script stops all services

Write-Host "=== DionoAutogen AI - Stopping Services ===" -ForegroundColor Yellow
Write-Host ""

# Try Docker Compose v2 first, fall back to v1
$composeCmd = $null

try {
    docker compose version | Out-Null
    $composeCmd = "docker compose"
} catch {
    try {
        docker-compose version | Out-Null
        $composeCmd = "docker-compose"
    } catch {
        Write-Host "✗ Docker Compose not found" -ForegroundColor Red
        exit 1
    }
}

& $composeCmd down

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✓ Services stopped successfully" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "✗ Failed to stop services" -ForegroundColor Red
    exit 1
}
