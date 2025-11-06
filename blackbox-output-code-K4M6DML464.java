@RestController
@RequestMapping("/api/auctions")
public class AuctionController {
    // ... existing code ...

    @GetMapping("/analytics")
    public List<Map<String, Object>> getAnalytics() {
        // Query the materialized view (use native query in repo)
        return itemRepo.getAnalytics();  // Implement in ItemRepository
    }
}