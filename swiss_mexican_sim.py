import pandas as pd
import numpy as np
import networkx as nx
import random
import time
import matplotlib.pyplot as plt

def generate_synthetic_ebay_data(num_items=10000, num_categories=50):
    print(f"Generating {num_items} synthetic eBay items...")
    items = []
    for i in range(num_items):
        category = random.randint(1, num_categories)
        base_value = round(np.random.lognormal(mean=3.0, sigma=1.0), 2)
        items.append({
            'item_id': i,
            'category': category,
            'estimated_value': max(1.0, base_value)
        })
    return pd.DataFrame(items)

def generate_combinatorial_bidders(items_df, num_bidders=5000, max_bundle_size=5):
    print(f"Synthesizing {num_bidders} combinatorial bidders...")
    bidders = []
    
    items_by_category = items_df.groupby('category')['item_id'].apply(list).to_dict()
    item_values = items_df.set_index('item_id')['estimated_value'].to_dict()
    
    for i in range(num_bidders):
        category = random.choice(list(items_by_category.keys()))
        available_in_cat = items_by_category[category]
        
        bundle_size = min(len(available_in_cat), random.randint(2, max_bundle_size))
        if bundle_size < 1:
            continue
            
        desired_bundle = random.sample(available_in_cat, bundle_size)
        true_value = sum(item_values[item] for item in desired_bundle)
        wtp_factor = random.uniform(0.7, 1.3)
        budget = round(true_value * wtp_factor, 2)
        
        bidders.append({
            'bidder_id': i,
            'bundle_O_i': set(desired_bundle),
            'bundle_size': bundle_size,
            'budget_B_i': budget,
            'true_value': true_value,
            'value_density': budget / bundle_size
        })
        
    return pd.DataFrame(bidders)

def greedy_mexican_allocation(bidders_df, total_items):
    print("Running the 'Mexican' Greedy Allocation Heuristic...")
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
            
    exec_time = time.time() - start_time
    satisfiability_rate = len(winning_bidders) / len(bidders_df) * 100
    item_clearance_rate = len(allocated_items) / total_items * 100
    
    return satisfiability_rate, item_clearance_rate, total_revenue, exec_time

def run_phase_transition_experiment():
    print("\n--- Running Tequila-Snow Phase Transition Experiment ---")
    items_df = generate_synthetic_ebay_data(num_items=10000, num_categories=20)
    
    bundle_sizes = [2, 3, 5, 8, 12, 15, 20]
    satisfiability_results = []
    
    for max_size in bundle_sizes:
        bidders_df = generate_combinatorial_bidders(items_df, num_bidders=5000, max_bundle_size=max_size)
        sat_rate, _, _, _ = greedy_mexican_allocation(bidders_df, len(items_df))
        satisfiability_results.append(sat_rate)
        print(f"Max Bundle {max_size}: {sat_rate:.2f}% Satisfiability")
        
    print("Experiment Complete. Results:")
    for i, size in enumerate(bundle_sizes):
        print(f"Bundle Max {size}: {satisfiability_results[i]:.2f}%")

if __name__ == "__main__":
    run_phase_transition_experiment()

def run_scaling_experiment():
    print("\n--- Running Asymptotic Scaling Experiment ---")
    sizes = [1000, 5000, 10000, 50000, 100000]
    times = []
    
    for size in sizes:
        items_df = generate_synthetic_ebay_data(num_items=max(10000, size), num_categories=50)
        bidders_df = generate_combinatorial_bidders(items_df, num_bidders=size, max_bundle_size=5)
        
        _, _, _, exec_time = greedy_mexican_allocation(bidders_df, len(items_df))
        times.append(exec_time)
        print(f"Bidders: {size}, Time: {exec_time:.4f}s")
        
    print("Scaling Experiment Complete.")
    print("Sizes:", sizes)
    print("Times:", times)

if __name__ == "__main__":
    run_scaling_experiment()
