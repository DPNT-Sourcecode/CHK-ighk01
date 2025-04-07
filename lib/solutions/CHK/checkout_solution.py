
class CheckoutSolution:
    # skus = unicode string
    def checkout(self, skus):
        # Check for illegal input
        if skus == "":
            return 0
        if not isinstance(skus, str) or not skus.isalpha():
            return -1
            
        # Initialize the price table
        price_table = {'A': 50, 'B': 30, 'C': 20, 'D': 15, 'E': 40, 'F': 10}
        
        # Initialize multi-buy offers (item: [(quantity, price), ...])
        # Offers are sorted in descending order of quantity for better customer benefit
        multi_buy_offers = {
            'A': [(5, 200), (3, 130)],
            'B': [(2, 45)]
        }
        
        # Get-one-free offers (buy X, get Y free)
        free_item_offers = {
            'E': (2, 'B'),  # Buy 2E, get one B free
            'F': (2, 'F')   # Buy 2F, get one F free
        }
        
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
        
        # Apply free item offers first
        free_items = {}
        for item, (required_count, free_item) in free_item_offers.items():
            if item in item_counts:
                if free_item == item:  # Self-referential offer like "2F get one F free"
                    # We need groups of 3 where only 2 are paid
                    groups = item_counts[item] // 3
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


