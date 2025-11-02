"""
Database migration script to add is_admin column and create admin user
Run this script to set up the admin functionality
"""

import sqlite3
from werkzeug.security import generate_password_hash

def migrate_database():
    # Connect to the database
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()

    try:
        # Add the is_admin column to the users table
        print("Adding is_admin column to users table...")
        cursor.execute('ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT 0')
        conn.commit()
        print("✅ Successfully added 'is_admin' column to users table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("✅ Column 'is_admin' already exists")
        else:
            print(f"❌ Error adding column: {e}")
            return

    # Check if admin user already exists
    cursor.execute("SELECT id, username FROM users WHERE username = 'admin'")
    existing_admin = cursor.fetchone()

    if existing_admin:
        # Update existing user to be admin
        cursor.execute("UPDATE users SET is_admin = 1 WHERE username = 'admin'")
        conn.commit()
        print(f"✅ Updated existing user 'admin' (ID: {existing_admin[0]}) to admin status")
    else:
        # Create new admin user
        admin_username = 'admin'
        admin_email = 'admin@avanii.com'
        admin_password = 'admin123'
        admin_password_hash = generate_password_hash(admin_password)

        try:
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, is_admin)
                VALUES (?, ?, ?, 1)
            ''', (admin_username, admin_email, admin_password_hash))
            conn.commit()
            print("✅ Successfully created admin user")
            print(f"   Username: {admin_username}")
            print(f"   Email: {admin_email}")
            print(f"   Password: {admin_password}")
            print("\n⚠️  IMPORTANT: Change the admin password after first login!")
        except sqlite3.IntegrityError as e:
            print(f"❌ Error creating admin user: {e}")

    conn.close()
    print("\n✅ Database migration completed successfully!")
    print("\nYou can now login to the admin panel at: http://localhost:5000/admin/login")
    print("Username: admin")
    print("Password: admin123")

if __name__ == "__main__":
    migrate_database()
