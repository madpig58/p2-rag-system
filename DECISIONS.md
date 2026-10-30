# Decision log

Your methods section, in your own words.
About one to two pages in total.

Answer these as you go, not the night before it is due.
Each answer is easier to write while the decision is still fresh, and prompt 1 only works if you write it before you see your own-corpus numbers.
Specifics beat polish: a short, honest answer with a number in it is worth more than a long vague one.

Each prompt ends with a marker line.
Replace that line with your answer.
`uv run p2 check` reports a marker as unfinished work, and `uv run p2 check --final` fails while any marker is left, so a finished log is part of being done.

Please do not let the agent write these for you.
These answers are about what you chose and what you knew, and the agent cannot know that.
Prompt 3 in particular only works in your own words.

---

## 1. Why this corpus, and what you expected

Why did you pick the corpus you used in stage 2, and why does it belong to a field or a question you care about?
Then say what you expected before you measured anything: which of `bm25`, `dense`, `hybrid` and `rerank` do you think will win on it, and which will do worst, and why?

Commit this answer before your first `uv run p2 score` on the own corpus.
Git history then shows that the expectation came first, which is what lets it be wrong in a way that teaches you something.
If you were surprised later, say so in prompt 4 or in EVAL.md; do not come back and rewrite this one.

I chose the USGS Mineral Commodity Summaries because I am interested in how minerals are connected to modern technology and industry. Many materials, such as lithium, cobalt, and rare earth elements, are important for batteries, electronics, and other technologies that we use every day. I wanted to explore how different retrieval systems handle information about these materials, especially when questions involve technical terms, specific minerals, or industrial applications.

Before evaluating the systems, I expected Rerank to perform the best because it uses Claude to examine the retrieved documents and decide which ones are most relevant to the question. I also thought BM25 would perform well because the corpus contains many specific mineral names, countries, and technical terms. My pre-registered hypothesis specifically predicted that BM25 would outperform Hybrid. However, I did not record a complete ranking of all four systems or a definite prediction about which would perform worst before running the experiments.

I am writing this explanation after completing the evaluation, rather than before the first scoring run as the assignment originally required. However, my BM25 versus Hybrid prediction was recorded in PREREG.md and committed before the relevance judgments and evaluation results. I have kept that original prediction unchanged instead of rewriting it to match the results.

---

## 2. A fork in the road

Name one real design choice where you could have gone two ways: the chunk size, the embedding model, how the two systems are fused, how many documents the reranker sees, a sentence in `prompts/answer.txt`, how you cleaned the corpus.

Say which you picked, what the alternative was, and what you gave up by not taking it.
If you measured both, give both numbers.
If you rejected the alternative without measuring it, say why that was a fair call, and what it cost you in time, tokens or complexity.

"There was no alternative" is not an answer.
Find the fork.

One design choice in my project was how to combine BM25 and Dense retrieval in the Hybrid system. I used Reciprocal Rank Fusion (RRF) with equal weights for both systems. An alternative was to give BM25 a higher weight because my corpus contains many specific mineral names and technical terms.

I initially kept equal weights because I wanted both keyword-based and semantic retrieval to contribute equally, without assuming that one method would always be more useful. This also gave me a simple baseline that I could compare against a modified version later.

I tested the alternative in my ablation experiment by doubling BM25's weight while keeping the Dense weight unchanged. The original Hybrid system achieved an MRR@10 of 0.856, while the weighted version achieved 0.881. The improvement was +0.024, with a 95% confidence interval of [-0.041, +0.093]. Since the interval includes zero, I cannot conclude that the weighted version is reliably better.

By choosing equal weights, I may have given up a small performance improvement on certain questions. However, increasing BM25's influence also reduced performance on other questions, such as h06. This tradeoff showed me that improving retrieval for one type of question does not necessarily improve it for every question.

---

## 3. Where you overruled the agent

One time Claude suggested, wrote or claimed something and you did not take it.
It might be a relevance judgment you disagreed with, a retriever it called finished when a run file showed otherwise, a number it summarized wrongly, or a license it said was fine.

