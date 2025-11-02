# Avanii - Plant Shop E-commerce Website

A fully functional Flask-based e-commerce website for selling plants with database-driven content management.

## Features

### 🛍️ Shop Features
- **Dynamic Product Listing**: All products are loaded from the database
- **Category Filtering**: Filter products by category (Indoor, Outdoor, Office, Potted, Flowering)
- **Sorting Options**: Sort by newest, price (low to high, high to low), name (A-Z, Z-A)
- **Pagination**: Configurable items per page (9, 12, 18, 24)
- **Product Search**: Search products by name
- **Product Tags**: Hot, Sale, and Featured product tags
- **Stock Management**: Real-time stock tracking

### 📦 Product Details
- Individual product pages with full details
- Product images, descriptions, SKU, category, tags
- Stock availability display
- Related products section (same category)
- Add to cart with quantity selection
- Social sharing buttons

### 🛒 Shopping Cart
- Session-based cart (no login required)
- Add/Remove items
- Update quantities
- Real-time cart total calculation
- Cart count badge in header
- Clear entire cart option

### 💾 Database-Driven
Everything is managed through the database:
- Products
- Categories
- Stock levels
- Prices
- Images
- Product attributes (SKU, tags, descriptions)

## Installation & Setup

### 1. Install Dependencies

```bash
pip install flask flask-bootstrap sqlalchemy flask-login
```

### 2. Initialize the Database

The application will automatically create the database tables on first run.

Edit `main.py` and uncomment the line to add sample data:

```python
if __name__ == "__main__":
    init_db()
    add_sample_data()  # Uncomment this line
    app.run(debug=True)
```

### 3. Run the Application

```bash
python main.py
```

The application will:
1. Create the database tables
2. Add sample categories and products
3. Start the Flask development server at `http://127.0.0.1:5000/`

### 4. After First Run

After running once with sample data, comment out the `add_sample_data()` line to prevent duplicate data:

```python
if __name__ == "__main__":
    init_db()
    # add_sample_data()  # Comment this after first run
    app.run(debug=True)
```

## Database Management

### Adding New Products

You can add products directly to the database using Python:

```python
from main import db_session, Product, Category

# Get a category
category = db_session.query(Category).filter_by(name="Indoor Plants").first()

# Create a new product
new_product = Product(
    name="Monstera Deliciosa",
    description="Beautiful Swiss cheese plant",
    price=29.99,
    image_filename="img/bg-img/monstera.png",
    stock=25,
    category=category,
    sku="MON001",
    tags="monstera, tropical, indoor",
    is_featured=True,
    is_hot=False,
    is_sale=False
)

db_session.add(new_product)
db_session.commit()
```

### Adding New Categories

```python
from main import db_session, Category

new_category = Category(
    name="Succulents",
    description="Low maintenance succulent plants"
)

db_session.add(new_category)
db_session.commit()
```

### Updating Stock

```python
from main import db_session, Product

product = db_session.query(Product).filter_by(sku="CT201801").first()
product.stock = 100
db_session.commit()
```

### Updating Prices

```python
from main import db_session, Product

product = db_session.query(Product).filter_by(name="Cactus Flower").first()
product.price = 12.99
product.is_sale = True  # Mark as on sale
db_session.commit()
```

## Database Schema

### Products Table
- `id`: Primary key
- `name`: Product name
- `description`: Product description
- `price`: Product price (float)
- `image_filename`: Path to product image
- `stock`: Available quantity
- `category_id`: Foreign key to categories
- `sku`: Stock Keeping Unit (unique)
- `tags`: Comma-separated tags
- `is_featured`: Boolean (shows in best sellers)
- `is_hot`: Boolean (shows "Hot" badge)
- `is_sale`: Boolean (shows "Sale" badge)
- `created_at`: Timestamp

### Categories Table
- `id`: Primary key
- `name`: Category name (unique)
- `description`: Category description

### Cart & CartItem Tables
- Session-based cart for guest users
- Can be extended to support logged-in users

## Routes

### Public Routes
- `/` - Homepage
- `/shop` - Product listing with filters
- `/shop/<product_id>` - Product details
- `/cart` - Shopping cart
- `/add-to-cart/<product_id>` - Add item to cart (POST)
- `/update-cart/<product_id>` - Update cart quantity (POST)
- `/remove-from-cart/<product_id>` - Remove item from cart
- `/clear-cart` - Clear all cart items

### Query Parameters for /shop
- `category`: Filter by category ID
- `min_price`: Minimum price filter
- `max_price`: Maximum price filter
- `sort`: Sort order (newest, price_low, price_high, name_asc, name_desc)
- `page`: Page number
- `per_page`: Items per page (9, 12, 18, 24)
- `search`: Search term

## Image Management

Place product images in the `static/img/bg-img/` directory and reference them in the database:

```python
product.image_filename = "img/bg-img/your-image.png"
```

## Extending the System

### Add User Authentication
Uncomment the login-related code in `main.py` to enable user accounts:
- User registration
- Login/logout
- User-specific carts
- Order history

### Add Checkout Process
Create checkout routes and templates for:
- Shipping information
- Payment processing
- Order confirmation

### Add Product Reviews
Extend the database schema to include reviews and ratings.

### Add Admin Panel
Create admin routes for:
- Adding/editing products via web interface
- Managing categories
- Viewing orders
- Managing stock

## Sample Data

The system comes with 10 sample products across 5 categories:
1. **Outdoor Plants**: Cactus Flower
2. **Indoor Plants**: Recuerdos Plant, Fern Plant, Peace Lily
3. **Office Plants**: Aloe Vera, Snake Plant
4. **Potted Plants**: Succulent Mix, Bonsai Tree
5. **Flowering Plants**: Tulip Flower, Orchid

All sample products have:
- Descriptions
- Prices ranging from $8.99 to $35.99
- Stock levels
- SKUs
- Category assignments
- Tags

## Troubleshooting

### Database Issues
If you encounter database errors, delete `site.db` and restart the application to recreate it.

### Import Errors
Ensure all dependencies are installed:
```bash
pip install flask flask-bootstrap sqlalchemy flask-login
```

### Images Not Loading
Verify that:
1. Images are in the `static/img/bg-img/` directory
2. The `image_filename` in the database includes the full path: `img/bg-img/filename.png`

## License

This project uses the Alazea template by Colorlib (CC BY 3.0).

## Support

For issues or questions, please contact: avanii.for.earth@gmail.com
