param(
    [Parameter(Mandatory=$true)][string]$RemoteUrl
)
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
python .\scripts\validate_repo.py
if (-not (Test-Path .git)) { git init; git branch -M main }
git add .
git status
git commit -m "Consolidate AQH Track 2 V9.2 and V12 submissions"
$hasOrigin = git remote | Select-String '^origin$'
if ($hasOrigin) { git remote set-url origin $RemoteUrl } else { git remote add origin $RemoteUrl }
git push -u origin main
