# Evaluation report

This is the report on what you built and what the numbers let you claim.
Two kinds of text live here.

The tables between a `p2:begin` comment line and its matching `p2:end` comment line are written by `uv run p2 score` from your committed run files and answers files.
Please do not edit anything between those two lines, because `uv run p2 check` recomputes them and fails when they differ.
A table that says no runs or answers exist yet is waiting for data; run `uv run p2 score` after you commit the files it needs.

Everything else is yours.
Each prompt ends with a marker line that you replace with your own writing; `uv run p2 check --final` fails while one is left.
Write what you measured, including what did not work.
What I read for is whether each claim matches its interval, not whether the result is good news.

Words used below: recall@10, MRR@10 and nDCG@10 are the three scores, each averaged over the queries of a set; step 7 of stage 1 in the README defines them, and lecture 14 goes deeper.
A paired interval is the 95% interval of the mean difference between two systems on the same queries, found by resampling the queries 10,000 times.
When an interval includes zero, the gold set cannot tell the two systems apart, and the right words are "not distinguishable on this gold set".
The minimum detectable difference is the smallest gap this many queries could reliably show, so a difference below it is invisible to this gold set, not absent.

---

## 1. Stage 1 - the shared corpus (30 CFR Chapter I)

### What you built

For each of `dense`, `hybrid` and `rerank`, one or two sentences: the embedding model, how documents were chunked, what was fused and how, how many candidates the reranker saw, and anything you changed from the 12 and 13 lab code.

**Dense:** I used the BAAI/bge-small-en-v1.5 embedding model to compare queries and documents using cosine similarity. Unlike Lab 12, which embedded entire articles, my system divides documents into 300-word chunks with 50-word overlap and uses each document's highest-scoring chunk.

**Hybrid:** I combined BM25 and Dense using Reciprocal Rank Fusion (RRF) with k = 60. Compared with Lab 13, my implementation combines full rankings instead of only the top results and excludes BM25 documents with zero scores.

**Rerank:** I used Claude Sonnet 5.5 to reorder the top 20 candidates retrieved by Hybrid. Similar to Lab 13, the system uses a numbered list and structured JSON output, but I adapted it to work with document chunks and preserve the original Hybrid ranking if Claude returns an invalid response.
### Practice queries (20)

Scores per system.

<!-- p2:begin shared-practice -->
| System | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| bm25 | 0.625 | 0.507 | 0.518 |
| dense | 0.558 | 0.562 | 0.480 |
| hybrid | 0.617 | 0.471 | 0.457 |
| rerank | 0.725 | 0.750 | 0.731 |

20 judged queries; nDCG uses binary labels; a random ranking of the 2,484 documents would get recall@10 near 0.004.
<!-- p2:end shared-practice -->

The same scores per query class.

<!-- p2:begin shared-practice-classes -->
| System | Metric | identifier (n=7) | paraphrase (n=7) | mixed (n=6) |
| --- | --- | ---: | ---: | ---: |
| bm25 | Recall@10 | 1.000 | 0.000 | 0.917 |
| bm25 | MRR@10 | 0.810 | 0.000 | 0.746 |
| bm25 | nDCG@10 | 0.857 | 0.000 | 0.728 |
| dense | Recall@10 | 0.214 | 0.595 | 0.917 |
| dense | MRR@10 | 0.333 | 0.714 | 0.653 |
| dense | nDCG@10 | 0.211 | 0.593 | 0.661 |
| hybrid | Recall@10 | 0.571 | 0.405 | 0.917 |
| hybrid | MRR@10 | 0.514 | 0.154 | 0.792 |
| hybrid | nDCG@10 | 0.435 | 0.203 | 0.779 |
| rerank | Recall@10 | 0.714 | 0.500 | 1.000 |
| rerank | MRR@10 | 0.714 | 0.571 | 1.000 |
| rerank | nDCG@10 | 0.714 | 0.516 | 1.000 |
<!-- p2:end shared-practice-classes -->

Differences between every pair of systems, each with its paired interval and the minimum detectable difference.

<!-- p2:begin shared-practice-pairs -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| dense minus bm25 | Recall@10 | -0.067 | [-0.350, +0.225] | 0.415 | not distinguishable |
| dense minus bm25 | MRR@10 | +0.055 | [-0.225, +0.343] | 0.412 | not distinguishable |
| dense minus bm25 | nDCG@10 | -0.039 | [-0.302, +0.231] | 0.385 | not distinguishable |
| hybrid minus bm25 | Recall@10 | -0.008 | [-0.225, +0.208] | 0.317 | not distinguishable |
| hybrid minus bm25 | MRR@10 | -0.036 | [-0.178, +0.084] | 0.193 | not distinguishable |
| hybrid minus bm25 | nDCG@10 | -0.062 | [-0.218, +0.082] | 0.218 | not distinguishable |
| hybrid minus dense | Recall@10 | +0.058 | [-0.117, +0.242] | 0.261 | not distinguishable |
| hybrid minus dense | MRR@10 | -0.091 | [-0.305, +0.110] | 0.300 | not distinguishable |
| hybrid minus dense | nDCG@10 | -0.023 | [-0.191, +0.137] | 0.240 | not distinguishable |
| rerank minus bm25 | Recall@10 | +0.100 | [-0.125, +0.325] | 0.331 | not distinguishable |
| rerank minus bm25 | MRR@10 | +0.243 | [+0.010, +0.476] | 0.339 | rerank higher |
| rerank minus bm25 | nDCG@10 | +0.212 | [-0.008, +0.426] | 0.316 | not distinguishable |
| rerank minus dense | Recall@10 | +0.167 | [-0.025, +0.350] | 0.271 | not distinguishable |
| rerank minus dense | MRR@10 | +0.188 | [-0.017, +0.392] | 0.294 | not distinguishable |
| rerank minus dense | nDCG@10 | +0.251 | [+0.062, +0.431] | 0.268 | rerank higher |
| rerank minus hybrid | Recall@10 | +0.108 | [+0.025, +0.209] | 0.141 | rerank higher |
| rerank minus hybrid | MRR@10 | +0.279 | [+0.128, +0.441] | 0.229 | rerank higher |
| rerank minus hybrid | nDCG@10 | +0.274 | [+0.159, +0.396] | 0.171 | rerank higher |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end shared-practice-pairs -->

