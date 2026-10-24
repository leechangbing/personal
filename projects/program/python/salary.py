import numpy as np
import pandas as pd

# 每档税率的上限值，最后一档使用一个极大值作为哨兵。
BRACKET_UPPER_BOUNDS = np.array(
    [36_000, 144_000, 300_000, 420_000, 660_000, 960_000, np.inf]
)
# 对应的税率与速算扣除数。
BRACKET_RATES = np.array([0.03, 0.10, 0.20, 0.25, 0.30, 0.35, 0.45])
BRACKET_QUICK_DEDUCTIONS = np.array([0, 2_520, 16_920, 31_920, 52_920, 85_920, 181_920])

BASIC_DEDUCTION = 14_500 * 12
SPECIAL_DEDUCTION = 8_000 * 12


def compute_tax_amount(taxable_income: np.ndarray) -> np.ndarray:
    """对一批应税收入做向量化个税计算。"""
    taxable_income = np.maximum(taxable_income, 0)
    bracket_idx = np.searchsorted(BRACKET_UPPER_BOUNDS, taxable_income, side="right")
    return taxable_income * BRACKET_RATES[bracket_idx] - BRACKET_QUICK_DEDUCTIONS[bracket_idx]


def build_salary_table(min_monthly_k: int = 40, max_monthly_k: int = 99) -> pd.DataFrame:
    """
    构建指定月薪区间（单位：千元）的薪资与税额表。
    结果包含年收入、应税收入、个税、税后现金等字段。
    """
    monthly_range = np.arange(min_monthly_k, max_monthly_k + 1)
    annual_income = monthly_range * 1_000 * 12
    taxable_income = annual_income - BASIC_DEDUCTION
    tax = compute_tax_amount(taxable_income)

    data = {
        "money_mouth": monthly_range,
        "org_money": annual_income,
        "pre_money": taxable_income,
        "tax": tax,
        "post_money": annual_income - tax - SPECIAL_DEDUCTION,
        "true_money": annual_income - tax,
    }
    return pd.DataFrame(data)


if __name__ == "__main__":
    salary_df = build_salary_table()
    salary_df.to_csv("money_mouth.csv", index=False)
    print(salary_df)