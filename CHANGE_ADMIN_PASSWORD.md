# How to Change Admin Password

## Method 1: Using the Admin Panel (Recommended) ✅

This is the easiest and safest way to change your admin password.

### Steps:

1. **Login to Admin Panel**
   - Go to: http://localhost:5000/admin/login
   - Enter current credentials (admin/admin123)

2. **Navigate to Change Password**
   
   You have two ways to access the change password page:
   
   **Option A - Top Navigation:**
   - Look at the top navigation bar
   - Click on "Change Password" (lock icon)
   
   **Option B - Sidebar:**
   - Look at the left sidebar
   - Scroll to the bottom
   - Click on "Change Password" (lock icon)

3. **Fill in the Password Form**
   - **Current Password**: Enter your current password (admin123 initially)
   - **New Password**: Enter your new password (minimum 6 characters)
   - **Confirm New Password**: Re-enter the same new password

4. **Submit**
   - Click "Change Password" button
   - You'll see a success message if everything is correct

5. **Done!**
   - Your password has been changed
   - Use the new password for future logins

### Password Requirements:
- ✅ Minimum 6 characters
- ✅ Use a strong, unique password
- ✅ Avoid common words or easily guessable information
- ✅ Mix of letters, numbers, and special characters recommended

### Common Errors:

**"Current password is incorrect"**
- You entered the wrong current password
- Try again with the correct current password

**"New passwords do not match"**
- The new password and confirm password fields don't match
- Make sure you type the exact same password in both fields

**"New password must be at least 6 characters long"**
- Your new password is too short
- Use at least 6 characters

---

## Method 2: Using Python Script (Advanced)

If you can't access the admin panel, you can change the password directly in the database.

### Steps:

1. **Create a script** (e.g., `change_admin_password.py`):

```python
import sqlite3
from werkzeug.security import generate_password_hash

# New password you want to set
NEW_PASSWORD = "your_new_password_here"

# Connect to database
conn = sqlite3.connect('site.db')
cursor = conn.cursor()

# Hash the new password
password_hash = generate_password_hash(NEW_PASSWORD)

# Update admin user's password
cursor.execute(
    "UPDATE users SET password_hash = ? WHERE username = 'admin'",
    (password_hash,)
)
conn.commit()

print(f"✅ Admin password changed successfully!")
print(f"New password: {NEW_PASSWORD}")

conn.close()
```

2. **Run the script**:
```bash
cd /Users/akshay/Desktop/code/Avani/Avanii/Avanii
python3 change_admin_password.py
```

3. **Login with new password**

---

## Method 3: Using Database Directly (Expert Level)

Only use this if you're comfortable with SQL.

### Steps:

1. **Open SQLite database**:
```bash
cd /Users/akshay/Desktop/code/Avani/Avanii/Avanii
sqlite3 site.db
```

2. **Generate password hash** (in Python):
```python
from werkzeug.security import generate_password_hash
print(generate_password_hash("your_new_password"))
# Copy the output hash
```

3. **Update database**:
```sql
UPDATE users 
SET password_hash = 'paste_the_hash_here' 
WHERE username = 'admin';
```

4. **Exit SQLite**:
```sql
.exit
```

---

## Quick Reference

### Admin Panel Password Change URL:
```
http://localhost:5000/admin/change-password
```

### Default Credentials (Initial):
- Username: `admin`
- Password: `admin123`

### Location of Credentials File:
```
/Users/akshay/Desktop/code/Avani/Avanii/Avanii/admin_credentials.txt
```

⚠️ **Important**: After changing your password, update the credentials file manually if you want to keep a record.

---

## Security Best Practices

1. ✅ Change the default password immediately after first login
2. ✅ Use a strong password (mix of uppercase, lowercase, numbers, symbols)
3. ✅ Don't share your admin password
4. ✅ Change password regularly (every 3-6 months)
5. ✅ Don't use the same password as other accounts
6. ✅ Consider using a password manager

---

## Troubleshooting

### Can't remember current password?
- Use Method 2 or Method 3 to reset it directly in the database

### Password change not working?
- Check that Flask app is running
- Verify you're logged in as admin
- Check browser console for JavaScript errors
- Check terminal for Python errors

### Locked out of admin panel?
1. Stop the Flask application
2. Use Method 2 to reset the password
3. Restart Flask application
4. Login with new password

---

## Need Help?

If you encounter any issues:
1. Check the terminal for error messages
2. Check browser console (F12) for frontend errors
3. Verify database connection is working
4. Make sure you're using the correct username (admin)

---

**Remember: Always keep your admin credentials secure! 🔒**
