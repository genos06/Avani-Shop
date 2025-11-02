# Quick Reference Card for Deployment

## 📋 Pre-Deployment Checklist

- [ ] Create GitHub account (if you don't have one)
- [ ] Create Render account (use GitHub login)
- [ ] Have GoDaddy domain credentials ready
- [ ] Generate secret key: `python3 generate_secret_key.py`

## 🚀 Quick Deployment Steps

### 1. Push to GitHub
```bash
cd /Users/akshay/Desktop/code/Avani/Avanii/Avanii
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/avanii-shop.git
git push -u origin main
```

### 2. Create PostgreSQL Database on Render
- Dashboard → New + → PostgreSQL
- Name: `avanii-db`
- Region: Choose closest to your users
- Create and copy **Internal Database URL**

### 3. Create Web Service on Render
- Dashboard → New + → Web Service
- Connect GitHub repo
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn main:app`
- Add Environment Variables:
  - `SECRET_KEY`: (generated from generate_secret_key.py)
  - `DATABASE_URL`: (Internal Database URL from step 2)
  - `FLASK_ENV`: `production`

### 4. Initialize Database (Using Render Shell)
```bash
python -c "from main import init_db; init_db()"
python -c "from main import add_sample_data; add_sample_data()"
python setup_admin.py
```

### 5. Connect GoDaddy Domain

**In Render:**
- Settings → Custom Domains → Add your domain

**In GoDaddy DNS Management:**
- Type: `CNAME`
- Name: `www`
- Value: `your-app-name.onrender.com`
- TTL: `600`

For root domain (@):
- Type: `A` or `ALIAS`
- Name: `@`
- Value: (Get from Render)

## 🔗 Important URLs

- Render Dashboard: https://dashboard.render.com
- GoDaddy DNS: https://dcc.godaddy.com/manage/dns
- DNS Checker: https://dnschecker.org
- Your App (after deployment): https://your-app-name.onrender.com

## 🔐 Environment Variables for Render

```
SECRET_KEY=<generated-secret-key>
DATABASE_URL=<postgres-connection-string>
FLASK_ENV=production
```

## 📞 Support

- Render Docs: https://render.com/docs
- Discord: Available if you need help with specific steps

## ⏱️ Expected Timeline

1. Push to GitHub: 2 minutes
2. Create database: 2-3 minutes
3. Deploy web service: 5-10 minutes
4. DNS propagation: 30 minutes - 48 hours (usually 1-2 hours)
5. SSL certificate: Automatic after DNS verification

## 💰 Costs

- First 90 days: FREE
- After 90 days: $7/month for PostgreSQL (optional: $7/month for web service)
- Free tier has 15-min inactivity spin-down (30-50s cold start)

## 🐛 Common Issues

**App won't start:**
- Check environment variables are set
- View logs in Render dashboard

**Database error:**
- Verify DATABASE_URL is correct
- Check database is in same region

**Domain not working:**
- Wait for DNS propagation (up to 48h)
- Verify DNS records in GoDaddy
- Check domain is added in Render

**403/404 errors:**
- Ensure all routes are working locally first
- Check static files are in correct location
