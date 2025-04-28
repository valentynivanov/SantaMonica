from flask import Flask, flash, redirect, render_template, request, session, jsonify, g
import sqlite3
import re
""" from flask_mail import Mail, Message """
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# Configure application
app = Flask(__name__)

# Configure Flask-Mail
""" app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'your_mail'
app.config['MAIL_PASSWORD'] = 'your_password'
mail = Mail(app) """

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'your-secret-key'
Session(app)

# Configure SQLite database
# Function to get a database connection
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("project.db")
        g.db.row_factory = sqlite3.Row
    return g.db

# Close the database connection at the end of the request
@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

# print(db.fetchall())

# Phone number validation function
def validate_number(contactnumber):
    pattern="[0]{1}[7]{1}[0-9]{9}"
    if re.match(pattern,contactnumber):
        return True
    return False

# Email validation function
def validate_email(email):
    # Email validation regex
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    return False

# Password validation function
def validate_password(password):
    # Password must be 8-20 characters long, contain letters and numbers, and no spaces, special characters, or emojis
    pattern = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,20}$'
    if re.match(pattern, password):
        return True
    return False

# Postcode validation function
def valid_postcode(postcode):
    # first part below, second part: 1 0-9 number,  2 A-Z letters
    postcodes = ["M1","M11","M12","M13","M14","M15","M16","M17","M18","M19","M2","M20","M21","M22","M23","M24","M25","M26","M27","M28","M29","M3","M30","M31","M32","M33","M34","M35","M38","M4","M40","M41","M42","M43","M44","M45","M46","M5","M6","M60","M7","M8","M9","M90"]
    # Regex for second part of the postcode: 1 digit followed by 2 uppercase letters
    pattern = r"^\d[A-Z]{2}$"

    # Split postcode into two parts
    parts = postcode.split()
    if len(parts) != 2:
        return False

    first_part, second_part = parts

    # Validate both parts
    if first_part in postcodes and re.match(pattern, second_part):
        return True

    return False

@app.before_request
def save_cart_before_login():
    # Save the cart only if the user is not logged in and the cart exists
    if session.get("user_id") is None and "cart" in session:
        session["saved_cart"] = session.get("cart", {})
        session.modified = True  # Mark session as modified

@app.after_request
def after_request(response):
    """Ensure responses aren't cached unless they are static assets"""
    if 'static' in request.path:
        response.headers["Cache-Control"] = "public, max-age=31536000"  # Long-term caching for static files
    else:
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
    return response

def get_cart_count():
    """Helper function to get the total number of items in the cart."""
    if 'cart' in session:
        return sum(session['cart'].values())
    return 0

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        if not email or not validate_email(email):
            flash("Must provide a valid email address")
            return redirect("/register")

        username = request.form.get("username")
        if not username:
            flash("Must provide username")
            return redirect("/register")

        password = request.form.get("password")
        if not password:
             flash("Must provide password")
             return redirect("/register")
        if not validate_password(password):
            flash("Your password must be 8-20 characters long, contain letters and numbers, and must not contain spaces, special characters, or emoji.")
            return redirect("/register")

        confirmation = request.form.get("confirmation")
        if not confirmation or password != confirmation:
             flash("Passwords do not match")
             return redirect("/register")

        if not email or not username or not password or not confirmation:
             return redirect("/register")

        hash = generate_password_hash(password, method='pbkdf2', salt_length=16)

        # Check if email already exist
        db = get_db()
        check = db.execute("SELECT email FROM users WHERE email=?", email).fetchall()
        if check:
            return flash("User already exist")
        else:
            db.execute("INSERT INTO users (email, username, hash) VALUES (?,?,?)", email, username, hash)

        # Restore cart if it exists
        if "saved_cart" in session:
            session["cart"] = session.pop("saved_cart")
            session.modified = True

        return redirect("/login")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Retrieve cart count from session
        cart_count = get_cart_count()
        return render_template("register.html", cart_count=cart_count)

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        # Ensure email was submitted
        if not email:
            flash("Must provide email")
            return render_template("login.html", error=True)

        # Ensure username was submitted
        if not password:
            flash("Must provide password")
            return render_template("login.html", error=True)

        # Query database for email
        db = get_db()
        rows = db.execute(
            "SELECT id, hash FROM users WHERE email=?", email
        ).fetchall()

        # Ensure email exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            # If login fails, pass a flag to display 'forgot password' button
            return render_template("login.html", error=True, email=request.form.get("email"))

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Restore cart if it exists
        if "saved_cart" in session:
            session["cart"] = session.pop("saved_cart")
            session.modified = True

        # Redirect user to home page
        return redirect("/cart")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Retrieve cart count from session
        cart_count = get_cart_count()
        return render_template("login.html", error=False, cart_count=cart_count)

