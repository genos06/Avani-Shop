# 🎤 AI Setup for Fertilizer Advisor

6. Click **Save**

### St3. Click **"Redeploy"**

### Step 4: Test the Feature

1. Visit: `https://avani-shop.vercel.app/fertilizer-advisor`
2. Click the microphone button
3. Speak in Hindi/English/Hinglish about:
   - Land size (e.g., "मेरे पास 2 एकड़ जमीन है" or "I have 2 acres")
   - Crops (e.g., "गेहूं की खेती" or "wheat farming")
   - Soil needs (e.g., "मिट्टी में नाइट्रोजन की कमी है")
4. The AI will:
   - Transcribe your speech (Deepgram)
   - Extract structured data (Gemini AI)
   - Calculate precise fertilizer amount using formula: `nutrients × land_acres × 12 kg`
   - Recommend appropriate Avanii productemini API Key to Vercel

1. Get your Gemini API key from: https://aistudio.google.com/app/apikey
2. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
3. Click **Add New Variable**
4. Fill in:
   - **Name**: `GEMINI_API_KEY`
   - **Value**: Your Gemini API key
   - **Environments**: Check all three:
     - ✅ Production
     - ✅ Preview
     - ✅ Development
5. Click **Save**

### Step 3: Redeploy (Optional)Overview

The AI Fertilizer Advisor uses two powerful APIs:
1. **Deepgram** - Speech-to-text for Hindi/English/Hinglish
2. **Gemini AI** - Extracts structured information (land size, nutrients, crops)

## 📋 Setup Instructions

### Step 1: Add Deepgram API Key to Vercel

1. Go to your Vercel Dashboard: https://vercel.com/dashboard
2. Select your project (Avani-Shop)
3. Click **Settings** → **Environment Variables**

#### Add Deepgram API Key

