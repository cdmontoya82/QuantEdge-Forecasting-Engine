# QuantEdge: Sports-Based Financial Risk & Probabilistic Forecasting Engine 📈⚽

**QuantEdge** is a high-performance predictive framework designed to identify value discrepancies in sports markets. By combining probabilistic modeling with financial risk management algorithms, the system transitions from simple "betting" to a disciplined **Statistical Arbitrage** approach.

---

## 🧠 Core Architecture

The engine is built on a modular pipeline designed for scalability and rigor:

1. **Statistical Modeling:** Implements discrete and continuous probability distributions to estimate true event frequencies based on historical offensive and defensive performance metrics.
2. **Value Identification (Expected Value):** Benchmarks calculated internal probabilities against public market odds to isolate positive-edge opportunities where $EV > 0$.
3. **Risk Management (Kelly Criterion):** Utilizes capital allocation optimization formulas to minimize the *Risk of Ruin* while maximizing long-term exponential growth.
4. **Confidence Intervals:** Incorporates variance analysis to provide a structural safety margin for every operational signal.

---

## 🛠️ Technical Stack

- **Language:** Python 3.x
- **Scientific Computing:** NumPy, SciPy (Probability Distributions)
- **Data Science:** Pandas
- **Visualization:** Matplotlib, Seaborn

---

## 📊 Key Formulas Applied

### 1. Expected Value ($EV$)
The model only triggers an alert when the expected value is positive. This benchmarks our internal probability against the market's implied probability:

$$EV = (P_{\text{internal}} \times \text{Net Profit}) - (P_{\text{loss}} \times \text{Stake})$$

Where:
* $P_{\text{internal}}$: The true probability calculated by our Poisson/Normal distribution engine.
* $\text{Net Profit}$: The potential decimal odds return minus the initial stake $(\text{Odds} - 1)$.
* $P_{\text{loss}}$: The complementary probability of losing the asset $(1 - P_{\text{internal}})$.

### 2. Probability Distribution (Poisson Process)
To model discrete event frequencies (such as goals or points scored by a team), the engine utilizes the Poisson Probability Mass Function (PMF):

$$P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}$$

Where:
* $\lambda$: The expected mean of events (calculated via offensive and defensive efficiency coefficients).
* $k$: The specific number of occurrences (e.g., scoring exactly 0, 1, or 2 goals).

### 3. Capital Allocation (Fractional Kelly Criterion)
To maximize the long-term exponential growth of the bankroll while structurally eliminating the *Risk of Ruin*, we implement a fractional optimization of the Kelly formula:

$$f^* = \alpha \times \frac{b \cdot p - q}{b}$$

Where:
* $f^*$: The optimal fraction of the current bankroll to allocate.
* $\alpha$: The fractional scaling factor (e.g., $\alpha = 0.3$ for a conservative safety margin).
* $b$: The net decimal odds received on the wager $(\text{Odds} - 1)$.
* $p$: The internal probability of winning.
* $q$: The internal probability of losing $(1 - p)$.

---

## 📂 Production & Data Ingestion Disclaimer

*To preserve proprietary Intellectual Property (IP), this public repository contains the foundational core statistical, valuation, and capital allocation engine. The automated real-time web-scraping layers, live API ingestion, and historic database pipelines remain private.*

---
*Developed as a showcase of Financial Analytics & Full-Stack Data Science integration.*
