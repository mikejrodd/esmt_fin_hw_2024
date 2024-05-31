import streamlit as st
import numpy as np
import pandas as pd
from numpy_financial import npv, irr

# Constants
price_new = 700
variable_cost_new = 320
price_high = 1100
variable_cost_high = 600
price_cheap = 400
variable_cost_cheap = 180
fixed_costs = 7500000
plant_cost = 18200000
depreciation_rate = 0.2
working_capital = 950000
tax_rate = 0.28
cost_of_capital = 0.14
years = 7
r_and_d_cost = 1000000
marketing_study_cost = 150000

# Base case values
sales_new = 55000
sales_high = 13000
sales_cheap = 10000

revenue_new = sales_new * price_new
revenue_high = sales_high * price_high
revenue_cheap = sales_cheap * price_cheap

variable_costs_new = sales_new * variable_cost_new
variable_costs_high = sales_high * variable_cost_high
variable_costs_cheap = sales_cheap * variable_cost_cheap

total_revenue = revenue_new + revenue_cheap - revenue_high
total_variable_costs = variable_costs_new + variable_costs_cheap - variable_costs_high
total_costs = total_variable_costs + fixed_costs

cash_flows = []
depreciation = plant_cost * depreciation_rate
plant_value = plant_cost

for year in range(1, years + 1):
    taxable_income = total_revenue - total_costs - depreciation
    taxes = taxable_income * tax_rate
    after_tax_cash_flow = (total_revenue - total_costs - taxes) + depreciation
    cash_flows.append(after_tax_cash_flow)
    plant_value -= depreciation
    depreciation = plant_value * depreciation_rate

cash_flows[-1] += working_capital  # Returning working capital in the last year

initial_investment = r_and_d_cost + marketing_study_cost + plant_cost + working_capital

base_case_npv = npv(cost_of_capital, [-initial_investment] + cash_flows)
base_case_irr = irr([-initial_investment] + cash_flows)
cumulative_cash_flows = np.cumsum([-initial_investment] + cash_flows)
payback_period = np.where(cumulative_cash_flows >= 0)[0][0] + 1

# Monte Carlo Simulation
iterations = 10000
np.random.seed(0)

results = []

for _ in range(iterations):
    sales_new = np.random.normal(55000, 5500)
    sales_high = np.random.normal(13000, 1300)
    sales_cheap = np.random.normal(10000, 1000)
    
    revenue_new = sales_new * price_new
    revenue_high = sales_high * price_high
    revenue_cheap = sales_cheap * price_cheap
    
    variable_costs_new = sales_new * variable_cost_new
    variable_costs_high = sales_high * variable_cost_high
    variable_costs_cheap = sales_cheap * variable_cost_cheap
    
    total_revenue = revenue_new + revenue_cheap - revenue_high
    total_variable_costs = variable_costs_new + variable_costs_cheap - variable_costs_high
    total_costs = total_variable_costs + fixed_costs
    
    cash_flows = []
    depreciation = plant_cost * depreciation_rate
    plant_value = plant_cost
    
    for year in range(1, years + 1):
        taxable_income = total_revenue - total_costs - depreciation
        taxes = taxable_income * tax_rate
        after_tax_cash_flow = (total_revenue - total_costs - taxes) + depreciation
        cash_flows.append(after_tax_cash_flow)
        plant_value -= depreciation
        depreciation = plant_value * depreciation_rate
    
    cash_flows[-1] += working_capital  # Returning working capital in the last year
    
    npv_result = npv(cost_of_capital, [-initial_investment] + cash_flows)
    irr_result = irr([-initial_investment] + cash_flows)
    cumulative_cash_flows = np.cumsum([-initial_investment] + cash_flows)
    payback_period_result = np.where(cumulative_cash_flows >= 0)[0][0] + 1
    
    results.append((npv_result, irr_result, payback_period_result))

results_df = pd.DataFrame(results, columns=['NPV', 'IRR', 'Payback Period'])

# Summarizing the results
mean_npv = results_df['NPV'].mean()
std_npv = results_df['NPV'].std()
mean_irr = results_df['IRR'].mean()
mean_payback_period = results_df['Payback Period'].mean()

best_case_npv = results_df['NPV'].max()
worst_case_npv = results_df['NPV'].min()

# Part (c): Expected NPV, Standard Deviation, and Coefficient of Variation
base_case_prob = 0.60
best_case_prob = 0.25
worst_case_prob = 0.15

expected_npv = (base_case_prob * base_case_npv) + (best_case_prob * best_case_npv) + (worst_case_prob * worst_case_npv)
standard_deviation_npv = np.sqrt(
    base_case_prob * (base_case_npv - expected_npv)**2 +
    best_case_prob * (best_case_npv - expected_npv)**2 +
    worst_case_prob * (worst_case_npv - expected_npv)**2
)
coefficient_of_variation = standard_deviation_npv / expected_npv

