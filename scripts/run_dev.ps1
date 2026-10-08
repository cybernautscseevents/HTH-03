# ClinScribe AI — Development Launcher (PowerShell)
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " ClinScribe AI — Ambient Clinical Intelligence (Indian OPD) " -ForegroundColor Green
Write-Host " 'From Conversation to Clinical Intelligence.'             " -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Start FastAPI backend
Write-Host "`n[1/2] Starting FastAPI Backend on http://localhost:8000..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\..\apps\api'; & 'C:\Program Files\Python313\python.exe' -m uvicorn main:app --reload --port 8000"

# 2. Start Next.js frontend
Write-Host "[2/2] Starting Next.js Web App on http://localhost:3000..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\..\apps\web'; npm run dev"

Write-Host "`nClinScribe AI services launched!" -ForegroundColor Green
Write-Host "Backend API:  http://localhost:8000 (Docs: http://localhost:8000/docs)" -ForegroundColor White
Write-Host "Frontend Web: http://localhost:3000" -ForegroundColor White
