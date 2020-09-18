Accuracy: The Hokohoko Benchmark
================================


Historically, researchers in foreign exchange prediction have shunned the use of an absolute measure (such as maximum
profit possible per trade). Hokohoko aims to change that, with the introduction of a new metric, *Speculative Accuracy*. This measures
how close to maximum profit a position makes from the ``OPEN`` price, whilst making allowance for trades for which
profit was impossible.

The logic behind this metric is that, for any given future period of time, the conditions of a taken Position may
be met, and thus the Position/prediction is correct. However, it is only maximally correct if its ``take_profit``
matches the observed ``HIGH``/``LOW`` (depending on trade **Direction**), and thus anything otherwise is only partially
correct. We also need to take into account the times where a Position cannot be profitable, and other times when there
is no movement in the market.

Therefore, given a Position with

.. math::

    \begin{equation}
    result=\lbrace
    max\_profit \in \mathbb{R}_{\geq 0},
    max\_loss \in \mathbb{R}_{\leq 0},
    actual\_profit \in \mathbb{R},
    taken \in \lbrace 0, 1 \rbrace \rbrace\ \ \ \ (1)
    \end{equation}

we define thus

.. math::

    \begin{equation}
    accuracy(result) = \left\{
    \begin{array}{@{}rl@{}}
    \frac{actual\_profit}{max\_profit}, & \text{if}\ max\_profit \gt 0 \\
    1.0, & \text{if}\ max\_profit = 0 \land taken = 0\ \ \ \ (2) \\
    \frac{-actual\_profit}{max\_loss}, & \text{if}\ max\_loss \lt 0 \\
    0.0, & \text{otherwise}
    \end{array}\right.
    \end{equation}

The astute observer will note that these equations are:

1. Unbounded to the negative - incorrect predictions are heavily penalised.
2. Highly optimistic - making a loss for a potential 1 pip profit is very heavily penalised.
3. Heavily skewed for correct ``DONT_BUY``, ``DONT_SELL``.
4. Not the absolute profit possible, allowing possible results > 100%.

To these, the author notes:

1. Accepted, no apologies. Make better predictions.
2. Accepted, still no apologies. As above.
3. Within the default dataset provided, ``¬taken`` will only be correct about two percent of the time. The heavy skew is
   considered acceptable in this scenario (and is logically true).
4. If a predictor can more accurately predict the dips and rises that allow for profits greater than from
   ``OPEN`` to ``HIGH``/``LOW``, it deserves the score it gets. Accepted.

