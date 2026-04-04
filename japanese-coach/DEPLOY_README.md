# 📦 Deploy Japanese Coach to GitHub Pages (Hidden)

## 🚀 Quick Deployment (Plug & Play)

### Step 1: Copy Files to PowerSync Repo
Copy the entire `deploy-package/` folder to your PowerSync repository:

```powershell
# Navigate to your PowerSync repo
cd "path\to\Powersync"

# Copy the hidden app folder (choose one URL option below)
```

### Step 2: Choose Your Hidden URL

**Option A: Random String (Most Hidden)** 🔒
- Copy to: `/j4p4n3s3-st9dy/`
- URL: `https://reyzasagara.github.io/Powersync/j4p4n3s3-st9dy/`
- Harder to guess, no link from main site

**Option B: Simple Hidden** 🔐
- Copy to: `/study/` or `/learn/`  
- URL: `https://reyzasagara.github.io/Powersync/study/`
- Simple, but still not linked anywhere

**Option C: Date-Based (Rotatable)** 🔄
- Copy to: `/202604/` (current month)
- URL: `https://reyzasagara.github.io/Powersync/202604/`
- Can change monthly for extra security

### Step 3: Deploy

```powershell
# In PowerSync repo
git add j4p4n3s3-st9dy/
git commit -m "Add internal tools"
git push origin main
```

Wait 1-2 minutes for GitHub Pages to rebuild, then access your hidden URL.

---

## 📌 How to Use

1. **Bookmark your hidden URL** - Don't share it publicly
2. **No links from main site** - It's invisible to visitors
3. **Easy removal**: Just delete the folder and push
   ```powershell
   git rm -r j4p4n3s3-st9dy/
   git commit -m "Remove internal tools"
   git push
   ```

---

## 🛡️ Security Notes

- GitHub Pages is **public by default** - Anyone with the URL CAN access it
- Hidden ≠ Private - It's just not discoverable without the link
- For true privacy, consider:
  - Password protection via JavaScript (basic)
  - Move to Netlify/Vercel with password protection
  - Keep it local-only

---

## 📂 Folder Structure

```
Powersync/
├── index.html              (Your main portfolio site)
├── styles.css              (Main site files)
├── script.js               (Main site files)
└── j4p4n3s3-st9dy/        ← Hidden Japanese app (NO LINK TO IT)
    ├── index.html
    ├── app.js
    ├── kana.js
    ├── mnemonics.js
    ├── phrases.js
    └── style.css
```

The hidden folder is completely **self-contained** - it won't affect your main site at all.

---

## ✅ Deployment Checklist

- [ ] Copy `deploy-package/` folder to PowerSync repo with chosen name
- [ ] Verify no links to it from main site (index.html, navigation, etc.)
- [ ] Add `.nojekyll` file in root if not exists (for GitHub Pages)
- [ ] Push to GitHub
- [ ] Test the hidden URL
- [ ] Bookmark the URL securely
- [ ] Delete this DEPLOY_README.md after deployment

---

## 🔧 Quick Commands Reference

```powershell
# Clone PowerSync (if not local)
git clone https://github.com/Reyzasagara/Powersync.git
cd Powersync

# Copy deploy package (EXAMPLE - adjust path)
Copy-Item -Recurse "..\nicetomeetyou\deploy-package\*" ".\j4p4n3s3-st9dy\"

# Deploy
git add .
git commit -m "Add hidden study tools"
git push

# Remove later
git rm -r j4p4n3s3-st9dy
git commit -m "Remove study tools"
git push
```

---

## 🎯 Recommended Hidden URL

I recommend: **`/j4p4n3s3-st9dy/`** (pronounced "japanese-study" in leet speak)

- Not guessable
- Not searchable in Google
- Easy to remember for you
- Professional enough if accidentally discovered