@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":

        email = request.form.get("email")
        if not email or not validate_email(email):
            flash("Must provide a valid email address")
            return redirect("/forgot_password")

        # Ensure user exists
        db = get_db()
        rows = db.execute("SELECT id FROM users WHERE email = ?", email).fetchall()
        if len(rows) != 1:
            return flash("User does not exist")

        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        # Ensure password and confirmation match
        if not new_password or new_password != confirmation:
            return flash("Passwords do not match")

        if not validate_password(new_password):
            flash("Your password must be 8-20 characters long, contain letters and numbers, and must not contain spaces, special characters, or emoji.")
            return redirect("/forgot_password")

        # Update the user's password
        new_hash = generate_password_hash(new_password)
        db.execute("UPDATE users SET hash = ? WHERE email = ?", new_hash, email)

        flash("Password successfully updated!")
        return redirect("/login")

    # Retrieve cart count from session
    cart_count = get_cart_count()
    return render_template("forgot_password.html", cart_count=cart_count)

@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/")
def index():
    # Retrieve cart count from session
    cart_count = get_cart_count()
    return render_template("index.html", cart_count=cart_count)

@app.route("/menu")
def menu():
    db = get_db()  # Get a new connection for this request
    # Fetch products for each category
    pizzas = db.execute("SELECT * FROM products WHERE category = 'pizza'").fetchall()
    sides = db.execute("SELECT * FROM products WHERE category = 'side'").fetchall()
    drinks = db.execute("SELECT * FROM products WHERE category = 'drink'").fetchall()

    # Retrieve cart from session
    cart = session.get('cart', {})

     # Create a dictionary mapping product IDs to quantities
    quantities = {int(product_id): quantity for product_id, quantity in cart.items()}

    cart_count = get_cart_count()
    return render_template("menu.html", pizzas=pizzas, sides=sides, drinks=drinks ,quantities=quantities, cart_count=cart_count)

