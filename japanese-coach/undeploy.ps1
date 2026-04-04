# 🗑️ Remove Japanese Coach from GitHub Pages
# Easy removal script

param(
    [string]$PowerSyncPath = "",
    [string]$HiddenName = ""
)

Write-Host "🗑️  Japanese Coach Removal Script" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""

# Get PowerSync repo path
if ($PowerSyncPath -eq "") {
    $PowerSyncPath = Read-Host "Enter path to your PowerSync repository"
}

# Verify PowerSync exists
if (-not (Test-Path $PowerSyncPath)) {
    Write-Host "❌ Error: PowerSync path not found: $PowerSyncPath" -ForegroundColor Red
    exit 1
}

# List existing hidden folders
Write-Host "📂 Searching for deployed apps..." -ForegroundColor Yellow
$possibleFolders = @()
Get-ChildItem -Path $PowerSyncPath -Directory | ForEach-Object {
    $folderName = $_.Name
    # Check if it contains our app files
    $hasIndex = Test-Path (Join-Path $_.FullName "index.html")
    $hasApp = Test-Path (Join-Path $_.FullName "app.js")
    $hasKana = Test-Path (Join-Path $_.FullName "kana.js")
    
    if ($hasIndex -and $hasApp -and $hasKana) {
        $possibleFolders += $folderName
    }
}

if ($possibleFolders.Count -eq 0) {
    Write-Host "❌ No deployed Japanese Coach apps found in $PowerSyncPath" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Found deployed apps:" -ForegroundColor Green
for ($i = 0; $i -lt $possibleFolders.Count; $i++) {
    Write-Host "  $($i + 1). $($possibleFolders[$i])" -ForegroundColor White
}

Write-Host ""
$selection = Read-Host "Select folder to remove (1-$($possibleFolders.Count))"
$selectedFolder = $possibleFolders[[int]$selection - 1]

if (-not $selectedFolder) {
    Write-Host "❌ Invalid selection" -ForegroundColor Red
    exit 1
}

$TargetPath = Join-Path $PowerSyncPath $selectedFolder

Write-Host ""
Write-Host "⚠️  WARNING: You are about to DELETE:" -ForegroundColor Red
Write-Host "   $TargetPath" -ForegroundColor Yellow
Write-Host ""
$confirm = Read-Host "Are you sure? Type 'DELETE' to confirm"

if ($confirm -ne "DELETE") {
    Write-Host "❌ Removal cancelled" -ForegroundColor Yellow
    exit 0
}

# Remove folder
Write-Host ""
Write-Host "🗑️  Removing $selectedFolder..." -ForegroundColor Yellow

Push-Location $PowerSyncPath

git rm -r $selectedFolder
$gitRemoveSuccess = $LASTEXITCODE -eq 0

if ($gitRemoveSuccess) {
    Write-Host "✅ Removed from Git" -ForegroundColor Green
    
    git commit -m "Remove hidden tools from /$selectedFolder/"
    git push origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Successfully removed and pushed!" -ForegroundColor Green
        Write-Host "🌐 The page will be offline in 1-2 minutes" -ForegroundColor Cyan
    } else {
        Write-Host ""
        Write-Host "⚠️  Git push failed. Run manually:" -ForegroundColor Yellow
        Write-Host "   git push origin main" -ForegroundColor White
    }
} else {
    Write-Host "⚠️  Git remove failed. Trying manual deletion..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $TargetPath
    Write-Host "✅ Folder deleted locally" -ForegroundColor Green
    Write-Host "⚠️  Remember to commit and push:" -ForegroundColor Yellow
    Write-Host "   git add ." -ForegroundColor White
    Write-Host "   git commit -m 'Remove hidden tools'" -ForegroundColor White
    Write-Host "   git push origin main" -ForegroundColor White
}

Pop-Location

Write-Host ""
Write-Host "✨ Removal complete!" -ForegroundColor Green
