-- ============================================================
--  Customer Churn Analysis — SQL Queries
--  Author  : Vishnupriya Ganesh
--  Dataset : telco_churn_cleaned
--  Tool    : MySQL / SQL Oracle
-- ============================================================

-- ─────────────────────────────────────────────────────────
-- Q1. Overall Churn Rate
-- ─────────────────────────────────────────────────────────
SELECT
    Churn,
    COUNT(*)                                          AS customer_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS churn_pct
FROM telco_churn_cleaned
GROUP BY Churn;


-- ─────────────────────────────────────────────────────────
-- Q2. Monthly Revenue at Risk
-- ─────────────────────────────────────────────────────────
SELECT
    ROUND(SUM(MonthlyCharges), 2) AS monthly_revenue_at_risk
FROM telco_churn_cleaned
WHERE Churn = 'Yes';


-- ─────────────────────────────────────────────────────────
-- Q3. Churn Rate by Contract Type
-- ─────────────────────────────────────────────────────────
SELECT
    Contract,
    COUNT(*)                                            AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)     AS churned,
    ROUND(
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2
    )                                                   AS churn_rate_pct
FROM telco_churn_cleaned
GROUP BY Contract
ORDER BY churn_rate_pct DESC;


-- ─────────────────────────────────────────────────────────
-- Q4. Churn Rate by Tenure Group
-- ─────────────────────────────────────────────────────────
SELECT
    CASE
        WHEN tenure BETWEEN 1  AND 12 THEN '0–12 months'
        WHEN tenure BETWEEN 13 AND 24 THEN '13–24 months'
        WHEN tenure BETWEEN 25 AND 48 THEN '25–48 months'
        ELSE '49–72 months'
    END                                                  AS tenure_group,
    COUNT(*)                                             AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)      AS churned,
    ROUND(
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2
    )                                                    AS churn_rate_pct
FROM telco_churn_cleaned
GROUP BY tenure_group
ORDER BY MIN(tenure);


-- ─────────────────────────────────────────────────────────
-- Q5. Churn Rate by Internet Service
-- ─────────────────────────────────────────────────────────
SELECT
    InternetService,
    COUNT(*)                                             AS total,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)      AS churned,
    ROUND(
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2
    )                                                    AS churn_rate_pct
FROM telco_churn_cleaned
GROUP BY InternetService
ORDER BY churn_rate_pct DESC;


-- ─────────────────────────────────────────────────────────
-- Q6. Churn Rate by Payment Method
-- ─────────────────────────────────────────────────────────
SELECT
    PaymentMethod,
    COUNT(*)                                             AS total,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)      AS churned,
    ROUND(
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2
    )                                                    AS churn_rate_pct,
    ROUND(AVG(MonthlyCharges), 2)                        AS avg_monthly_charge
FROM telco_churn_cleaned
GROUP BY PaymentMethod
ORDER BY churn_rate_pct DESC;


-- ─────────────────────────────────────────────────────────
-- Q7. Average Monthly Charges — Churned vs Retained
-- ─────────────────────────────────────────────────────────
SELECT
    Churn,
    ROUND(AVG(MonthlyCharges), 2)  AS avg_monthly_charge,
    ROUND(AVG(TotalCharges), 2)    AS avg_total_charge,
    ROUND(AVG(tenure), 1)          AS avg_tenure_months
FROM telco_churn_cleaned
GROUP BY Churn;


-- ─────────────────────────────────────────────────────────
-- Q8. High-Risk Customer Segment
--     (Month-to-month + Fiber optic + Electronic check
--      + tenure < 12 months)
-- ─────────────────────────────────────────────────────────
SELECT
    customerID,
    tenure,
    Contract,
    InternetService,
    PaymentMethod,
    MonthlyCharges,
    Churn
FROM telco_churn_cleaned
WHERE Contract       = 'Month-to-month'
  AND InternetService = 'Fiber optic'
  AND PaymentMethod   = 'Electronic check'
  AND tenure         <= 12
ORDER BY MonthlyCharges DESC;


-- ─────────────────────────────────────────────────────────
-- Q9. Tech Support Impact on Churn (Internet Users Only)
-- ─────────────────────────────────────────────────────────
SELECT
    TechSupport,
    COUNT(*)                                              AS total,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)       AS churned,
    ROUND(
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2
    )                                                     AS churn_rate_pct
FROM telco_churn_cleaned
WHERE InternetService != 'No'
  AND TechSupport     != 'No internet service'
GROUP BY TechSupport
ORDER BY churn_rate_pct DESC;


-- ─────────────────────────────────────────────────────────
-- Q10. Senior Citizen Churn Analysis
-- ─────────────────────────────────────────────────────────
SELECT
    SeniorCitizen,
    COUNT(*)                                              AS total,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)       AS churned,
    ROUND(
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2
    )                                                     AS churn_rate_pct,
    ROUND(AVG(MonthlyCharges), 2)                         AS avg_monthly_charge
FROM telco_churn_cleaned
GROUP BY SeniorCitizen;


-- ─────────────────────────────────────────────────────────
-- Q11. Monthly Revenue by Customer Segment (for Power BI)
-- ─────────────────────────────────────────────────────────
SELECT
    Contract,
    InternetService,
    Churn,
    COUNT(*)                          AS customer_count,
    ROUND(SUM(MonthlyCharges), 2)     AS total_monthly_revenue,
    ROUND(AVG(MonthlyCharges), 2)     AS avg_monthly_charge
FROM telco_churn_cleaned
GROUP BY Contract, InternetService, Churn
ORDER BY total_monthly_revenue DESC;


-- ─────────────────────────────────────────────────────────
-- Q12. Churn by Gender
-- ─────────────────────────────────────────────────────────
SELECT
    gender,
    COUNT(*)                                              AS total,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)       AS churned,
    ROUND(
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2
    )                                                     AS churn_rate_pct
FROM telco_churn_cleaned
GROUP BY gender;
