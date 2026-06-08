"""
============================================================
  Customer Churn Analysis — EDA & Visualization
  Author  : Vishnupriya Ganesh
  Dataset : Telco Customer Churn (7,043 records)
  Tools   : Python, Pandas, Matplotlib, Seaborn
============================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
import os

warnings.filterwarnings("ignore")

# ── Plot style ────────────────────────────────────────────
sns.set_theme(style="whitegrid", font_scale=1.05)
PALETTE   = {"Yes": "#E24B4A", "No": "#1D9E75"}
CLR_MAIN  = "#185FA5"
CLR_ACC   = "#1D9E75"
CLR_WARN  = "#E24B4A"
FIGSIZE   = (14, 6)

os.makedirs("outputs", exist_ok=True)

# ════════════════════════════════════════════════════════════
# 1. LOAD & INSPECT
# ════════════════════════════════════════════════════════════
print("=" * 60)
print("  CUSTOMER CHURN ANALYSIS — EDA REPORT")
print("=" * 60)

df = pd.read_csv("telco_churn_raw.csv")

print(f"\n📦 Raw dataset shape : {df.shape}")
print(f"   Columns           : {list(df.columns)}")
print(f"\n🔍 Missing values:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
print(f"\n📊 Data types:\n{df.dtypes}")

# ════════════════════════════════════════════════════════════
# 2. DATA CLEANING
# ════════════════════════════════════════════════════════════
print("\n" + "─" * 60)
print("  STEP 2 — DATA CLEANING")
print("─" * 60)

df_clean = df.copy()

# Fill missing TotalCharges with median
median_tc = df_clean["TotalCharges"].median()
df_clean["TotalCharges"].fillna(median_tc, inplace=True)
print(f"✅ Filled {df['TotalCharges'].isnull().sum()} missing TotalCharges with median: {median_tc:.2f}")

# Ensure correct dtypes
df_clean["TotalCharges"] = pd.to_numeric(df_clean["TotalCharges"], errors="coerce")
df_clean["SeniorCitizen"] = df_clean["SeniorCitizen"].map({0: "No", 1: "Yes"})

# Tenure groups
bins   = [0, 12, 24, 48, 72]
labels = ["0–12 months", "13–24 months", "25–48 months", "49–72 months"]
df_clean["TenureGroup"] = pd.cut(df_clean["tenure"], bins=bins, labels=labels)

# Monthly charge bins
df_clean["ChargeGroup"] = pd.cut(
    df_clean["MonthlyCharges"],
    bins=[0, 35, 65, 90, 120],
    labels=["Low (<$35)", "Medium ($35–65)", "High ($65–90)", "Premium (>$90)"]
)

print(f"✅ Created TenureGroup and ChargeGroup columns")
print(f"✅ No duplicate rows: {df_clean.duplicated().sum()}")
print(f"\n✅ Clean dataset shape : {df_clean.shape}")

# Save cleaned CSV for Power BI
df_clean.to_csv("outputs/telco_churn_cleaned.csv", index=False)
print("💾 Saved: outputs/telco_churn_cleaned.csv")

# ════════════════════════════════════════════════════════════
# 3. KEY METRICS SUMMARY
# ════════════════════════════════════════════════════════════
print("\n" + "─" * 60)
print("  STEP 3 — KEY METRICS")
print("─" * 60)

total          = len(df_clean)
churned        = (df_clean["Churn"] == "Yes").sum()
retained       = total - churned
churn_rate     = churned / total * 100
avg_tenure     = df_clean["tenure"].mean()
avg_monthly    = df_clean["MonthlyCharges"].mean()
revenue_at_risk = df_clean[df_clean["Churn"] == "Yes"]["MonthlyCharges"].sum()

print(f"\n  Total Customers      : {total:,}")
print(f"  Churned              : {churned:,}  ({churn_rate:.1f}%)")
print(f"  Retained             : {retained:,}  ({100-churn_rate:.1f}%)")
print(f"  Avg Tenure           : {avg_tenure:.1f} months")
print(f"  Avg Monthly Charges  : ${avg_monthly:.2f}")
print(f"  Monthly Revenue @ Risk : ${revenue_at_risk:,.0f}")

# ════════════════════════════════════════════════════════════
# 4. CHART 1 — Overall Churn Distribution
# ════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=FIGSIZE)
fig.suptitle("Chart 1 — Overall Churn Distribution", fontsize=14, fontweight="bold", y=1.01)

counts = df_clean["Churn"].value_counts()
colors = [PALETTE["No"], PALETTE["Yes"]]

# Pie
axes[0].pie(
    counts,
    labels=[f"Retained\n{counts['No']:,} ({100-churn_rate:.1f}%)",
            f"Churned\n{counts['Yes']:,} ({churn_rate:.1f}%)"],
    colors=colors,
    startangle=90,
    wedgeprops={"edgecolor": "white", "linewidth": 2},
    textprops={"fontsize": 11}
)
axes[0].set_title("Churn vs Retained")

# Bar
bar = axes[1].bar(["Retained", "Churned"], counts.values, color=colors, width=0.5, edgecolor="white")
for rect, val in zip(bar, counts.values):
    axes[1].text(rect.get_x() + rect.get_width()/2, rect.get_height() + 50,
                 f"{val:,}", ha="center", va="bottom", fontweight="bold", fontsize=12)
axes[1].set_ylabel("Number of Customers")
axes[1].set_title("Customer Count by Churn Status")
axes[1].set_ylim(0, counts.max() * 1.15)
sns.despine(ax=axes[1], left=True)

plt.tight_layout()
plt.savefig("outputs/chart1_churn_distribution.png", dpi=150, bbox_inches="tight")
plt.close()
print("\n📊 Chart 1 saved: outputs/chart1_churn_distribution.png")

# ════════════════════════════════════════════════════════════
# 5. CHART 2 — Churn by Contract Type
# ════════════════════════════════════════════════════════════
contract_churn = (
    df_clean.groupby(["Contract", "Churn"])
    .size()
    .reset_index(name="count")
)
contract_pct = df_clean.groupby("Contract")["Churn"].apply(
    lambda x: (x == "Yes").mean() * 100
).reset_index(name="churn_rate")

fig, axes = plt.subplots(1, 2, figsize=FIGSIZE)
fig.suptitle("Chart 2 — Churn by Contract Type", fontsize=14, fontweight="bold", y=1.01)

pivot = contract_churn.pivot(index="Contract", columns="Churn", values="count").fillna(0)
pivot.plot(kind="bar", ax=axes[0], color=[PALETTE["No"], PALETTE["Yes"]],
           edgecolor="white", width=0.6)
axes[0].set_title("Customer Count by Contract & Churn")
axes[0].set_xlabel("")
axes[0].set_ylabel("Count")
axes[0].legend(title="Churn", labels=["No", "Yes"])
axes[0].tick_params(axis="x", rotation=15)
sns.despine(ax=axes[0], left=True)

colors_bar = [PALETTE["Yes"] if r > 30 else CLR_ACC for r in contract_pct["churn_rate"]]
bars = axes[1].bar(contract_pct["Contract"], contract_pct["churn_rate"],
                   color=colors_bar, width=0.5, edgecolor="white")
for rect, val in zip(bars, contract_pct["churn_rate"]):
    axes[1].text(rect.get_x() + rect.get_width()/2, rect.get_height() + 0.5,
                 f"{val:.1f}%", ha="center", va="bottom", fontweight="bold", fontsize=12)
axes[1].set_title("Churn Rate (%) by Contract Type")
axes[1].set_ylabel("Churn Rate (%)")
axes[1].set_ylim(0, contract_pct["churn_rate"].max() * 1.2)
axes[1].tick_params(axis="x", rotation=15)
sns.despine(ax=axes[1], left=True)

plt.tight_layout()
plt.savefig("outputs/chart2_contract_churn.png", dpi=150, bbox_inches="tight")
plt.close()
print("📊 Chart 2 saved: outputs/chart2_contract_churn.png")

# Print insight
mtm_rate = contract_pct[contract_pct["Contract"] == "Month-to-month"]["churn_rate"].values[0]
two_yr   = contract_pct[contract_pct["Contract"] == "Two year"]["churn_rate"].values[0]
print(f"   💡 Insight: Month-to-month churn rate {mtm_rate:.1f}% vs Two-year {two_yr:.1f}%")
print(f"   📌 Month-to-month customers churn {mtm_rate/two_yr:.1f}x more than two-year customers")

# ════════════════════════════════════════════════════════════
# 6. CHART 3 — Churn by Tenure Group
# ════════════════════════════════════════════════════════════
tenure_churn = df_clean.groupby("TenureGroup")["Churn"].apply(
    lambda x: (x == "Yes").mean() * 100
).reset_index(name="churn_rate")

fig, axes = plt.subplots(1, 2, figsize=FIGSIZE)
fig.suptitle("Chart 3 — Churn by Customer Tenure", fontsize=14, fontweight="bold", y=1.01)

colors_t = [PALETTE["Yes"] if r > 25 else CLR_ACC for r in tenure_churn["churn_rate"]]
bars = axes[0].bar(tenure_churn["TenureGroup"].astype(str),
                   tenure_churn["churn_rate"], color=colors_t, width=0.55, edgecolor="white")
for rect, val in zip(bars, tenure_churn["churn_rate"]):
    axes[0].text(rect.get_x() + rect.get_width()/2, rect.get_height() + 0.5,
                 f"{val:.1f}%", ha="center", va="bottom", fontweight="bold")
axes[0].set_title("Churn Rate by Tenure Group")
axes[0].set_ylabel("Churn Rate (%)")
axes[0].set_xlabel("Tenure Group")
axes[0].tick_params(axis="x", rotation=15)
sns.despine(ax=axes[0], left=True)

# Tenure distribution for churned vs retained
sns.histplot(data=df_clean, x="tenure", hue="Churn",
             palette=PALETTE, bins=30, ax=axes[1], alpha=0.75, multiple="layer")
axes[1].set_title("Tenure Distribution — Churned vs Retained")
axes[1].set_xlabel("Tenure (months)")
axes[1].set_ylabel("Count")
sns.despine(ax=axes[1], left=True)

plt.tight_layout()
plt.savefig("outputs/chart3_tenure_churn.png", dpi=150, bbox_inches="tight")
plt.close()
print("📊 Chart 3 saved: outputs/chart3_tenure_churn.png")

early_churn = tenure_churn[tenure_churn["TenureGroup"] == "0–12 months"]["churn_rate"].values[0]
print(f"   💡 Insight: Customers in first 12 months churn at {early_churn:.1f}%")

# ════════════════════════════════════════════════════════════
# 7. CHART 4 — Monthly Charges vs Churn
# ════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=FIGSIZE)
fig.suptitle("Chart 4 — Monthly Charges vs Churn", fontsize=14, fontweight="bold", y=1.01)

sns.boxplot(data=df_clean, x="Churn", y="MonthlyCharges",
            palette=PALETTE, ax=axes[0], width=0.5, linewidth=1.5)
axes[0].set_title("Monthly Charges Distribution by Churn")
axes[0].set_xlabel("Churn")
axes[0].set_ylabel("Monthly Charges ($)")
sns.despine(ax=axes[0], left=True)

charge_churn = df_clean.groupby("ChargeGroup")["Churn"].apply(
    lambda x: (x == "Yes").mean() * 100
).reset_index(name="churn_rate")

colors_c = [PALETTE["Yes"] if r > 35 else CLR_ACC for r in charge_churn["churn_rate"]]
bars = axes[1].bar(charge_churn["ChargeGroup"].astype(str),
                   charge_churn["churn_rate"], color=colors_c, width=0.55, edgecolor="white")
for rect, val in zip(bars, charge_churn["churn_rate"]):
    axes[1].text(rect.get_x() + rect.get_width()/2, rect.get_height() + 0.5,
                 f"{val:.1f}%", ha="center", va="bottom", fontweight="bold")
axes[1].set_title("Churn Rate by Monthly Charge Group")
axes[1].set_ylabel("Churn Rate (%)")
axes[1].set_xlabel("Charge Group")
axes[1].tick_params(axis="x", rotation=15)
sns.despine(ax=axes[1], left=True)

plt.tight_layout()
plt.savefig("outputs/chart4_charges_churn.png", dpi=150, bbox_inches="tight")
plt.close()
print("📊 Chart 4 saved: outputs/chart4_charges_churn.png")

avg_churned  = df_clean[df_clean["Churn"] == "Yes"]["MonthlyCharges"].mean()
avg_retained = df_clean[df_clean["Churn"] == "No"]["MonthlyCharges"].mean()
print(f"   💡 Insight: Churned avg charge ${avg_churned:.2f} vs Retained ${avg_retained:.2f}")

# ════════════════════════════════════════════════════════════
# 8. CHART 5 — Internet Service & Tech Support vs Churn
# ════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=FIGSIZE)
fig.suptitle("Chart 5 — Internet Service & Tech Support vs Churn", fontsize=14, fontweight="bold", y=1.01)

internet_churn = df_clean.groupby("InternetService")["Churn"].apply(
    lambda x: (x == "Yes").mean() * 100
).reset_index(name="churn_rate")

colors_i = [PALETTE["Yes"] if r > 30 else CLR_ACC for r in internet_churn["churn_rate"]]
bars = axes[0].bar(internet_churn["InternetService"], internet_churn["churn_rate"],
                   color=colors_i, width=0.5, edgecolor="white")
for rect, val in zip(bars, internet_churn["churn_rate"]):
    axes[0].text(rect.get_x() + rect.get_width()/2, rect.get_height() + 0.5,
                 f"{val:.1f}%", ha="center", va="bottom", fontweight="bold")
axes[0].set_title("Churn Rate by Internet Service Type")
axes[0].set_ylabel("Churn Rate (%)")
axes[0].set_xlabel("Internet Service")
sns.despine(ax=axes[0], left=True)

tech_churn = df_clean[df_clean["InternetService"] != "No"].groupby("TechSupport")["Churn"].apply(
    lambda x: (x == "Yes").mean() * 100
).reset_index(name="churn_rate")
tech_churn = tech_churn[tech_churn["TechSupport"] != "No internet service"]

colors_ts = [PALETTE["Yes"] if r > 35 else CLR_ACC for r in tech_churn["churn_rate"]]
bars = axes[1].bar(tech_churn["TechSupport"], tech_churn["churn_rate"],
                   color=colors_ts, width=0.4, edgecolor="white")
for rect, val in zip(bars, tech_churn["churn_rate"]):
    axes[1].text(rect.get_x() + rect.get_width()/2, rect.get_height() + 0.5,
                 f"{val:.1f}%", ha="center", va="bottom", fontweight="bold")
axes[1].set_title("Churn Rate by Tech Support (Internet Users Only)")
axes[1].set_ylabel("Churn Rate (%)")
axes[1].set_xlabel("Tech Support")
sns.despine(ax=axes[1], left=True)

plt.tight_layout()
plt.savefig("outputs/chart5_internet_techsupport.png", dpi=150, bbox_inches="tight")
plt.close()
print("📊 Chart 5 saved: outputs/chart5_internet_techsupport.png")

# ════════════════════════════════════════════════════════════
# 9. CHART 6 — Payment Method vs Churn
# ════════════════════════════════════════════════════════════
pay_churn = df_clean.groupby("PaymentMethod")["Churn"].apply(
    lambda x: (x == "Yes").mean() * 100
).reset_index(name="churn_rate").sort_values("churn_rate", ascending=True)

fig, ax = plt.subplots(figsize=(10, 5))
fig.suptitle("Chart 6 — Churn Rate by Payment Method", fontsize=14, fontweight="bold")

colors_p = [PALETTE["Yes"] if r > 30 else CLR_ACC for r in pay_churn["churn_rate"]]
bars = ax.barh(pay_churn["PaymentMethod"], pay_churn["churn_rate"],
               color=colors_p, height=0.5, edgecolor="white")
for rect, val in zip(bars, pay_churn["churn_rate"]):
    ax.text(rect.get_width() + 0.5, rect.get_y() + rect.get_height()/2,
            f"{val:.1f}%", va="center", fontweight="bold")
ax.set_xlabel("Churn Rate (%)")
ax.set_xlim(0, pay_churn["churn_rate"].max() * 1.2)
sns.despine(ax=ax, left=True, bottom=True)

plt.tight_layout()
plt.savefig("outputs/chart6_payment_churn.png", dpi=150, bbox_inches="tight")
plt.close()
print("📊 Chart 6 saved: outputs/chart6_payment_churn.png")

# ════════════════════════════════════════════════════════════
# 10. CHART 7 — Correlation Heatmap (numeric features)
# ════════════════════════════════════════════════════════════
df_num = df_clean.copy()
df_num["Churn_bin"]        = (df_num["Churn"] == "Yes").astype(int)
df_num["Senior_bin"]       = (df_num["SeniorCitizen"] == "Yes").astype(int)
df_num["Contract_bin"]     = df_num["Contract"].map(
    {"Month-to-month": 0, "One year": 1, "Two year": 2})
df_num["Internet_bin"]     = df_num["InternetService"].map(
    {"No": 0, "DSL": 1, "Fiber optic": 2})
df_num["TechSupport_bin"]  = df_num["TechSupport"].map(
    {"No": 0, "Yes": 1, "No internet service": 0})
df_num["Paperless_bin"]    = (df_num["PaperlessBilling"] == "Yes").astype(int)

corr_cols = ["tenure", "MonthlyCharges", "TotalCharges", "Senior_bin",
             "Contract_bin", "Internet_bin", "TechSupport_bin",
             "Paperless_bin", "Churn_bin"]

corr_matrix = df_num[corr_cols].corr()

fig, ax = plt.subplots(figsize=(10, 8))
fig.suptitle("Chart 7 — Correlation Heatmap (Churn Drivers)", fontsize=14, fontweight="bold")

mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt=".2f",
            cmap="RdYlGn", center=0, vmin=-1, vmax=1,
            square=True, linewidths=0.5,
            annot_kws={"size": 10}, ax=ax)
ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right", fontsize=10)
ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=10)

plt.tight_layout()
plt.savefig("outputs/chart7_correlation_heatmap.png", dpi=150, bbox_inches="tight")
plt.close()
print("📊 Chart 7 saved: outputs/chart7_correlation_heatmap.png")

# ════════════════════════════════════════════════════════════
# 11. SUMMARY DASHBOARD (combined)
# ════════════════════════════════════════════════════════════
fig = plt.figure(figsize=(18, 14))
fig.suptitle(
    "Customer Churn Analysis — Executive Summary Dashboard\nTelco Dataset | 7,043 Customers | Vishnupriya Ganesh",
    fontsize=15, fontweight="bold", y=0.98
)

# ── KPI boxes ─────────────────────────────────────────────
kpis = [
    ("Total Customers", f"{total:,}", CLR_MAIN),
    ("Churn Rate",       f"{churn_rate:.1f}%", CLR_WARN),
    ("Monthly Revenue\nAt Risk", f"${revenue_at_risk:,.0f}", CLR_WARN),
    ("Avg Tenure",       f"{avg_tenure:.0f} months", CLR_ACC),
    ("Avg Monthly\nCharges", f"${avg_monthly:.2f}", CLR_MAIN),
]

for i, (label, value, color) in enumerate(kpis):
    ax_kpi = fig.add_axes([0.02 + i*0.195, 0.87, 0.175, 0.08])
    ax_kpi.set_facecolor("#F8F9FA")
    ax_kpi.set_xlim(0, 1); ax_kpi.set_ylim(0, 1)
    ax_kpi.axis("off")
    ax_kpi.text(0.5, 0.72, value, ha="center", va="center",
                fontsize=16, fontweight="bold", color=color,
                transform=ax_kpi.transAxes)
    ax_kpi.text(0.5, 0.22, label, ha="center", va="center",
                fontsize=9, color="#555555",
                transform=ax_kpi.transAxes)
    for spine in ["top","bottom","left","right"]:
        ax_kpi.spines[spine].set_visible(True)
        ax_kpi.spines[spine].set_color("#DDDDDD")

# Row 1
ax1 = fig.add_subplot(3, 3, 4)
counts_dash = df_clean["Churn"].value_counts()
ax1.pie(counts_dash, labels=["Retained", "Churned"], colors=[CLR_ACC, CLR_WARN],
        autopct="%1.1f%%", startangle=90,
        wedgeprops={"edgecolor": "white", "linewidth": 2}, textprops={"fontsize": 9})
ax1.set_title("Churn Distribution", fontsize=11, fontweight="bold")

ax2 = fig.add_subplot(3, 3, 5)
mtm_data = contract_pct.copy()
cols = [CLR_WARN if r > 30 else CLR_ACC for r in mtm_data["churn_rate"]]
bars2 = ax2.bar(mtm_data["Contract"], mtm_data["churn_rate"], color=cols, width=0.5, edgecolor="white")
for b, v in zip(bars2, mtm_data["churn_rate"]):
    ax2.text(b.get_x()+b.get_width()/2, b.get_height()+0.5, f"{v:.1f}%",
             ha="center", fontsize=9, fontweight="bold")
ax2.set_title("Churn Rate by Contract", fontsize=11, fontweight="bold")
ax2.set_ylabel("Churn Rate (%)")
ax2.tick_params(axis="x", rotation=12, labelsize=8)
sns.despine(ax=ax2, left=True)

ax3 = fig.add_subplot(3, 3, 6)
t_data = tenure_churn.copy()
cols3 = [CLR_WARN if r > 35 else CLR_ACC for r in t_data["churn_rate"]]
bars3 = ax3.bar(t_data["TenureGroup"].astype(str), t_data["churn_rate"],
                color=cols3, width=0.55, edgecolor="white")
for b, v in zip(bars3, t_data["churn_rate"]):
    ax3.text(b.get_x()+b.get_width()/2, b.get_height()+0.5, f"{v:.1f}%",
             ha="center", fontsize=9, fontweight="bold")
ax3.set_title("Churn Rate by Tenure Group", fontsize=11, fontweight="bold")
ax3.set_ylabel("Churn Rate (%)")
ax3.tick_params(axis="x", rotation=12, labelsize=8)
sns.despine(ax=ax3, left=True)

# Row 2
ax4 = fig.add_subplot(3, 3, 7)
sns.boxplot(data=df_clean, x="Churn", y="MonthlyCharges",
            palette=PALETTE, ax=ax4, width=0.4, linewidth=1.2)
ax4.set_title("Monthly Charges vs Churn", fontsize=11, fontweight="bold")
ax4.set_xlabel("Churn"); ax4.set_ylabel("Monthly Charges ($)")
sns.despine(ax=ax4, left=True)

ax5 = fig.add_subplot(3, 3, 8)
cols5 = [CLR_WARN if r > 30 else CLR_ACC for r in internet_churn["churn_rate"]]
bars5 = ax5.bar(internet_churn["InternetService"], internet_churn["churn_rate"],
                color=cols5, width=0.45, edgecolor="white")
for b, v in zip(bars5, internet_churn["churn_rate"]):
    ax5.text(b.get_x()+b.get_width()/2, b.get_height()+0.5, f"{v:.1f}%",
             ha="center", fontsize=9, fontweight="bold")
ax5.set_title("Churn by Internet Service", fontsize=11, fontweight="bold")
ax5.set_ylabel("Churn Rate (%)")
sns.despine(ax=ax5, left=True)

ax6 = fig.add_subplot(3, 3, 9)
p_sorted = pay_churn.sort_values("churn_rate")
cols6 = [CLR_WARN if r > 30 else CLR_ACC for r in p_sorted["churn_rate"]]
ax6.barh(p_sorted["PaymentMethod"], p_sorted["churn_rate"],
         color=cols6, height=0.45, edgecolor="white")
for i, (v, label) in enumerate(zip(p_sorted["churn_rate"], p_sorted["PaymentMethod"])):
    ax6.text(v + 0.3, i, f"{v:.1f}%", va="center", fontsize=9, fontweight="bold")
ax6.set_title("Churn by Payment Method", fontsize=11, fontweight="bold")
ax6.set_xlabel("Churn Rate (%)")
ax6.tick_params(axis="y", labelsize=8)
sns.despine(ax=ax6, left=True, bottom=True)

plt.subplots_adjust(hspace=0.45, wspace=0.35)
plt.savefig("outputs/dashboard_executive_summary.png", dpi=150, bbox_inches="tight")
plt.close()
print("\n📊 Executive Dashboard saved: outputs/dashboard_executive_summary.png")

# ════════════════════════════════════════════════════════════
# 12. FINAL SUMMARY REPORT
# ════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("  FINAL FINDINGS SUMMARY")
print("=" * 60)

mtm_rate_val  = contract_pct[contract_pct["Contract"] == "Month-to-month"]["churn_rate"].values[0]
two_yr_val    = contract_pct[contract_pct["Contract"] == "Two year"]["churn_rate"].values[0]
early_val     = tenure_churn[tenure_churn["TenureGroup"] == "0–12 months"]["churn_rate"].values[0]
fiber_val     = internet_churn[internet_churn["InternetService"] == "Fiber optic"]["churn_rate"].values[0]
echeque_val   = pay_churn[pay_churn["PaymentMethod"] == "Electronic check"]["churn_rate"].values[0]

print(f"""
  📌 Finding 1 — Contract Type is #1 Churn Driver
     Month-to-month: {mtm_rate_val:.1f}% churn  |  Two-year: {two_yr_val:.1f}% churn
     → {mtm_rate_val/two_yr_val:.1f}x higher churn for month-to-month customers

  📌 Finding 2 — Early Tenure = Highest Risk
     Customers in first 12 months churn at {early_val:.1f}%
     → Onboarding & early engagement programs are critical

  📌 Finding 3 — Fiber Optic Customers Churn Most
     Fiber optic churn rate: {fiber_val:.1f}%
     → Suggests service quality/pricing concerns with premium tier

  📌 Finding 4 — Monthly Revenue At Risk: ${revenue_at_risk:,.0f}
     {churned:,} churned customers × avg ${avg_churned:.2f}/month

  📌 Finding 5 — Electronic Check = Highest Churn Payment
     Electronic check churn rate: {echeque_val:.1f}%
     → Auto-pay enrollment could significantly reduce churn

  ✅ BUSINESS RECOMMENDATIONS:
     1. Offer discounts to convert month-to-month → annual contracts
     2. Launch 90-day onboarding program for new customers
     3. Review Fiber optic pricing & SLA to improve satisfaction
     4. Incentivize auto-pay enrollment (bank transfer / credit card)
     5. Proactive outreach to high-monthly-charge customers at risk
""")

print("=" * 60)
print("  All outputs saved to: outputs/")
print("  Files: 7 charts + 1 dashboard + 1 cleaned CSV")
print("=" * 60)
