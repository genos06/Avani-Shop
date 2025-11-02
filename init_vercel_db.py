"""
Initialize database for Vercel deployment with PostgreSQL
This script creates tables and admin user for production
"""

import os
from main import Base, engine, db_session, User, Category, Product, Cart
from werkzeug.security import generate_password_hash

def init_database():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(engine)
    print("✅ Database tables created successfully!")

def create_admin_user():
    """Create admin user if not exists"""
    print("\nChecking for admin user...")
    
    # Check if admin user already exists
    admin = db_session.query(User).filter_by(username='admin').first()
    
    if admin:
        print(f"✅ Admin user already exists (ID: {admin.id})")
        # Ensure user has admin privileges
        if not admin.is_admin:
            admin.is_admin = True
            db_session.commit()
            print("✅ Updated existing user to admin status")
    else:
        # Create new admin user
        admin_username = 'admin'
        admin_email = 'admin@avanii.com'
        admin_password = 'admin123'
        
        admin = User(
            username=admin_username,
            email=admin_email,
            password_hash=generate_password_hash(admin_password),
            is_admin=True
        )
        db_session.add(admin)
        db_session.commit()
        
        # Create cart for admin
        admin_cart = Cart(user_id=admin.id)
        db_session.add(admin_cart)
        db_session.commit()
        
        print("✅ Admin user created successfully!")
        print(f"   Username: {admin_username}")
        print(f"   Email: {admin_email}")
        print(f"   Password: {admin_password}")
        print("\n⚠️  IMPORTANT: Change the admin password after first login!")

def add_sample_categories():
    """Add sample categories if database is empty"""
    if db_session.query(Category).count() > 0:
        print("\n✅ Categories already exist")
        return
    
    print("\nAdding sample categories...")
    categories_data = [
        {"name": "Outdoor Plants", "description": "Plants perfect for outdoor gardens"},
        {"name": "Indoor Plants", "description": "Plants for indoor decoration"},
        {"name": "Office Plants", "description": "Low maintenance plants for offices"},
        {"name": "Potted Plants", "description": "Plants in decorative pots"},
        {"name": "Flowering Plants", "description": "Beautiful flowering plants"}
    ]
    
    for cat_data in categories_data:
        category = Category(**cat_data)
        db_session.add(category)
    
    db_session.commit()
    print("✅ Sample categories added!")

def add_sample_products():
    """Add sample products if database is empty"""
    if db_session.query(Product).count() > 0:
        print("\n✅ Products already exist")
        return
    
    print("\nAdding sample products...")
    categories = db_session.query(Category).all()
    
    if not categories:
        print("⚠️  No categories found. Add categories first.")
        return
    
    products_data = [
        {"name": "Cactus Flower", "description": "Beautiful cactus with colorful flowers", "price": 10.99, "image_filename": "img/bg-img/40.png", "stock": 50, "category": categories[0], "sku": "CT201801", "tags": "cactus, flower, hot", "is_hot": True, "is_featured": True},
        {"name": "Tulip Flower", "description": "Classic tulip plant", "price": 11.99, "image_filename": "img/bg-img/41.png", "stock": 30, "category": categories[4], "sku": "CT201802", "tags": "tulip, flower", "is_featured": True},
        {"name": "Recuerdos Plant", "description": "Elegant indoor plant", "price": 9.99, "image_filename": "img/bg-img/34.jpg", "stock": 40, "category": categories[1], "sku": "CT201803", "tags": "indoor, green", "is_featured": True},
        {"name": "Succulent Mix", "description": "Mixed succulent arrangement", "price": 15.99, "image_filename": "img/bg-img/42.png", "stock": 25, "category": categories[3], "sku": "CT201804", "tags": "succulent, potted"},
        {"name": "Fern Plant", "description": "Lush green fern", "price": 12.50, "image_filename": "img/bg-img/43.png", "stock": 35, "category": categories[1], "sku": "CT201805", "tags": "fern, indoor, green"},
    ]
    
    for prod_data in products_data:
        product = Product(**prod_data)
        db_session.add(product)
    
    db_session.commit()
    print("✅ Sample products added!")

if __name__ == "__main__":
    print("=" * 50)
    print("Initializing Vercel Database")
    print("=" * 50)
    
    try:
        init_database()
        create_admin_user()
        add_sample_categories()
        add_sample_products()
        
        print("\n" + "=" * 50)
        print("✅ Database initialization complete!")
        print("=" * 50)
        print("\nAdmin Login Details:")
        print("URL: https://your-app.vercel.app/admin/login")
        print("Username: admin")
        print("Password: admin123")
        print("\n⚠️  CHANGE PASSWORD IMMEDIATELY after first login!")
        
    except Exception as e:
        print(f"\n❌ Error during initialization: {e}")
        import traceback
        traceback.print_exc()
