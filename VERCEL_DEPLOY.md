# Deploy Avanii Shop to Vercel

This guide will help you deploy your Flask e-commerce application to Vercel.

## 📋 Pre-Deployment Checklist

- [ ] Vercel account (sign up at https://vercel.com)
- [ ] GitHub account
- [ ] PostgreSQL database (can use Vercel Postgres, Neon, or Supabase)
- [ ] Generated SECRET_KEY

## 🚀 Deployment Steps

### 1. Generate Secret Key

```bash
python3 generate_secret_key.py
```

Save the generated secret key - you'll need it for environment variables.

### 2. Set Up PostgreSQL Database

You have several options for PostgreSQL:

#### Option A: Vercel Postgres (Recommended)
1. Go to your Vercel dashboard
2. Select your project → Storage → Create Database
3. Choose Postgres
4. Copy the connection string (starts with `postgres://`)

#### Option B: Neon (Free Tier Available)
1. Go to https://neon.tech
2. Create a new project
3. Copy the connection string

#### Option C: Supabase (Free Tier Available)
1. Go to https://supabase.com
2. Create a new project
3. Go to Project Settings → Database
4. Copy the connection string (use "Connection pooling" for production)

### 3. Push Code to GitHub

```bash
cd /Users/akshay/Desktop/code/deployment
git init
git add .
git commit -m "Deploy to Vercel"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/avanii-shop.git
git push -u origin main
```

### 4. Deploy to Vercel

#### Method 1: Via Vercel Dashboard (Easier)

1. Go to https://vercel.com/dashboard
2. Click **"Add New..."** → **"Project"**
3. Import your GitHub repository
4. Configure your project:
   - **Framework Preset**: Other
   - **Root Directory**: ./
   - **Build Command**: (leave empty)
   - **Output Directory**: (leave empty)

5. Add Environment Variables:
   - Click **"Environment Variables"**
   - Add the following:
     ```
     SECRET_KEY=your-generated-secret-key
     DATABASE_URL=your-postgres-connection-string
     FLASK_ENV=production
     ```

6. Click **"Deploy"**

#### Method 2: Via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# Add environment variables
vercel env add SECRET_KEY
vercel env add DATABASE_URL
vercel env add FLASK_ENV

# Deploy to production
vercel --prod
```

### 5. Initialize Database

After deployment, you need to initialize your database. Use Vercel's shell or run locally with production DATABASE_URL:

```bash
# Set your production DATABASE_URL temporarily
export DATABASE_URL="your-production-database-url"

# Initialize database
python3 -c "from main import init_db; init_db()"

# Add sample data (optional)
python3 -c "from main import add_sample_data; add_sample_data()"

# Create admin user
python3 setup_admin.py
```

Or use Vercel CLI:
```bash
vercel env pull .env.local
python3 -c "from main import init_db; init_db()"
python3 -c "from main import add_sample_data; add_sample_data()"
python3 setup_admin.py
```

### 6. Configure Custom Domain (Optional)

#### In Vercel Dashboard:
1. Go to your project → Settings → Domains
2. Add your custom domain (e.g., avanii.com or www.avanii.com)
3. Follow Vercel's instructions to update your DNS settings

#### In Your Domain Provider (GoDaddy, Namecheap, etc.):
- **For subdomain (www):**
  - Type: `CNAME`
  - Name: `www`
  - Value: `cname.vercel-dns.com`

- **For root domain (@):**
  - Type: `A`
  - Name: `@`
  - Value: `76.76.21.21`

## 🔐 Environment Variables

Make sure these are set in Vercel:

```env
SECRET_KEY=<your-generated-secret-key>
DATABASE_URL=<postgresql-connection-string>
FLASK_ENV=production
```

## 📁 Project Structure

Key files for Vercel deployment:
- `vercel.json` - Vercel configuration
- `.vercelignore` - Files to exclude from deployment
- `main.py` - Flask application
- `requirements.txt` - Python dependencies

## 🔗 Important URLs

- Vercel Dashboard: https://vercel.com/dashboard
- Vercel Documentation: https://vercel.com/docs
- Your Deployed App: `https://your-project.vercel.app`

## 💰 Costs

- **Vercel Hobby Plan**: FREE
  - Unlimited deployments
  - Automatic HTTPS
  - 100GB bandwidth per month
  - Serverless functions

- **Database Options:**
  - Vercel Postgres: Free tier available (256 MB)
  - Neon: Free tier available (0.5 GB)
  - Supabase: Free tier available (500 MB)

## 🔄 Continuous Deployment

Vercel automatically deploys when you push to your GitHub repository:

```bash
# Make changes to your code
git add .
git commit -m "Update features"
git push origin main

# Vercel will automatically deploy the changes
```

## 🐛 Troubleshooting

### Application Fails to Start

**Check Logs:**
1. Go to Vercel Dashboard → Your Project → Deployments
2. Click on the failed deployment
3. View the build and runtime logs

**Common Issues:**
- Missing environment variables
- Database connection string format (must start with `postgresql://`, not `postgres://`)
- Python package compatibility

### Database Connection Errors

**Fix SQLAlchemy URL:**
The application automatically fixes `postgres://` to `postgresql://`, but verify:
```python
# In main.py - already handled
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
```

### Static Files Not Loading

Vercel serves static files automatically. Check:
- Files are in `/static/` directory
- Paths in templates use `{{ url_for('static', filename='...') }}`

### Function Timeout

Vercel has a 10-second timeout for Hobby plan:
- Optimize database queries
- Add indexes to frequently queried columns
- Consider upgrading to Pro plan (60-second timeout)

## 📊 Monitoring

### View Logs:
```bash
vercel logs your-project-url
```

### In Dashboard:
- Go to your project
- Click "Deployments" tab
- Select deployment to view logs

## 🔄 Rolling Back

If something goes wrong:
1. Go to Vercel Dashboard → Deployments
2. Find a previous working deployment
3. Click "..." → "Promote to Production"

## 🎯 Best Practices

1. **Use Environment Variables** - Never commit secrets
2. **Enable Caching** - Speed up deployments
3. **Monitor Logs** - Check for errors regularly
4. **Database Backups** - Regular backups of your PostgreSQL database
5. **Test Locally First** - Always test changes before deploying

## 📞 Need Help?

- Vercel Documentation: https://vercel.com/docs
- Vercel Community: https://github.com/vercel/vercel/discussions
- Flask Documentation: https://flask.palletsprojects.com/

## 🎉 Post-Deployment

After successful deployment:

1. ✅ Test all pages and functionality
2. ✅ Verify admin login works
3. ✅ Test product browsing and filtering
4. ✅ Test cart and checkout process
5. ✅ Verify order creation
6. ✅ Set up monitoring and alerts

Your Avanii Shop is now live! 🚀