The 40 test queries have no answer key in this repo.
Your test run files are scored by the course and the score comes back to you as feedback, so nothing goes here for them.

### What the intervals let you claim

Which differences are distinguishable from zero and which are not?
What is the minimum detectable difference at 20 queries, and what does that say about any gap smaller than it?
Which claim from lecture 12 or 13 did your numbers support, and which did they leave open?

On the shared practice corpus, Rerank achieved the highest MRR@10 at 0.750, compared with 0.507 for BM25, 0.562 for Dense, and 0.471 for Hybrid.

The difference between Rerank and Hybrid was +0.279, with a 95% confidence interval of [+0.128, +0.441]. Since this interval does not include zero, the results support a measurable improvement from reranking. Rerank also performed better than BM25 in MRR@10, although the interval was wider.

However, the differences between BM25, Dense, and Hybrid were not distinguishable from zero. With only 20 judged queries, the minimum detectable difference for Hybrid versus BM25 in MRR@10 was 0.193, much larger than the observed difference of 0.036. This means the evaluation may be too small to detect modest improvements.

The results support the idea from the retrieval labs that reranking can improve the ordering of relevant documents. However, they do not establish that combining keyword and semantic retrieval always improves performance.

---

## 2. Stage 1 - cited answers on the 12 shared questions

<!-- p2:begin answers -->
| Label | System | Verified (in) | 95% interval | not_found (in) | Declined (out) | 95% interval | Quotes found |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| rerank | rerank | 8 of 8 (100%) | [0.676, 1.000] | 0 of 8 (0%) | 4 of 4 (100%) | [0.510, 1.000] | 14 of 14 |
<!-- p2:end answers -->

Which system answered, and why that one?
What did you change in `prompts/answer.txt`, if anything, and did the verified share or the declined share move?

Then read three in-corpus answers that `uv run p2 verify` passed.
For each one, open the cited chunk and say whether the quote really supports the claim next to it.
The check proves a quote is a real piece of the chunk and cannot prove that it supports the claim, so this reading is the part only you can do.

I chose Rerank for answer generation because it achieved the highest retrieval MRR@10 on the shared practice corpus. I kept the original answer prompt unchanged and used the top five retrieved chunks as evidence for each answer.

All eight answerable questions passed the automatic citation verification, and all four unanswerable questions were correctly declined. All 14 quoted passages were found in their cited chunks. The verified share was 100%, with a 95% Wilson interval of [0.676, 1.000], while the decline share was also 100%, with an interval of [0.510, 1.000].

However, automatic verification only confirms that a quoted passage exists in the cited source. It does not prove that the passage logically supports the claim. For that reason, I also examined individual answers and their evidence.

I reviewed three verified answers to check whether their citations actually support the claims.

For a01, the answer states that a mine operator must contact MSHA within 15 minutes after a fatal accident. Section 50.10 directly supports this answer because it specifies both the reporting deadline and the death of an individual at the mine.

For a02, the answer gives a minimum incombustible dust content of 80 percent. Section 75.403 directly establishes this requirement. The answer also explains that the additional methane-related increase does not apply when methane is absent. This is a reasonable interpretation of the regulation, although that conclusion is not separately supported by a claim citation.

For a03, the answer states that an approved self-rescue device must provide protection for at least one hour. Section 75.1714 supports this requirement. Although the quoted passage omits the beginning of the sentence, the full source confirms that operators must make these devices available to underground miners.

Overall, all three answers are supported by their cited regulations. However, this review also demonstrates why automatic quote verification is not sufficient by itself: an exact quotation can be valid while some parts of an answer still require interpretation or additional context.

---

## 3. Stage 2 - your corpus and your gold set

### The corpus

What is it, where did it come from, how many documents and how many megabytes, and what is the license basis for publishing it?
Name the one or two documents you were least sure about and what you decided.
Say which of the allowed sources in the brief it comes from.

I selected the U.S. Geological Survey (USGS) Mineral Commodity Summaries from 2022, 2023, and 2024 as my own corpus. The collection contains 264 documents, with 88 mineral commodity chapters from each year. The documents total approximately 1.87 MB and contain information about mineral production, imports, industrial uses, and supply.

I chose this corpus because it contains specific mineral names, technical terminology, and descriptions of industrial applications. This makes it suitable for comparing keyword-based and semantic retrieval.

The corpus comes from the USGS publications listed as an allowed source in the project brief. All 264 entries in my manifest are marked as U.S. government public-domain material, and the license checker reported no failures. However, the original volumes reserve rights for separately copyrighted third-party material. I therefore checked the extracted chapter text for copyright notices and image credits, and none were found. My corpus consists of extracted chapter text rather than third-party photographs or illustrations.

One issue I considered was the change in chapter filenames between years. For example, the 2022 industrial diamond chapter has a different filename pattern from the 2023 and 2024 diamond chapters, even though they cover the same commodity. I kept them as separate documents because each represents a different publication year.

### The gold set

