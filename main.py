from flask import Flask, render_template, url_for, request, redirect, flash, jsonify, session as flask_session
from flask_bootstrap import Bootstrap
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey, create_engine, String, Text, Float, Integer, Boolean, DateTime
from sqlalchemy.orm import Session, relationship
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from typing import Optional
import os



class Base(DeclarativeBase):
    pass

app = Flask(__name__)

# Configuration for production and development
if os.environ.get('DATABASE_URL'):
    # Production: Use PostgreSQL from Render
    database_url = os.environ.get('DATABASE_URL')
    # Fix for Render's postgres:// URL (SQLAlchemy needs postgresql://)
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-secret-key-change-this')
    engine = create_engine(database_url, echo=False)
else:
    # Development: Use SQLite
    app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
    engine = create_engine("sqlite:///site.db", echo=True)

bootstrap = Bootstrap(app)
db_session = Session(engine)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(Base, UserMixin):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(200), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    cart: Mapped["Cart"] = relationship("Cart", back_populates="user", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username}>"

@login_manager.user_loader
def load_user(user_id):
    return db_session.get(User, int(user_id))

class Category(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    products: Mapped[list["Product"]] = relationship("Product", back_populates="category")

    def __repr__(self):
        return f"<Category {self.name}>"

class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    image_filename: Mapped[str] = mapped_column(String(300), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, default=0)
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey('categories.id'), nullable=True)
    category: Mapped[Optional["Category"]] = relationship("Category", back_populates="products")
    sku: Mapped[Optional[str]] = mapped_column(String(50), unique=True, nullable=True)
    tags: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)  # Comma-separated tags
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)
    is_hot: Mapped[bool] = mapped_column(Boolean, default=False)
    is_sale: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    cart_items: Mapped[list["CartItem"]] = relationship("CartItem", back_populates="product", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Product {self.name}>"

class Cart(Base):
    __tablename__ = 'carts'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True, nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="cart")
    cart_items: Mapped[list["CartItem"]] = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")

    def get_total(self):
        return sum(item.get_subtotal() for item in self.cart_items)

    def get_item_count(self):
        return sum(item.quantity for item in self.cart_items)

    def __repr__(self):
        return f"<Cart user_id={self.user_id}>"

