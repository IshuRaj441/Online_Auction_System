from flask_socketio import SocketIO, emit
from models import db, AuctionItem

socketio = SocketIO(cors_allowed_origins="*")

def init_sockets(app):
    socketio.init_app(app)

@socketio.on("place_bid")
def place_bid(data):
    item = AuctionItem.query.get(data["item_id"])

    if data["amount"] > item.highest_bid:
        item.highest_bid = data["amount"]
        item.highest_bidder = data["bidder"]
        db.session.commit()

        emit("bid_update", {
            "item_id": item.id,
            "amount": item.highest_bid,
            "bidder": item.highest_bidder
        }, broadcast=True)
