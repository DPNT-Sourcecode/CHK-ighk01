
class CheckoutSolution:

    # skus = unicode string
    def checkout(self, skus):
        # Check for illegal input
        if skus is "":
            return 0
        if not isinstance(skus, str) or not skus.isalpha():
            return -1

        # Initialize the price table and special offers
        price_table = {'A': 50, 'B': 30, 'C': 20, 'D': 15}
        special_offers = {'A': (3, 130), 'B': (2, 45)}

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
        # Calculate the total price considering special offers  
        for item, count in item_counts.items():
            if item in special_offers:
                offer_count, offer_price = special_offers[item]
                total_price += (count // offer_count) * offer_price
                total_price += (count % offer_count) * price_table[item]
            else:
                total_price += count * price_table[item]
        return total_price
        