class CartItem(Base):
    __tablename__ = 'cart_items'
    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey('carts.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    cart: Mapped["Cart"] = relationship("Cart", back_populates="cart_items")
    product: Mapped["Product"] = relationship("Product", back_populates="cart_items")

    def get_subtotal(self):
        return self.product.price * self.quantity

    def __repr__(self):
        return f"<CartItem cart_id={self.cart_id} product_id={self.product_id} qty={self.quantity}>"

class Order(Base):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    user: Mapped["User"] = relationship("User", backref="orders")
    
    # Billing Details
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    phone: Mapped[str] = mapped_column(String(10), nullable=False)
    telephone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    company: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    address: Mapped[str] = mapped_column(String(300), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    postcode: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    order_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Order Details
    total_amount: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default='pending')  # pending, processing, completed, cancelled
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    order_items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Order {self.id} - User {self.user_id} - ${self.total_amount}>"

class OrderItem(Base):
    __tablename__ = 'order_items'
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)  # Store price at time of order
    
    order: Mapped["Order"] = relationship("Order", back_populates="order_items")
    product: Mapped["Product"] = relationship("Product")
    
    def get_subtotal(self):
        return self.price * self.quantity
    
    def __repr__(self):
        return f"<OrderItem order_id={self.order_id} product_id={self.product_id} qty={self.quantity}>"
    

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        user = db_session.query(User).filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=remember)
            
            # Merge session cart with user's database cart
            if 'cart' in flask_session and flask_session['cart']:
                # Get or create user's cart
                user_cart = db_session.query(Cart).filter_by(user_id=user.id).first()
                if not user_cart:
                    user_cart = Cart(user_id=user.id)
                    db_session.add(user_cart)
                    db_session.commit()
                
                # Merge session cart items
                for product_id_str, quantity in flask_session['cart'].items():
                    product_id = int(product_id_str)
                    cart_item = db_session.query(CartItem).filter_by(
                        cart_id=user_cart.id, 
                        product_id=product_id
                    ).first()
                    
                    if cart_item:
                        cart_item.quantity += quantity
                    else:
                        cart_item = CartItem(
                            cart_id=user_cart.id,
                            product_id=product_id,
                            quantity=quantity
                        )
                        db_session.add(cart_item)
                
                db_session.commit()
                flask_session.pop('cart', None)
            
            flash(f'Welcome back, {user.username}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template("login.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required', 'error')
            return render_template("register.html")
        
        if password != password_confirm:
            flash('Passwords do not match', 'error')
            return render_template("register.html")
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return render_template("register.html")
        
        # Check if user already exists
        if db_session.query(User).filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template("register.html")
        
        if db_session.query(User).filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template("register.html")
        
        # Create new user
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(
            username=username,
            email=email,
            password_hash=hashed_password
        )
        db_session.add(new_user)
        db_session.commit()
        
        # Create cart for user
        user_cart = Cart(user_id=new_user.id)
        db_session.add(user_cart)
        db_session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template("register.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))


@app.route("/shop")
def shop():
    # Get filter parameters
    category_filter = request.args.get('category', type=int)
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort_by = request.args.get('sort', 'newest')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 9, type=int)
    search = request.args.get('search', '')

    # Get price range from all products for slider
    from sqlalchemy import func
    price_range = db_session.query(
        func.min(Product.price).label('min_price'),
        func.max(Product.price).label('max_price')
    ).first()
    
    # Set default price range if no products exist
    price_min = price_range.min_price if price_range.min_price else 0
    price_max = price_range.max_price if price_range.max_price else 100
    
    # Use filtered values if provided, otherwise use full range
    filter_min = min_price if min_price is not None else price_min
    filter_max = max_price if max_price is not None else price_max

    # Base query
    query = db_session.query(Product)

    # Apply filters
    if category_filter:
        query = query.filter(Product.category_id == category_filter)
    
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))

    # Apply sorting
    if sort_by == 'price_low':
        query = query.order_by(Product.price.asc())
    elif sort_by == 'price_high':
        query = query.order_by(Product.price.desc())
    elif sort_by == 'name_asc':
        query = query.order_by(Product.name.asc())
    elif sort_by == 'name_desc':
        query = query.order_by(Product.name.desc())
    else:  # newest
        query = query.order_by(Product.created_at.desc())

    # Get total count before pagination
    total = query.count()
    
    # Apply pagination
    products = query.limit(per_page).offset((page - 1) * per_page).all()
    
    # Get all categories for sidebar
    categories = db_session.query(Category).all()
    
    # Get best sellers (top 3 featured products)
    best_sellers = db_session.query(Product).filter(Product.is_featured == True).limit(3).all()
    
    # Calculate pagination info
    total_pages = (total + per_page - 1) // per_page
    start_item = (page - 1) * per_page + 1
    end_item = min(page * per_page, total)
    
    return render_template("shop.html", 
                         products=products,
                         categories=categories,
                         best_sellers=best_sellers,
                         total=total,
                         page=page,
                         per_page=per_page,
                         total_pages=total_pages,
                         start_item=start_item,
                         end_item=end_item,
                         sort_by=sort_by,
                         category_filter=category_filter,
                         price_min=int(price_min),
                         price_max=int(price_max),
                         filter_min=int(filter_min),
                         filter_max=int(filter_max))

@app.route("/shop/<int:product_id>")
def shop_details(product_id):
    product = db_session.get(Product, product_id)
    if not product:
        flash("Product not found", "error")
        return redirect(url_for('shop'))
    
    # Get related products (same category, exclude current product)
    related_products = []
    if product.category_id:
        related_products = db_session.query(Product).filter(
            Product.category_id == product.category_id,
            Product.id != product_id
        ).limit(4).all()
    
    return render_template("shop-details.html", product=product, related_products=related_products)

