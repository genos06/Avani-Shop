# 🚀 Quick Start - Admin Panel

## Step 1: Verify Setup
The admin system has been set up! The database migration has been completed and the admin user has been created.

## Step 2: Start the Application
```bash
cd /Users/akshay/Desktop/code/Avani/Avanii/Avanii
python3 main.py
```

## Step 3: Access Admin Panel
Open your browser and go to:
```
http://localhost:5000/admin/login
```

## Step 4: Login
Use these credentials:
- **Username**: `admin`
- **Password**: `admin123`

## Step 5: Explore the Dashboard

### Dashboard Features:
1. **Statistics Cards** - See totals for orders, products, users, and revenue
2. **Recent Orders** - Quick view of latest customer orders
3. **Quick Actions** - Fast access to common tasks

### Main Sections:

#### 📦 Orders Management
- View all customer orders
- Update order status (Pending → Processing → Completed)
- View detailed order information
- See shipping addresses and customer details

#### 🛍️ Products Management  
- Add new products with prices in ₹
- Edit existing products
- Update stock quantities (in kg)
- Set product flags (Featured, Hot, Sale)
- Assign categories

#### 🏷️ Categories Management
- Create product categories
- Edit category information
- View product count per category

#### 👥 Users Management
- View all registered users
- See user order history
- Manage user accounts

## Quick Actions

### Add a New Product:
1. Click **Products** in sidebar
2. Click **Add New Product** button
3. Fill in the form:
   - Product name
   - Price in ₹
   - Stock in kg
   - Image path (e.g., `img/bg-img/product.jpg`)
   - Category (optional)
4. Set product flags if needed (Featured, Hot, Sale)
5. Click **Add Product**

### Update Order Status:
1. Click **Orders** in sidebar
2. Click **View** on any order
3. Use the **Update Status** dropdown on the right
4. Select new status (Pending/Processing/Completed/Cancelled)
5. Click **Update Status**

### Create a Category:
1. Click **Categories** in sidebar
2. Click **Add New Category** button
3. Enter category name and description
4. Click **Add Category**

## Important Notes

⚠️ **Change the default admin password after first login!**

💡 **Tips:**
- All prices are in Indian Rupees (₹)
- All quantities are in kilograms (kg)
- Use clear, descriptive product and category names
- Keep order statuses updated for customer tracking
- Regular stock updates ensure accurate inventory

## URLs Reference

- **Admin Login**: http://localhost:5000/admin/login
- **Dashboard**: http://localhost:5000/admin/dashboard
- **Orders**: http://localhost:5000/admin/orders
- **Products**: http://localhost:5000/admin/products
- **Categories**: http://localhost:5000/admin/categories
- **Users**: http://localhost:5000/admin/users
- **Main Site**: http://localhost:5000/

## Credentials Location

Your admin credentials are saved in:
```
/Users/akshay/Desktop/code/Avani/Avanii/Avanii/admin_credentials.txt
```

## Need Help?

Check these files for detailed information:
- **ADMIN_GUIDE.md** - Comprehensive admin documentation
- **ADMIN_IMPLEMENTATION.md** - Technical implementation details

---

**You're all set! Start managing your store! 🌿**
