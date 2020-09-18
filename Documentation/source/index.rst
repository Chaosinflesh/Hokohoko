.. image:: _static/hokohoko.svg
   :width: 80
   :align: center

*******************************************************
Hokohoko: Foreign Exchange Predictor Evaluation Library
*******************************************************

*Hokohoko means "to trade, barter, exchange, sell, buy, export, alternate" in
Te Reo Māori.* [1]_

Version
=======

|version|

Introduction & Background
=========================

Hokohoko is a benchmark designed to evaluate FOREX speculation algorithms, in order
to provide researchers with a standard, domain-specific and domain-applicable benchmark that can be used to provide
true comparative analysis of different predictive techniques. It is intended to solve three problems prevalent within
the corpus of literature devoted to foreign exchange prediction, as identified by Bradley (2020): [2]_

(1) First, there is the problem of data source selection and bias. Over the years, many papers have been published on the
problem of predicting foreign exchange rates, with hundreds of different predictors and variations proposed. However,
for the most part, there has been no *recent* standard data set used in the evaluation of the predictors. Consequently,
for as many papers and methods published, there have been almost as many different datasets used to benchmark them,
rendering relative comparison between papers, and thus predictors, largely impossible. Due to the fluid and
unpredictable nature of the foreign exchange markets, no one currency pair or time period is comparable to another.
Despite this however, it is not uncommon to find researchers, *sometimes even within the same paper*, using different
datasets to compare their predictor to previous research. Furthermore, datasets are often selected or doctored in such
a way as to to produce favourable results for the researcher.

(2) Second, little attention has been paid to correctly measuring predictor performance with specific application to the
foreign exchange domain. For the most part, researchers have resorted to using standard measures from the
statistical or physical domains, which tend to focus on the prediction of singular values, rather than the *range
values* produced by the foreign exchange market. Whilst the occasional researcher has attempted to shoehorn the foreign
exchange range to a singular value (via average of ``HIGH``/``LOW``, ``OPEN``/``CLOSE``, or similar), most have simply
ignored the problem. The problem with the shoe-horn approach is that it loses information.

(3) Third, there is no standard 'previous method' which researchers compare their results to, particularly in the
application of machine learning to foreign exchange prediction. There are two main reasons for this:

   I. There is a clear demarcation between foreign exchange machine learning research prior to and after 2001. This is
   because of the influential work of Yao & Tan (2000) [3]_. Prior to their work, the standard to beat was
   **Buy-and-Hold** (a correlation of the **Efficient Market Hypothesis (EMH)** and its corollary, the **Random Walk**
   of the markets), with nearly all research showing ANNs significantly inferior to Buy-and-Hold for foreign exchange
   prediction. However, Yao & Tan claimed their ANN actually beat an **ARIMA** predictor with perfect foresight - a
   predictor that had never been proven to beat B&H itself. Despite this, and claiming

      *'Now that ANNs beat Buy-and-Hold ... [we are justified not to test against it]'*

   researchers for the most part started to ignore B&H. However, they tend not just to ignore Buy-and-Hold, but most
   other prior
   published work, with no one **best** previous predictor used as a benchmark. This issue is severely compounded by the
   often vague descriptions given of algorithms, rendering comparison difficult.

   II. There has been a tendency, from before Yao & Tan, but reinforced by them, to report the success of a predictor
   via *profits made*. This measure ignores its own locality, and combined with [1], renders comparative analysis of
   predictors impossible. Why was Yao & Tan's paper so influential? Basically, it told researchers what they wanted to
   hear, and ushered in a period of busy-but-low-fidelity research into the area of foreign exchange research, with
   **the vast majority of researchers reporting biased and generally incomparable performances for their algorithms.**

Hokohoko aims to solve all three problems. First, it provides access to a **large, standardised selection of real trade
rates** (50 currency pairs over 7 years),
along with **standardised parameters** drawn from analysis of the foreign exchange prediction corpus. It makes use of
parallelization to run **multiple benchmarks and simulations across different time periods,** increasing the accuracy of
the reported results. Second, it provides access to a set of **standard metrics**, that can be used alongside a simulation to allow
comparative analysis of benchmark results to actual
performance. Third, it **includes a set of standard predictors**, allowing **direct comparison** of predictor
performance under identical conditions. And it does all this in a cross-platform way with minimal dependencies.