@app.route("/add-to-cart/<int:product_id>", methods=['POST'])
def add_to_cart(product_id):
    # Check if user is logged in
    if not current_user.is_authenticated:
        flash('You should login first to add items to cart', 'error')
        return redirect(url_for('login'))
    
    product = db_session.get(Product, product_id)
    if not product:
        return jsonify({'success': False, 'message': 'Product not found'}), 404
    
    quantity = int(request.form.get('quantity', 1))
    
    if current_user.is_authenticated:
        # User is logged in, use database cart
        user_cart = db_session.query(Cart).filter_by(user_id=current_user.id).first()
        if not user_cart:
            user_cart = Cart(user_id=current_user.id)
            db_session.add(user_cart)
            db_session.commit()
        
        cart_item = db_session.query(CartItem).filter_by(
            cart_id=user_cart.id,
            product_id=product_id
        ).first()
        
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(
                cart_id=user_cart.id,
                product_id=product_id,
                quantity=quantity
            )
            db_session.add(cart_item)
        
        db_session.commit()
    
    flash(f'{product.name} added to cart!', 'success')
    return redirect(request.referrer or url_for('shop'))

@app.route("/cart")
def cart():
    cart_items = []
    total = 0
    
    if current_user.is_authenticated:
        # User is logged in, use database cart
        user_cart = db_session.query(Cart).filter_by(user_id=current_user.id).first()
        if user_cart:
            for cart_item in user_cart.cart_items:
                subtotal = cart_item.get_subtotal()
                cart_items.append({
                    'product': cart_item.product,
                    'quantity': cart_item.quantity,
                    'subtotal': subtotal
                })
                total += subtotal
    else:
        # User not logged in, use session cart
        if 'cart' in flask_session and flask_session['cart']:
            for product_id_str, quantity in flask_session['cart'].items():
                product = db_session.get(Product, int(product_id_str))
                if product:
                    subtotal = product.price * quantity
                    cart_items.append({
                        'product': product,
                        'quantity': quantity,
                        'subtotal': subtotal
                    })
                    total += subtotal
    
    return render_template("cart.html", cart_items=cart_items, total=total)

@app.route("/update-cart/<int:product_id>", methods=['POST'])
def update_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    
    if current_user.is_authenticated:
        # User is logged in, update database cart
        user_cart = db_session.query(Cart).filter_by(user_id=current_user.id).first()
        if user_cart:
            cart_item = db_session.query(CartItem).filter_by(
                cart_id=user_cart.id,
                product_id=product_id
            ).first()
            
            if cart_item:
                if quantity <= 0:
                    db_session.delete(cart_item)
                else:
                    cart_item.quantity = quantity
                db_session.commit()
    else:
        # User not logged in, update session cart
        if 'cart' in flask_session:
            product_id_str = str(product_id)
            if quantity <= 0:
                flask_session['cart'].pop(product_id_str, None)
            else:
                flask_session['cart'][product_id_str] = quantity
            flask_session.modified = True
    
    return redirect(url_for('cart'))

@app.route("/remove-from-cart/<int:product_id>")
def remove_from_cart(product_id):
    if current_user.is_authenticated:
        # User is logged in, remove from database cart
        user_cart = db_session.query(Cart).filter_by(user_id=current_user.id).first()
        if user_cart:
            cart_item = db_session.query(CartItem).filter_by(
                cart_id=user_cart.id,
                product_id=product_id
            ).first()
            if cart_item:
                db_session.delete(cart_item)
                db_session.commit()
    else:
        # User not logged in, remove from session cart
        if 'cart' in flask_session:
            flask_session['cart'].pop(str(product_id), None)
            flask_session.modified = True
    
    flash('Item removed from cart', 'success')
    return redirect(url_for('cart'))

