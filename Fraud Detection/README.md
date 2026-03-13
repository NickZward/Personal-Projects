# 💳 Credit Card Fraud Detection

A machine learning project to detect fraudulent payment transactions using real-world data, built to explore patterns, handle class imbalance, and evaluate models with metrics that actually matter in a payments context.

---

## 📌 Project Overview

Financial fraud detection is one of the most impactful applications of data science in the payments industry. This project walks through the full analytical pipeline:

- Exploratory data analysis of 284,000+ transactions
- Identifying fraud patterns by time, amount, and transaction features
- Handling extreme class imbalance (only 0.17% of transactions are fraudulent)
- Training and comparing two classification models
- Evaluating with fraud-appropriate metrics (not just accuracy)
- Tuning the decision threshold based on business trade-offs

---

## 📂 Dataset

**Source:** [Kaggle — Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)

The dataset contains credit card transactions made by European cardholders in September 2013.

| Property | Value |
|----------|-------|
| Total transactions | 284,807 |
| Fraudulent transactions | 492 (0.17%) |
| Features | V1–V28 (PCA-anonymised), Amount, Time |
| Target | `Class` (0 = legitimate, 1 = fraud) |

> Note: Features V1–V28 are the result of PCA transformation to protect cardholder privacy, this mirrors how real payments data is often shared in industry.

**To download:**
```bash
# Option 1: Kaggle CLI
kaggle datasets download -d mlg-ulb/creditcardfraud
unzip creditcardfraud.zip

# Option 2: Manual download
# Visit https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud and download creditcard.csv
```

Place `creditcard.csv` in the root of this project folder.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Core language |
| pandas | Data manipulation |
| NumPy | Numerical operations |
| scikit-learn | Modelling & evaluation |
| Matplotlib / Seaborn | Visualisation |
| Jupyter Notebook | Interactive analysis |

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/fraud-detection.git
cd fraud-detection
```

### 2. Install dependencies
```bash
pip install pandas numpy scikit-learn matplotlib seaborn jupyter
```

### 3. Launch the notebook
```bash
jupyter notebook fraud_detection.ipynb
```

Run cells top to bottom. All outputs — charts, metrics, and model results are generated inline.

---

## 📊 Key Findings

### Fraud patterns
- Fraudulent transactions peak during **overnight hours**, when real-time monitoring is typically lower
- Fraud amounts are **more concentrated in the €0–€200 range**, while legitimate transactions have more high-value outliers
- Several PCA features (notably **V14, V4, V11**) show strongly different distributions between fraud and legitimate transactions, these become the most important predictors

### Model performance (test set)

| Model | ROC-AUC | PR-AUC | Recall (Fraud) | Precision (Fraud) |
|-------|---------|--------|---------------|------------------|
| Logistic Regression | ~0.97 | ~0.70 | ~0.90 | ~0.07 |
| Random Forest | ~0.99 | ~0.87 | ~0.84 | ~0.88 |

> Exact numbers will vary slightly due to random seeds. Random Forest significantly outperforms on PR-AUC, which matters most in imbalanced fraud data.

### Why accuracy is the wrong metric here
A model predicting *every transaction as legitimate* achieves **99.83% accuracy**, and catches **zero fraud**. This project uses Precision, Recall, and AUC-PR instead, which actually reflect model usefulness in a fraud context.

---

## ⚖️ Threshold Tuning

One of the most important (and often overlooked) aspects of fraud model deployment is **decision threshold tuning**.

By default, models flag a transaction as fraud when probability > 0.5. But in payments:

- Lowering the threshold → **catch more fraud**, but more false alarms (unnecessary blocks)
- Raising the threshold → **fewer false alarms**, but miss more fraud

This project includes a full threshold analysis showing the Precision/Recall/F1 trade-off curve, so the right threshold can be chosen based on business priorities — for example, whether the cost of a missed fraud case outweighs the cost of a blocked legitimate transaction.

---

## 📁 Project Structure

```
fraud-detection/
│
├── fraud_detection.ipynb   # Main analysis notebook
├── README.md               # This file
└── creditcard.csv          # Dataset (download separately from Kaggle)
```

---

## 🔮 Potential Next Steps

- [ ] Try **XGBoost or LightGBM** — typically best-in-class for tabular fraud data
- [ ] Implement **SMOTE** (synthetic oversampling) as an alternative to undersampling
- [ ] Add **SHAP values** for model explainability, essential in regulated financial environments
- [ ] Build a **Streamlit dashboard** to explore predictions interactively
- [ ] Wrap the model in a **FastAPI endpoint** to simulate real-time transaction scoring

---

## 👤 Author

**Nick Zwart**  
Fraud Data Analyst | ABN AMRO Bank  
[LinkedIn](https://www.linkedin.com/in/nick-zwart/) · [GitHub](https://github.com/your-username)

---

## 📄 License

This project is for educational and portfolio purposes. The dataset is provided by the [Machine Learning Group at ULB](https://mlg.ulb.ac.be/wordpress/) and is publicly available on Kaggle.
