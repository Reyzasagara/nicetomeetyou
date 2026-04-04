# 🔐 Optional Password Protection Setup

If you want basic password protection (to prevent casual discovery), follow these steps:

## ⚠️ Important Notes
- This is **client-side JavaScript** protection - NOT truly secure
- Anyone can view the password in the HTML source code
- It's just to prevent **casual visitors** from accessing your app
- For real security, use server-side authentication or keep it local only

## 🚀 Setup Steps

### 1. Choose Your Password
Edit `password_protection.html` line 109:
```javascript
const CORRECT_PASSWORD = 'study2026'; // 👈 CHANGE THIS!
```
Change `'study2026'` to your own password (e.g., `'reyza123'`, `'N5Master'`, etc.)

### 2. Rename Files
In your deployed folder:
```powershell
# Rename the main app
Rename-Item "index.html" "app.html"

# Rename the password page to be the entry point
Rename-Item "password_protection.html" "index.html"
```

### 3. File Structure After Setup
```
j4p4n3s3-st9dy/
├── index.html          ← Password page (entry point)
├── app.html            ← Main Japanese Coach app (protected)
├── app.js
├── kana.js
├── mnemonics.js
├── phrases.js
└── style.css
```

### 4. Deploy
```powershell
git add .
git commit -m "Add password protection"
git push
```

### 5. Access
1. Go to: `https://reyzasagara.github.io/Powersync/j4p4n3s3-st9dy/`
2. Enter your password
3. 🎉 Redirected to the app!

---

## 🔓 Remove Password Protection

If you want to remove the password later:

```powershell
# Restore original names
Rename-Item "index.html" "password_protection.html"
Rename-Item "app.html" "index.html"

# Or just delete the password file
Remove-Item "password_protection.html"

git add .
git commit -m "Remove password protection"
git push
```

---

## 💡 Alternative: No Password, Just Hidden URL

**Recommended approach for your use case:**
- Don't link to the page from your main site
- Use a non-obvious URL like `/j4p4n3s3-st9dy/`
- Keep the URL bookmarked privately
- No password needed (simpler, faster access)
- Still not discoverable by visitors

**Why this works:**
- GitHub Pages doesn't generate a sitemap for unlisted pages
- Search engines won't find it without links pointing to it  
- Visitors would need to guess the exact URL
- Much simpler than password protection

**Trade-off:**
- If someone gets your URL, they can access it
- But who would guess `/j4p4n3s3-st9dy/`? 😄

---

## 🎯 Recommendation

For your study app, I recommend **NO password protection**:
1. Use hidden URL: `/j4p4n3s3-st9dy/`
2. Don't link to it from your main site
3. Bookmark it privately in your browser
4. ✅ Simple, fast, and good enough

Only add password protection if you're genuinely worried someone might discover/share the URL.
