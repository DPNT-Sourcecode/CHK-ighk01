class CheckoutSolution:
    # skus = unicode string
    def checkout(self, skus):
        # Check for illegal input
        if skus == "":
            return 0
        if not isinstance(skus, str) or not skus.isalpha():
            return -1
            
        # Initialize the price table
        price_table = {
            'A': 50, 'B': 30, 'C': 20, 'D': 15, 'E': 40, 'F': 10,
            'G': 20, 'H': 10, 'I': 35, 'J': 60, 'K': 70, 'L': 90,
            'M': 15, 'N': 40, 'O': 10, 'P': 50, 'Q': 30, 'R': 50,
            'S': 20, 'T': 20, 'U': 40, 'V': 50, 'W': 20, 'X': 17,
            'Y': 20, 'Z': 21
        }
        
        # Initialize multi-buy offers (item: [(quantity, price), ...])
        # Offers are sorted in descending order of quantity for better customer benefit
        multi_buy_offers = {
            'A': [(5, 200), (3, 130)],
            'B': [(2, 45)],
            'H': [(10, 80), (5, 45)],
            'K': [(2, 120)],
            'P': [(5, 200)],
            'Q': [(3, 80)],
            'V': [(3, 130), (2, 90)]
        }
        
        # Get-one-free offers (buy X, get Y free)
        free_item_offers = {
            'E': (2, 'B'),  # Buy 2E, get one B free
            'F': (2, 'F'),  # Buy 2F, get one F free
            'N': (3, 'M'),  # Buy 3N, get one M free
            'R': (3, 'Q'),  # Buy 3R, get one Q free
            'U': (3, 'U')   # Buy 3U, get one U free
        }
        
        # Group discount offers (group of items, quantity, price)
        group_offers = [
            (['S', 'T', 'X', 'Y', 'Z'], 3, 45)  # Buy any 3 of (S,T,X,Y,Z) for 45
        ]
        
        # Initialize total price and item counts
        total_price = 0
        item_counts = {}
        
        # Count the occurrences of each item
        for item in skus:
            if item not in price_table:
                return -1
            if item in item_counts:
                item_counts[item] += 1
            else:
                item_counts[item] = 1
        
        # Apply group discount offers first
        # These are processed first as they potentially give the best value to customer
        for group_items, required_count, offer_price in group_offers:
            # Count how many qualifying items we have
            qualifying_items = []
            for item in group_items:
                if item in item_counts:
                    # Add each qualifying item to the list, repeated by its count
                    qualifying_items.extend([item] * item_counts[item])
            
            # Sort items by price in descending order to get the best value
            # This ensures we use the most expensive items in the group offer
            qualifying_items.sort(key=lambda x: price_table[x], reverse=True)
            
            # Apply the group offer as many times as possible
            num_offers_applied = len(qualifying_items) // required_count
            if num_offers_applied > 0:
                # Add the offers to the total price
                total_price += num_offers_applied * offer_price
                
                # Remove the used items from the counts
                used_items = qualifying_items[:num_offers_applied * required_count]
                for item in used_items:
                    item_counts[item] -= 1
                    # Remove the item if its count becomes 0
                    if item_counts[item] == 0:
                        del item_counts[item]
        
        # Apply free item offers
        free_items = {}
        for item, (required_count, free_item) in free_item_offers.items():
            if item in item_counts:
                if free_item == item:  # Self-referential offer like "3U get one U free"
                    # We need groups of (required_count + 1) where only required_count are paid
                    groups = item_counts[item] // (required_count + 1)
                    if groups > 0:
                        if item in free_items:
                            free_items[item] += groups
                        else:
                            free_items[item] = groups
                elif free_item in item_counts:  # Cross-item offer like "2E get one B free"
                    # Calculate how many free items customer gets
                    num_free = item_counts[item] // required_count
                    # Limit to the number of free items actually in the basket
                    actual_free = min(num_free, item_counts[free_item])
                    if actual_free > 0:
                        if free_item in free_items:
                            free_items[free_item] += actual_free
                        else:
                            free_items[free_item] = actual_free
        
        # Calculate the total price with special offers
        for item, count in item_counts.items():
            # Subtract any free items from the count
            if item in free_items:
                count = max(0, count - free_items[item])
            
            if item in multi_buy_offers:
                # Apply multi-buy offers in descending order of quantity
                remaining_count = count
                for offer_count, offer_price in multi_buy_offers[item]:
                    if remaining_count >= offer_count:
                        offer_applications = remaining_count // offer_count
                        total_price += offer_applications * offer_price
                        remaining_count = remaining_count % offer_count
                
                # Add the price of remaining items
                total_price += remaining_count * price_table[item]
            else:
                # No special offer for this item
                total_price += count * price_table[item]
        
        return total_price