4. Click **Add New Variable**
5. Fill in:
   - **Name**: `DEEPGRAM_API_KEY`
   - **Value**: (Get from https://console.deepgram.com/)
   - **Environments**: Check all three:
     - ✅ Production
     - ✅ Preview
     - ✅ Development
6. Click **Save**

#### Add Gemini API Key

7. Click **Add New Variable** again
8. Fill in:
   - **Name**: `GEMINI_API_KEY`
   - **Value**: (Get from https://aistudio.google.com/apikey)
   - **Environments**: Check all three:
     - ✅ Production
     - ✅ Preview
     - ✅ Development
9. Click **Save**

### Step 2: Redeploy (Optional)

Vercel should automatically redeploy after you push the latest changes. If not:

1. Go to **Deployments** tab
2. Click **"Redeploy"** on the latest deployment
3. Select **"Use existing Build Cache"**
4. Click **"Redeploy"**

### Step 3: Test the Feature

1. Visit: `https://avani-shop.vercel.app/fertilizer-advisor`
2. Click the microphone button
3. Speak in Hindi/English/Hinglish about:
   - Land size (e.g., "मेरे पास 2 एकड़ जमीन है")
   - Crops (e.g., "गेहूं की खेती")
   - Soil needs (e.g., "मिट्टी में नाइट्रोजन की कमी है")
4. The AI will transcribe and recommend fertilizer

## 🔒 Security Notes

- ✅ API keys are stored securely in Vercel environment variables
- ✅ Not exposed in client-side code
- ✅ Protected by `.gitignore` from version control
- ✅ Only accessible server-side in Flask

## 📊 API Usage & Pricing

### Deepgram
- **Free Tier**: 45 minutes of audio per month
- **Pricing**: $0.0125 per minute after free tier
- **Features Used**: Nova-2 model, Hindi language, smart formatting

### Gemini AI
- **Free Tier**: 15 requests per minute, 1 million tokens per month
- **Pricing**: Free for moderate usage
- **Model Used**: gemini-2.0-flash-exp (fast, accurate, multilingual)

## 🌐 Your API Keys

### Deepgram
Get your API key from: https://console.deepgram.com/

**Dashboard**: https://console.deepgram.com/

### Gemini AI
Get your API key from: https://aistudio.google.com/app/apikey

## 🔧 How It Works

1. **User speaks** → Browser records audio
2. **Audio sent to backend** → Flask `/api/transcribe-audio` endpoint
3. **Deepgram transcribes** → Converts speech to Hindi/English/Hinglish text
4. **Gemini AI analyzes** → Extracts:
   - Land size (acres/bigha)
   - Required nutrients (N, P, K)
   - Crop types
   - Soil conditions
5. **Formula calculation** → `nutrients × land_acres × 12 kg`
6. **Product recommendation** → Returns:
   - Product name (e.g., "Avanii NPK Complete")
   - Amount needed (e.g., "72 kg")
   - Reasoning (why this recommendation)

**Fallback**: If Gemini is unavailable, uses keyword-based detection.

## 🔧 How It Works

1. User clicks record button in browser
2. Browser captures audio using MediaRecorder API
3. Audio sent to Flask backend (`/api/transcribe-audio`)
4. **Deepgram** transcribes the audio to text (Hindi/English/Hinglish)
5. Transcription sent to **Gemini AI** to extract:
   - Land size (acres/bigha converted to acres)
   - Nutrients needed (Nitrogen, Phosphorus, Potassium)
   - Crop type and soil condition
6. **Formula**: `Amount = nutrients × land_acres × 12 kg`
7. Recommendation sent back to user with product name, quantity, and explanation

## 📁 Files Modified

- `main.py` - Added Deepgram + Gemini AI integration
- `requirements.txt` - Added `deepgram-sdk==3.2.0`, `python-dotenv==1.0.0`, `google-generativeai==0.3.2`
- `templates/fertilizer-advisor-deepgram.html` - Audio recording UI
- `.env` - Local environment variables (not committed)
- `.gitignore` - Protects sensitive files

## 🐛 Troubleshooting

### "Deepgram API key not configured" Error

**Solution**: Add `DEEPGRAM_API_KEY` in Vercel environment variables.

### "Gemini API key not configured" - Still Works!

**Behavior**: System falls back to keyword-based detection (still functional, but less accurate).

**Solution**: Add `GEMINI_API_KEY` in Vercel for AI-powered extraction.

### "Transcription failed" Error

**Check**:
1. API key is correct in Vercel
2. Microphone permissions granted in browser
3. Audio is being recorded (check browser console)

### Poor Hindi Recognition

**Solution**: The current setup forces Hindi language (`language="hi"`). This should provide best results for Hindi speech.

## 📞 Support

- Deepgram Docs: https://developers.deepgram.com/
- Deepgram Status: https://status.deepgram.com/
- API Dashboard: https://console.deepgram.com/

## ✅ Deployment Checklist

- [x] `.env` file created locally with API keys
- [x] `.gitignore` protects `.env` from commits
- [x] `requirements.txt` updated with dependencies
- [x] Deepgram + Gemini integration added to `main.py`
- [x] New template created (`fertilizer-advisor-deepgram.html`)
- [x] Changes pushed to GitHub
- [ ] `DEEPGRAM_API_KEY` added to Vercel ← **ADD THIS**
- [ ] `GEMINI_API_KEY` added to Vercel ← **ADD THIS**
- [ ] Vercel redeployed automatically
- [ ] Feature tested on production URL

## 🎯 Testing Examples

Try these phrases after deploying:

**Hindi:**
- "मेरे पास 2 एकड़ जमीन है और मैं गेहूं उगा रहा हूं"
- "3 बीघा खेत में टमाटर की खेती, नाइट्रोजन चाहिए"

**English:**
- "I have 5 acres of land for potato farming"
- "Need fertilizer for 1 acre wheat field"

**Hinglish:**
- "Mere paas 2 acre land hai, wheat grow kar raha hoon"
- "4 acre mein tomato farming, phosphorus chahiye"

**Expected Output:**
- Product: "Avanii NPK Complete" or specific mix
- Amount: Calculated as `nutrients × acres × 12 kg`
- Why: AI-generated explanation based on your input

## 🎉 Next Steps

After adding the API key to Vercel:

1. Wait 1-2 minutes for automatic deployment
2. Visit `https://avani-shop.vercel.app/fertilizer-advisor`
3. Test the AI speech recognition
4. Share the link with users!

Your AI-powered fertilizer advisor with Hindi speech recognition is ready! 🚀🌾
