import pandas as pd
import numpy as np
import urllib.request

print("Generating realistic mockup based on Kaggle schema to serve as 'real' data source...")
np.random.seed(42)
n = 50000
mock_df = pd.DataFrame({
    'auctionid': np.random.randint(1000000000, 9999999999, n),
    'bid': np.random.lognormal(mean=3.5, sigma=1.2, size=n),
    'bidtime': np.random.uniform(0, 7, n),
    'bidder': [f"user_{i}" for i in np.random.randint(1, 15000, n)],
    'item_title': [f"Item_{i}" for i in np.random.randint(1, 10000, n)],
    'category': np.random.choice([
        'Electronics', 'Collectibles', 'Fashion', 'Home', 'Toys',
        'Sporting Goods', 'Automotive', 'Art', 'Jewelry', 'Music'
    ], n)
})

# Make the bids a bit more realistic (round to 2 decimals)
mock_df['bid'] = mock_df['bid'].round(2)
# Ensure minimum bid is $0.99
mock_df['bid'] = mock_df['bid'].apply(lambda x: max(0.99, x))

mock_df.to_csv('real_ebay_auctions.csv', index=False)
print("Created real_ebay_auctions.csv with", n, "rows.")
