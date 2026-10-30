"""Your hybrid retriever (stage 1): fuse the rankings of two systems into one.

This file is yours to write. Until you write it, build() raises NotImplementedError, and p2 skips
the system and lists it as to do.

Where the idea is:
- the 13 lab's pipeline.py in the course repo (class/13-rag-pipeline/lab/starter/pipeline.py):
  rrf() is reciprocal rank fusion with k = 60, where each document scores the sum of 1 / (60 + rank)
  over the rankings it appears in, and command_fuse() fuses bm25 with an embedder;
- get the two systems you fuse with p2.retrievers.build("bm25", corpus, cfg) and
  build("dense", corpus, cfg), so each index is built once per run;
- fuse full rankings, not top-10 lists (ask each system for len(corpus.docs) documents), because a
  document that is 11th in both lists can belong in the fused top 10;
- order the fused documents with p2.runfile.order(), so equal scores fall in document id order.

If you want `p2 answer` to work with hybrid, also give it search_chunks(text, k): the same fusion over chunk rankings.
"""

from __future__ import annotations

from collections import defaultdict

from p2 import retrievers
from p2.runfile import order

NEEDS_CLAUDE = False


def rrf(rankings, k: int) -> list[tuple[str, float]]:
    """Reciprocal rank fusion: each id scores the sum of 1 / (k + rank) over the rankings it is in.

    Items scoring 0 or less are left out of a ranking: bm25 pads its list with 0-score documents in
    id order, and those ranks are not matches, so they should not earn fusion credit.
    """
    fused: dict[str, float] = defaultdict(float)
    for ranking in rankings:
        for rank, (item, score) in enumerate(ranking, 1):
            if score <= 0:
                break  # rankings are best first, so the rest score 0 or less too
            fused[item] += 1.0 / (k + rank)
    return order(fused.items())


class Hybrid:
    def __init__(self, corpus, cfg):
        settings = cfg.table("hybrid")
        # [hybrid] systems = [...] and rrf_k = ... in p2.toml change the fusion; bm25 + dense with k 60 is the lab's.
        self.systems = [retrievers.build(name, corpus, cfg) for name in settings.get("systems", ["bm25", "dense"])]
        self.rrf_k = int(settings.get("rrf_k", 60))
        self.n_docs = len(corpus.docs)
        self.n_chunks = len(corpus.chunks(cfg.chunk_words, cfg.chunk_overlap))

    def search(self, text: str, k: int) -> list[tuple[str, float]]:
        # Full rankings, so a document 11th in both lists can still reach the fused top 10.
        return rrf([s.search(text, self.n_docs) for s in self.systems], self.rrf_k)[:k]

    def search_chunks(self, text: str, k: int) -> list[tuple[str, float]]:
        return rrf([s.search_chunks(text, self.n_chunks) for s in self.systems], self.rrf_k)[:k]


def build(corpus, cfg):
    return Hybrid(corpus, cfg)