How many queries, how many with origin `hand` and how many with origin `claude`, and which query classes did you use and why?
How did you decide that a document is relevant: write your relevance rule in two or three sentences, the way the brief does for the shared corpus.
How did you find candidates (the systems' top 10, a keyword search, reading), and did you read every document before you labeled it?
Your labels are binary (`rel` 1) unless you say otherwise: if you use graded labels, declare the scale here, for example 2 means the document answers the query fully and 1 means it helps.

I created 40 evaluation questions, including 10 questions developed by me and 30 drafted using Claude. The questions were divided into three categories: 11 identifier questions, 10 paraphrase questions, and 19 mixed questions. I used these categories to compare how different retrieval systems handle exact mineral names, alternative wording, and questions that combine both approaches.

I used binary relevance judgments, where 1 means relevant and 0 means not relevant. I considered a document relevant if it directly answered the question or provided substantial evidence supporting the information being requested. Simply mentioning the same mineral was not enough to make a document relevant.

To find candidate documents, I mainly searched for mineral-specific chapters across the 2022, 2023, and 2024 USGS publications. I compared information from different years to determine whether each document contained evidence relevant to the question. Instead of reading every document in the entire corpus, I focused on the relevant sentences and excerpts within the candidate documents.

My review worksheet contains 123 query-document candidates, including 102 positive and 21 negative judgments. The 102 positive judgments were recorded in eval/own/qrels.txt. I also considered cases where information overlapped between different minerals, such as rare earth elements and yttrium.

One limitation of my approach is that I primarily examined documents associated with the mineral mentioned in each question. Because I relied on selected passages rather than reading every document in full, I may have missed additional relevant information in other chapters. This means my gold set provides a useful basis for comparing retrieval systems, but it may not represent every relevant document in the corpus.

---

## 4. Stage 2 - results on your corpus

Scores per system on your gold set.

<!-- p2:begin own -->
| System | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| bm25 | 0.950 | 0.816 | 0.852 |
| dense | 0.871 | 0.795 | 0.807 |
| hybrid | 0.950 | 0.856 | 0.873 |
| rerank | 0.958 | 0.975 | 0.962 |
| ablation/hybrid_bm25w2 | 0.950 | 0.881 | 0.884 |

40 judged queries; nDCG uses binary labels; a random ranking of the 264 documents would get recall@10 near 0.038.
<!-- p2:end own -->

The same scores per query class.

<!-- p2:begin own-classes -->
| System | Metric | mixed (n=19) | identifier (n=11) | paraphrase (n=10) |
| --- | --- | ---: | ---: | ---: |
| bm25 | Recall@10 | 0.947 | 0.909 | 1.000 |
| bm25 | MRR@10 | 0.816 | 0.818 | 0.812 |
| bm25 | nDCG@10 | 0.862 | 0.818 | 0.871 |
| dense | Recall@10 | 0.939 | 1.000 | 0.600 |
| dense | MRR@10 | 0.833 | 0.955 | 0.548 |
| dense | nDCG@10 | 0.861 | 0.952 | 0.545 |
| hybrid | Recall@10 | 0.947 | 1.000 | 0.900 |
| hybrid | MRR@10 | 0.921 | 0.841 | 0.750 |
| hybrid | nDCG@10 | 0.928 | 0.887 | 0.754 |
| rerank | Recall@10 | 0.947 | 1.000 | 0.933 |
| rerank | MRR@10 | 0.947 | 1.000 | 1.000 |
| rerank | nDCG@10 | 0.947 | 1.000 | 0.947 |
| ablation/hybrid_bm25w2 | Recall@10 | 0.947 | 0.970 | 0.933 |
| ablation/hybrid_bm25w2 | MRR@10 | 0.886 | 0.831 | 0.925 |
| ablation/hybrid_bm25w2 | nDCG@10 | 0.910 | 0.869 | 0.851 |
<!-- p2:end own-classes -->

The same scores for the queries you wrote yourself (`hand`) and the ones a model drafted (`claude`), with the difference between the two groups and its interval.
Once both groups have queries, the table also says whether `bm25`'s lead over `dense` differs between them, and what share of each query's content words its best relevant document contains, which is stretch option 6.

<!-- p2:begin own-origins -->
| System | Metric | hand (n=10) | claude (n=30) | hand minus claude | 95% interval | Reading |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| bm25 | Recall@10 | 0.800 | 1.000 | -0.200 | [-0.500, +0.000] | not distinguishable |
| bm25 | MRR@10 | 0.600 | 0.887 | -0.287 | [-0.562, -0.017] | claude higher |
| bm25 | nDCG@10 | 0.669 | 0.913 | -0.245 | [-0.496, -0.019] | claude higher |
| dense | Recall@10 | 0.900 | 0.861 | +0.039 | [-0.194, +0.222] | not distinguishable |
| dense | MRR@10 | 0.850 | 0.777 | +0.073 | [-0.178, +0.290] | not distinguishable |
| dense | nDCG@10 | 0.860 | 0.790 | +0.070 | [-0.167, +0.271] | not distinguishable |
| hybrid | Recall@10 | 0.900 | 0.967 | -0.067 | [-0.289, +0.067] | not distinguishable |
| hybrid | MRR@10 | 0.825 | 0.867 | -0.042 | [-0.294, +0.170] | not distinguishable |
| hybrid | nDCG@10 | 0.844 | 0.883 | -0.039 | [-0.271, +0.139] | not distinguishable |
| rerank | Recall@10 | 0.900 | 0.978 | -0.078 | [-0.300, +0.067] | not distinguishable |
| rerank | MRR@10 | 0.900 | 1.000 | -0.100 | [-0.300, +0.000] | not distinguishable |
| rerank | nDCG@10 | 0.900 | 0.982 | -0.082 | [-0.300, +0.053] | not distinguishable |
| ablation/hybrid_bm25w2 | Recall@10 | 0.867 | 0.978 | -0.111 | [-0.333, +0.044] | not distinguishable |
| ablation/hybrid_bm25w2 | MRR@10 | 0.748 | 0.925 | -0.177 | [-0.449, +0.058] | not distinguishable |
| ablation/hybrid_bm25w2 | nDCG@10 | 0.790 | 0.916 | -0.125 | [-0.367, +0.076] | not distinguishable |

The hand and claude queries are different queries, so the interval of hand minus claude comes from resampling the queries within each group (10,000 times), not from pairing them.

Do model-written queries favor keyword search? bm25's lead over dense (bm25 minus dense, per query) on the claude queries and on the hand queries, and claude minus hand:

| Metric | Lead on claude | Lead on hand | Claude minus hand | 95% interval | Reading |
| --- | ---: | ---: | ---: | ---: | --- |
| Recall@10 | +0.139 | -0.100 | +0.239 | [+0.061, +0.483] | bm25 gains more on claude queries |
| MRR@10 | +0.111 | -0.250 | +0.361 | [+0.054, +0.679] | bm25 gains more on claude queries |
| nDCG@10 | +0.124 | -0.191 | +0.315 | [+0.074, +0.578] | bm25 gains more on claude queries |

Mean content-word overlap, the share of a query's content words found in its best relevant document: hand 0.68 (10 queries), claude 0.77 (30 queries).

Stretch option 6 asks for at least 20 judged queries of each origin; here there are 10 hand and 30 claude.
<!-- p2:end own-origins -->

Differences between every pair of systems.

<!-- p2:begin own-pairs -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| dense minus bm25 | Recall@10 | -0.079 | [-0.183, +0.017] | 0.144 | not distinguishable |
| dense minus bm25 | MRR@10 | -0.020 | [-0.157, +0.113] | 0.198 | not distinguishable |
| dense minus bm25 | nDCG@10 | -0.045 | [-0.165, +0.070] | 0.170 | not distinguishable |
| hybrid minus bm25 | Recall@10 | +0.000 | [-0.058, +0.067] | 0.088 | not distinguishable |
| hybrid minus bm25 | MRR@10 | +0.041 | [-0.048, +0.133] | 0.132 | not distinguishable |
| hybrid minus bm25 | nDCG@10 | +0.021 | [-0.047, +0.091] | 0.100 | not distinguishable |
| hybrid minus dense | Recall@10 | +0.079 | [+0.017, +0.158] | 0.103 | hybrid higher |
| hybrid minus dense | MRR@10 | +0.061 | [-0.022, +0.150] | 0.122 | not distinguishable |
| hybrid minus dense | nDCG@10 | +0.066 | [+0.001, +0.136] | 0.097 | hybrid higher |
| rerank minus bm25 | Recall@10 | +0.008 | [-0.050, +0.075] | 0.085 | not distinguishable |
| rerank minus bm25 | MRR@10 | +0.159 | [+0.075, +0.253] | 0.130 | rerank higher |
| rerank minus bm25 | nDCG@10 | +0.110 | [+0.047, +0.182] | 0.100 | rerank higher |
| rerank minus dense | Recall@10 | +0.087 | [+0.025, +0.167] | 0.104 | rerank higher |
| rerank minus dense | MRR@10 | +0.180 | [+0.087, +0.290] | 0.148 | rerank higher |
| rerank minus dense | nDCG@10 | +0.155 | [+0.077, +0.246] | 0.121 | rerank higher |
| rerank minus hybrid | Recall@10 | +0.008 | [+0.000, +0.025] | 0.023 | not distinguishable |
| rerank minus hybrid | MRR@10 | +0.119 | [+0.050, +0.200] | 0.110 | rerank higher |
| rerank minus hybrid | nDCG@10 | +0.089 | [+0.042, +0.142] | 0.073 | rerank higher |
| ablation/hybrid_bm25w2 minus bm25 | Recall@10 | +0.000 | [-0.050, +0.050] | 0.067 | not distinguishable |
| ablation/hybrid_bm25w2 minus bm25 | MRR@10 | +0.065 | [+0.007, +0.137] | 0.094 | ablation/hybrid_bm25w2 higher |
| ablation/hybrid_bm25w2 minus bm25 | nDCG@10 | +0.032 | [-0.016, +0.082] | 0.071 | not distinguishable |
| ablation/hybrid_bm25w2 minus dense | Recall@10 | +0.079 | [+0.013, +0.158] | 0.108 | ablation/hybrid_bm25w2 higher |
| ablation/hybrid_bm25w2 minus dense | MRR@10 | +0.085 | [-0.030, +0.204] | 0.171 | not distinguishable |
| ablation/hybrid_bm25w2 minus dense | nDCG@10 | +0.077 | [-0.012, +0.169] | 0.131 | not distinguishable |
| ablation/hybrid_bm25w2 minus hybrid | Recall@10 | +0.000 | [-0.025, +0.025] | 0.033 | not distinguishable |
| ablation/hybrid_bm25w2 minus hybrid | MRR@10 | +0.024 | [-0.041, +0.093] | 0.097 | not distinguishable |
| ablation/hybrid_bm25w2 minus hybrid | nDCG@10 | +0.011 | [-0.029, +0.051] | 0.058 | not distinguishable |
| ablation/hybrid_bm25w2 minus rerank | Recall@10 | -0.008 | [-0.025, +0.000] | 0.023 | not distinguishable |
| ablation/hybrid_bm25w2 minus rerank | MRR@10 | -0.094 | [-0.172, -0.029] | 0.104 | rerank higher |
| ablation/hybrid_bm25w2 minus rerank | nDCG@10 | -0.077 | [-0.131, -0.034] | 0.070 | rerank higher |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end own-pairs -->

Which differences are distinguishable and which are not, at your gold-set size?
Do the `hand` queries and the `claude` queries tell the same story?
Did your prediction in `DECISIONS.md` prompt 1 hold?

On my USGS corpus, Rerank achieved the best overall retrieval performance, with an MRR@10 of 0.975, compared with 0.856 for Hybrid, 0.816 for BM25, and 0.795 for Dense.

Rerank outperformed Hybrid in MRR@10 by +0.119, with a 95% paired bootstrap interval of [+0.050, +0.200]. Since the interval excludes zero, the results support a measurable advantage for Rerank on my gold set. However, the difference between Hybrid and BM25 was only +0.041, with an interval of [-0.048, +0.133]. Because this interval includes zero, the two systems are not distinguishable on my gold set.

I also compared the questions I developed myself with those drafted by Claude. BM25 achieved an MRR@10 of 0.600 on the hand questions and 0.887 on the Claude questions, while Dense achieved 0.850 and 0.777, respectively. The results suggest that question wording may affect how well keyword-based and semantic retrieval perform. The average content-word overlap was also higher for Claude questions (0.77) than for hand questions (0.68), which may partly explain BM25's stronger performance on Claude-generated questions.

My pre-registered prediction was that BM25 would outperform Hybrid on this corpus. The observed results did not support that direction, since Hybrid's MRR@10 was slightly higher. Nevertheless, the confidence interval includes zero, so the evidence does not establish a clear difference between them.

Overall, Rerank provided the strongest retrieval performance, but the comparison also shows the limitations of a 40-question gold set. Some differences between retrieval methods were too small to distinguish reliably, and the high scores of several systems leave relatively little room for further improvement.

---

## 5. The ablation

Change one thing and keep everything else the same.
Write your hypothesis here before you run it, in one sentence with a direction: "I expect X to raise MRR@10 on my corpus because Y."
The run file for it lives in `runs/own/ablation/`.

<!-- p2:begin own-ablation -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| ablation/hybrid_bm25w2 minus bm25 | Recall@10 | +0.000 | [-0.050, +0.050] | 0.067 | not distinguishable |
| ablation/hybrid_bm25w2 minus bm25 | MRR@10 | +0.065 | [+0.007, +0.137] | 0.094 | ablation/hybrid_bm25w2 higher |
| ablation/hybrid_bm25w2 minus bm25 | nDCG@10 | +0.032 | [-0.016, +0.082] | 0.071 | not distinguishable |
| ablation/hybrid_bm25w2 minus dense | Recall@10 | +0.079 | [+0.013, +0.158] | 0.108 | ablation/hybrid_bm25w2 higher |
| ablation/hybrid_bm25w2 minus dense | MRR@10 | +0.085 | [-0.030, +0.204] | 0.171 | not distinguishable |
| ablation/hybrid_bm25w2 minus dense | nDCG@10 | +0.077 | [-0.012, +0.169] | 0.131 | not distinguishable |
| ablation/hybrid_bm25w2 minus hybrid | Recall@10 | +0.000 | [-0.025, +0.025] | 0.033 | not distinguishable |
| ablation/hybrid_bm25w2 minus hybrid | MRR@10 | +0.024 | [-0.041, +0.093] | 0.097 | not distinguishable |
| ablation/hybrid_bm25w2 minus hybrid | nDCG@10 | +0.011 | [-0.029, +0.051] | 0.058 | not distinguishable |
| ablation/hybrid_bm25w2 minus rerank | Recall@10 | -0.008 | [-0.025, +0.000] | 0.023 | not distinguishable |
| ablation/hybrid_bm25w2 minus rerank | MRR@10 | -0.094 | [-0.172, -0.029] | 0.104 | rerank higher |
| ablation/hybrid_bm25w2 minus rerank | nDCG@10 | -0.077 | [-0.131, -0.034] | 0.070 | rerank higher |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end own-ablation -->

The queries your ablation helped and hurt, against the system it varies, by reciprocal rank.
`p2 score` finds that system from a line such as `BASE = "bm25"` in your variant's file, or else from its name: `bm25_lab` varies `bm25`.

<!-- p2:begin own-ablation-queries -->
ablation/hybrid_bm25w2 against hybrid (BASE = "hybrid" in p2/retrievers/hybrid_bm25w2.py): it helped 5 queries, hurt 3 and left 32 unchanged.

| Query | Class | Origin | hybrid RR | ablation/hybrid_bm25w2 RR | Change | Effect |
| --- | --- | --- | ---: | ---: | ---: | --- |
| c17 | paraphrase | claude | 0.333 | 1.000 | +0.667 | helped |
| c01 | identifier | claude | 0.500 | 1.000 | +0.500 | helped |
| c12 | paraphrase | claude | 0.500 | 1.000 | +0.500 | helped |
| c14 | paraphrase | claude | 0.500 | 1.000 | +0.500 | helped |
| c20 | paraphrase | claude | 0.167 | 0.250 | +0.083 | helped |
| h06 | mixed | hand | 1.000 | 0.333 | -0.667 | hurt |
| c09 | identifier | claude | 1.000 | 0.500 | -0.500 | hurt |
| h03 | identifier | hand | 0.250 | 0.143 | -0.107 | hurt |

RR is the reciprocal rank of the first relevant document in the top 10 (0 when none is there), the per-query value behind MRR@10; the queries at the top of each list are the ones to read.
<!-- p2:end own-ablation-queries -->

What did you change, what happened, and does the interval support the claim you want to make?
If the result is not distinguishable, say what size of effect your gold set could have seen.
Read the queries at the top of each list in the second table, and say whether your change explains them.

I expect increasing BM25's weight in the hybrid system to improve MRR@10 on my corpus because many questions contain specific mineral names and technical terms that keyword-based retrieval can identify directly.


I changed one variable in my Hybrid retrieval system by increasing the BM25 weight from 1.0 to 2.0 while keeping the Dense weight at 1.0. The RRF parameter (k = 60), corpus, and evaluation queries remained unchanged.

My hypothesis was that increasing the BM25 weight would improve MRR@10 because my corpus contains specific mineral names and technical terminology. The results moved in the predicted direction: MRR@10 increased from 0.856 to 0.881, while nDCG@10 increased from 0.873 to 0.884. Recall@10 remained unchanged at 0.950.

However, the MRR@10 difference was only +0.024, with a 95% paired bootstrap interval of [-0.041, +0.093]. Since this interval includes zero, I cannot conclude that increasing BM25's weight reliably improves retrieval performance. The minimum detectable difference was 0.097, which is larger than the observed improvement.

Of the 40 questions, five improved, three became worse, and 32 remained unchanged. For example, c17 improved from a reciprocal rank of 0.333 to 1.000, while h06 decreased from 1.000 to 0.333. Four of the five improved questions were paraphrase questions, suggesting that the benefit was not limited to questions containing exact mineral identifiers.

Overall, the ablation provided some support for the direction of my hypothesis, but the evidence was not strong enough to establish a reliable improvement. It also showed that changing the relative influence of keyword and semantic retrieval can help some questions while hurting others.

To understand the results more closely, I examined c17 and h06, the queries with the largest positive and negative changes.

For c17, which asks about a lightweight structural metal produced from Great Salt Lake brine, the first relevant magnesium-metal document moved from rank 3 to rank 1. BM25 ranked the magnesium-metal chapters highly, while Dense favored the potash chapters. Doubling BM25's weight moved the relevant magnesium-metal documents above the potash documents. Interestingly, the question did not explicitly mention magnesium, suggesting that keyword retrieval can also succeed through related terms rather than exact mineral names.

For h06, which asks how rare earth elements are used in catalysts, the first relevant document fell from rank 1 to rank 3. BM25 favored yttrium chapters, while Dense ranked the rare-earths chapters higher. Increasing BM25's weight pushed the yttrium documents above the relevant rare-earths documents. This shows how overlapping technical terminology between related commodities can reduce retrieval quality.

These examples demonstrate that increasing BM25's influence consistently moved the results toward BM25's original ranking, but whether that improved performance depended on which documents BM25 preferred. Therefore, the observed improvement in overall MRR@10 does not establish that a larger BM25 weight is always beneficial.

---

## 6. Failure analysis

Pick the queries where your best system on your own corpus failed: the relevant document is missing from the top 10, or sits far below the top.
Take at least five, and read what the system returned next to what was relevant.
Then sort the failures by cause, for example a vocabulary mismatch, near-duplicate documents, a chunk that cut the answer in half, a query that is ambiguous, or a label that was wrong, because sometimes the gold set is what failed.

| qid | what the best system returned | what was relevant | cause | what you would try |
|---|---|---|---|---|

The Rerank system achieved an MRR@10 of 0.975 on my corpus, leaving relatively few retrieval failures to analyze. Only two queries, h08 and c20, showed genuine retrieval problems. For the other 38 questions, the first relevant document appeared at rank 1, and all judged relevant documents were within the top 10.

For h08, the question asked what material is commonly used to protect steel from rusting. The relevant zinc chapters used terms such as "galvanizing" and "galvanized steel" rather than "rust" or "corrosion." As a result, Rerank returned cadmium and other metal-related chapters instead of zinc. This suggests that vocabulary mismatch can prevent relevant documents from entering the candidate set.

For c20, Rerank retrieved the 2022 cesium chapter at rank 1 but missed the 2023 and 2024 cesium chapters within the top 10. These documents were ranked outside Hybrid's top 20 candidates, so Rerank could not promote them. The relevant sentences were also located in chunks containing substantial statistical information, which may have reduced their semantic similarity scores.

I also examined three additional limitations rather than treating them as retrieval failures. For c27, Claude returned an invalid ranking, causing the system to retain Hybrid's original order without affecting the score. For c02, relevant antimony documents contained different production figures, showing the importance of publication year. For h06, the rare-earth chapters identified catalyst applications but did not fully explain the underlying mechanism, raising questions about how strictly relevance should be judged.

Overall, the main problems were vocabulary mismatch, candidate selection, and limitations in relevance judgments. Since the gold set contains only 40 questions and the system already performs near the evaluation ceiling, additional questions and more detailed relevance labels would help reveal weaknesses that the current metrics may not capture.

---

## 7. Cross-corpus comparison

The two tables to compare are the shared-corpus scores in section 1 and your own-corpus scores in section 4, with their intervals.
If you want them side by side, copy the rows you need into a table here and say that you copied them.

Did the winner change between the shared corpus and yours?
Why, or why not: what is different about the two collections (document length, vocabulary, identifiers, near-duplicates, how the queries were written), and which of your explanations did you test and which are guesses?
Say what 20 queries on one side and your gold-set size on the other cannot support.

The retrieval results differed between the shared corpus and my own corpus, although Rerank achieved the highest MRR@10 in both. On the shared corpus, Rerank reached 0.750, compared with 0.975 on my USGS corpus. The other three systems also achieved higher MRR@10 scores on my corpus.

One difference was the relative performance of BM25 and Hybrid. On the shared corpus, BM25 achieved 0.507 while Hybrid achieved 0.471. On my corpus, BM25 achieved 0.816 while Hybrid achieved 0.856. However, the confidence intervals for these comparisons included zero in both datasets, so neither difference establishes a reliable advantage.

The collections also have different characteristics. The shared corpus contains 2,484 mining regulation documents with legal terminology and section identifiers, while my corpus contains 264 mineral commodity chapters with specific mineral names, production statistics, and similar information repeated across publication years. These differences may affect how keyword-based and semantic retrieval identify relevant documents.

Another possible explanation for the higher scores on my corpus is the way I constructed the gold set. I mainly examined mineral-specific chapters across three years, which may have made relevant documents easier to identify while leaving some cross-commodity evidence unlabeled. This is a limitation of my evaluation rather than proof that my corpus is inherently easier to search.

The shared evaluation contains only 20 judged queries, while my own evaluation contains 40. These sample sizes limit how confidently I can generalize the results. Although Rerank was the strongest system in both evaluations, I cannot conclude that it will always outperform other retrieval methods on different collections or questions.

Overall, the results suggest that retrieval performance depends on the characteristics of the corpus, the wording of the queries, and the relevance judgments used for evaluation. The observed differences are informative, but the explanations involving corpus structure and document repetition remain hypotheses rather than experimentally established causes.

---

## 8. Stretch

498E: the stretch is one of the six options in the brief's "One stretch" section, and that section says what earns the 25 points for each.
It is optional, so `uv run p2 check --final` never waits on this section.
598E: the rider is your stretch, so write "rider" below and put its results in section 9; the other options add no points, because the project is capped at 150.

Whichever option you chose, write these five things:

1. The option's name.
2. What you did, and the files that hold it.
3. The table `p2 score` wrote for it, by name: one of the three below, `own-ablation` and `own-ablation-queries` in section 5 for a second ablation, `own-origins` in section 4 for the hand and claude queries, or `repeats` in section 9 for the rider.
4. What its interval lets you claim, and what it does not.
5. One thing you would do next, and what result would tell you it worked.

For a second ablation, write its hypothesis here before you run it, and commit it, so your history shows that it came first.
For the hand and claude queries, do the same with your prediction before you score.

### Claim-level faithfulness check (option 2)

Claude's verdicts from `p2 judge` against your own verdicts in the calibration file.

<!-- p2:begin stretch-judge -->
_No judged answers yet (stretch option 2): `uv run p2 judge answers/shared/LABEL.json` writes them, your own verdicts go in answers/shared/LABEL.calibration.tsv, and then `uv run p2 score` fills this table._
<!-- p2:end stretch-judge -->

### Cost and latency (option 3)

The Claude calls, tokens and seconds in every trace you committed, and what a cheaper system or answers file saves against what it loses.

<!-- p2:begin stretch-cost -->
Every trace in traces/ that records a Claude call:

| Trace | System | Spans | Claude calls | Saved | Input tokens | Output tokens | Seconds | Input per span | Output per span | Seconds per span |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| traces/answers-rerank.jsonl | rerank | 12 | 24 | 4 | 211,563 | 4,470 | 217.6 | 17,630 | 372 | 18.1 |
| traces/answers-rerank.r1.jsonl | rerank | 12 | 24 | 0 | 196,654 | 4,526 | 198.2 | 16,388 | 377 | 16.5 |
| traces/answers-rerank.r2.jsonl | rerank | 12 | 24 | 0 | 215,760 | 4,538 | 195.8 | 17,980 | 378 | 16.3 |
| traces/answers-rerank.r3.jsonl | rerank | 12 | 24 | 0 | 215,396 | 4,767 | 220.3 | 17,950 | 397 | 18.4 |
| traces/own-own-rerank.jsonl | rerank | 40 | 40 | 0 | 750,331 | 3,769 | 315.7 | 18,758 | 94 | 7.9 |
| traces/shared-practice-rerank.jsonl | rerank | 20 | 20 | 2 | 267,338 | 2,134 | 153.7 | 13,367 | 107 | 7.7 |
| traces/shared-practice-rerank.r1.jsonl | rerank | 20 | 20 | 0 | 253,467 | 1,981 | 145.5 | 12,673 | 99 | 7.3 |
| traces/shared-practice-rerank.r2.jsonl | rerank | 20 | 20 | 0 | 264,152 | 2,145 | 163.3 | 13,208 | 107 | 8.2 |
| traces/shared-practice-rerank.r3.jsonl | rerank | 20 | 20 | 0 | 266,940 | 2,129 | 147.9 | 13,347 | 106 | 7.4 |
| traces/shared-test-rerank.jsonl | rerank | 40 | 40 | 0 | 482,520 | 3,911 | 318.1 | 12,063 | 98 | 8.0 |

A span is one query of a run, one question of an answers file, or one claim of a judged file. A saved reply costs nothing now, so it counts the tokens and the seconds of the call that made it.

Every pair of systems on the same queries where at least one calls Claude, the one with fewer Claude input tokens per query first:

| Cheaper minus dearer | Queries | MRR@10 difference | 95% interval | Input tokens saved per query | Seconds saved per query | Reading |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| shared practice: bm25 minus rerank | 20 | -0.243 | [-0.476, -0.010] | 13,367 | 7.7 | rerank higher |
| shared practice: dense minus rerank | 20 | -0.188 | [-0.392, +0.017] | 13,367 | 7.7 | not distinguishable |
| shared practice: hybrid minus rerank | 20 | -0.279 | [-0.441, -0.128] | 13,367 | 7.7 | rerank higher |
| own: bm25 minus rerank | 40 | -0.159 | [-0.253, -0.075] | 18,758 | 7.9 | rerank higher |
| own: dense minus rerank | 40 | -0.180 | [-0.290, -0.087] | 18,758 | 7.9 | rerank higher |
| own: hybrid minus rerank | 40 | -0.119 | [-0.200, -0.050] | 18,758 | 7.9 | rerank higher |

The difference is the cheaper system's score minus the dearer one's, with its paired interval; the savings count Claude calls only, so a system that makes none saves all of the other's.

Systems that do not call Claude, from traces/retrieval/ on the machine that last ran `p2 score` (git ignores that folder, so `p2 check` does not compare this part):

| Trace | System | Queries | Seconds | Milliseconds per query |
| --- | --- | ---: | ---: | ---: |
| traces/retrieval/own-own-ablation-hybrid_bm25w2.jsonl | hybrid_bm25w2 | 40 | 0.47 | 11.8 |
| traces/retrieval/own-own-bm25.jsonl | bm25 | 40 | 0.05 | 1.3 |
| traces/retrieval/own-own-dense.jsonl | dense | 40 | 0.62 | 15.4 |
| traces/retrieval/own-own-hybrid.jsonl | hybrid | 40 | 0.41 | 10.2 |
| traces/retrieval/shared-practice-bm25.jsonl | bm25 | 20 | 0.08 | 4.1 |
| traces/retrieval/shared-practice-dense.jsonl | dense | 20 | 0.28 | 13.8 |
| traces/retrieval/shared-practice-hybrid.jsonl | hybrid | 20 | 0.64 | 31.8 |
| traces/retrieval/shared-test-bm25.jsonl | bm25 | 40 | 0.16 | 4.0 |
| traces/retrieval/shared-test-dense.jsonl | dense | 40 | 0.80 | 20.0 |
| traces/retrieval/shared-test-hybrid.jsonl | hybrid | 40 | 1.01 | 25.3 |
<!-- p2:end stretch-cost -->

### The grep agent (option 5)

Your stretch run on some of your own queries against the four systems on the same queries.

<!-- p2:begin stretch-agent -->
_No stretch runs yet (stretch option 5): `uv run p2 run --corpus own --queries eval/own/agent.queries.tsv --system agent --stretch` writes one to runs/own/stretch/, then `uv run p2 score` fills this table._
<!-- p2:end stretch-agent -->

### Your stretch

I completed the CSCI598E rider by running three independent repeats of Rerank retrieval and three repeats of cited answer generation on the shared corpus. The results are recorded in the run files, answer files, and corresponding traces, with the generated comparison tables in Section 9.

The purpose was to examine whether Claude's nondeterministic responses would affect retrieval performance, citation verification, and the ability to decline unanswerable questions.

Across the repeats, the evaluation scores remained unchanged, although some rankings, retrieved chunks, and citations differed. This suggests stable performance on the tested questions, but it does not establish that every generated answer will always be identical or correct.

As a next step, I would test a larger and more diverse question set. I would consider that useful if the verification and decline rates remained high while the variation across runs stayed small.

---

## 9. 598E only - repeats and the pre-registered claim

498E students can leave this section as it is; nothing checks it.
598E students replace each line that starts with "598E: write", and `uv run p2 check --final` counts those lines as work still to do until they are gone.

### Repeats on the shared corpus

Three runs of the reranker on the practice queries, and three answers files, with their run-to-run spread and Wilson intervals.

<!-- p2:begin repeats -->
Repeated runs of rerank on shared/practice:

| Run | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| rerank.r1 | 0.725 | 0.750 | 0.731 |
| rerank.r2 | 0.725 | 0.750 | 0.731 |
| rerank.r3 | 0.725 | 0.750 | 0.731 |
| range (max minus min) | 0.000 | 0.000 | 0.000 |

| Comparison | Metric | Mean difference | 95% interval | Reading |
| --- | --- | ---: | ---: | --- |
| rerank.r1 minus hybrid | Recall@10 | +0.108 | [+0.025, +0.209] | rerank.r1 higher |
| rerank.r2 minus hybrid | Recall@10 | +0.108 | [+0.025, +0.209] | rerank.r2 higher |
| rerank.r3 minus hybrid | Recall@10 | +0.108 | [+0.025, +0.209] | rerank.r3 higher |
| rerank.r1 minus hybrid | MRR@10 | +0.279 | [+0.128, +0.441] | rerank.r1 higher |
| rerank.r2 minus hybrid | MRR@10 | +0.279 | [+0.128, +0.441] | rerank.r2 higher |
| rerank.r3 minus hybrid | MRR@10 | +0.279 | [+0.128, +0.441] | rerank.r3 higher |
| rerank.r1 minus hybrid | nDCG@10 | +0.274 | [+0.159, +0.396] | rerank.r1 higher |
| rerank.r2 minus hybrid | nDCG@10 | +0.274 | [+0.159, +0.396] | rerank.r2 higher |
| rerank.r3 minus hybrid | nDCG@10 | +0.274 | [+0.159, +0.396] | rerank.r3 higher |

Repeated answers shared/rerank:

| File | Verified (in) | 95% interval | Declined (out) | 95% interval |
| --- | ---: | ---: | ---: | ---: |
| rerank.r1 | 8 of 8 (100%) | [0.676, 1.000] | 4 of 4 (100%) | [0.510, 1.000] |
| rerank.r2 | 8 of 8 (100%) | [0.676, 1.000] | 4 of 4 (100%) | [0.510, 1.000] |
| rerank.r3 | 8 of 8 (100%) | [0.676, 1.000] | 4 of 4 (100%) | [0.510, 1.000] |
| range (max minus min) | 0.000 |  | 0.000 |  |

Each repeat answers the same questions, so the repeats are not independent trials and their counts are not pooled into one interval.
<!-- p2:end repeats -->

Does the reranker's gain over its first stage survive the run-to-run variation?
Write what the spread is, how it compares with the gain, and what the Wilson intervals on the verified share and the declined share say about 8 and 4 questions.


The three Rerank retrieval repeats produced identical evaluation scores: Recall@10 of 0.725, MRR@10 of 0.750, and nDCG@10 of 0.731. Compared with Hybrid, the MRR@10 improvement was +0.279, with a 95% paired bootstrap interval of [+0.128, +0.441]. Since this interval excludes zero and all three repeats produced the same metric values, the measured advantage of Rerank survived the observed run-to-run variation.

However, the rankings were not completely identical. The retrieved document order changed across repeats, although the judged relevant documents remained at the same ranks. This means the evaluation scores were stable even when the exact ranking differed.

The answer-generation repeats also produced consistent verification results. In each of the three runs, all eight answerable questions passed citation verification and all four unanswerable questions were declined. The verified share was 100%, with a 95% Wilson interval of [0.676, 1.000], while the declined share was 100%, with an interval of [0.510, 1.000].

Despite these identical rates, the generated answers were not completely the same. For example, a07 cited both surface and underground regulations in two repeats, but only the underground regulation in the second repeat. The repeated runs therefore demonstrate stability in the measured outcomes rather than identical outputs.

Because the same questions were used for each repeat, the observations are not independent samples and should not be pooled into a larger confidence interval. The small number of questions also limits how broadly these results can be generalized.

### The pre-registered claim

The claim, the smallest effect, the gold-set size and the test are in `PREREG.md`, committed before your own gold-set judgments.
Here, say whether you followed the plan, what the interval turned out to be, and what that means.
The outcome section of `PREREG.md` holds the short version.


My pre-registered hypothesis predicted that BM25 would outperform Hybrid on my USGS corpus, with a meaningful MRR@10 difference of 0.15.

The observed MRR@10 was 0.816 for BM25 and 0.856 for Hybrid, giving a BM25 minus Hybrid difference of approximately -0.041. The 95% paired bootstrap interval was [-0.133, +0.048], which includes zero.

The observed direction was opposite to my prediction, and the interval does not establish a statistically distinguishable difference between the two systems. The entire interval is also within the pre-specified meaningful difference of 0.15, so the results do not support a practically meaningful advantage for BM25 on this gold set.

This result demonstrates why pre-registering a hypothesis matters. Although my original expectation was not supported, I can report the outcome without changing the hypothesis after seeing the results.