Hokohoko was created and written by Neil Bradley, at the University of Waikato, New Zealand. Further information can be
found in the associated paper [2]_ for more information.

Bugs and issues can be reported `here <https://github.com/nc-bradley/Hokohoko/issues>`_.


Installation
============
[TODO: PyPI]

Hokohoko's source code can be found at `<https://github.com/nc-bradley/Hokohoko>`_.


Overview
========

When invoked, Hokohoko breaks the **Data** up into several equal-length, overlapping **Periods**. Each Period consists of
a **Training** area followed by a **Test** area. It then creates a **Pool** of processes, and continuously assigns
Periods to the Pool, running the specified **Predictor** within its own memory space and collating the returned
**Account** histories. Once all the Accounts have been collated, it sends them to the **Assessor** for processing and output.

As each Period moves through the dataset, the Predictor is sent a **Bar** of data for each
iteration. The Predictor can then place **Orders** (``BUY``, ``SELL``, ``DONT_BUY``, ``DONT_SELL``),
which Hokohoko then evaluates for a predefined time (**Hold**). Hokohoko ensures that each Period is long enough to always fully
evaluate every position taken. In addition, Hokohoko adds the appropriate ``DONT_BUY``, ``DONT_SELL`` Positions if
they are not explicitly provided by the Predictor.

Hokohoko then keeps track of Orders and **Positions** within the Account, and fully evaluates each
every minute. Orders become Positions when their ``open_bid`` is met, with one significant exception: If the Order has
a ``take_profit`` or ``stop_loss`` specified that would cause immediate closure, but is specified to open immediately
(``open_bid == None``), the Order is cancelled. Once opened, the Order becomes a Position, which is evaluated until
either its ``take_profit`` or ``stop_loss`` are fulfilled, or it is manually closed by the Predictor. If a Position would
trigger both its ``take_profit`` and ``stop_loss`` in the same minute, the ``take_profit`` is selected.

Additionally, Hokohoko
keeps track of the Account **Balance** and **Equity**, updating each as often as required. Importantly,
Orders and Positions are only evaluated within the Test portion of the Period, however the Predictor is not made aware
of when this is - so it should always make a prediction.


How to use
==========

Hokohoko provides a simple API, similar to that provided by trading software, which researchers can use to test their
algorithms in. It can be invoked either through the commandline::

   # This uses the default settings, but changes predictor and gives it some options.
   # See Configuration Options or try --help for more information about the options.

   python3 -m hokohoko.Hokohoko -P hokohoko.predictors.SameAsLast \
       "--direction OFFSET_SAME --tp_ratio 1.0 --sl_ratio 0.01"

or imported into a pre-existing project (see the included Example.py).

.. include:: downloads.rst


Sample Output
=============

TODO: Update when OS refactor completed.

Configuration Options
=====================

Hokohoko uses a ``NamedTuple`` (``hokohoko.Hokohoko.Config``) to hold the configuration options for a run. It can be configured
either
via instantiation (such as in ``Example.py``) or command line options (if running Hokohoko stand-alone):

.. code-block:: Text

    --simulate
                    Runs in simulate mode instead of benchmark.

    -P, --predictor PREDICTOR "PARAMETERS"

        PREDICTOR   The fully qualified name of the predictor to use.
                    Defaults to `hokohoko.standard.DoNothing`.

        PARAMETERS  The parameters to pass to the predictor.
                    Defaults to `None`.


    -A, --assessor ASSESSOR "PARAMETERS"

        ASSESSOR    The fully qualified name of the assessor to use.
                    Defaults to `hokohoko.standard.Logger`.

        PARAMETERS  The parameters to pass to the assessor.
                    Defaults to `None`.

    -D, --data DATA_SOURCE PARAMETERS

        DATA_SOURCE The fully qualified name of the data source to use.
                    Defaults to `hokohoko.standard.Npz`.

        PARAMETERS  The parameters to pass to the data source.
                    Should be a quoted string, defaults to `data.Npz`.


    -S, --subset "SUBSET"

        SUBSET      Symbol subset to use. Comma separated codes, e.g. 'AUDUSD,AUDNZD'. Symbols
                    requested that do not exist in the data source are ignored.
                    Defaults to `None`.

