# DionoAutogen AI - Stop Script for Windows PowerShell
# This script stops all services

Write-Host "=== DionoAutogen AI - Stopping Services ===" -ForegroundColor Yellow
Write-Host ""

docker-compose down

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✓ Services stopped successfully" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "✗ Failed to stop services" -ForegroundColor Red
    exit 1
}
