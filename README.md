# 📉 Customer Churn Analysis — Telco Dataset

> **End-to-end data analytics project** | Python · SQL · Power BI  
> **Author:** Vishnupriya Ganesh | Senior Data Analyst  
> **Dataset:** Telco Customer Churn (7,043 records, 17 features)

---

## 📌 Business Problem

A telecom company is losing customers at an alarming rate.  
**The goal:** Identify *who* is churning, *why* they churn, and *what actions* the business can take to reduce churn and protect monthly revenue.

---

## 🎯 Project Objectives

1. Understand the overall churn rate and revenue impact
2. Identify top drivers of customer churn
3. Segment customers by risk level
4. Deliver 5 actionable business recommendations
5. Build a Power BI dashboard for ongoing monitoring

---

## 🗂️ Project Structure

```
customer-churn-analysis/
│
├── data/
│   ├── telco_churn_raw.csv          # Original raw dataset
│   └── telco_churn_cleaned.csv      # Cleaned dataset (output of EDA)
│
├── outputs/
│   ├── chart1_churn_distribution.png
│   ├── chart2_contract_churn.png
│   ├── chart3_tenure_churn.png
│   ├── chart4_charges_churn.png
│   ├── chart5_internet_techsupport.png
│   ├── chart6_payment_churn.png
│   ├── chart7_correlation_heatmap.png
│   └── dashboard_executive_summary.png
│
├── churn_analysis.py                # Main EDA + visualization script
├── churn_queries.sql                # SQL analysis queries
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

---

## 🛠️ Tools & Technologies

| Tool | Purpose |
|------|---------|
| **Python 3.x** | EDA, data cleaning, visualization |
| **Pandas** | Data manipulation and transformation |
| **Matplotlib / Seaborn** | Charts and visualizations |
| **SQL (MySQL)** | Data querying and segmentation |
| **Power BI** | Interactive dashboard and business reporting |
| **Claude AI** | Accelerated insight generation via AI prompts |

---

## 📊 Dataset Overview

| Column | Description |
|--------|-------------|
| `customerID` | Unique customer identifier |
| `tenure` | Months as a customer |
| `Contract` | Month-to-month / One year / Two year |
| `InternetService` | DSL / Fiber optic / No |
| `MonthlyCharges` | Monthly bill amount ($) |
| `TotalCharges` | Total amount charged |
| `PaymentMethod` | How the customer pays |
| `TechSupport` | Whether tech support is subscribed |
| `Churn` | **Target variable** — Yes / No |

---

## 🔍 Data Cleaning Steps

```python
# Step 1: Handle missing values
df['TotalCharges'].fillna(df['TotalCharges'].median(), inplace=True)

# Step 2: Fix data types
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df['SeniorCitizen'] = df['SeniorCitizen'].map({0: 'No', 1: 'Yes'})

# Step 3: Create new features
df['TenureGroup'] = pd.cut(df['tenure'],
    bins=[0, 12, 24, 48, 72],
    labels=['0–12 months', '13–24 months', '25–48 months', '49–72 months'])

df['ChargeGroup'] = pd.cut(df['MonthlyCharges'],
    bins=[0, 35, 65, 90, 120],
    labels=['Low (<$35)', 'Medium ($35–65)', 'High ($65–90)', 'Premium (>$90)'])
```

---

## 📈 Key Findings

### 🔴 Finding 1 — Overall Churn Rate: 43%
- **3,032** out of 7,043 customers have churned
- Monthly revenue at risk: **$205,656**

### 🔴 Finding 2 — Contract Type is the #1 Driver
| Contract | Churn Rate |
|----------|-----------|
| Month-to-month | **55.3%** |
| One year | 38.4% |
| Two year | 29.0% |

> Month-to-month customers churn at **1.9x the rate** of two-year contract customers.

### 🔴 Finding 3 — New Customers Are Highest Risk
- Customers in first **12 months** churn at **49.2%**
- Churn drops significantly after 24 months

### 🟡 Finding 4 — Fiber Optic Drives High Churn
- Fiber optic internet churn rate: **49.9%**
- DSL churn rate: **38.5%** — significantly lower
- No internet: lowest churn (**21.3%**)

### 🟡 Finding 5 — Electronic Check Customers Churn Most
- Electronic check payment churn: **48.2%**
- Auto-pay methods (bank transfer, credit card) churn much less

### 🟢 Finding 6 — Churned Customers Pay More
- Churned avg monthly charge: **$67.83**
- Retained avg monthly charge: **$62.81**
- High-paying customers leaving = highest revenue loss

---

## 💡 Business Recommendations

| # | Recommendation | Expected Impact |
|---|---------------|----------------|
| 1 | Offer 15–20% discount to convert month-to-month → annual plans | Reduce churn rate by ~15% |
| 2 | Launch structured 90-day onboarding program for new customers | Reduce early churn by ~20% |
| 3 | Audit Fiber optic pricing & service quality (SLA review) | Reduce Fiber churn by ~10% |
| 4 | Incentivize auto-pay enrollment (waive setup fee or offer discount) | Reduce payment-linked churn |
| 5 | Proactive outreach to high-charge customers (>$80/month) at risk | Protect premium revenue segment |

---

## 🚀 How to Run This Project

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/customer-churn-analysis.git
cd customer-churn-analysis
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the EDA Script
```bash
python churn_analysis.py
```

### 4. View Outputs
All charts are saved in the `outputs/` folder.  
Open `telco_churn_cleaned.csv` in Power BI for the interactive dashboard.

---

## 📦 Requirements

```
pandas>=1.5.0
numpy>=1.23.0
matplotlib>=3.6.0
seaborn>=0.12.0
scikit-learn>=1.1.0
```

---

## 🔗 Power BI Dashboard

The interactive Power BI dashboard includes:
- Churn KPI summary cards (total churn %, revenue at risk)
- Churn breakdown by contract type, tenure, internet service
- Customer segment risk matrix
- Monthly trend analysis
- Drill-through filters by gender, senior status, payment method

> 📂 File: `Customer_Churn_Dashboard.pbix` *(available in repository)*

---

## 📝 Project Highlights for Resume

- Analyzed **7,000+ customer records** using Python (Pandas) and SQL to identify churn patterns
- Identified month-to-month contract customers churn at **1.9x the rate** of annual subscribers
- Built interactive Power BI dashboard tracking churn rate, revenue at risk, and customer segments
- Leveraged **AI prompts (Claude)** to accelerate data exploration, reducing analysis time by ~40%
- Delivered **5 actionable retention strategies** with projected business impact

---

## 👩‍💻 Author

**Vishnupriya Ganesh** — Senior Data Analyst  
📧 vinujai2277@gmail.com  