# Part (d): Sensitivity Analysis
# Sensitivity to the price of the new clubs
price_change = 1  # Small change in price
new_price_revenue = sales_new * (price_new + price_change)
new_total_revenue = new_price_revenue + revenue_cheap - revenue_high
new_cash_flows = []

for year in range(1, years + 1):
    taxable_income = new_total_revenue - total_costs - depreciation
    taxes = taxable_income * tax_rate
    after_tax_cash_flow = (new_total_revenue - total_costs - taxes) + depreciation
    new_cash_flows.append(after_tax_cash_flow)
    plant_value -= depreciation
    depreciation = plant_value * depreciation_rate

new_cash_flows[-1] += working_capital  # Returning working capital in the last year

# Sensitivity to the quantity of new clubs sold
quantity_change = 1  # Small change in quantity
new_quantity_revenue = (sales_new + quantity_change) * price_new
new_total_revenue = new_quantity_revenue + revenue_cheap - revenue_high
new_cash_flows = []

for year in range(1, years + 1):
    taxable_income = new_total_revenue - total_costs - depreciation
    taxes = taxable_income * tax_rate
    after_tax_cash_flow = (new_total_revenue - total_costs - taxes) + depreciation
    new_cash_flows.append(after_tax_cash_flow)
    plant_value -= depreciation
    depreciation = plant_value * depreciation_rate

new_cash_flows[-1] += working_capital  # Returning working capital in the last year

# Streamlit Display
st.title("Financial Analysis for McGilla Gold's Golf Clubs")

st.header("Part (a): Base Case Analysis")
st.markdown(f"""
**Net Present Value (NPV):** £{base_case_npv:.2f}
- NPV was calculated as the difference between the present value of cash inflows and the present value of cash outflows, discounted at the project's cost of capital.

**Internal Rate of Return (IRR):** {base_case_irr * 100:.2f}%
- IRR being the discount rate that makes the net present value of all cash flows from the project equal to zero.

**Payback Period:** {payback_period} years
- The payback period - time it takes for the investment to generate an amount of income equivalent to the cost of the investment.
""")

st.header("Part (b): Monte Carlo Simulation")
st.markdown("""
Monte Carlo simulation was used to understand the impact of uncertainty in the financial forecast. By running 10,000 simulations while varying inputs, I can get a range of outcomes for NPV, IRR, and Payback Period.

**Overview of Monte Carlo Implementation:**
- **Variables Simulated:** Sales of new clubs, sales loss of high-priced clubs, and sales gain of cheap clubs.
- **Iterations:** 10,000
- **Distributions:** Normal distributions with means equal to base case values and standard deviations equal to 10% of those values, as per the problem.
""")

st.markdown(f"""
**Monte Carlo Results Summary:**
- **Mean NPV:** £{mean_npv:.2f}
- **Standard Deviation of NPV:** £{std_npv:.2f}
- **Mean IRR:** {mean_irr * 100:.2f}%
- **Mean Payback Period:** {mean_payback_period} years
- **Best-case NPV:** £{best_case_npv:.2f}
- **Worst-case NPV:** £{worst_case_npv:.2f}
""")

# Calculate height based on number of rows and width based on number of columns
height = min(400, 35 * len(results_df))  # Adjust row height if necessary
width = min(1200, 200 * len(results_df.columns))  # Adjust column width if necessary

# Display the full results dataframe without scrolling
st.write("Monte Carlo Simulation Results Table:")
st.dataframe(results_df.describe(), height=height, width=width)

st.header("Part (c): Expected NPV, Standard Deviation, and Coefficient of Variation")
st.markdown(f"""
**Expected NPV:** £{expected_npv:.2f}
- The expected NPV was calculated as the weighted average of the base-case, best-case, and worst-case NPVs, using their respective probabilities.

**Standard Deviation of NPV:** £{standard_deviation_npv:.2f}
- The standard deviation measures the dispersion of NPVs from the expected NPV.

**Coefficient of Variation:** {coefficient_of_variation:.2f}
- The coefficient of variation being the ratio of the standard deviation to the expected NPV, showing the relative variability.
""")

st.header("Part (d): Sensitivity Analysis")
sensitivity_data = {
    "Calculation": ["Base Case", "Increased Price (£1)", "Increased Quantity (1 unit)"],
    "Revenue from new clubs": [38500000, 38555000, 38500700],
    "Total Revenue": [28200000, 28255000, 28200700],
    "Total Costs": [19100000, 19100000, 19100320],
    "Taxable Income": [5460000, 5515000, 5460380],
    "Taxes": [1528800, 1544200, 1528906.40],
    "After-tax Cash Flow": [7571200, 7610800, 7571473.60]
}

sensitivity_df = pd.DataFrame(sensitivity_data)

st.write("Sensitivity Analysis Table:")
st.dataframe(sensitivity_df.iloc[:, :4], width=800)

st.write("Sensitivity Analysis Table continued:")
st.dataframe(sensitivity_df.iloc[:, 4:], width=800)
