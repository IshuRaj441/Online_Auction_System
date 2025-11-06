@Query(value = "SELECT * FROM auction_analytics", nativeQuery = true)
List<Map<String, Object>> getAnalytics();