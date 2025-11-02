#!/usr/bin/env python3
"""
Quick Start Script for Avanii Shop
Run this to set up everything automatically
"""

import subprocess
import sys
import os

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def check_dependencies():
    """Check if required packages are installed"""
    print_header("Checking Dependencies")
    
    required = ['flask', 'flask_bootstrap', 'sqlalchemy', 'flask_login']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is NOT installed")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        install = input("\nWould you like to install them now? (y/n): ")
        if install.lower() == 'y':
            print("\nInstalling dependencies...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", 
                                 "flask", "flask-bootstrap", "sqlalchemy", "flask-login"])
            print("\n✓ Dependencies installed successfully!")
        else:
            print("\nPlease install dependencies manually:")
            print("pip install flask flask-bootstrap sqlalchemy flask-login")
            sys.exit(1)
    else:
        print("\n✓ All dependencies are installed!")

def initialize_database():
    """Initialize the database with sample data"""
    print_header("Initializing Database")
    
    if os.path.exists('site.db'):
        print("⚠️  Database already exists!")
        overwrite = input("Do you want to recreate it? This will delete all data! (yes/no): ")
        if overwrite.lower() != 'yes':
            print("Keeping existing database.")
            return
        else:
            os.remove('site.db')
            print("✓ Old database removed")
    
    print("\nCreating database and adding sample data...")
    
    try:
        from main import init_db, add_sample_data
        init_db()
        print("✓ Database tables created")
        
        add_sample_data()
        print("✓ Sample data added")
        
        print("\n" + "="*60)
        print("DATABASE SETUP COMPLETE!")
        print("="*60)
        print("\nSample Data Added:")
        print("  • 5 Categories (Indoor, Outdoor, Office, Potted, Flowering)")
        print("  • 10 Products with various prices and stock levels")
        print("  • 3 Featured products for 'Best Sellers'")
        
    except Exception as e:
        print(f"\n✗ Error initializing database: {e}")
        sys.exit(1)

def show_instructions():
    """Show instructions for using the system"""
    print_header("Quick Start Guide")
    
    print("🚀 Your Avanii Shop is ready to go!\n")
    
    print("TO START THE APPLICATION:")
    print("  python main.py")
    print("  Then open: http://127.0.0.1:5000/\n")
    
    print("TO MANAGE PRODUCTS:")
    print("  python manage_db.py")
    print("  (Interactive menu for adding/editing products)\n")
    
    print("IMPORTANT PAGES:")
    print("  • Homepage:        http://127.0.0.1:5000/")
    print("  • Shop:            http://127.0.0.1:5000/shop")
    print("  • Cart:            http://127.0.0.1:5000/cart")
    print("  • Product Detail:  http://127.0.0.1:5000/shop/<product_id>\n")
    
    print("DOCUMENTATION:")
    print("  • README.md - Full documentation")
    print("  • IMPLEMENTATION_SUMMARY.md - Feature overview")
    print("  • manage_db.py - Database management tool\n")
    
    print("NEXT STEPS:")
    print("  1. Start the app: python main.py")
    print("  2. Browse to http://127.0.0.1:5000/shop")
    print("  3. Add products to cart and test features")
    print("  4. Use manage_db.py to add your own products\n")

def main():
    """Main setup routine"""
    print("\n" + "="*60)
    print("  AVANII SHOP - QUICK START SETUP")
    print("="*60)
    print("\nThis script will:")
    print("  1. Check and install required dependencies")
    print("  2. Create the database")
    print("  3. Add sample products and categories")
    print("  4. Show you how to start the application\n")
    
    proceed = input("Continue? (y/n): ")
    if proceed.lower() != 'y':
        print("\nSetup cancelled.")
        sys.exit(0)
    
    # Step 1: Check dependencies
    check_dependencies()
    
    # Step 2: Initialize database
    initialize_database()
    
    # Step 3: Show instructions
    show_instructions()
    
    # Ask if user wants to start the app now
    print("="*60)
    start_now = input("\nWould you like to start the application now? (y/n): ")
    if start_now.lower() == 'y':
        print("\n🚀 Starting Avanii Shop...\n")
        try:
            subprocess.run([sys.executable, "main.py"])
        except KeyboardInterrupt:
            print("\n\n✓ Application stopped.")
    else:
        print("\n✓ Setup complete! Run 'python main.py' when you're ready.\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✓ Setup cancelled by user.\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}\n")
        sys.exit(1)
