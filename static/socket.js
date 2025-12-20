const socket = io();

function placeBid(itemId, bidder, amount) {
  socket.emit("place_bid", {
    item_id: itemId,
    bidder: bidder,
    amount: amount
  });
}

socket.on("bid_update", data => {
  document.getElementById(`bid-${data.item_id}`).innerText =
    data.amount + " by " + data.bidder;
});
