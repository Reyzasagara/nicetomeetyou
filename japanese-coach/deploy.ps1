# 🚀 Deploy Japanese Coach to GitHub Pages
# Easy plug-and-play deployment script

param(
    [string]$PowerSyncPath = "",
    [string]$HiddenName = "j4p4n3s3-st9dy"
)

Write-Host "📦 Japanese Coach Deployment Script" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Get PowerSync repo path
if ($PowerSyncPath -eq "") {
    $PowerSyncPath = Read-Host "Enter path to your PowerSync repository (e.g., C:\repos\Powersync)"
}

# Verify PowerSync exists
if (-not (Test-Path $PowerSyncPath)) {
    Write-Host "❌ Error: PowerSync path not found: $PowerSyncPath" -ForegroundColor Red
    exit 1
}

# Check if it's a git repo
if (-not (Test-Path "$PowerSyncPath\.git")) {
    Write-Host "⚠️  Warning: $PowerSyncPath is not a Git repository" -ForegroundColor Yellow
    $continue = Read-Host "Continue anyway? (y/n)"
    if ($continue -ne "y") { exit 0 }
}

# Ask for custom hidden name
Write-Host ""
Write-Host "Choose hidden URL name:" -ForegroundColor Yellow
Write-Host "  1. j4p4n3s3-st9dy (recommended - leet speak)" -ForegroundColor Green
Write-Host "  2. study" -ForegroundColor White
Write-Host "  3. learn" -ForegroundColor White
Write-Host "  4. 202604 (date-based)" -ForegroundColor White
Write-Host "  5. Custom name" -ForegroundColor White
$choice = Read-Host "Enter choice (1-5)"

switch ($choice) {
    "1" { $HiddenName = "j4p4n3s3-st9dy" }
    "2" { $HiddenName = "study" }
    "3" { $HiddenName = "learn" }
    "4" { $HiddenName = (Get-Date -Format "yyyyMM") }
    "5" { $HiddenName = Read-Host "Enter custom folder name (no spaces)" }
    default { $HiddenName = "j4p4n3s3-st9dy" }
}

$TargetPath = Join-Path $PowerSyncPath $HiddenName

Write-Host ""
Write-Host "📂 Target: $TargetPath" -ForegroundColor Cyan
Write-Host "🌐 URL: https://reyzasagara.github.io/Powersync/$HiddenName/" -ForegroundColor Cyan
Write-Host ""

# Check if target already exists
if (Test-Path $TargetPath) {
    Write-Host "⚠️  Folder already exists: $TargetPath" -ForegroundColor Yellow
    $overwrite = Read-Host "Overwrite? (y/n)"
    if ($overwrite -eq "y") {
        Remove-Item -Recurse -Force $TargetPath
        Write-Host "✅ Removed old version" -ForegroundColor Green
    } else {
        Write-Host "❌ Deployment cancelled" -ForegroundColor Red
        exit 0
    }
}

# Create target directory
New-Item -ItemType Directory -Path $TargetPath -Force | Out-Null

# Copy all necessary files
$SourcePath = $PSScriptRoot
$FilesToCopy = @(
    "index.html",
    "app.js",
    "kana.js",
    "mnemonics.js",
    "phrases.js",
    "style.css"
)

Write-Host "📦 Copying files..." -ForegroundColor Yellow
foreach ($file in $FilesToCopy) {
    $source = Join-Path $SourcePath $file
    if (Test-Path $source) {
        Copy-Item $source -Destination $TargetPath
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  Missing: $file" -ForegroundColor Yellow
    }
}

# Create .nojekyll if not exists (for GitHub Pages)
$nojekyll = Join-Path $PowerSyncPath ".nojekyll"
if (-not (Test-Path $nojekyll)) {
    New-Item -ItemType File -Path $nojekyll -Force | Out-Null
    Write-Host "✅ Created .nojekyll file" -ForegroundColor Green
}

Write-Host ""
Write-Host "✅ Files copied successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Cyan
Write-Host "  1. cd `"$PowerSyncPath`"" -ForegroundColor White
Write-Host "  2. git add ." -ForegroundColor White
Write-Host "  3. git commit -m `"Add hidden study tools`"" -ForegroundColor White
Write-Host "  4. git push origin main" -ForegroundColor White
Write-Host ""
Write-Host "  5. Wait 1-2 minutes for GitHub Pages to build" -ForegroundColor Yellow
Write-Host "  6. Access: https://reyzasagara.github.io/Powersync/$HiddenName/" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔖 Bookmark your URL and keep it private!" -ForegroundColor Yellow
Write-Host ""

# Ask if user wants to auto-commit
$autoCommit = Read-Host "Run git commands now? (y/n)"
if ($autoCommit -eq "y") {
    Push-Location $PowerSyncPath
    
    Write-Host ""
    Write-Host "Running git commands..." -ForegroundColor Yellow
    
    git add .
    git commit -m "Add hidden Japanese learning tools to /$HiddenName/"
    git push origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Deployed successfully!" -ForegroundColor Green
        Write-Host "🌐 Your app will be live in 1-2 minutes at:" -ForegroundColor Cyan
        Write-Host "   https://reyzasagara.github.io/Powersync/$HiddenName/" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "⚠️  Git push failed. Check your credentials and try manually." -ForegroundColor Yellow
    }
    
    Pop-Location
}

Write-Host ""
Write-Host "✨ Deployment complete!" -ForegroundColor Green
