"""Your reranker (stage 1): ask Claude to reorder a first-stage system's top 20.

NEEDS_CLAUDE = True tells p2 that searching calls claude -p, so CI never regenerates this system's
runs; you produce them on your machine and commit them with their traces.

A listwise reranker in the shape of the 13 lab's rerank_one(): the first stage's top 20 go to Claude
as numbered passages, a JSON schema forces the reply into {"order": [20 numbers, each 1..20]}, a reply
that is not each number exactly once keeps the first-stage order, and everything below the 20 keeps
its order underneath. One call per query, through p2.claude.call, which caches replies in
.cache/claude/ and records the tokens in the run's trace.

- search ranks documents: each of hybrid's top 20 documents is shown as its best fused chunk (the
  chunk that gave the document its place), under the document's title.
- search_chunks ranks chunks the same way over hybrid's top 20 chunks, for `p2 answer`.
- The final ranking gets the score 1 / rank, so scores fall strictly and no ties need breaking.
"""

from __future__ import annotations

from p2 import claude, retrievers
from p2.corpus import docid_of

NEEDS_CLAUDE = True
FIRST_STAGE = "hybrid"
CANDIDATES = 20

PROMPT = """You are ranking passages from a document collection for a search query.

Query: {query}

Passages:
{passages}

Order all {n} passages from most to least relevant to the query. A passage is relevant if it answers the query.
Reply with every passage number from 1 to {n} exactly once, most relevant first."""


def schema(n: int) -> dict:
    return {
        "type": "object",
        "properties": {
            "order": {
                "type": "array",
                "items": {"type": "integer", "minimum": 1, "maximum": n},
                "minItems": n,
                "maxItems": n,
            }
        },
        "required": ["order"],
        "additionalProperties": False,
    }


class Rerank:
    def __init__(self, corpus, cfg):
        self.corpus = corpus
        self.cfg = cfg
        self.model = cfg.model
        self.first = retrievers.build(FIRST_STAGE, corpus, cfg)
        self.chunk_text = corpus.chunk_texts(cfg.chunk_words, cfg.chunk_overlap)
        self.n_docs = len(corpus.docs)
        self.n_chunks = len(self.chunk_text)

    def _reorder(self, query: str, ids: list[str], texts: list[str]) -> list[str]:
        """The ids in Claude's order; the first-stage order when the reply is not a permutation."""
        n = len(ids)
        if n < 2:
            return ids
        passages = "\n\n".join(f"[{i}] {t}" for i, t in enumerate(texts, 1))
        reply = claude.call(PROMPT.format(query=query, passages=passages, n=n), schema(n),
                            model=self.cfg.model, cache_dir=claude.cache_folder(self.cfg))
        order = (reply.output or {}).get("order") if reply.error is None else None
        if not isinstance(order, list) or sorted(order) != list(range(1, n + 1)):
            return ids  # keep the first-stage order
        return [ids[i - 1] for i in order]

    def _passage(self, chunk_id: str) -> str:
        """A chunk under its document's title; the first chunk already starts with the title line."""
        body = self.chunk_text[chunk_id]
        return body if body.startswith("# ") else f"# {self.corpus.docs[docid_of(chunk_id)].title}\n{body}"

    def search(self, text: str, k: int) -> list[tuple[str, float]]:
        ranked = [d for d, _ in self.first.search(text, self.n_docs)]
        top = ranked[:CANDIDATES]
        best_chunk: dict[str, str] = {}
        for cid, _ in self.first.search_chunks(text, self.n_chunks):
            best_chunk.setdefault(docid_of(cid), cid)
            if len(best_chunk) >= self.n_docs or all(d in best_chunk for d in top):
                break
        texts = [self._passage(best_chunk[d]) for d in top]
        final = self._reorder(text, top, texts) + ranked[CANDIDATES:]
        return [(d, 1.0 / r) for r, d in enumerate(final[:k], 1)]

    def search_chunks(self, text: str, k: int) -> list[tuple[str, float]]:
        ranked = [c for c, _ in self.first.search_chunks(text, self.n_chunks)]
        top = ranked[:CANDIDATES]
        texts = [self._passage(c) for c in top]
        final = self._reorder(text, top, texts) + ranked[CANDIDATES:]
        return [(c, 1.0 / r) for r, c in enumerate(final[:k], 1)]


def build(corpus, cfg):
    return Rerank(corpus, cfg)
