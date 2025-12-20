from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from datetime import datetime, timedelta
from models import db, User, AuctionItem, Bid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secure-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user and user.password == request.form["password"]:
            login_user(user)
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/register", methods=["POST"])
def register():
    user = User(username=request.form["username"], password=request.form["password"])
    db.session.add(user)
    db.session.commit()
    return redirect("/")

@app.route("/dashboard")
@login_required
def dashboard():
    items = AuctionItem.query.all()
    return render_template("dashboard.html", items=items)

@app.route("/create", methods=["POST"])
@login_required
def create_auction():
    item = AuctionItem(
        title=request.form["title"],
        description=request.form["description"],
        end_time=datetime.utcnow() + timedelta(days=1)
    )
    db.session.add(item)
    db.session.commit()
    return redirect("/dashboard")

@app.route("/bid/<int:item_id>", methods=["POST"])
@login_required
def bid(item_id):
    item = AuctionItem.query.get(item_id)
    bid_amount = float(request.form["amount"])

    if datetime.utcnow() < item.end_time and bid_amount > item.highest_bid:
        item.highest_bid = bid_amount
        item.highest_bidder = request.form["bidder"]
        db.session.commit()

    return redirect("/dashboard")

if __name__ == "__main__":
    app.run(debug=True)
