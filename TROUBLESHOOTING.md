# Troubleshooting Guide

## Common Issues and Solutions

### 1. App Fails to Deploy on Render

**Symptoms:**
- Build fails
- Deployment shows errors in logs
- Site returns 502 Bad Gateway

**Solutions:**

#### A. Check Build Logs
1. Go to Render Dashboard
2. Click on your web service
3. Click "Logs" tab
4. Look for error messages

#### B. Common Build Errors

**Error: "No module named 'flask'"**
```
Solution: Ensure requirements.txt is in the root directory
Check: pip install -r requirements.txt works locally
```

**Error: "Failed to build psycopg2"**
```
Solution: Use psycopg2-binary instead
In requirements.txt: psycopg2-binary==2.9.9
```

**Error: "Could not find a version that satisfies the requirement"**
```
Solution: Update package versions in requirements.txt
Try: pip install --upgrade flask sqlalchemy
```

#### C. Environment Variables Missing

**Check these are set:**
- `SECRET_KEY` - Your generated secret key
- `DATABASE_URL` - From PostgreSQL database
- `FLASK_ENV` - Set to "production"

---

### 2. Database Connection Errors

**Symptoms:**
- "could not connect to server"
- "connection refused"
- "database does not exist"

**Solutions:**

#### A. Check DATABASE_URL Format
```python
# Wrong format (Render gives this):
postgres://user:password@host:5432/dbname

# Correct format (SQLAlchemy needs this):
postgresql://user:password@host:5432/dbname

# Your main.py already handles this conversion!
```

#### B. Verify Database Status
1. Go to Render Dashboard
2. Click on PostgreSQL database
3. Check status is "Available"
4. Try "Connect" button to test

#### C. Database Not Initialized
```bash
# Use Render Shell to run:
python -c "from main import init_db; init_db()"
```

---

### 3. Static Files Not Loading

**Symptoms:**
- No CSS styling
- Images don't show
- JavaScript not working

**Solutions:**

#### A. Check Template Links
```html
<!-- Wrong: -->
<link href="/static/css/style.css" rel="stylesheet">

<!-- Correct: -->
<link href="{{ url_for('static', filename='css/style.css') }}" rel="stylesheet">
```

#### B. Verify Static Files in Git
```bash
# Check if static files are committed:
git ls-files static/

# If empty, add them:
git add static/
git commit -m "Add static files"
git push
```

#### C. Check File Permissions
```bash
# Static files should be readable:
ls -la static/
# Should show: -rw-r--r--
```

---

### 4. GoDaddy Domain Not Working

**Symptoms:**
- Domain shows error
- "This site can't be reached"
- Still showing GoDaddy parking page

**Solutions:**

#### A. Verify DNS Records in GoDaddy
```
Correct setup:
1. Type: CNAME, Name: www, Value: avanii-shop.onrender.com
2. Type: CNAME, Name: @, Value: avanii-shop.onrender.com
   OR
   Type: A, Name: @, Value: [IP from Render]
```

#### B. Check DNS Propagation
- Visit: https://dnschecker.org
- Enter your domain
- Should show Render's IP/CNAME globally
- Can take 24-48 hours, usually 1-2 hours

#### C. Verify in Render
1. Go to web service settings
2. Scroll to "Custom Domains"
3. Domain should show "Verified" status
4. SSL certificate should say "Active"

#### D. Common DNS Mistakes
```
❌ Wrong: Value = https://avanii-shop.onrender.com
✅ Correct: Value = avanii-shop.onrender.com

❌ Wrong: TTL = 3600 or higher (slow propagation)
✅ Correct: TTL = 600 (faster propagation)

❌ Wrong: Multiple conflicting A/CNAME records
✅ Correct: Remove old records before adding new ones
```

---

### 5. Login/Registration Not Working

**Symptoms:**
- Can't login with correct password
- Registration fails
- Session lost on refresh

**Solutions:**

#### A. Check SECRET_KEY
```bash
# In Render dashboard, verify SECRET_KEY is set
# Should be 64 character hex string
```

#### B. Database Issue
```bash
# Use Render Shell:
python -c "from main import db_session, User; print(db_session.query(User).all())"
```

#### C. Session Cookie Issues
```python
# In main.py, ensure:
app.config['SESSION_COOKIE_SECURE'] = True  # For HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
```

---

### 6. Admin Panel Not Accessible

**Symptoms:**
- Can't access /admin/login
- "Admin access required" message
- Login works but admin panel doesn't

**Solutions:**

#### A. Create Admin User
```bash
# Use Render Shell:
python setup_admin.py

# Or manually:
python -c "
from main import db_session, User
from werkzeug.security import generate_password_hash
user = db_session.query(User).filter_by(username='admin').first()
if user:
    user.is_admin = True
    db_session.commit()
    print('Admin status granted')
"
```

#### B. Check Admin Status
```bash
python -c "
from main import db_session, User
user = db_session.query(User).filter_by(username='YOUR_USERNAME').first()
print(f'Is Admin: {user.is_admin}')
"
```

---

### 7. Cart Issues

**Symptoms:**
- Cart empty after login
- Items disappear
- Duplicate items

**Solutions:**

