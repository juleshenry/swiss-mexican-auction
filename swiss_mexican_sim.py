import pandas as pd
import numpy as np
import networkx as nx
import random
import time

def generate_synthetic_ebay_data(num_items=10000, num_categories=50):
    """
    Simulates a base Kaggle-style eBay dataset.
    """
    print(f"Generating {num_items} synthetic eBay items...")
    items = []
    for i in range(num_items):
        category = random.randint(1, num_categories)
        # Base value follows a log-normal distribution (many cheap items, few expensive)
        base_value = round(np.random.lognormal(mean=3.0, sigma=1.0), 2)
        items.append({
            'item_id': i,
            'category': category,
            'estimated_value': max(1.0, base_value)
        })
    return pd.DataFrame(items)

def generate_combinatorial_bidders(items_df, num_bidders=5000):
    """
    Synthesizes the "Swiss" bundles (O_i) and budgets (B_i).
    """
    print(f"Synthesizing {num_bidders} combinatorial bidders...")
    bidders = []
    
    # Group items by category for realistic co-purchasing bundles
    items_by_category = items_df.groupby('category')['item_id'].apply(list).to_dict()
    item_values = items_df.set_index('item_id')['estimated_value'].to_dict()
    
    for i in range(num_bidders):
        # Pick a primary category for this bidder's interest
        category = random.choice(list(items_by_category.keys()))
        available_in_cat = items_by_category[category]
        
        # Bundle size: mostly 2-5 items
        bundle_size = min(len(available_in_cat), random.randint(2, 5))
        if bundle_size < 1:
            continue
            
        # O_i: The specific subset of items desired
        desired_bundle = random.sample(available_in_cat, bundle_size)
        
        # B_i: The rigid budget ceiling
        # Calculated as the true sum of values * a willingness-to-pay factor (0.7 to 1.3)
        true_value = sum(item_values[item] for item in desired_bundle)
        wtp_factor = random.uniform(0.7, 1.3)
        budget = round(true_value * wtp_factor, 2)
        
        bidders.append({
            'bidder_id': i,
            'bundle_O_i': set(desired_bundle),
            'bundle_size': bundle_size,
            'budget_B_i': budget,
            'true_value': true_value,
            'value_density': budget / bundle_size # B_i / |O_i|
        })
        
    return pd.DataFrame(bidders)

def greedy_mexican_allocation(bidders_df, total_items):
    """
    The "Mexican" Layer: A fast, greedy heuristic approximation.
    Sorts by Value Density (Budget / Bundle Size) and allocates if items are available.
    """
    print("Running the 'Mexican' Greedy Allocation Heuristic...")
    start_time = time.time()
    
    # Sort bidders by Value Density descending (most aggressive bidders first)
    sorted_bidders = bidders_df.sort_values(by='value_density', ascending=False)
    
    allocated_items = set()
    winning_bidders = []
    total_revenue = 0.0
    
    for _, bidder in sorted_bidders.iterrows():
        bundle = bidder['bundle_O_i']
        
        # Check if the bundle is conflict-free (none of the items are already allocated)
        if allocated_items.isdisjoint(bundle):
            # Clinch the bundle
            allocated_items.update(bundle)
            winning_bidders.append(bidder['bidder_id'])
            total_revenue += bidder['budget_B_i']
            
    exec_time = time.time() - start_time
    
    satisfiability_rate = len(winning_bidders) / len(bidders_df) * 100
    item_clearance_rate = len(allocated_items) / total_items * 100
    
    print("\n--- Auction Results ---")
    print(f"Execution Time: {exec_time:.4f} seconds")
    print(f"Winning Bidders: {len(winning_bidders)} out of {len(bidders_df)} ({satisfiability_rate:.2f}% Satisfiability)")
    print(f"Items Allocated: {len(allocated_items)} out of {total_items} ({item_clearance_rate:.2f}% Clearance)")
    print(f"Total Extracted Revenue: ${total_revenue:,.2f}")
    
    return winning_bidders, total_revenue

if __name__ == "__main__":
    # 1. Base Reality
    items_df = generate_synthetic_ebay_data(num_items=50000, num_categories=100)
    
    # 2. Synthesize Desires & Constraints
    bidders_df = generate_combinatorial_bidders(items_df, num_bidders=20000)
    
    # 3. Simulation & Analysis
    winning_bids, revenue = greedy_mexican_allocation(bidders_df, total_items=len(items_df))
