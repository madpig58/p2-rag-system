# Pre-registration (598E)

This file is for 598E students; it is the second half of the 598E rider, and 498E students can ignore it or delete it.

A pre-registration is a claim you write down, with the test that will judge it, before you can see the answer.
Its value is that the claim can be wrong in a way anyone can check, and that you cannot adjust it afterwards to fit the numbers.
A well-powered result that says "no effect as large as the one I cared about" scores as well as a confirmation, so you have no reason to bend the claim.

**Git history is how I will know the order.**
Commit this file, filled in through section 4, before the first commit that puts a judgment line into `eval/own/qrels.txt` (or any other file under `eval/own/`).
`uv run p2 check` reads `git log` to find the first commit in which sections 1 to 4 have no TODO marker left and some words of yours in each, and confirms that it comes before your first judgment; a copy that was filled in afterwards fails.
Right after that commit, `p2 check` names it and waits for your first judgment; it asks for section 5 separately, once you have scored your own corpus.
You may ingest your corpus and write queries first, but not the relevance judgments.
After that first commit, do not edit sections 1 to 4, because `p2 check` compares them with the commit where you filled them in.
If something must change, add a dated entry in section 6 and leave the original as it was.

You need your stage 1 scores for section 3, so score the shared corpus first.

---

## 1. Hypothesis

One sentence, about your own corpus, naming two of your systems and a direction.
For example: "On my corpus of Kubernetes documentation, `rerank` has a higher MRR@10 than `hybrid`, because the queries are paraphrases that a first-stage fusion ranks too low."
It should be something you could be wrong about.


I predict that BM25 will achieve a higher MRR@10 than Hybrid on my USGS Mineral Commodity Summaries 2022–2024 corpus. These documents contain specific mineral names, countries, years, and production statistics. I expect exact keyword matching to be more effective for identifying the correct documents, while combining BM25 with dense retrieval may sometimes lower the rankings of relevant documents.

---

## 2. The smallest effect that matters

Name one metric, MRR@10 or nDCG@10, and choose it now so you cannot pick the better one afterwards.
Then say how large a difference between the two systems would matter to a person using the search, and why that size.
A difference of 0.02 is usually not worth a reranker's cost in time and tokens.
In this course, choose a Δ of at least 0.15 unless you argue for a larger one, because a smaller gap takes more queries than one project can judge.
Call your number Δ (delta).



My primary evaluation metric will be MRR@10, and I will use Δ = 0.15 as the smallest meaningful difference.

I chose MRR@10 because it measures how highly the first relevant document appears in the search results. I consider a difference of 0.15 meaningful because finding relevant information closer to the top of the results can noticeably improve the user's search experience.

---

## 3. How many queries you need

The size of the gold set follows from three numbers: how large a difference you want to detect (Δ), how variable the per-query differences are (sd), and the usual choices of a 5% false-alarm rate and 80% power.

```
n = ((1.96 + 0.84) * sd / Δ)^2
```

Here sd is the standard deviation of the per-query differences between your two systems, which `results/results.json` holds for the shared practice queries.
Compute it from your stage 1 runs for the same two systems, or the nearest pair you have, and say which pair you used.
With only 20 practice queries the sd is itself noisy, so be generous and round up.

Some numbers to calibrate against.
At sd 0.3 and Δ 0.10 the formula gives about 71 queries, and with the t distribution's small-sample correction it is a few more, about 73.
At sd 0.3, a gold set of 30 queries can only detect a difference of about 0.15, which is why 30 queries cannot support a claim about a gap of 0.10.
The spreads you will measure on the shared practice queries are mostly larger than 0.3: from about 0.31 for `hybrid` against `bm25` to about 0.66 for `dense` against `bm25`.
For `rerank` against `hybrid` the sd is about 0.39, so a Δ of 0.10 needs about 120 queries, 0.15 about 55, and 0.20 about 31.
So the course's Δ of 0.15 means about 55 queries for that pair; at an sd of 0.66 it would mean about 150, so compare a pair whose spread you can afford.
Choose Δ and the size of your gold set together: the smallest effect that matters to a user, and a number of queries you can write and judge in the time you have.
If the two do not meet, say which one you gave ground on and why.

