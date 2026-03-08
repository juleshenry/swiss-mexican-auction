Title: Optimal Allocation in Budget-Constrained Combinatorial Markets: A Mechanism Design Approach to eBay-Style Auctions
Abstract

In the landscape of modern digital marketplaces like eBay, the challenge of resource allocation transcends simple price discovery. This paper explores the "Satisfiability and Expenditure Problem" (SEP), where bidders possess fixed budgets Bi​ and desire specific subsets Oi​ of a global set of items Ω. We investigate whether a mechanism can simultaneously maximize auctioneer revenue (budget expenditure) and satisfy bidder demand. We demonstrate that while this problem is fundamentally NP-complete, state-of-the-art approximation algorithms and market-clearing equilibrium concepts provide a robust framework for near-optimal efficiency in large-scale electronic commerce.
1. Introduction

The evolution of online auctions has moved beyond the sale of isolated items toward complex, interdependent transactions. A recurring dilemma for participants on platforms like eBay is the "exposure problem," where a bidder may win only a fraction of a desired set, rendering their expenditure inefficient or their objectives unmet.

This paper addresses a specific configuration of this problem: the Budget-Constrained Combinatorial Auction (BCCA). In this model, each actor i enters the market with a hard budget constraint Bi​ and a specific "all-or-nothing" interest in a bundle Oi​⊆Ω. The objective of the platform is twofold:

    Satisfiability: Ensuring that every participating actor receives their requested subset Oi​.

    Revenue Maximization: Maximizing the total budget drawn from the participants (max∑Bi​).

2. The Complexity of "Satisfying Everyone"

From a game-theoretic perspective, the goal of satisfying all actors' desired bundles is structurally identical to the Set Packing Problem. If multiple actors desire overlapping subsets of Ω, the auctioneer must decide which subset of actors can be "satisfied" without conflict.

As established in computational complexity theory, determining if a perfect allocation exists—where all actors receive their Oi​—is NP-complete. The addition of budget constraints transforms the problem into a multi-dimensional knapsack variant, further complicating the search for an optimal global price point that clears the market while respecting individual financial ceilings.
3. Algorithmic Frontiers: Beyond Exact Solutions

Given the intractability of finding an exact solution for large n, this research evaluates three primary "State-of-the-Art" (SOTA) algorithmic approaches:

    Linear Programming (LP) Relaxations: By treating items as divisible in the short term, we can use randomized rounding to achieve an O(m​) approximation of the optimal allocation.

    Budget-Constrained Fisher Markets: We model the auction as a market in equilibrium, where prices are adjusted dynamically until the "Maximum Bang-per-Buck" (MBB) condition is met for each bidder.

    Greedy Approximation: Utilizing value-density heuristics (e.g., ∣Oi​∣Bi​​), we can provide a fast, 1-1/e approximation for submodular valuations, which is often sufficient for real-time auction environments.

4. Conclusion and Research Objective

The quest to "satisfy everyone on eBay" is not merely a matter of logistics, but a fundamental challenge of algorithmic mechanism design. This paper will further analyze the trade-offs between Strategyproofness (ensuring bidders don't lie about their budgets) and Social Welfare (ensuring the most items reach the most people).