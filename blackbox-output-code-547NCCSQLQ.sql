-- Existing tables from before (users, items, bids)

-- Add indexes for performance
CREATE INDEX idx_items_auction_end ON items (auction_end);
CREATE INDEX idx_bids_item_id ON bids (item_id);
CREATE INDEX idx_bids_bidder_id ON bids (bidder_id);

-- Partition bids table by year for scalability
CREATE TABLE bids_y2023 PARTITION OF bids FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');
CREATE TABLE bids_y2024 PARTITION OF bids FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

-- Stored procedure to close auctions and notify winners
CREATE OR REPLACE PROCEDURE close_auction(item_id INT)
LANGUAGE plpgsql AS $$
DECLARE
    winner_id INT;
BEGIN
    SELECT bidder_id INTO winner_id FROM bids WHERE item_id = item_id ORDER BY amount DESC LIMIT 1;
    UPDATE items SET auction_end = NOW() WHERE id = item_id;
    -- Simulate notification (integrate with email service)
    RAISE NOTICE 'Auction closed for item %; Winner: %', item_id, winner_id;
END;
$$;

-- Materialized view for real-time analytics (refresh via cron or trigger)
CREATE MATERIALIZED VIEW auction_analytics AS
SELECT 
    i.id,
    i.title,
    json_build_object(
        'total_bids', COUNT(b.id),
        'highest_bid', MAX(b.amount),
        'bidders', json_agg(DISTINCT b.bidder_id)
    ) AS stats
FROM items i
LEFT JOIN bids b ON i.id = b.item_id
GROUP BY i.id, i.title;