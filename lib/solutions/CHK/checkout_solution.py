"""
CHK_R1
ROUND 1 - Our supermarket
The purpose of this challenge is to implement a supermarket checkout that calculates the total price of a number of items.

In a normal supermarket, things are identified using Stock Keeping Units, or SKUs.
In our store, we'll use individual letters of the alphabet (A, B, C, and so on).
Our goods are priced individually. In addition, some items are multi-priced: buy n of them, and they'll cost you y pounds.
For example, item A might cost 50 pounds individually, but this week we have a special offer:
 buy three As and they'll cost you 130.

Our price table and offers:
+------+-------+----------------+
| Item | Price | Special offers |
+------+-------+----------------+
| A    | 50    | 3A for 130     |
| B    | 30    | 2B for 45      |
| C    | 20    |                |
| D    | 15    |                |
+------+-------+----------------+


Notes:
 - For any illegal input return -1

In order to complete the round you need to implement the following method:

checkout(string) -> integer
 - param[0] = a string containing the SKUs of all the products in the basket
 - @return = an integer representing the total checkout value of the items


"""
class CheckoutSolution:

    # skus = unicode string
    def checkout(self, skus):
        # Check for illegal input
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
        