.. warning::

    The following options are included to ease testing and debugging. They should **NOT** be used otherwise.

.. code-block:: Text

    -n, --period-number PERIOD_COUNT

        PERIOD_COUNT    The number of Periods to test across.
                        Defaults to 256.


    -c, --process-count PROCESS_COUNT

        PROCESS_COUNT   The number of processes to run concurrently. More processes require more
                        RAM (see Limitations).
                        Defaults to 8.


    -f, --past-minutes PAST_MINUTES

        PAST_MINUTES    How many minutes in each Bar. In simulation mode, determines the period
                        for on_bar().
                        Defaults to 1440.


    -t, --hold-minutes HOLD_MINUTES

        HOLD_MINUTES    How many future minutes to evaluate a Position for. Has no effect in
                        simulate mode.
                        Defaults to 1440.

    --load-limit LOAD_LIMIT

        LOAD_LIMIT      Limits the number of minutes to load from the data source.
                        Defaults to `None`.

    --training-minutes TRAINING_MINUTES

        TRAINING_MINUTES    Override the default training area length (the period of data provided
                            to predictors where any returned Positions are ignored for benchmarking
                            or simulation.
                            Defaults to 10080 * 26 * 3, approximately 18 months.


    --test-minutes TEST_MINUTES

        TEST_MINUTES    Override the default test area length (the period where Positions from the
                        predictor are evaluated.
                        Defaults to 10080 * 26, approximately 6 months.


    --profiling
                        Enables profiling output. (files will be called 'profile_[period_id]'), in
                        the current directory.
                        Defaults to False.


Limitations
===========

* Hokohoko has significant RAM requirements. The default settings need approximately 1GB per concurrent process, plus 1.6GB during
  file load. Default settings of 8 concurrent processes therefore requires about 9.6GB of RAM, not including the RAM
  required by each predictor. RAM usage is reduced for subsets.
* Hokohoko has been successfully tested using Python 3.6, 3.7 and 3.8 on Windows 10, Debian and Ubuntu.
* The base ``hokohoko`` package requires ``numpy`` only. The additional packages ``hokohoko_assessors`` and ``hokohoko_predictors`` may have
  additional requirements, such as ``scipy``.
* Hokohoko is intended to be cross-platform. It therefore configures Python to use 'spawn' for each period
  benchmarked/simulated.
* Simulate is indicative, not authoritative, as to relative performance.
* Due to the nature of the foreign exchange markets, long term predictions are usually based on fundamental rather
  than technical analysis. As Hokohoko is intended to be used on the latter, it may be that it is unsuitable for use with
  fundamentalist strategies (such as Cootner, Bollinger etc.) which intend to hold long-term positions. Such strategies
  will often score poorly in Hokohoko, and their score has little to no correlation with their long-term profitability.


API Reference
=============

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. toctree::
   :glob:

   modules


LICENSE
=======

.. literalinclude:: ../../LICENSE
    :language: Text


Glossary
========

.. glossary::
    :sorted:

    Random Walk
        In the event of an efficient market, it is theorised (and for the most part observed) that the behaviour of
        asset prices in the market follow a random walk - that is that there is no correlation between past and future
        behaviour.

    Efficient Market Hypothesis
        Outlined in detail by Fama (1965), [4]_ [5]_ the EMH proposes that for a large enough market, there will be a buyer for every
        seller, the buyers are highly intelligent and react to and disseminate new information rapidly, and thus, all
        relevant information is already represented in the current price. Therefore, past information in old prices has
        no bearing on future prices, and the past is not an indication of the future.

    Data
        The source of data. Hokohoko provides access to a 2.6GB file, data.Npz which contains 7 years of currency data for
        50 currency pairs. The data includes real UTC timestamps so that external data sources may be referenced by the
        Predictor.

    Period
        An individual benchmark/simulation unit. Hokohoko's default data file provides enough data to run 11 Periods before
        they before overlapping. Periods are intended to be self-contained - whilst Predictors may access external data,
        they should not share anything out, or risk invalidating the results.

    Training
        The initial period of time for which a Period runs, during which data is passed to the Predictor as normal, but
        Orders are ignored, and no results are collected.

    Test
        The period following Training, where like Training, data is passed in the Predictor, but Orders will be
        actioned or assessed (depending on the mode). The result histories are collected during this time.

    Pool
        Hokohoko uses multiple processes to a) get around Python's GIL, and b) make it harder for Predictors to share information.
        The Pool size determines the number of Periods that may be processed simultaneously, at increased RAM cost.

    Predictor
        Predictor is the main API for a predictive algorithm to concern itself with. It needs to be inherited as a base
        for custom prediction algorithms, and provides access to the Period's Account, methods to place and close
        Orders, and a deterministic RNG (via self).

    Assessor
        The class that is used to assess the outcomes. Hokohoko ships with logs the Order histories for external analysis only.
        The base Assessor class is provided to allow custom assessors to be created, and the package ``hokohoko_assessors`` contains
        a selection of additional Assessors.

    Bar
        A Bar is a single period of data, similar to that provided by trading software. See the API for further
        information.

    Order
        A request to open a trade. See the API for further information.

    Hold Minutes
        The length of time for which an Order will be assessed in Benchmark mode.

    Position
        An Order that has activated. See the API for further information.

    Account
        Each Period includes an Account, linked to the Predictor, which allows access to the Order and Position lists.
        The Order predictions and their outcomes are also stored in the Account.

    TAKE_PROFIT
        A specific, profitable value at which a Position will close.

    STOP_LOSS
        A specific value at which a Position will close, accepting a loss.

    Balance
        The balance of currency available in the Account. Hokohoko does not keep track of margins, so all Accounts start at
        0.0, and there are no restrictions on trade volumes. Balance is only changed by closing Positions, either
        through ``take_profit`` or ``stop_loss``, manually or at the end of a Bar [TODO: Reword this!].

    Equity
        The real value of the Account, if all open Positions were to be closed instantaneously.

    OPEN
        The open price for a currency.

    Direction
        The direction of a trade. Hokohoko accepts ``BUY``, ``SELL``, ``DONT_BUY`` and ``DONT_SELL``.

    Accuracy
        The benchmark method introduced by Hokohoko.

    DoNothing
        The included Predictor, which makes no predictions, thereby ensuring Hokohoko always generates
        ``dont_buy`` and ``dont_sell`` Orders.

    Buy-and-Hold
        A trading strategy where a Position is bought and held for a pre-determined length of time, with the
        acceptance that the result of the outcome will be largely random.

    Symbol
        The name of a currency pair, e.g. ``AUDUSD``. The first part indicates the base currency, and the second
        the target currency. This distinction is irrelevant for the Accuracy benchmark, but is very import when
        simulating.


References
==========

.. [1]
    The name was determined in conjunction with Associate Professor Te Taka Keegan, Associate Dean Māori of Wananga Putaiao,
    Te Wananga o Waikato (Division of Health, Engineering, Computing and Science, University of Waikato).

.. [2]
    Bradley, N. C. (2020). Hokohoko: A Comprehensive Framework for Evaluating Artificial Intelligence-based and Statistical
    Techniques for Foreign Exchange Speculation (Thesis, Master of Science (Research) (MSc(Research))).
    The University of Waikato, Hamilton, New Zealand. Retrieved from `<https://hdl.handle.net/10289/13752>`_.

.. [3]
    Yao, J. & Tan, C.L. "A Case Study on Using Neural Networks to Perform Technical Forecasting of Forex"
    *Neurocomputing 34* (2000) 79-98.

.. [4]
    Fama, E. (1965a). "Random Walks in Stock Market Prices", *Financial Analysts Journal, 21(5),* 55-59.

.. [5]
    Fama, E. (1965b). "The Behaviour of Stock Market Prices", *The Journal of Business, 38,* 34-105.


.. codeauthor:: Neil Bradley
