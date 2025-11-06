package com.auction.service;

import com.auction.entity.Item;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

@Service
public class AuctionService {
    // ... existing code ...

    @Cacheable("items")
    public List<Item> getActiveItems() {
        return itemRepo.findByAuctionEndAfter(LocalDateTime.now());
    }
}