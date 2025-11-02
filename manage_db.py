"""
Database Management Script for Avanii Shop
Use this script to manage products, categories, and other database operations
"""

from main import db_session, Product, Category, Base, engine
from datetime import datetime


def list_all_products():
    """List all products in the database"""
    products = db_session.query(Product).all()
    print("\n=== ALL PRODUCTS ===")
    print(f"{'ID':<5} {'Name':<30} {'Price':<10} {'Stock':<8} {'Category':<20}")
    print("-" * 80)
    for p in products:
        cat_name = p.category.name if p.category else "None"
        print(f"{p.id:<5} {p.name:<30} ${p.price:<9.2f} {p.stock:<8} {cat_name:<20}")
    print(f"\nTotal products: {len(products)}\n")


def list_all_categories():
    """List all categories in the database"""
    categories = db_session.query(Category).all()
    print("\n=== ALL CATEGORIES ===")
    print(f"{'ID':<5} {'Name':<30} {'Product Count':<15}")
    print("-" * 55)
    for c in categories:
        print(f"{c.id:<5} {c.name:<30} {len(c.products):<15}")
    print(f"\nTotal categories: {len(categories)}\n")


def add_product_interactive():
    """Interactive function to add a new product"""
    print("\n=== ADD NEW PRODUCT ===\n")
    
    # Display categories
    list_all_categories()
    
    name = input("Product Name: ")
    description = input("Description: ")
    price = float(input("Price: "))
    stock = int(input("Stock Quantity: "))
    image_filename = input("Image Filename (e.g., img/bg-img/product.png): ")
    sku = input("SKU (unique code): ")
    tags = input("Tags (comma-separated): ")
    
    category_id = input("Category ID (or leave blank): ")
    category = None
    if category_id:
        category = db_session.get(Category, int(category_id))
    
    is_featured = input("Is Featured? (y/n): ").lower() == 'y'
    is_hot = input("Is Hot? (y/n): ").lower() == 'y'
    is_sale = input("Is Sale? (y/n): ").lower() == 'y'
    
    product = Product(
        name=name,
        description=description,
        price=price,
        stock=stock,
        image_filename=image_filename,
        sku=sku,
        tags=tags,
        category=category,
        is_featured=is_featured,
        is_hot=is_hot,
        is_sale=is_sale
    )
    
    db_session.add(product)
    db_session.commit()
    
    print(f"\n✓ Product '{name}' added successfully! (ID: {product.id})\n")


def add_category_interactive():
    """Interactive function to add a new category"""
    print("\n=== ADD NEW CATEGORY ===\n")
    
    name = input("Category Name: ")
    description = input("Description: ")
    
    category = Category(name=name, description=description)
    
    db_session.add(category)
    db_session.commit()
    
    print(f"\n✓ Category '{name}' added successfully! (ID: {category.id})\n")


def update_stock():
    """Update product stock"""
    list_all_products()
    
    product_id = int(input("\nEnter Product ID to update stock: "))
    product = db_session.get(Product, product_id)
    
    if not product:
        print("Product not found!")
        return
    
    print(f"\nCurrent stock for '{product.name}': {product.stock}")
    new_stock = int(input("Enter new stock quantity: "))
    
    product.stock = new_stock
    db_session.commit()
    
    print(f"✓ Stock updated to {new_stock}\n")


def update_price():
    """Update product price"""
    list_all_products()
    
    product_id = int(input("\nEnter Product ID to update price: "))
    product = db_session.get(Product, product_id)
    
    if not product:
        print("Product not found!")
        return
    
    print(f"\nCurrent price for '{product.name}': ${product.price:.2f}")
    new_price = float(input("Enter new price: "))
    
    product.price = new_price
    db_session.commit()
    
    print(f"✓ Price updated to ${new_price:.2f}\n")


def delete_product():
    """Delete a product"""
    list_all_products()
    
    product_id = int(input("\nEnter Product ID to delete: "))
    product = db_session.get(Product, product_id)
    
    if not product:
        print("Product not found!")
        return
    
    confirm = input(f"Are you sure you want to delete '{product.name}'? (yes/no): ")
    if confirm.lower() == 'yes':
        db_session.delete(product)
        db_session.commit()
        print(f"✓ Product '{product.name}' deleted successfully!\n")
    else:
        print("Deletion cancelled.\n")


def search_products():
    """Search for products"""
    search_term = input("\nEnter search term: ")
    products = db_session.query(Product).filter(Product.name.ilike(f'%{search_term}%')).all()
    
    if not products:
        print("No products found.\n")
        return
    
    print(f"\n=== SEARCH RESULTS FOR '{search_term}' ===")
    print(f"{'ID':<5} {'Name':<30} {'Price':<10} {'Stock':<8}")
    print("-" * 60)
    for p in products:
        print(f"{p.id:<5} {p.name:<30} ${p.price:<9.2f} {p.stock:<8}")
    print()


def set_featured_products():
    """Set products as featured"""
    list_all_products()
    
    product_ids = input("\nEnter Product IDs to mark as featured (comma-separated): ")
    ids = [int(id.strip()) for id in product_ids.split(',')]
    
    for pid in ids:
        product = db_session.get(Product, pid)
        if product:
            product.is_featured = True
            print(f"✓ '{product.name}' marked as featured")
    
    db_session.commit()
    print()


def bulk_import_products():
    """Bulk import products from a list"""
    print("\n=== BULK IMPORT PRODUCTS ===")
    print("Format: name|description|price|stock|image_filename|sku|category_id|tags")
    print("Enter 'done' when finished\n")
    
    count = 0
    while True:
        data = input(f"Product {count + 1}: ")
        if data.lower() == 'done':
            break
        
        try:
            parts = data.split('|')
            name, desc, price, stock, img, sku, cat_id, tags = parts
            
            category = None
            if cat_id.strip():
                category = db_session.get(Category, int(cat_id))
            
            product = Product(
                name=name.strip(),
                description=desc.strip(),
                price=float(price),
                stock=int(stock),
                image_filename=img.strip(),
                sku=sku.strip(),
                category=category,
                tags=tags.strip()
            )
            
            db_session.add(product)
            count += 1
            print(f"  ✓ Added '{name.strip()}'")
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    db_session.commit()
    print(f"\n✓ Successfully imported {count} products!\n")


def main_menu():
    """Main menu for database management"""
    while True:
        print("\n" + "="*50)
        print("AVANII SHOP - DATABASE MANAGEMENT")
        print("="*50)
        print("\n1.  List All Products")
        print("2.  List All Categories")
        print("3.  Add New Product")
        print("4.  Add New Category")
        print("5.  Update Product Stock")
        print("6.  Update Product Price")
        print("7.  Delete Product")
        print("8.  Search Products")
        print("9.  Set Featured Products")
        print("10. Bulk Import Products")
        print("0.  Exit")
        
        choice = input("\nEnter your choice: ")
        
        if choice == '1':
            list_all_products()
        elif choice == '2':
            list_all_categories()
        elif choice == '3':
            add_product_interactive()
        elif choice == '4':
            add_category_interactive()
        elif choice == '5':
            update_stock()
        elif choice == '6':
            update_price()
        elif choice == '7':
            delete_product()
        elif choice == '8':
            search_products()
        elif choice == '9':
            set_featured_products()
        elif choice == '10':
            bulk_import_products()
        elif choice == '0':
            print("\nGoodbye!\n")
            break
        else:
            print("\nInvalid choice. Please try again.\n")


if __name__ == "__main__":
    main_menu()
