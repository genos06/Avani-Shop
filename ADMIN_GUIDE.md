# Admin Dashboard Guide

## Overview
The Avanii Admin Dashboard is a complete administrative interface for managing your e-commerce store. It provides full control over products, categories, orders, and users.

## Access Information

### Admin Login URL
```
http://localhost:5000/admin/login
```

### Default Credentials
```
Username: admin
Password: admin123
Email: admin@avanii.com
```

**⚠️ IMPORTANT: Change these credentials after your first login!**

## Features

### 1. Dashboard
- **Statistics Overview**: View total orders, products, users, and revenue
- **Recent Orders**: Quick view of the latest orders
- **Quick Actions**: Fast access to common tasks

### 2. Orders Management (`/admin/orders`)
- View all customer orders
- See order details (items, shipping address, customer info)
- Update order status (Pending → Processing → Completed/Cancelled)
- Delete orders
- Track order timeline and customer information

**Order Statuses:**
- **Pending**: New orders awaiting processing
- **Processing**: Orders being prepared for shipment
- **Completed**: Successfully delivered orders
- **Cancelled**: Cancelled or refunded orders

### 3. Products Management (`/admin/products`)
- View all products in a table format
- Add new products with full details
- Edit existing product information
- Delete products
- Manage product attributes:
  - Name, description, price, stock
  - SKU, category, tags
  - Image path
  - Product flags (Featured, Hot, Sale)

### 4. Categories Management (`/admin/categories`)
- Create product categories
- Edit category names and descriptions
- Delete categories (products will be unassigned)
- View product count per category

### 5. Users Management (`/admin/users`)
- View all registered users
- See user details (username, email, admin status)
- View order count per user
- Delete users (except yourself)
- Identify admin users

## How to Use

### Adding a New Product
1. Go to **Products** → **Add New Product**
2. Fill in required fields:
   - Product Name
   - Price (in ₹)
   - Stock (in kg)
   - Image Filename (path relative to static folder)
3. Optional fields:
   - Description, SKU, Category, Tags
   - Flags: Featured, Hot, Sale
4. Click **Add Product**

### Managing Orders
1. Go to **Orders** to see all orders
2. Click **View** on any order to see full details
3. Update order status using the dropdown
4. View customer information and shipping address
5. See itemized order breakdown with quantities

### Creating Categories
1. Go to **Categories** → **Add New Category**
2. Enter category name (required)
3. Add optional description
4. Click **Add Category**

### Managing Users
1. Go to **Users** to see all registered users
2. View user statistics
3. Delete users if needed (you cannot delete yourself)

## Security Features

- **Admin-Only Access**: All admin routes require admin authentication
- **Login Protection**: Redirects non-admin users to login page
- **Self-Protection**: Cannot delete your own admin account
- **Password Hashing**: All passwords are securely hashed

## Database Schema

### Users Table (with is_admin)
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email
- `password_hash`: Hashed password
- `is_admin`: Boolean flag for admin access

### Products Table
- Complete product information including price, stock, images
- Category relationships
- Product flags (featured, hot, sale)

### Orders Table
- Customer billing information
- Order status tracking
- Total amount and timestamps
- Relationship to order items

### Categories Table
- Category name and description
- Relationship to products

## File Locations

### Admin Credentials
```
/Avanii/admin_credentials.txt
```

### Admin Templates
```
/Avanii/templates/admin/
├── admin_login.html       # Login page
├── admin_base.html        # Base template with navigation
├── dashboard.html         # Main dashboard
├── orders.html            # Orders list
├── order_details.html     # Single order view
├── products.html          # Products list
├── product_form.html      # Add/Edit product
├── categories.html        # Categories list
├── category_form.html     # Add/Edit category
└── users.html             # Users list
```

### Admin Routes (in main.py)
- `/admin/login` - Admin login
- `/admin/dashboard` - Main dashboard
- `/admin/orders` - Orders management
- `/admin/products` - Products management
- `/admin/categories` - Categories management
- `/admin/users` - Users management

## Setup & Migration

### Initial Setup
The admin system has already been set up by running:
```bash
python3 setup_admin.py
```

This script:
1. Adds `is_admin` column to users table
2. Creates the default admin user
3. Sets up necessary database structure

### Re-running Setup
If you need to re-run the setup (safe to run multiple times):
```bash
cd /Users/akshay/Desktop/code/Avani/Avanii/Avanii
python3 setup_admin.py
```

## Tips & Best Practices

1. **Change Default Password**: First thing after login!
2. **Regular Backups**: Backup `site.db` regularly
3. **Order Management**: Keep orders updated with current status
4. **Stock Management**: Update product stock levels regularly
5. **Category Organization**: Use clear, descriptive category names
6. **Product Images**: Ensure image paths are correct before adding products

## Troubleshooting

### Can't Access Admin Panel
- Make sure you're using the admin username and password
- Check that the database migration ran successfully
- Verify the user has `is_admin = 1` in the database

### Changes Not Appearing
- Check for flash messages indicating errors
- Verify database commit was successful
- Refresh the page

### Database Errors
- Ensure all required fields are filled
- Check for unique constraint violations (duplicate usernames/emails)
- Verify foreign key relationships

## Navigation

### Main Site Navigation
- Click "View Site" in the top navigation to open the main site in a new tab
- You stay logged in as admin

### Admin Navigation
- Use the left sidebar to navigate between sections
- Dashboard provides quick overview and links
- Each section has breadcrumb navigation

## Support

For issues or questions about the admin system, check:
1. Flash messages at the top of pages (errors/success messages)
2. Browser console for JavaScript errors
3. Terminal/server logs for Python errors

## Currency & Units
- All prices are displayed in Indian Rupees (₹)
- All quantities are in kilograms (kg)
- Phone numbers must be 10 digits (Indian format)

---

**Enjoy managing your Avanii store! 🌿**
