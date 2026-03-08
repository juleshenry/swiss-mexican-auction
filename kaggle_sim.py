import pandas as pd
import numpy as np
import time
import networkx as nx
from collections import defaultdict
import random

def load_kaggle_data():
    print("Loading Real/Kaggle-style eBay data...")
    df = pd.read_csv('real_ebay_auctions.csv')
    
    # We want to group by item to find the "true value" (max bid)
    # This represents the base items in Omega
    items_df = df.groupby('item_title').agg({
        'bid': 'max',
        'category': 'first'
    }).reset_index()
    
    items_df.rename(columns={'item_title': 'item_id', 'bid': 'estimated_value'}, inplace=True)
    return items_df

def generate_kaggle_combinatorial_bidders(items_df, num_bidders=10000, max_bundle_size=5):
    print(f"Synthesizing {num_bidders} combinatorial bidders from Kaggle distributions...")
    bidders = []
    
    items_by_category = items_df.groupby('category')['item_id'].apply(list).to_dict()
    item_values = items_df.set_index('item_id')['estimated_value'].to_dict()
    
    for i in range(num_bidders):
        category = random.choice(list(items_by_category.keys()))
        available_in_cat = items_by_category[category]
        
        # Power law distribution for bundle sizes to mimic real-world (many want 2-3, few want 15)
        # But capped at max_bundle_size for the phase transition experiments
        bundle_size = min(len(available_in_cat), random.randint(2, max_bundle_size))
        
        if bundle_size < 1:
            continue
            
        desired_bundle = random.sample(available_in_cat, bundle_size)
        true_value = sum(item_values[item] for item in desired_bundle)
        
        # Real-world willingness to pay varies wildly
        wtp_factor = random.uniform(0.6, 1.4) 
        budget = round(true_value * wtp_factor, 2)
        
        bidders.append({
            'bidder_id': i,
            'bundle_O_i': set(desired_bundle),
            'bundle_size': bundle_size,
            'budget_B_i': budget,
            'value_density': budget / bundle_size
        })
        
    return pd.DataFrame(bidders)

def run_kaggle_tequila_snow():
    print("\n--- Running Tequila-Snow Phase Transition on Kaggle Data ---")
    items_df = load_kaggle_data()
    print(f"Loaded {len(items_df)} unique items from Kaggle dataset.")
    
    bundle_sizes = [2, 3, 4, 6, 8, 12, 16]
    satisfiability_results = []
    clearance_results = []
    revenue_results = []
    
    for max_size in bundle_sizes:
        bidders_df = generate_kaggle_combinatorial_bidders(items_df, num_bidders=5000, max_bundle_size=max_size)
        
        # Greedy Allocation (Mexican Layer)
        start_time = time.time()
        sorted_bidders = bidders_df.sort_values(by='value_density', ascending=False)
        allocated_items = set()
        winning_bidders = []
        total_revenue = 0.0
        
        for _, bidder in sorted_bidders.iterrows():
            bundle = bidder['bundle_O_i']
            if allocated_items.isdisjoint(bundle):
                allocated_items.update(bundle)
                winning_bidders.append(bidder['bidder_id'])
                total_revenue += bidder['budget_B_i']
                
        sat_rate = len(winning_bidders) / len(bidders_df) * 100
        clear_rate = len(allocated_items) / len(items_df) * 100
        
        satisfiability_results.append(sat_rate)
        clearance_results.append(clear_rate)
        revenue_results.append(total_revenue)
        
        print(f"Max Bundle {max_size}: Sat = {sat_rate:.2f}%, Clearance = {clear_rate:.2f}%, Rev = ${total_revenue:,.0f}")
        
    return bundle_sizes, satisfiability_results, clearance_results, revenue_results

if __name__ == "__main__":
    run_kaggle_tequila_snow()