After you score the own corpus, the minimum detectable difference that `uv run p2 score` prints for your two systems is this same calculation run the other way.
It should come out at or below your Δ.
If it does not, your queries varied more than your stage 1 sd suggested, and you will say so in the outcome.



I will compare BM25 and Hybrid using the standard deviation of their per-query MRR@10 differences from the shared practice dataset.

The measured standard deviation was 0.308, and my chosen minimum meaningful difference is Δ = 0.15.

Using the sample-size formula:

n = ((1.96 + 0.84) × 0.308 / 0.15)² ≈ 33.06

This means I need at least 34 queries. I plan to use 40 queries to provide a small margin beyond the calculated minimum.

However, this estimate is based on only 20 shared practice queries. The variability may differ on my USGS corpus, so I will report whether my final evaluation achieves the planned detectable difference.

---

## 4. The test, and what each result will mean

The test is the paired 95% interval of the mean difference between your two systems on your own gold set, from the `own-pairs` table that `uv run p2 score` writes in `EVAL.md`.
Write the rule now.
This is the default rule, and you can tighten it, but do not loosen it after you see your numbers.

| The interval is | I will say |
|---|---|
| entirely above zero in the direction I predicted | supported: the difference is distinguishable from zero |
| entirely on the other side of zero | contradicted: the opposite of my hypothesis holds on this gold set |
| around zero, with both ends inside plus or minus Δ | well-powered null: a difference as large as Δ is ruled out |
| around zero, with an end beyond plus or minus Δ | inconclusive: the gold set could not settle it, and I say so |


I will evaluate the difference between BM25 and Hybrid using MRR@10, defining the difference as BM25 minus Hybrid.

I will use the paired 95% confidence interval generated by uv run p2 score.

If the entire interval is above zero, I will consider my hypothesis supported.

If the entire interval is below zero, I will consider my hypothesis contradicted.

If the interval includes zero and both endpoints fall within −0.15 and +0.15, I will report a well-powered null result.

If the interval includes zero but extends beyond ±0.15, I will consider the result inconclusive.

I will follow these rules regardless of which system achieves the higher average score.

---

## 5. Outcome (write this after the fact)

What was the interval?
Which row of the table in section 4 is it?
Did your gold set reach the size section 3 asked for, and what was the minimum detectable difference that `uv run p2 score` printed?
What would you do next, and what would you want a reader to take from this?

My pre-registered hypothesis predicted that BM25 would outperform Hybrid by at least 0.15 MRR@10 on my USGS corpus. I expected BM25 to perform better because the documents contain specific mineral names, countries, years, and technical terminology that keyword-based retrieval could match directly.

The actual results did not support my prediction. BM25 achieved an MRR@10 of 0.816, while Hybrid achieved 0.856. The observed BM25 minus Hybrid difference was approximately -0.041, which was in the opposite direction from my hypothesis.

The 95% paired bootstrap interval was [-0.133, +0.048]. Since this interval includes zero, I cannot conclude that either system reliably outperformed the other on my gold set. The minimum detectable difference was approximately 0.132, indicating that this evaluation had limited sensitivity to smaller performance differences.

My original prediction was therefore not supported. Although Hybrid achieved a slightly higher observed score, the evidence was insufficient to establish a clear advantage for Hybrid. The interval also did not support the predicted meaningful BM25 advantage of 0.15.

One possible explanation is that semantic retrieval contributed useful information even in a corpus containing many specific technical terms. However, I did not isolate that explanation experimentally, so I cannot claim it as a confirmed cause.

This result reinforced the importance of pre-registration. Rather than changing my hypothesis after seeing the results, I can compare the original expectation with the actual evidence and acknowledge that the outcome was different from what I predicted.

---

## 6. Amendments

Dated entries only, one per change, each saying what changed and why.
Leave this section as it is if nothing changed.
