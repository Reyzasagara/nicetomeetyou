# 🚀 QUICK START - Deploy to GitHub Pages

## ✨ Easiest Method (Recommended)

### Step 1: Run Deploy Script
```powershell
cd "c:\Users\rag\PT. Dharma Polimetal\PowerSync - Dokumen\PersonalBio\nicetomeetyou\japanese-coach"

.\deploy.ps1
```

The script will ask you:
1. **PowerSync repo path** - Where is your PowerSync folder?
2. **Hidden URL name** - Choose from preset options or enter custom
3. **Auto-deploy** - Want to automatically run git commands?

### Step 2: Access Your App
Wait 1-2 minutes, then visit:
```
https://reyzasagara.github.io/Powersync/j4p4n3s3-st9dy/
```

### Step 3: Bookmark It! 🔖
Save this URL privately - it's not linked anywhere on your main site.

---

## 🗑️ Remove Later (If Needed)

```powershell
.\undeploy.ps1
```

Script will find and remove the deployed app automatically.

---

## 📦 Manual Method (If Script Fails)

### 1. Copy Files Manually
```powershell
# Create hidden folder in PowerSync
mkdir "C:\path\to\Powersync\j4p4n3s3-st9dy"

# Copy these 6 files:
Copy-Item index.html "C:\path\to\Powersync\j4p4n3s3-st9dy\"
Copy-Item app.js "C:\path\to\Powersync\j4p4n3s3-st9dy\"
Copy-Item kana.js "C:\path\to\Powersync\j4p4n3s3-st9dy\"
Copy-Item mnemonics.js "C:\path\to\Powersync\j4p4n3s3-st9dy\"
Copy-Item phrases.js "C:\path\to\Powersync\j4p4n3s3-st9dy\"
Copy-Item style.css "C:\path\to\Powersync\j4p4n3s3-st9dy\"
```

### 2. Create .nojekyll (if not exists)
```powershell
cd "C:\path\to\Powersync"
New-Item -ItemType File ".nojekyll"
```

### 3. Deploy to GitHub
```powershell
git add .
git commit -m "Add hidden study tools"
git push origin main
```

### 4. Done! 🎉
Access at: `https://reyzasagara.github.io/Powersync/j4p4n3s3-st9dy/`

---

## 🎯 Hidden URL Options

Pick one you like:

| URL | Description | Privacy Level |
|-----|-------------|---------------|
| `/j4p4n3s3-st9dy/` | Leet speak "japanese-study" | ⭐⭐⭐⭐⭐ Most Hidden |
| `/study/` | Simple, clean | ⭐⭐⭐ Moderate |
| `/202604/` | Date-based (current month) | ⭐⭐⭐⭐ High |
| `/learn-jp/` | Descriptive | ⭐⭐ Low |
| `/rz-study/` | Your initials | ⭐⭐⭐⭐ High |

**Recommendation:** Use `/j4p4n3s3-st9dy/` - hard to guess, easy for you to remember.

---

## ✅ Checklist

- [ ] Run `deploy.ps1` script
- [ ] Wait 1-2 minutes for GitHub Pages to build
- [ ] Test the hidden URL in browser
- [ ] Bookmark the URL privately
- [ ] Verify no links to it from main site
- [ ] Start studying! 📚✨

---

## 🔧 Troubleshooting

**Script execution error?**
```powershell
# Enable script execution
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

**GitHub Pages not working?**
- Check GitHub repo settings → Pages → Make sure it's enabled
- Source should be "main" branch, "/" (root) folder
- Wait up to 5 minutes for first-time builds

**404 Error on hidden URL?**
- Make sure you pushed to GitHub
- Check the folder name matches your URL
- Verify `.nojekyll` file exists in repo root

**Files not updating?**
- Hard refresh: `Ctrl + Shift + R`
- Clear browser cache
- Wait a few minutes for GitHub to rebuild

---

## 📱 Pro Tips

1. **Mobile Access**: The app is fully responsive - works great on phone!
2. **Offline**: After first load, most features work offline
3. **Data Sync**: Your progress is saved in browser localStorage
4. **Multiple Devices**: Use same URL on phone/tablet/laptop (progress won't sync between devices)
5. **Backup Progress**: Use the History tab to export your study data

---

## 🎓 Ready to Study!

Your app is now:
- ✅ Hidden from public view
- ✅ Not linked anywhere on main site
- ✅ Only you know the URL
- ✅ Fully functional
- ✅ Easy to remove later

頑張って！(Good luck with your Japanese studies!) 🇯🇵