@app.route("/clear-cart")
def clear_cart():
    if current_user.is_authenticated:
        # User is logged in, clear database cart
        user_cart = db_session.query(Cart).filter_by(user_id=current_user.id).first()
        if user_cart:
            for cart_item in user_cart.cart_items:
                db_session.delete(cart_item)
            db_session.commit()
    else:
        # User not logged in, clear session cart
        flask_session.pop('cart', None)
    
    flash('Cart cleared', 'success')
    return redirect(url_for('cart'))

@app.route("/checkout", methods=['GET', 'POST'])
@login_required
def checkout():
    # Get user's cart
    user_cart = db_session.query(Cart).filter_by(user_id=current_user.id).first()
    
    if not user_cart or not user_cart.cart_items:
        flash('Your cart is empty', 'error')
        return redirect(url_for('shop'))
    
    if request.method == 'POST':
        # Validate all required fields
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        city = request.form.get('city', '').strip()
        state = request.form.get('state', '').strip()
        country = request.form.get('country', 'india')
        
        # Check if all required fields are filled
        if not all([first_name, last_name, email, phone, address, city, state]):
            flash('Please fill in all required fields', 'error')
            return redirect(url_for('checkout'))
        
        # Validate phone number (must be exactly 10 digits)
        if not phone.isdigit() or len(phone) != 10:
            flash('Phone number must be exactly 10 digits', 'error')
            return redirect(url_for('checkout'))
        
        # Optional fields
        telephone = request.form.get('telephone', '').strip()
        company = request.form.get('company', '').strip()
        postcode = request.form.get('postcode', '').strip()
        order_notes = request.form.get('order_notes', '').strip()
        
        # Calculate total
        total_amount = user_cart.get_total()
        
        # Create order
        new_order = Order(
            user_id=current_user.id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            telephone=telephone if telephone else None,
            company=company if company else None,
            address=address,
            city=city,
            state=state,
            country=country,
            postcode=postcode if postcode else None,
            order_notes=order_notes if order_notes else None,
            total_amount=total_amount,
            status='pending'
        )
        db_session.add(new_order)
        db_session.flush()  # Get the order ID
        
        # Create order items from cart items
        for cart_item in user_cart.cart_items:
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            db_session.add(order_item)
        
        # Clear the cart
        for cart_item in user_cart.cart_items:
            db_session.delete(cart_item)
        
        db_session.commit()
        
        flash(f'Order #{new_order.id} placed successfully! Thank you for your purchase.', 'success')
        return redirect(url_for('order_confirmation', order_id=new_order.id))
    
    # GET request - show checkout form
    cart_items = []
    total = user_cart.get_total()
    
    for cart_item in user_cart.cart_items:
        cart_items.append({
            'product': cart_item.product,
            'quantity': cart_item.quantity,
            'subtotal': cart_item.get_subtotal()
        })
    
    return render_template("checkout.html", cart_items=cart_items, total=total, user=current_user)

@app.route("/order-confirmation/<int:order_id>")
@login_required
def order_confirmation(order_id):
    order = db_session.get(Order, order_id)
    
    if not order or order.user_id != current_user.id:
        flash('Order not found', 'error')
        return redirect(url_for('shop'))
    
    return render_template("order-confirmation.html", order=order)

@app.route("/orders")
@login_required
def orders():
    # Get all orders for the current user
    user_orders = db_session.query(Order).filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    
    return render_template("orders.html", orders=user_orders)

@app.route("/order/<int:order_id>")
@login_required
def order_details(order_id):
    order = db_session.get(Order, order_id)
    
    if not order or order.user_id != current_user.id:
        flash('Order not found', 'error')
        return redirect(url_for('orders'))
    
    return render_template("order-details.html", order=order)

@app.context_processor
def inject_cart_count():
    """Make cart count available to all templates"""
    cart_count = 0
    if current_user.is_authenticated:
        # User is logged in, get count from database cart
        user_cart = db_session.query(Cart).filter_by(user_id=current_user.id).first()
        if user_cart:
            cart_count = user_cart.get_item_count()
    else:
        # User not logged in, get count from session cart
        if 'cart' in flask_session:
            cart_count = sum(flask_session['cart'].values())
    return dict(cart_count=cart_count)