What did it do?
How did you notice?
What did you do instead?

If it genuinely never happened, say so plainly, and then say what you would have had to check in order to notice.
Being honest here costs you far less than a story you cannot defend when you record your video.

One situation where I did not simply accept Claude's output was during the Rerank evaluation. For query c27, Claude returned an invalid ranking by repeating the number 19 and leaving out 20. The system detected the invalid response and used the original Hybrid ranking instead.

After reviewing the issue, I considered adding `uniqueItems: true` to the output schema to prevent duplicate ranking numbers. However, I decided to keep the existing implementation because I wanted to maintain consistency with the experiments that had already been completed.

Instead of ignoring the problem, I documented the limitation and checked whether it affected the evaluation. For c27, the fallback did not change the score because Hybrid already ranked the relevant tungsten documents at the top.

This experience reminded me that AI-generated results should not be trusted without verification. Even when Claude follows a structured prompt, its output can contain errors, and I need to decide whether correcting an issue is worth changing the experimental setup.

---

## 4. A number you do not trust

Pick one number in `EVAL.md` that you do not fully trust, and say why.
It could be a mean over a small query class, a difference whose interval includes zero, a verified share of 100%, a score on a gold set you wrote yourself, or a result you got only once.

What would have to be true for you to trust it?
Did you do anything to test it, and what did that show?

One number I do not fully trust is the Rerank system's MRR@10 of 0.975 on my own corpus. Although this is a very high score, I think it may give an overly optimistic impression of how well the system would perform on unfamiliar questions.

One reason is that my evaluation set contains only 40 questions, and 30 of them were drafted by Claude. Rerank achieved an MRR@10 of 1.000 on the Claude-generated questions but 0.900 on the 10 questions I developed myself. This difference makes me wonder whether the evaluation questions are sufficiently diverse and challenging.

I examined the results by question origin and also investigated individual failures. For example, h08 showed that the system struggled when the question used different vocabulary from the relevant documents, while c20 showed that relevant documents could be missed when they fell outside the reranker's candidate pool. These cases suggest that the overall score does not capture every weakness.

To trust the result more, I would need a larger evaluation set containing more independently written questions, more difficult paraphrases, and questions that do not directly mention the target mineral. I would also review the relevance judgments more carefully to check whether any relevant documents were missed.

I still consider the score useful for comparing systems on my current gold set, but I would not treat it as proof that Rerank will achieve the same performance on other questions or collections.

---

## 5. What is still wrong

One thing in your system, your corpus or your gold set that is not right, not finished, or that you do not fully understand.

What would you do next, and how would you find out whether it matters?
Name the file, the query or the document where someone could look.

One limitation that remains in my system is that Rerank only considers the top 20 documents retrieved by Hybrid. This means that even if a relevant document exists in the corpus, Rerank cannot promote it if Hybrid places it outside the candidate pool.

I noticed this problem in query c20, which asks about a dense drilling fluid made from an alkali metal salt that is rented and returned for reprocessing. All three cesium chapters were judged relevant, but Hybrid ranked the 2023 and 2024 cesium documents at positions 31 and 21. Since Rerank only examines the top 20 candidates, these two documents were never considered, even though they contained relevant information.

If I continued developing this system, I would experiment with increasing the reranking candidate pool from 20 to 40 or 50 documents. I would also consider improving the first-stage retrieval system, since a larger candidate pool would increase the number of documents Claude needs to evaluate.

To determine whether this change matters, I would run the modified system on the same 40 evaluation questions and compare Recall@10, MRR@10, and nDCG@10 against the original Rerank system. I would specifically examine whether the missing cesium documents in c20 move into the top 10, while also measuring any additional API cost and processing time.

The relevant evidence can be found in `runs/own/rerank.trec`, the Hybrid run results, and `p2/retrievers/rerank.py`. I have not tested a larger candidate pool yet, so this remains a proposed improvement rather than a demonstrated solution.
