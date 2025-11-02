# Login System Implementation Guide

## Overview
A complete user authentication system has been implemented for the Avanii plant e-commerce website with user registration, login/logout functionality, and cart persistence.

## Features Implemented

### 1. User Authentication
- **Registration**: New users can create accounts with username, email, and password
- **Login**: Users can log in with username and password
- **Logout**: Authenticated users can log out
- **Password Security**: Passwords are hashed using `werkzeug.security` (pbkdf2:sha256)
- **Remember Me**: Option to stay logged in across sessions

### 2. Cart Persistence
- **Session-based Cart**: For non-logged-in users, cart data is stored in Flask session
- **Database Cart**: For logged-in users, cart data is stored in the database
- **Cart Merging**: When a user logs in with items in their session cart, those items are automatically merged with their database cart

### 3. User Interface
- **Bootstrap-styled Login Page**: Clean, responsive login form
- **Bootstrap-styled Register Page**: Registration form with validation
- **Header Updates**: 
  - Shows "Login" link for anonymous users
  - Shows "Logout (username)" for authenticated users
  - Cart count updates dynamically
- **Flash Messages**: Success, error, and info messages displayed to users

## Files Modified/Created

### Modified Files:
1. **`main.py`**:
   - Added login, register, and logout routes
   - Updated cart functionality to support both session and database storage
   - Added cart merging logic on login
   - Modified cart operations (add, update, remove, clear) to work with authenticated users

2. **`templates/header.html`**:
   - Added conditional logic to show Login/Logout based on authentication status
   - Added flash message display section
   - Properly structured to work as a dependency (doesn't close html/body tags)

3. **`templates/login.html`**:
   - Added link to registration page
   - Removed duplicate flash messages (now handled in header)

### Created Files:
1. **`templates/register.html`**:
   - Complete registration form with Bootstrap styling
   - Fields: username, email, password, password confirmation
   - Client-side and server-side validation
   - Link back to login page

## How It Works

### Registration Flow:
1. User fills out registration form with username, email, and password
2. Server validates:
   - All fields are filled
   - Password is at least 6 characters
   - Passwords match
   - Username/email don't already exist
3. Password is hashed and user is created in database
4. A cart is automatically created for the user
5. User is redirected to login page

### Login Flow:
1. User enters username and password
2. Server validates credentials against hashed password
3. If valid:
   - User is logged in using Flask-Login
   - Session cart (if any) is merged with user's database cart
   - User is redirected to home or requested page
4. If invalid, error message is shown

### Cart Operations:

#### For Anonymous Users:
- Cart stored in `flask_session['cart']` as `{product_id: quantity}`
- Persists across page loads within the same session

#### For Authenticated Users:
- Cart stored in database with `Cart` and `CartItem` models
- Persists across sessions and devices
- Related to user via foreign key

### Cart Count Display:
- Template context processor `inject_cart_count()` runs on every request
- For authenticated users: queries database cart
- For anonymous users: counts session cart items
- Available as `{{ cart_count }}` in all templates

## Security Features

1. **Password Hashing**: Uses `pbkdf2:sha256` algorithm
2. **Login Required Decorator**: `@login_required` protects authenticated-only routes
3. **Session Secret Key**: Configured in app (change for production!)
4. **User Isolation**: Each user can only access their own cart

## Database Schema

### User Table:
- `id`: Primary key
- `username`: Unique, not null
- `email`: Unique, not null
- `password_hash`: Not null (stores hashed password)

### Cart Table:
- `id`: Primary key
- `user_id`: Foreign key to User (unique, one cart per user)

### CartItem Table:
- `id`: Primary key
- `cart_id`: Foreign key to Cart
- `product_id`: Foreign key to Product
- `quantity`: Integer, default 1

## Usage

### Starting the Application:
```bash
cd /Users/akshay/Desktop/code/Avani/Avanii/Avanii
python3 main.py
```

The app runs on **port 5001**: http://127.0.0.1:5001

### Testing the System:

1. **Register a new user**:
   - Navigate to http://127.0.0.1:5001/login
   - Click "Register here"
   - Fill out the form and submit

2. **Login**:
   - Go to http://127.0.0.1:5001/login
   - Enter your credentials

3. **Add items to cart**:
   - Browse products
   - Add items to cart
   - Cart persists even after logout/login

4. **Logout**:
   - Click "Logout (username)" in the header

## Routes

### Authentication Routes:
- `GET/POST /login` - Login page
- `GET/POST /register` - Registration page
- `GET /logout` - Logout (requires authentication)

### Cart Routes:
- `POST /add-to-cart/<product_id>` - Add product to cart
- `GET /cart` - View cart
- `POST /update-cart/<product_id>` - Update cart item quantity
- `GET /remove-from-cart/<product_id>` - Remove item from cart
- `GET /clear-cart` - Clear entire cart

## Future Enhancements

Consider adding:
1. Password reset functionality
2. Email verification
3. User profile page
4. Order history
5. Address management
6. Social login (Facebook, Google)
7. Two-factor authentication
8. Password strength requirements
9. Rate limiting for login attempts
10. CAPTCHA for registration

## Notes

- Database tables are automatically created on app startup via `init_db()`
- Sample products can be added by uncommenting `add_sample_data()` in `main.py`
- Session cart data is automatically cleaned up after login (merged into database cart)
- Flask-Login handles session management automatically
- Bootstrap 4 is used for styling (not Bootstrap 5)

## Troubleshooting

### Port 5000 in use:
App is configured to run on port 5001 to avoid conflicts with macOS AirPlay Receiver

### Flash messages not appearing:
Make sure all pages include both `header.html` and `footer.html`

### Cart count not updating:
The `inject_cart_count()` context processor should run automatically. Check that it's defined in `main.py`

### Login not working:
1. Check password was hashed during registration
2. Verify database has the user record
3. Check Flask session secret key is set
4. Ensure cookies are enabled in browser
