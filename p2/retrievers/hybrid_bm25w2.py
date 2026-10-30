"""Ablation of hybrid: weighted reciprocal rank fusion, bm25's vote counted twice.

One change from hybrid: each document scores 2 / (60 + bm25 rank) + 1 / (60 + dense rank) instead of
1 / (60 + bm25 rank) + 1 / (60 + dense rank). The systems, rrf k = 60, full rankings, the skipping of
0-score bm25 padding and the tie order are hybrid's.
"""

from __future__ import annotations

from collections import defaultdict

from p2.retrievers.hybrid import Hybrid
from p2.runfile import order

NEEDS_CLAUDE = False
BASE = "hybrid"

WEIGHTS = {"bm25": 2.0, "dense": 1.0}


def weighted_rrf(rankings, weights, k: int) -> list[tuple[str, float]]:
    """hybrid.rrf with each ranking's 1 / (k + rank) multiplied by that ranking's weight."""
    fused: dict[str, float] = defaultdict(float)
    for ranking, weight in zip(rankings, weights):
        for rank, (item, score) in enumerate(ranking, 1):
            if score <= 0:
                break  # rankings are best first, so the rest score 0 or less too
            fused[item] += weight / (k + rank)
    return order(fused.items())


class WeightedHybrid(Hybrid):
    def __init__(self, corpus, cfg):
        super().__init__(corpus, cfg)
        names = cfg.table("hybrid").get("systems", ["bm25", "dense"])
        self.weights = [WEIGHTS.get(name, 1.0) for name in names]

    def search(self, text: str, k: int) -> list[tuple[str, float]]:
        return weighted_rrf([s.search(text, self.n_docs) for s in self.systems], self.weights, self.rrf_k)[:k]

    def search_chunks(self, text: str, k: int) -> list[tuple[str, float]]:
        return weighted_rrf([s.search_chunks(text, self.n_chunks) for s in self.systems], self.weights, self.rrf_k)[:k]


def build(corpus, cfg):
    return WeightedHybrid(corpus, cfg)
