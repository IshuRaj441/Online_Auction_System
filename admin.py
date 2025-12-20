from flask import Blueprint, render_template
from models import User, AuctionItem

admin = Blueprint("admin", __name__)

@admin.route("/admin")
def admin_panel():
    users = User.query.all()
    items = AuctionItem.query.all()
    return render_template("admin.html", users=users, items=items)
