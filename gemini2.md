Title: Computational Limits and Market Equilibrium in Budget-Constrained Combinatorial Auctions
1. Problem Formulation: The "All-or-Nothing" eBay Dilemma

We define a market where a set of actors N competes for a global set of discrete objects Ω. Each actor i∈N is characterized by a tuple (Oi​,Bi​):

    Target Bundle (Oi​): A specific subset Oi​⊆Ω representing the only combination of items that provides utility to the actor.

    Budget Ceiling (Bi​): A rigid financial constraint where the actor cannot spend more than Bi​, regardless of the perceived value.

The central tension of this research is the Satisfiability-Expenditure Paradox: The auctioneer seeks to maximize total revenue (∑pj​) while ensuring that for every winning bidder i, the price of their desired bundle ∑j∈Oi​​pj​≤Bi​.
2. The Complexity Landscape: From Set Packing to NP-Hardness

The primary hurdle in "satisfying everyone" is structural. Even if budgets were infinite, the problem of selecting the maximum number of non-overlapping bundles Oi​ is a classic Set Packing Problem.

When we introduce the budget Bi​, the problem evolves into a Multi-Dimensional Knapsack Problem. We assert that finding an allocation that maximizes expenditure while satisfying Oi​ is NP-complete because:

    Feasibility: Determining if a conflict-free allocation exists for all requested Oi​ is hard.

    Optimization: Selecting the highest-value "packing" (highest Bi​) among competing bidders is computationally intensive for large m (items) and n (bidders).

3. Theoretical Frameworks for Resolution

To address these complexities, we explore three pillars of economic theory:
A. Walrasian Equilibrium with Budget Constraints

In a standard Walrasian equilibrium, prices are set such that supply equals demand. However, in our "eBay" model, budgets are fixed. We look for a price vector p where:

    Each bidder receives their Oi​ if and only if ∑j∈Oi​​pj​≤Bi​.

    The market clears (no item is over-allocated).

    The Expenditure Catch: In budget-constrained environments, a traditional equilibrium may not exist. We therefore look for Walrasian-like states where prices are high enough to prevent over-demand but low enough to respect Bi​.

B. Ausubel’s Clinching Auctions

For dynamic settings, we analyze the "Clinching" mechanism. Unlike a standard ascending auction where you might lose at the last second, a clinching auction allows a bidder to "clinch" an item when the remaining supply is less than the total demand from other bidders at the current price.

    Budget Adaptation: As the price rises, a bidder's "effective demand" drops once the price hits Bi​. This ensures the auction remains "strategy-proof"—bidders have no incentive to lie about their budget.

C. Fisher Market Models

We treat this as a Fisher Market, where bidders are not just participants in a single sale, but agents in a system with "monopoly money" (Bi​). The goal is to find prices that equate the total budget to the total value of items sold, maximizing "the bang per buck" (utility/price ratio).
4. State-of-the-Art Algorithmic Solutions

Because the problem is NP-complete, we propose moving toward Approximation Algorithms:

    Greedy Allocation: Prioritize bidders with the highest "Budget Density" (Bi​/∣Oi​∣).

    LP-Rounding: Solving the Fractional relaxation of the allocation problem and using randomized rounding to assign items.

    Configuration LP: A state-of-the-art technique that creates a variable for every possible bundle, allowing us to approximate the optimal revenue within an O(logm) factor.

Would you like me to focus the next section on a specific mathematical proof for the NP-completeness of the budget-constrained version?