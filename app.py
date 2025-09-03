from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import Error
import json

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ---------- DB Connection ----------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",  # your MySQL password
        database="bookstore"
    )

# ---------- HOME ----------
@app.route("/")
def index():
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT id, title, author, price, stock FROM books")
        books = cur.fetchall()
        cur.close()
        conn.close()
    except Error as e:
        return f"Database error: {e}", 500
    return render_template("index.html", books=books)

# ---------- ADD TO CART ----------
@app.route("/add_to_cart/<int:book_id>", methods=["POST"])
def add_to_cart(book_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT id, title, author, price, stock FROM books WHERE id = %s", (book_id,))
        book = cur.fetchone()
        cur.close()
        conn.close()
    except Error as e:
        return f"Database error: {e}", 500

    if not book:
        flash("Book not found!")
        return redirect(url_for("index"))

    cart = session.get("cart", [])

    # Check if book already in cart, increase quantity
    found = False
    for item in cart:
        if int(item["id"]) == int(book["id"]):
            item["quantity"] += 1
            found = True
            break
    if not found:
        cart.append({
            "id": int(book["id"]),
            "title": str(book["title"]),
            "author": str(book["author"]),
            "price": float(book["price"]),
            "quantity": 1
        })

    session["cart"] = cart
    session.modified = True
    flash(f"Added {book['title']} to cart!")
    return redirect(url_for("cart"))

# ---------- VIEW CART ----------
@app.route("/cart")
def cart():
    cart = session.get("cart", [])
    total = sum(item["price"] * item["quantity"] for item in cart) if cart else 0.0
    return render_template("cart.html", cart=cart, total=total)

# ---------- REMOVE ITEM ----------
@app.route("/remove_from_cart/<int:book_id>", methods=["POST"])
def remove_from_cart(book_id):
    cart = session.get("cart", [])
    cart = [item for item in cart if int(item["id"]) != book_id]
    session["cart"] = cart
    session.modified = True
    flash("Item removed from cart.")
    return redirect(url_for("cart"))

# ---------- CLEAR CART ----------
@app.route("/clear_cart")
def clear_cart():
    session.pop("cart", None)
    flash("Cart cleared.")
    return redirect(url_for("cart"))

# ---------- CHECKOUT ----------
@app.route("/checkout")
def checkout():
    cart = session.get("cart", [])
    if not cart:
        flash("Your cart is empty!")
        return redirect(url_for("index"))
    total = sum(item["price"] * item["quantity"] for item in cart)
    return render_template("checkout.html", cart=cart, total=total)

# ---------- CONFIRM ORDER ----------
@app.route("/confirm_order", methods=["POST"])
def confirm_order():
    # Here you can save order to DB or just clear the cart
    session.pop("cart", None)
    flash("Your order has been placed successfully!")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
