# Deployment Guide: Deploying Avanii to Render with Custom GoDaddy Domain

This guide will walk you through deploying your Flask application to Render and connecting your custom GoDaddy domain.

## Part 1: Preparing Your Application for Deployment

### Step 1: Update Your Flask Configuration

Before deploying, you need to make your app production-ready. The current setup uses SQLite, which won't persist on Render's free tier. For production, you should use PostgreSQL.

### Step 2: Install Required Dependencies Locally (Optional - for testing)

```bash
pip install -r requirements.txt
```

## Part 2: Deploy to Render

### Step 1: Create a GitHub Repository

1. Go to [GitHub](https://github.com) and create a new repository
2. Name it something like `avanii-shop`
3. Don't initialize with README (since you already have code)

### Step 2: Push Your Code to GitHub

In your terminal, navigate to your project folder and run:

```bash
cd /Users/akshay/Desktop/code/Avani/Avanii/Avanii
git init
git add .
git commit -m "Initial commit for Render deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/avanii-shop.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

### Step 3: Create a Render Account

1. Go to [Render](https://render.com)
2. Sign up using your GitHub account (recommended for easy integration)

### Step 4: Create a PostgreSQL Database on Render

1. From your Render dashboard, click **"New +"** → **"PostgreSQL"**
2. Configure the database:
   - **Name**: `avanii-db`
   - **Database**: `avanii_production`
   - **User**: `avanii_user`
   - **Region**: Choose closest to your users (e.g., Singapore for India)
   - **Plan**: Free (or paid for better performance)
3. Click **"Create Database"**
4. Wait for the database to be created
5. Copy the **Internal Database URL** (you'll need this)

### Step 5: Create a Web Service on Render

1. From your Render dashboard, click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure the web service:
   - **Name**: `avanii-shop`
   - **Region**: Same as your database
   - **Branch**: `main`
   - **Root Directory**: Leave blank (or specify if your code is in a subdirectory)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn main:app`
   - **Plan**: Free (or paid for better performance)

4. Add Environment Variables:
   - Click **"Add Environment Variable"**
   - Add these variables:
     - `SECRET_KEY`: Generate a random secret key (use: `python -c "import secrets; print(secrets.token_hex(32))"`)
     - `DATABASE_URL`: Paste the Internal Database URL from your PostgreSQL database
     - `FLASK_ENV`: `production`

5. Click **"Create Web Service"**

### Step 6: Wait for Deployment

Render will now build and deploy your application. This may take 5-10 minutes. You can watch the logs in real-time.

Once deployed, you'll get a URL like: `https://avanii-shop.onrender.com`

## Part 3: Update Your App to Use PostgreSQL

You need to modify `main.py` to use PostgreSQL instead of SQLite in production. The DATABASE_URL from Render will be in the format: `postgres://...` but SQLAlchemy requires `postgresql://...`

**Important Note**: I'll create an updated version of your main.py file that handles this automatically.

## Part 4: Connect Your GoDaddy Custom Domain

### Step 1: Get Your Render Web Service URL

1. Go to your web service dashboard on Render
2. Under **"Settings"** → **"Custom Domains"**, click **"Add Custom Domain"**
3. Enter your domain name (e.g., `yourdomain.com` or `www.yourdomain.com`)
4. Render will provide you with DNS records to add

### Step 2: Configure DNS in GoDaddy

1. Log in to your [GoDaddy Account](https://www.godaddy.com)
2. Go to **"My Products"** → Find your domain → Click **"DNS"**
3. You'll need to add/modify these DNS records:

**For root domain (yourdomain.com):**
- Type: `CNAME` or `A`
- Name: `@`
- Value: Your Render service URL (copy from Render dashboard)
- TTL: `600` seconds (or default)

**For www subdomain (www.yourdomain.com):**
- Type: `CNAME`
- Name: `www`
- Value: Your Render service URL (e.g., `avanii-shop.onrender.com`)
- TTL: `600` seconds (or default)

4. Click **"Save"**

**Note**: DNS changes can take 24-48 hours to propagate, but often happen within 30 minutes to a few hours.

### Step 3: Verify in Render

1. Go back to Render dashboard
2. Under **"Custom Domains"**, click **"Verify"** next to your domain
3. Render will check the DNS records
4. Once verified, Render will automatically provision an SSL certificate (HTTPS)

## Part 5: Initialize Your Production Database

After deployment, you need to initialize the database with tables and optionally add sample data.

### Option 1: Using Render Shell (Recommended)

1. Go to your web service on Render
2. Click **"Shell"** in the top right
3. Run these commands:
```bash
python -c "from main import init_db; init_db()"
python -c "from main import add_sample_data; add_sample_data()"
```

### Option 2: Add an initialization route (temporary)

You can add a temporary route to initialize the database, then remove it after use.

## Part 6: Set Up Admin Account

After initializing the database, you need to create an admin account:

```bash
python setup_admin.py
```

Or use the Render shell to run Python commands to create an admin user.

## Troubleshooting

### Issue: App crashes on startup
- Check the logs in Render dashboard
- Verify all environment variables are set correctly
- Ensure DATABASE_URL is correct

### Issue: Database connection fails
- Make sure the DATABASE_URL is using `postgresql://` not `postgres://`
- Verify the database is in the same region as your web service
- Check database status in Render dashboard

### Issue: Static files not loading
- Ensure all paths in your templates use `url_for('static', filename='...')`
- Check that static files are committed to git

### Issue: Domain not connecting
- Wait 24-48 hours for DNS propagation
- Use [DNS Checker](https://dnschecker.org) to verify DNS propagation
- Verify DNS records are correct in GoDaddy
- Make sure you added the domain in Render's Custom Domains section

## Post-Deployment Checklist

- [ ] Application is running on Render
- [ ] Database is connected and working
- [ ] Admin account created
- [ ] Sample data loaded (if desired)
- [ ] Custom domain connected
- [ ] SSL certificate active (HTTPS working)
- [ ] Test all functionality (login, shop, cart, checkout)
- [ ] Monitor logs for any errors

## Costs

### Render Free Tier Limitations:
- Web service: 750 hours/month (enough for 1 site running 24/7)
- PostgreSQL: 90 days free, then $7/month
- Services spin down after 15 minutes of inactivity (30-50 second cold start)

### Paid Options:
- **Starter ($7/month)**: No spin down, better performance
- **PostgreSQL ($7/month)**: Required after 90-day trial

## Security Recommendations

1. **Change the SECRET_KEY**: Never use the default one in production
2. **Use strong admin password**: Change default admin credentials
3. **Enable HTTPS**: Render provides free SSL certificates
4. **Regular backups**: Download database backups regularly from Render
5. **Environment variables**: Never commit sensitive data to GitHub

## Need Help?

- Render Documentation: https://render.com/docs
- GoDaddy Support: https://www.godaddy.com/help
- Flask Documentation: https://flask.palletsprojects.com/

## Next Steps

After successful deployment:
1. Test all features thoroughly
2. Set up monitoring and alerts
3. Configure database backups
4. Set up a staging environment for testing changes
5. Consider using a CDN for static assets