#### A. Check Cart Model
```bash
# Verify cart exists for user:
python -c "
from main import db_session, Cart, current_user
cart = db_session.query(Cart).filter_by(user_id=1).first()
print(cart.cart_items if cart else 'No cart')
"
```

#### B. Session vs Database Cart
```python
# The app merges session cart with database cart on login
# Check this logic in the login() function
```

---

### 8. Orders Not Saving

**Symptoms:**
- Checkout completes but no order
- Order confirmation page errors
- Missing order data

**Solutions:**

#### A. Check Database Tables
```bash
python -c "
from main import engine, Order, OrderItem
from sqlalchemy import inspect
inspector = inspect(engine)
print('Tables:', inspector.get_table_names())
"
```

#### B. Verify Order Creation
```bash
python -c "
from main import db_session, Order
orders = db_session.query(Order).all()
print(f'Total orders: {len(orders)}')
"
```

---

### 9. Slow Performance / Cold Starts

**Symptoms:**
- First request takes 30-50 seconds
- Site seems slow
- Timeout errors

**Solutions:**

#### A. Free Tier Limitation
```
Render's free tier spins down after 15 minutes of inactivity
First request after spin down takes 30-50 seconds (cold start)

Solution: Upgrade to Starter plan ($7/month) for always-on service
```

#### B. Keep Service Alive (Free Hack)
```bash
# Use a service like UptimeRobot or Cron-job.org
# Ping your site every 14 minutes: https://yourdomain.com
```

#### C. Optimize Database Queries
```python
# Use eager loading:
products = db_session.query(Product).options(
    joinedload(Product.category)
).all()
```

---

### 10. SSL Certificate Issues

**Symptoms:**
- "Not Secure" warning
- Mixed content errors
- Certificate error

**Solutions:**

#### A. Wait for Certificate Provisioning
```
Render automatically provisions Let's Encrypt certificates
Can take 5-10 minutes after DNS verification
```

#### B. Force HTTPS
```python
# Add to main.py:
from flask import redirect, request

@app.before_request
def before_request():
    if not request.is_secure and os.environ.get('FLASK_ENV') == 'production':
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)
```

#### C. Check Mixed Content
```html
<!-- All links should use HTTPS or relative URLs -->
❌ <img src="http://example.com/image.jpg">
✅ <img src="https://example.com/image.jpg">
✅ <img src="/static/img/image.jpg">
```

---

## Emergency Commands

### Reset Database
```bash
# ⚠️ WARNING: This deletes all data!
python -c "
from main import Base, engine
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
print('Database reset complete')
"
```

### Create Emergency Admin
```bash
python -c "
from main import db_session, User
from werkzeug.security import generate_password_hash
user = User(
    username='emergency_admin',
    email='admin@emergency.com',
    password_hash=generate_password_hash('ChangeMe123!'),
    is_admin=True
)
db_session.add(user)
db_session.commit()
print('Emergency admin created')
"
```

### Clear All Carts
```bash
python -c "
from main import db_session, CartItem
db_session.query(CartItem).delete()
db_session.commit()
print('All carts cleared')
"
```

### Check App Health
```bash
python -c "
from main import app, db_session, User, Product
print('✓ App initialized')
print(f'✓ Users: {db_session.query(User).count()}')
print(f'✓ Products: {db_session.query(Product).count()}')
print('✓ All systems operational')
"
```

---

## Getting Help

### 1. Check Render Logs
- Dashboard → Your Service → Logs tab
- Shows real-time application logs
- Look for Python errors, tracebacks

### 2. Render Community
- https://community.render.com
- Search for similar issues
- Post your error logs

### 3. Flask Documentation
- https://flask.palletsprojects.com
- Comprehensive troubleshooting guides

### 4. Enable Debug Mode (Temporarily)
```python
# Only for testing! Remove after fixing issue
app.run(debug=True)
```

**Never leave debug mode on in production!**

---

## Useful Diagnostic Commands

```bash
# Check Python version
python --version

# Check installed packages
pip list

# Test database connection
python -c "from main import engine; engine.connect()"

# List all routes
python -c "from main import app; print(app.url_map)"

# Check environment variables
python -c "import os; print(os.environ.get('DATABASE_URL')[:20])"

# Test secret key
python -c "from main import app; print(len(app.config['SECRET_KEY']))"
```

---

## Prevention Tips

1. **Test locally before deploying**
   ```bash
   python main.py
   # Visit http://localhost:5001
   ```

2. **Use staging environment**
   - Create separate Render service for testing
   - Test changes before production deploy

3. **Monitor regularly**
   - Check Render dashboard daily
   - Review error logs
   - Monitor database size

4. **Backup frequently**
   - Download database backups weekly
   - Keep Git commits regular
   - Document all changes

5. **Version control**
   ```bash
   git tag v1.0.0  # Tag stable releases
   git push --tags
   ```

---

## Still Stuck?

If none of these solutions work:

1. Copy error logs from Render
2. Note what you were trying to do
3. Check what changed recently
4. Try rolling back to last working version:
   ```bash
   git log  # Find last good commit
   git revert HEAD  # Undo last commit
   git push
   ```

4. Reach out with specific error messages and steps to reproduce

Good luck! 🍀
