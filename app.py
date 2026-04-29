from flask import Flask, render_template, flash, request, redirect, url_for, session
from config import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY


cart = [] # Set an empty list to hold the items in the cart
users = {"admin": "password"}



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/menu")
def menu():
    return render_template("menu.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/add_to_cart", methods=["POST", "GET"])
def add_to_cart():
    if request.method == "POST":
        item = request.form.get("item")
        quantity = request.form.get("quantity", "1")
        if item:
            cart.append({"item": item.replace("_", " ").title(), "quantity": quantity})
            return redirect(url_for("menu"))
    return render_template("add_to_cart.html")


@app.route("/reservations", methods=["POST", "GET"])
def reservations():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        date = request.form.get("date")
        time = request.form.get("time")
        guest = request.form.get("guest")
        
        if name and email and date and time and guest:
            flash("Reservation successful!", "success")
            return redirect(url_for("index"))
    return render_template("reservations.html")


@app.route("/cart")
@app.route("/view_cart")
@app.route("/view_cart.html", methods=["POST", "GET"])
def view_cart():
    return render_template("view_cart.html", cart=cart)



    




# login and register routes for user authentication

@app.route("/login", methods=["POST", "GET"])
def login():
    """
    1. get the username and password from the form
    2. check if the username and password are correct
    3. if correct, redirect to the home page
    4. if incorrect, show an error message
    5. if the user is already logged in, redirect to the home page
    6. if the user is not logged in, show the login form
    7. if the user clicks the register link, redirect to the register page
    8. return the login template
    """
    if request.method == "POST":
        # get the username and password from the form
        username = request.form.get("username")
        password = request.form.get("password")
        
        # check if the username and password are correct 
        if users.get(username) == password:
            return redirect(url_for("index"))
        # if incorrect, show an error message
        error = "Invalid username or password"
        return render_template("login.html", error=error)
    return render_template("login.html")
        

@app.route("/register", methods=["POST", "GET"])
def register():
    """
    1. get the username and password from the form
    2. check if the username is already taken
    3. if the username is already taken, show an error message
    4. if the username is not taken, create a new user and redirect to the login page
    5. return the register template
    """
    if request.method == "POST":
        # get the username and password from the form
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        
        # check if the username is already taken
        if username in users:
            error = "Username already taken"
            return render_template("register.html", error=error)
        # if the username is not taken, create a new user and redirect to the login page
        users[username] = {"password": password, "email": email}
        return redirect(url_for("login"))
    return render_template("register.html")



if __name__ == "__main__":
    app.run(debug=True)
