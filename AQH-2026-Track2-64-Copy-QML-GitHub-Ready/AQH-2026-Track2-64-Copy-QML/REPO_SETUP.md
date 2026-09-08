# GitHub publication

After extracting the repository pack:

```powershell
cd "AQH-2026-Track2-64-Copy-QML"
python .\scripts\validate_repo.py
git init
git branch -M main
git add .
git commit -m "Consolidate AQH Track 2 V9.2 and V12 submissions"
git remote add origin https://github.com/YOUR_USERNAME/AQH-2026-Track2-64-Copy-QML.git
git push -u origin main
```

Or use:

```powershell
.\scripts\publish_to_github.ps1 -RemoteUrl "https://github.com/YOUR_USERNAME/AQH-2026-Track2-64-Copy-QML.git"
```

Recommended GitHub releases:

- `v9.2-incumbent` -> `releases/AQH_Track2_FINAL_SUBMISSION_V9_2_GITHUB_READY.zip`
- `v12.0-research` -> `releases/AQH_Track2_V12_FINAL_SUBMISSION_GITHUB_READY.zip`

Do not attach anything from an organizer-private evaluation directory.
