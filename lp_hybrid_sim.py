import pandas as pd
import numpy as np
import random
import time
from scipy.optimize import linprog

def generate_small_market(num_items=500, num_bidders=1000, max_bundle=3):
    items_df = pd.DataFrame({
        'item_id': range(num_items),
        'estimated_value': np.random.lognormal(mean=3.0, sigma=1.0, size=num_items)
    })
    item_values = items_df.set_index('item_id')['estimated_value'].to_dict()
    
    bidders = []
    for i in range(num_bidders):
        bundle_size = random.randint(1, max_bundle)
        bundle = random.sample(range(num_items), bundle_size)
        true_value = sum(item_values[j] for j in bundle)
        budget = round(true_value * random.uniform(0.8, 1.5), 2)
        bidders.append({
            'bidder_id': i,
            'bundle': bundle,
            'budget': budget,
            'value_density': budget / bundle_size
        })
    return items_df, pd.DataFrame(bidders)

def pure_greedy(bidders_df, num_items):
    sorted_bidders = bidders_df.sort_values(by='value_density', ascending=False)
    allocated = set()
    rev = 0.0
    for _, b in sorted_bidders.iterrows():
        if allocated.isdisjoint(b['bundle']):
            allocated.update(b['bundle'])
            rev += b['budget']
    return rev

def lp_guided_greedy(bidders_df, num_items):
    # Formulate LP
    # max sum(B_i * x_i) s.t. sum(x_i for i where j in O_i) <= 1
    # linprog does min c^T x s.t. A_ub x <= b_ub
    n_bidders = len(bidders_df)
    c = -bidders_df['budget'].values # negative for maximization
    
    A_ub = np.zeros((num_items, n_bidders))
    for i, b in bidders_df.iterrows():
        for j in b['bundle']:
            A_ub[j, i] = 1
            
    b_ub = np.ones(num_items)
    bounds = [(0, 1) for _ in range(n_bidders)]
    
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
    
    if not res.success:
        return pure_greedy(bidders_df, num_items)
        
    x_star = res.x
    bidders_df['lp_score'] = bidders_df['value_density'] * (1 + x_star)
    
    sorted_bidders = bidders_df.sort_values(by='lp_score', ascending=False)
    allocated = set()
    rev = 0.0
    for _, b in sorted_bidders.iterrows():
        if allocated.isdisjoint(b['bundle']):
            allocated.update(b['bundle'])
            rev += b['budget']
            
    # Return both fractional optimal (upper bound) and the hybrid greedy result
    return -res.fun, rev

if __name__ == "__main__":
    np.random.seed(42)
    random.seed(42)
    
    items, bidders = generate_small_market(num_items=500, num_bidders=1000)
    
    greedy_rev = pure_greedy(bidders, 500)
    lp_bound, hybrid_rev = lp_guided_greedy(bidders, 500)
    
    print("--- Addressing the Optimality Gap ---")
    print(f"Theoretical Absolute Maximum (Fractional LP Bound): ${lp_bound:,.2f}")
    print(f"Pure 'Mexican' Greedy Revenue:                      ${greedy_rev:,.2f}")
    print(f"Swiss-Fallback (LP-Guided Greedy) Revenue:          ${hybrid_rev:,.2f}")
    
    improvement = ((hybrid_rev - greedy_rev) / greedy_rev) * 100
    gap_closed = ((hybrid_rev - greedy_rev) / (lp_bound - greedy_rev)) * 100
    print(f"\nLP-Guidance Revenue Improvement over Pure Greedy: +{improvement:.2f}%")
    print(f"Percentage of the 'Unreachable' Optimality Gap Closed: {gap_closed:.2f}%")