# ============================================
# ADMIN ROUTES
# ============================================

def admin_required(f):
    """Decorator to require admin access"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/admin/login", methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = db_session.query(User).filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password) and user.is_admin:
            login_user(user)
            flash('Welcome to Admin Dashboard!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials', 'error')
    
    return render_template("admin/admin_login.html")

@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    # Get statistics
    total_users = db_session.query(User).count()
    total_products = db_session.query(Product).count()
    total_categories = db_session.query(Category).count()
    total_orders = db_session.query(Order).count()
    
    # Get recent orders
    recent_orders = db_session.query(Order).order_by(Order.created_at.desc()).limit(5).all()
    
    # Get total revenue
    from sqlalchemy import func
    total_revenue = db_session.query(func.sum(Order.total_amount)).filter(Order.status != 'cancelled').scalar() or 0
    
    return render_template("admin/dashboard.html", 
                         total_users=total_users,
                         total_products=total_products,
                         total_categories=total_categories,
                         total_orders=total_orders,
                         recent_orders=recent_orders,
                         total_revenue=total_revenue)

# ============================================
# ADMIN - USERS MANAGEMENT
# ============================================

@app.route("/admin/users")
@admin_required
def admin_users():
    users = db_session.query(User).all()
    return render_template("admin/users.html", users=users)

@app.route("/admin/users/<int:user_id>/delete", methods=['POST'])
@admin_required
def admin_delete_user(user_id):
    user = db_session.get(User, user_id)
    if user and user.id != current_user.id:  # Can't delete yourself
        db_session.delete(user)
        db_session.commit()
        flash(f'User {user.username} deleted successfully', 'success')
    else:
        flash('Cannot delete this user', 'error')
    return redirect(url_for('admin_users'))

# ============================================
# ADMIN - PRODUCTS MANAGEMENT
# ============================================

@app.route("/admin/products")
@admin_required
def admin_products():
    products = db_session.query(Product).all()
    return render_template("admin/products.html", products=products)

@app.route("/admin/products/add", methods=['GET', 'POST'])
@admin_required
def admin_add_product():
    if request.method == 'POST':
        product = Product(
            name=request.form.get('name'),
            description=request.form.get('description'),
            price=float(request.form.get('price')),
            image_filename=request.form.get('image_filename'),
            stock=int(request.form.get('stock')),
            category_id=int(request.form.get('category_id')) if request.form.get('category_id') else None,
            sku=request.form.get('sku'),
            tags=request.form.get('tags'),
            is_featured=bool(request.form.get('is_featured')),
            is_hot=bool(request.form.get('is_hot')),
            is_sale=bool(request.form.get('is_sale'))
        )
        db_session.add(product)
        db_session.commit()
        flash('Product added successfully', 'success')
        return redirect(url_for('admin_products'))
    
    categories = db_session.query(Category).all()
    return render_template("admin/product_form.html", product=None, categories=categories)

@app.route("/admin/products/<int:product_id>/edit", methods=['GET', 'POST'])
@admin_required
def admin_edit_product(product_id):
    product = db_session.get(Product, product_id)
    if not product:
        flash('Product not found', 'error')
        return redirect(url_for('admin_products'))
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price'))
        product.image_filename = request.form.get('image_filename')
        product.stock = int(request.form.get('stock'))
        product.category_id = int(request.form.get('category_id')) if request.form.get('category_id') else None
        product.sku = request.form.get('sku')
        product.tags = request.form.get('tags')
        product.is_featured = bool(request.form.get('is_featured'))
        product.is_hot = bool(request.form.get('is_hot'))
        product.is_sale = bool(request.form.get('is_sale'))
        
        db_session.commit()
        flash('Product updated successfully', 'success')
        return redirect(url_for('admin_products'))
    
    categories = db_session.query(Category).all()
    return render_template("admin/product_form.html", product=product, categories=categories)

@app.route("/admin/products/<int:product_id>/delete", methods=['POST'])
@admin_required
def admin_delete_product(product_id):
    product = db_session.get(Product, product_id)
    if product:
        db_session.delete(product)
        db_session.commit()
        flash('Product deleted successfully', 'success')
    return redirect(url_for('admin_products'))

# ============================================
# ADMIN - CATEGORIES MANAGEMENT
# ============================================

@app.route("/admin/categories")
@admin_required
def admin_categories():
    categories = db_session.query(Category).all()
    return render_template("admin/categories.html", categories=categories)

@app.route("/admin/categories/add", methods=['GET', 'POST'])
@admin_required
def admin_add_category():
    if request.method == 'POST':
        category = Category(
            name=request.form.get('name'),
            description=request.form.get('description')
        )
        db_session.add(category)
        db_session.commit()
        flash('Category added successfully', 'success')
        return redirect(url_for('admin_categories'))
    
    return render_template("admin/category_form.html", category=None)

@app.route("/admin/categories/<int:category_id>/edit", methods=['GET', 'POST'])
@admin_required
def admin_edit_category(category_id):
    category = db_session.get(Category, category_id)
    if not category:
        flash('Category not found', 'error')
        return redirect(url_for('admin_categories'))
    
    if request.method == 'POST':
        category.name = request.form.get('name')
        category.description = request.form.get('description')
        db_session.commit()
        flash('Category updated successfully', 'success')
        return redirect(url_for('admin_categories'))
    
    return render_template("admin/category_form.html", category=category)

@app.route("/admin/categories/<int:category_id>/delete", methods=['POST'])
@admin_required
def admin_delete_category(category_id):
    category = db_session.get(Category, category_id)
    if category:
        db_session.delete(category)
        db_session.commit()
        flash('Category deleted successfully', 'success')
    return redirect(url_for('admin_categories'))

# ============================================
# ADMIN - ORDERS MANAGEMENT
# ============================================

@app.route("/admin/orders")
@admin_required
def admin_orders():
    orders = db_session.query(Order).order_by(Order.created_at.desc()).all()
    return render_template("admin/orders.html", orders=orders)

@app.route("/admin/orders/<int:order_id>")
@admin_required
def admin_order_details(order_id):
    order = db_session.get(Order, order_id)
    if not order:
        flash('Order not found', 'error')
        return redirect(url_for('admin_orders'))
    return render_template("admin/order_details.html", order=order)

@app.route("/admin/orders/<int:order_id>/update-status", methods=['POST'])
@admin_required
def admin_update_order_status(order_id):
    order = db_session.get(Order, order_id)
    if order:
        new_status = request.form.get('status')
        order.status = new_status
        db_session.commit()
        flash(f'Order #{order_id} status updated to {new_status}', 'success')
    return redirect(url_for('admin_order_details', order_id=order_id))

@app.route("/admin/orders/<int:order_id>/delete", methods=['POST'])
@admin_required
def admin_delete_order(order_id):
    order = db_session.get(Order, order_id)
    if order:
        db_session.delete(order)
        db_session.commit()
        flash('Order deleted successfully', 'success')
    return redirect(url_for('admin_orders'))

# ============================================
# ADMIN - CHANGE PASSWORD
# ============================================

@app.route("/admin/change-password", methods=['GET', 'POST'])
@admin_required
def admin_change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Verify current password
        if not check_password_hash(current_user.password_hash, current_password):
            flash('Current password is incorrect', 'error')
            return redirect(url_for('admin_change_password'))
        
        # Check if new passwords match
        if new_password != confirm_password:
            flash('New passwords do not match', 'error')
            return redirect(url_for('admin_change_password'))
        
        # Check password length
        if len(new_password) < 6:
            flash('New password must be at least 6 characters long', 'error')
            return redirect(url_for('admin_change_password'))
        
        # Update password - get fresh user from database
        user = db_session.get(User, current_user.id)
        user.password_hash = generate_password_hash(new_password)
        db_session.commit()
        
        flash('Password changed successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template("admin/change_password.html")












def init_db():
    """Initialize the database with tables"""
    Base.metadata.create_all(engine)
    print("Database tables created successfully!")

def add_sample_data():
    """Add sample products and categories for testing"""
    # Check if data already exists
    if db_session.query(Category).count() > 0:
        print("Sample data already exists!")
        return
    
    # Add categories
    categories_data = [
        {"name": "Outdoor Plants", "description": "Plants perfect for outdoor gardens"},
        {"name": "Indoor Plants", "description": "Plants for indoor decoration"},
        {"name": "Office Plants", "description": "Low maintenance plants for offices"},
        {"name": "Potted Plants", "description": "Plants in decorative pots"},
        {"name": "Flowering Plants", "description": "Beautiful flowering plants"}
    ]
    
    categories = []
    for cat_data in categories_data:
        category = Category(**cat_data)
        db_session.add(category)
        categories.append(category)
    
    db_session.commit()
    
    # Add sample products
    products_data = [
        {"name": "Cactus Flower", "description": "Beautiful cactus with colorful flowers", "price": 10.99, "image_filename": "img/bg-img/40.png", "stock": 50, "category": categories[0], "sku": "CT201801", "tags": "cactus, flower, hot", "is_hot": True, "is_featured": True},
        {"name": "Tulip Flower", "description": "Classic tulip plant", "price": 11.99, "image_filename": "img/bg-img/41.png", "stock": 30, "category": categories[4], "sku": "CT201802", "tags": "tulip, flower", "is_featured": True},
        {"name": "Recuerdos Plant", "description": "Elegant indoor plant", "price": 9.99, "image_filename": "img/bg-img/34.jpg", "stock": 40, "category": categories[1], "sku": "CT201803", "tags": "indoor, green", "is_featured": True},
        {"name": "Succulent Mix", "description": "Mixed succulent arrangement", "price": 15.99, "image_filename": "img/bg-img/42.png", "stock": 25, "category": categories[3], "sku": "CT201804", "tags": "succulent, potted"},
        {"name": "Fern Plant", "description": "Lush green fern", "price": 12.50, "image_filename": "img/bg-img/43.png", "stock": 35, "category": categories[1], "sku": "CT201805", "tags": "fern, indoor, green"},
        {"name": "Aloe Vera", "description": "Medicinal aloe vera plant", "price": 8.99, "image_filename": "img/bg-img/44.png", "stock": 60, "category": categories[2], "sku": "CT201806", "tags": "aloe, medicinal"},
        {"name": "Snake Plant", "description": "Low maintenance snake plant", "price": 14.99, "image_filename": "img/bg-img/45.png", "stock": 45, "category": categories[2], "sku": "CT201807", "tags": "snake plant, office"},
        {"name": "Orchid", "description": "Beautiful orchid flower", "price": 25.99, "image_filename": "img/bg-img/46.png", "stock": 20, "category": categories[4], "sku": "CT201808", "tags": "orchid, flower, elegant"},
        {"name": "Peace Lily", "description": "Peaceful white lily", "price": 18.99, "image_filename": "img/bg-img/47.png", "stock": 28, "category": categories[1], "sku": "CT201809", "tags": "lily, flower, peace", "is_sale": True},
        {"name": "Bonsai Tree", "description": "Miniature bonsai tree", "price": 35.99, "image_filename": "img/bg-img/48.png", "stock": 15, "category": categories[3], "sku": "CT201810", "tags": "bonsai, tree, miniature"},
    ]
    
    for prod_data in products_data:
        product = Product(**prod_data)
        db_session.add(product)
    
    db_session.commit()
    print("Sample data added successfully!")

# Vercel requires the app to be available at module level
app = app

if __name__ == "__main__":
    # Initialize database
    init_db()
    
    # Add sample data (comment out after first run if you don't want to reset data)
    # add_sample_data()
    
    app.run(debug=True, port=5001)