@app.route('/add-to-cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = {}

    if product_id in session['cart']:
        session['cart'][product_id] += 1
    else:
        session['cart'][product_id] = 1

    session.modified = True

    # Fetch product details
    db = get_db()
    product = db.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()  # Pass product_id as a tuple
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    subtotal = product['price'] * session['cart'][product_id]

    total_price = sum(
        db.execute("SELECT price FROM products WHERE id = ?", (pid,)).fetchone()['price'] * qty
        for pid, qty in session['cart'].items()
    )

    return jsonify({
        'product_id': product_id,
        'cart_count': sum(session['cart'].values()),
        'new_quantity': session['cart'][product_id],
        'subtotal': subtotal,
        'total_price': total_price,
    })

@app.route('/cart')
def cart():
    cart_items = []
    total_price = 0
    cart_count = 0

    if 'cart' in session and session['cart']:
        product_ids = list(session['cart'].keys())

        # Create placeholders
        placeholders = ', '.join(['?'] * len(product_ids))

        # Format the SQL query
        query = f"SELECT * FROM products WHERE id IN ({placeholders})"

        # Execute the query with the unpacked product IDs
        db = get_db()
        products = db.execute(query, tuple(product_ids)).fetchall() # Pass product_ids as a tuple

        for product in products:
            product_id = product["id"]
            quantity = session['cart'][product_id]
            product_dict = {
                "image_path": product["image_path"],
                "id": product_id,
                "name": product["name"],
                "description": product["description"],
                "price": product["price"],
                "quantity": quantity,
            }
            cart_items.append(product_dict)
            total_price += product["price"] * quantity

            cart_count = get_cart_count()

    return render_template('cart.html', cart_items=cart_items, total_price=total_price, cart_count=cart_count)

@app.route('/remove-from-cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    if 'cart' not in session or product_id not in session['cart']:
        return jsonify({'error': 'Product not in cart'}), 404

    current_quantity = session['cart'][product_id]

    if current_quantity > 1:
        session['cart'][product_id] -= 1
    else:
        del session['cart'][product_id]  # Remove item if quantity is 1

    session.modified = True

    # Recalculate total price
    db = get_db()
    total_price = sum(
        db.execute("SELECT price FROM products WHERE id = ?", (pid,)).fetchone()['price'] * qty
        for pid, qty in session['cart'].items()
    )

    cart_count = sum(session['cart'].values())

    # Return updated data
    return jsonify({
        'cart_count': cart_count,
        'new_quantity': session['cart'].get(product_id, 0),
        'subtotal': db.execute("SELECT price FROM products WHERE id = ?", (product_id,)).fetchone()['price'] * session['cart'].get(product_id, 0),
        'total_price': total_price
    })

@app.route('/clear-cart', methods=['POST'])
def clear_cart():
    # Clear the cart by removing the 'cart' key from the session
    session.pop('cart', None)

    flash('Your cart has been cleared.', 'success')

    return redirect('/cart')


@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = session.get('cart', {})
    if not cart_items:
        flash("Your cart is empty!")
        return redirect('/')

    if request.method == "POST":
        # Collect form inputs
        name = request.form.get("name")
        contactnumber = request.form.get("contactnumber")
        email = request.form.get("email")
        postcode = request.form.get("postcode")
        address_line1 = request.form.get("address_line1")
        address_line2 = request.form.get("address_line2")
        address_line3 = request.form.get("address_line3")
        delivery_option = request.form.get("delivery_option")

        # Validate inputs
        if not name:
            flash("Must provide a valid name")
            return redirect("/checkout")
        if not contactnumber or not validate_number(contactnumber):
            flash("Must provide a valid contact number")
            return redirect("/checkout")
        if not email or not validate_email(email):
            flash("Must provide a valid email address")
            return redirect("/checkout")

        print("Delivery Option:", delivery_option)

        if not delivery_option:
            flash("Please select a delivery option.")
            return redirect("/checkout")

        if delivery_option == "delivery":
            if not postcode.startswith("M"):
                flash("We only deliver to Manchester postcodes. Please select 'Collect' to proceed.")
                return redirect("/checkout")
            if not address_line1 or not address_line2 or not address_line3:
                flash("Complete address is required for delivery.")
                return redirect("/checkout")

        if delivery_option == "collect":
            if not postcode or postcode or postcode.startswith("M"):
                # Skip address validation for collection
                pass
            else:
                flash("You can only collect from our restaurant.")
                return redirect("/checkout")

        # Send email
        """ msg = Message(
                "Order Confirmation",
                sender="Santa Monica",
                recipients=[email]
        )
        msg.body = f"Hi {name},\n\nYour order has been placed successfully! While we are prepairing your order, please check your email for updates or expect a call from our team member soon.\n\nBest regards,\nSanta Monica Team"
        try:
            mail.send(msg)
        except Exception as e:
            print(f"Failed to send email: {e}") """

        # Clear the cart after successful or failed order placement
        session.pop("cart", None)

        try:
            return redirect("/success")
        except ValueError:
            return render_template('fail.html')
    db = get_db()

    total_price = sum(
        db.execute("SELECT price FROM products WHERE id = ?", (pid,)).fetchone()['price'] * qty
        for pid, qty in session['cart'].items()
    )
    # Retrieve cart count from session
    cart_count = get_cart_count()
    return render_template('checkout.html', cart_count=cart_count, total_price=total_price)


@app.route('/about', methods=['GET','POST'])
def about():
    # Retrieve cart count from session
    cart_count = get_cart_count()
    return render_template('about.html', cart_count=cart_count)


@app.route('/contact', methods=['GET','POST'])
def contact():
    # Retrieve cart count from session
    cart_count = get_cart_count()
    return render_template('contact_us.html', cart_count=cart_count)

@app.route('/success', methods=['GET','POST'])
def success():
    # Retrieve cart count from session
    cart_count = get_cart_count()
    return render_template('success.html', cart_count=cart_count)
