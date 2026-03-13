# 💳 Payment Acceptance Rate Analyser

An end-to-end payments analysis project simulating 250,000 European transactions to identify why payments fail, which segments underperform, and how intelligent retry logic recovers lost revenue. The kind of analysis that sits at the core of modern payment processor value propositions.

---

## 📌 Project Overview

Authorization rate optimisation is one of the most impactful levers in the payments industry. For every 1 percentage point improvement in acceptance rate, a merchant processing €10M annually recovers €100,000 in otherwise lost revenue.

This project simulates a realistic European payments dataset and analyses acceptance rates across multiple dimensions, culminating in a **retry simulation** that quantifies the revenue difference between naive and intelligent retry strategies. This is something Adyen and similar processors sell as a core feature to enterprise merchants.

---

## 📂 Dataset

This project uses a **synthetic dataset** of 250,000 transactions generated to reflect real-world European payment patterns. No proprietary or sensitive data is used.

The data is designed with realistic rules baked in:

| Property | Detail |
|----------|--------|
| Transactions | 250,000 |
| Payment methods | Credit Card, Debit Card, iDEAL, PayPal, Klarna, Prepaid Card |
| Countries | Netherlands, Germany, France, UK, Belgium, Spain, Italy, Sweden, Poland, Austria |
| Decline reasons | 8 categories (soft and hard declines) |
| Time dimension | Hour of day, day of week |

Key patterns built into the data:
- iDEAL achieves ~98% authorization (bank redirect, no card network friction)
- Authorization rates drop significantly for transactions above €500
- Overnight transactions (01:00-05:00) decline more than business-hours transactions
- Southern and Eastern European markets show lower baseline acceptance rates

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Core language |
| pandas | Data manipulation |
| NumPy | Synthetic data generation & simulation |
| Matplotlib / Seaborn | Visualisation |
| Jupyter Notebook | Interactive analysis |

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/payment-acceptance-rate.git
cd payment-acceptance-rate
```

### 2. Install dependencies
```bash
pip install pandas numpy matplotlib seaborn jupyter
```

### 3. Launch the notebook
```bash
jupyter notebook payment_acceptance_rate.ipynb
```

No external dataset download needed. The synthetic data is generated in the first cell.

---

## 📊 Analysis Sections

### 1. Authorization Rate by Payment Method
Which methods perform best? iDEAL and PayPal significantly outperform card-based methods, with important implications for checkout optimisation.

### 2. Country-Level Analysis
A heatmap of authorization rates across 10 European markets reveals meaningful variation, from the Netherlands at the top to Poland at the bottom, driven by differences in banking infrastructure and issuer behaviour.

### 3. Decline Reason Breakdown
Not all declines are equal. The analysis categorises decline codes into hard declines (stolen card, suspected fraud) and soft declines (insufficient funds, exceeds limit), distinguishing the ones worth acting on from those that aren't.

### 4. Amount Bucket Analysis
Authorization rates drop sharply for high-value transactions. Understanding this threshold helps merchants set appropriate checkout flows and authentication strategies.

### 5. Time-of-Day & Day-of-Week Patterns
Overnight transactions face a measurably higher decline rate as issuer fraud scoring tightens during off-hours, with direct implications for retry timing.

### 6. Multi-dimensional Segment Analysis
The ten best and worst performing segments across country, payment method, and amount bucket combinations — the kind of drill-down a payments analyst would present to a merchant account manager.

---

## 🔁 Retry Simulation: The Differentiating Feature

The standout module of this project simulates and compares two retry strategies head-to-head:

**Naive retry:** retry all declines immediately, same payment method, regardless of decline code or time of day.

**Smart retry:** apply three rules:
1. Skip hard declines entirely (stolen card, fraud, expired card, invalid number)
2. Only retry during business hours (09:00-18:00) when issuer approval rates are higher
3. For high-value card failures (>€250), route to an alternative method (PayPal) instead of retrying the same card

### Why naive retry causes active harm

Rapid repeated retries on hard declines don't just fail. They signal desperation to card issuers, which can lower a merchant's overall authorization rate. Every retry attempt also has a processing cost, and retrying a suspected fraud transaction can trigger a card block, creating a worse experience for a legitimate customer.

### Results

| Metric | Naive retry | Smart retry |
|--------|-------------|-------------|
| Retry attempts | All declines | Eligible only |
| Retry efficiency | ~14% | ~43% |
| Recovered revenue | Lower | Significantly higher |

> Exact figures are generated when you run the notebook against the synthetic data.

---

## 💡 Key Takeaways

- **iDEAL is significantly underutilised** by merchants outside the Netherlands. For Dutch merchants especially, making iDEAL the default checkout method is the single highest-impact change available.
- **20%+ of declines are recoverable** through smarter retry logic, alternative method routing, or prompting customers to update card details.
- **Retry timing matters.** The gap between overnight and business-hours authorization rates means scheduled retries outperform immediate retries for subscription and recurring billing use cases.
- **Hard declines should never be retried.** Doing so wastes attempts, increases processing costs, and risks issuer friction that degrades overall acceptance rates.

---

## 📁 Project Structure

```
payment-acceptance-rate/
│
├── payment_acceptance_rate.ipynb   # Main analysis notebook
└── README.md                       # This file
```

---

## 👤 Author

**Nick Zwart**  
Fraud Data Analyst | ABN AMRO Bank  
[LinkedIn](https://www.linkedin.com/in/nick-zwart/) · [GitHub](https://github.com/NickZward)

---

## 📄 License

This project is for educational and portfolio purposes. All data is synthetically generated and does not represent any real individuals or transactions.
