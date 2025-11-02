# Quick Fix: Initialize Admin User on Vercel

Your admin page is not working because the database hasn't been initialized yet. Follow these steps:

## Option 1: Initialize Locally (Easiest)

1. **Get your DATABASE_URL from Vercel:**
   - Go to https://vercel.com/dashboard
   - Click on your project (avani-shop)
   - Go to Settings → Environment Variables
   - Copy the `DATABASE_URL` value

2. **Run the initialization script:**
   ```bash
   cd /Users/akshay/Desktop/code/deployment
   
   # Set the database URL (replace with your actual URL)
   export DATABASE_URL="postgresql://user:password@host/database"
   export SECRET_KEY="your-secret-key"
   
   # Run initialization
   python3 init_vercel_db.py
   ```

3. **Login to admin:**
   - URL: https://avani-shop.vercel.app/admin/login
   - Username: `admin`
   - Password: `admin123`

## Option 2: Using Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Link to your project
cd /Users/akshay/Desktop/code/deployment
vercel link

# Pull environment variables
vercel env pull

# Initialize database
python3 init_vercel_db.py
```

## Option 3: Quick Command (Copy-Paste)

Replace `YOUR_DATABASE_URL` with your actual database URL from Vercel:

```bash
cd /Users/akshay/Desktop/code/deployment && \
export DATABASE_URL="YOUR_DATABASE_URL" && \
python3 init_vercel_db.py
```

## What This Does

The script will:
- ✅ Create all database tables (users, products, categories, orders, etc.)
- ✅ Create admin user (username: admin, password: admin123)
- ✅ Add sample categories (Indoor Plants, Outdoor Plants, etc.)
- ✅ Add sample products for testing

## After Initialization

1. Login at: https://avani-shop.vercel.app/admin/login
2. Change admin password immediately!
3. Go to Admin Dashboard → Change Password

## Troubleshooting

**"No module named psycopg2"**
```bash
pip3 install psycopg2-binary
```

**"Connection refused"**
- Make sure you copied the correct DATABASE_URL from Vercel
- The URL should start with `postgresql://` or `postgres://`

**"Admin user already exists"**
- This is fine! The script will just update the existing user
- Try logging in with: admin / admin123

## Need Help?

Check the full guide: VERCEL_DEPLOY.md
