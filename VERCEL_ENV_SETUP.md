# 🚀 Vercel Environment Variables Setup

## ⚠️ IMPORTANT: Add Gemini API Key to Vercel

The `.env` file is NOT pushed to GitHub (protected by `.gitignore`). You must manually add environment variables to Vercel.

## 📋 Step-by-Step Instructions

### Step 1: Go to Vercel Dashboard
1. Visit: https://vercel.com/dashboard
2. Select your project: **Avani-Shop** (or **avanii-shop**)

### Step 2: Add GEMINI_API_KEY

1. Click **Settings** (in top navigation)
2. Click **Environment Variables** (left sidebar)
3. Click **Add New** button
4. Fill in:
   ```
   Key: GEMINI_API_KEY
   Value: AIzaSyB_9GgIcnuEz-40TZmpHEv1Zn5B5u95t7w
   ```
5. Select all environments:
   - ✅ Production
   - ✅ Preview
   - ✅ Development
6. Click **Save**

### Step 3: Verify All Required Environment Variables

Make sure you have ALL of these in Vercel:

| Variable | Status | Value |
|----------|--------|-------|
| `SECRET_KEY` | ✅ Should already exist | Your Flask secret key |
| `DATABASE_URL` | ✅ Should already exist | PostgreSQL connection string |
| `FLASK_ENV` | ✅ Should already exist | `production` |
| `DEEPGRAM_API_KEY` | ⚠️ Check if exists | `19d3d3267970b9826b1d47a8396755d1d63232e1` |
| `GEMINI_API_KEY` | ❌ **ADD THIS NOW** | `AIzaSyB_9GgIcnuEz-40TZmpHEv1Zn5B5u95t7w` |

### Step 4: Redeploy (if needed)

After adding the environment variable:

**Option A: Automatic**
- Vercel should automatically redeploy
- Wait 1-2 minutes

**Option B: Manual**
1. Go to **Deployments** tab
2. Click **⋯** (three dots) on latest deployment
3. Click **Redeploy**
4. Confirm

### Step 5: Test the Feature

1. Visit: `https://avani-shop.vercel.app/fertilizer-advisor`
2. Click the microphone button
3. Speak in Hindi/English about your land size and crops
4. Check if you get fertilizer recommendations

## 🔍 How to Check if It's Working

### Test in Browser Console
1. Open fertilizer advisor page
2. Press F12 (Developer Tools)
3. Go to Console tab
4. Record and speak
5. Look for errors:
   - ❌ "Gemini API key not configured" → Key missing in Vercel
   - ❌ "Contact for consultation" → Gemini not extracting data
   - ✅ Shows product name and amount → Working!

## 🐛 Troubleshooting

### Error: "Gemini API key not configured"
**Problem**: Environment variable not set in Vercel
**Solution**: Follow Step 2 above

### Error: "Contact for consultation (land size not provided)"
**Problem**: Gemini API working but not extracting data properly
**Solution**: Check the transcription - might be speech recognition issue

### Feature works locally but not on Vercel
**Problem**: Environment variable only in local `.env`, not in Vercel
**Solution**: Add to Vercel (Step 2)

## 📸 Screenshots Guide

### Where to find Environment Variables in Vercel:
```
Vercel Dashboard
  → Select Project
    → Settings (top menu)
      → Environment Variables (left sidebar)
        → Add New button
```

### Your Environment Variables should look like:
```
DEEPGRAM_API_KEY     19d3d3267970b9826b1d47a8396755d1d6323...  Production, Preview, Development
GEMINI_API_KEY       AIzaSyB_9GgIcnuEz-40TZmpHEv1Zn5B5u95...  Production, Preview, Development
SECRET_KEY           <your-secret-key>                        Production, Preview, Development
DATABASE_URL         postgresql://...                         Production, Preview, Development
FLASK_ENV            production                               Production, Preview, Development
```

## ✅ Verification Checklist

- [ ] Logged into Vercel dashboard
- [ ] Found project (Avani-Shop)
- [ ] Opened Settings → Environment Variables
- [ ] Added GEMINI_API_KEY with correct value
- [ ] Selected all three environments (Production, Preview, Development)
- [ ] Clicked Save
- [ ] Waited for automatic redeploy OR manually redeployed
- [ ] Tested fertilizer advisor page on production URL
- [ ] Feature working correctly

## 🔐 Security Notes

✅ `.env` file is in `.gitignore` - never pushed to GitHub
✅ API keys only stored in Vercel's secure environment
✅ Not exposed in client-side code
✅ Only accessible to server-side Flask code

## 📞 Need Help?

- Vercel Environment Variables Docs: https://vercel.com/docs/environment-variables
- Your Project Settings: https://vercel.com/[your-username]/avani-shop/settings/environment-variables

---

**Remember**: Local `.env` ≠ Vercel environment variables. They are separate!
