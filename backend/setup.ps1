# PowerShell setup script for Windows users

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "E-Commerce Product Recommender - Quick Setup" -ForegroundColor Cyan
Write-Host "============================================================`n" -ForegroundColor Cyan

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python not found! Please install Python 3.8 or higher." -ForegroundColor Red
    exit 1
}
Write-Host "SUCCESS: Python found!`n" -ForegroundColor Green

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists`n" -ForegroundColor Gray
} else {
    python -m venv venv
    Write-Host "SUCCESS: Virtual environment created!`n" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "SUCCESS: Virtual environment activated!`n" -ForegroundColor Green

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies!" -ForegroundColor Red
    exit 1
}
Write-Host "SUCCESS: Dependencies installed!`n" -ForegroundColor Green

# Create .env file
Write-Host "Setting up environment file..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host ".env file already exists`n" -ForegroundColor Gray
} else {
    Copy-Item ".env.example" ".env"
    Write-Host "SUCCESS: .env file created!" -ForegroundColor Green
    Write-Host "WARNING: Please add your OpenAI API key to .env`n" -ForegroundColor Magenta
}

# Initialize database
Write-Host "Initializing database..." -ForegroundColor Yellow
python database.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to initialize database!" -ForegroundColor Red
    exit 1
}
Write-Host "SUCCESS: Database initialized and seeded!`n" -ForegroundColor Green

# Summary
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "============================================================`n" -ForegroundColor Cyan

Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Edit .env and add your OpenAI API key (optional)" -ForegroundColor White
Write-Host "   2. Run: " -NoNewline -ForegroundColor White
Write-Host "uvicorn main:app --reload" -ForegroundColor Cyan
Write-Host "   3. Visit: " -NoNewline -ForegroundColor White
Write-Host "http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "   4. Try API: " -NoNewline -ForegroundColor White
Write-Host "http://localhost:8000/recommend/1" -ForegroundColor Cyan

Write-Host "`nTip: The system works without OpenAI API, but explanations will be basic" -ForegroundColor Gray
Write-Host "Happy coding!`n" -ForegroundColor Green
