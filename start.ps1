# 🚀 E-commerce Product Recommender - Quick Start Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "E-commerce Product Recommender System" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if backend server is already running
$backendRunning = $false
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/users" -Method GET -TimeoutSec 2 -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        $backendRunning = $true
        Write-Host "SUCCESS: Backend is already running on http://127.0.0.1:8000" -ForegroundColor Green
    }
} catch {
    Write-Host "INFO: Backend is not running yet" -ForegroundColor Yellow
}

# Start backend if not running
if (-not $backendRunning) {
    Write-Host ""
    Write-Host "Step 1: Starting Backend Server..." -ForegroundColor Cyan
    Write-Host "---------------------------------------" -ForegroundColor Gray
    
    # Start backend in a new window
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; .\.venv\Scripts\activate; Write-Host 'Backend Server Starting...' -ForegroundColor Green; uvicorn main:app --reload"
    
    Write-Host "Waiting for backend to start..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
    
    # Verify backend started
    $attempts = 0
    $maxAttempts = 10
    while ($attempts -lt $maxAttempts) {
        try {
            $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/users" -Method GET -TimeoutSec 2 -ErrorAction SilentlyContinue
            if ($response.StatusCode -eq 200) {
                Write-Host "SUCCESS: Backend started successfully!" -ForegroundColor Green
                break
            }
        } catch {
            $attempts++
            Write-Host "Waiting... ($attempts/$maxAttempts)" -ForegroundColor Yellow
            Start-Sleep -Seconds 2
        }
    }
}

Write-Host ""
Write-Host "Step 2: Starting Frontend Server..." -ForegroundColor Cyan
Write-Host "---------------------------------------" -ForegroundColor Gray

# Start frontend in a new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\ecommerce-recommender-frontend'; Write-Host 'Frontend Server Starting...' -ForegroundColor Green; npm run dev"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "SERVERS STARTING!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend API:  http://127.0.0.1:8000" -ForegroundColor White
Write-Host "API Docs:     http://127.0.0.1:8000/docs" -ForegroundColor White
Write-Host "Frontend App: http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C in each terminal window to stop the servers" -ForegroundColor Yellow
Write-Host ""
Write-Host "Happy coding! " -ForegroundColor Green
