# DionoAutogen AI - Start Script for Windows PowerShell
# This script starts all services using Docker Compose

Write-Host "=== DionoAutogen AI - Starting Services ===" -ForegroundColor Green
Write-Host ""

# Check if Docker is running
Write-Host "Checking Docker..." -ForegroundColor Yellow
try {
    docker info | Out-Null
    Write-Host "✓ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    Write-Host "  1. Open Docker Desktop from Start Menu" -ForegroundColor Yellow
    Write-Host "  2. Wait for Docker to start (whale icon in system tray)" -ForegroundColor Yellow
    Write-Host "  3. Run this script again" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Starting services..." -ForegroundColor Yellow

# Try Docker Compose v2 first, fall back to v1
Write-Host "Checking Docker Compose version..." -ForegroundColor Yellow
$composeCmd = $null

try {
    docker compose version | Out-Null
    $composeCmd = "docker compose"
    Write-Host "Using Docker Compose v2" -ForegroundColor Green
} catch {
    try {
        docker-compose version | Out-Null
        $composeCmd = "docker-compose"
        Write-Host "Using Docker Compose v1" -ForegroundColor Green
    } catch {
        Write-Host "✗ Docker Compose not found" -ForegroundColor Red
        Write-Host "Please install Docker Desktop which includes Docker Compose" -ForegroundColor Yellow
        exit 1
    }
}

# Start services
& $composeCmd up -d

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=== Services Started Successfully ===" -ForegroundColor Green
    Write-Host ""
    Write-Host "Access the application:" -ForegroundColor Cyan
    Write-Host "  Frontend: http://localhost:3000" -ForegroundColor White
    Write-Host "  Backend:  http://localhost:8000" -ForegroundColor White
    Write-Host "  API Docs: http://localhost:8000/docs" -ForegroundColor White
    Write-Host ""
    Write-Host "Default Login:" -ForegroundColor Cyan
    Write-Host "  Username: demo" -ForegroundColor White
    Write-Host "  Password: demo" -ForegroundColor White
    Write-Host ""
    Write-Host "To stop services, run: .\stop.ps1" -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "✗ Failed to start services" -ForegroundColor Red
    Write-Host "Check the error messages above" -ForegroundColor Yellow
    exit 1
}
