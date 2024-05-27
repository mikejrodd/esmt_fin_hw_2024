import streamlit as st
import numpy as np
import numpy_financial as npf

# Constants
initial_investment = 9.8
cost_of_capital = 0.078
cash_flow_A = 2.01
cash_flow_B_initial = 1.47
growth_rate_B = 0.026

st.title('FIN 27 May Problem 2')

# Section a: Payback Period and Discounted Payback Period
st.header('a. Payback Period and Discounted Payback Period')

# Payback Period for Investment A
payback_period_A = initial_investment / cash_flow_A
st.subheader('Investment A:')
st.write(f'Payback Period: {payback_period_A:.2f} years')
st.write("Investment A recovers its initial investment in approximately 4.88 years.")

# Payback Period for Investment B
year = 0
cumulative_cash_flow_B = 0
while cumulative_cash_flow_B < initial_investment:
    year += 1
    cumulative_cash_flow_B += cash_flow_B_initial * (1 + growth_rate_B) ** (year - 1)
payback_period_B = year
st.subheader('Investment B:')
st.write(f'Payback Period: {payback_period_B:.2f} years')
st.write("Investment B recovers its initial investment in approximately 7 years.")

# Discounted Payback Period for Investment A
year = 0
cumulative_discounted_cash_flow_A = 0
while cumulative_discounted_cash_flow_A < initial_investment:
    year += 1
    cumulative_discounted_cash_flow_A += cash_flow_A / (1 + cost_of_capital) ** year
discounted_payback_period_A = year
st.subheader('Investment A:')
st.write(f'Discounted Payback Period: {discounted_payback_period_A:.2f} years')
st.write("Considering the time value of money, Investment A recovers its initial investment in approximately 7 years.")

# Discounted Payback Period for Investment B
year = 0
cumulative_discounted_cash_flow_B = 0
while cumulative_discounted_cash_flow_B < initial_investment:
    year += 1
    cumulative_discounted_cash_flow_B += (cash_flow_B_initial * (1 + growth_rate_B) ** (year - 1)) / (1 + cost_of_capital) ** year
discounted_payback_period_B = year
st.subheader('Investment B:')
st.write(f'Discounted Payback Period: {discounted_payback_period_B:.2f} years')
st.write("Considering the time value of money, Investment B recovers its initial investment in approximately 9 years.")

# Section b: Internal Rate of Return (IRR)
st.header('b. Internal Rate of Return (IRR)')

# IRR for Investment A
irr_A = npf.irr([-initial_investment] + [cash_flow_A] * 100)
st.subheader('Investment A:')
st.write(f'IRR: {irr_A:.2%}')
st.write("Investment A has an IRR of 20.51%, indicating a higher return rate per dollar invested.")

# IRR for Investment B
cash_flows_B = [-initial_investment] + [cash_flow_B_initial * (1 + growth_rate_B) ** (i - 1) for i in range(1, 101)]
irr_B = npf.irr(cash_flows_B)
st.subheader('Investment B:')
st.write(f'IRR: {irr_B:.2%}')
st.write("Investment B has an IRR of 17.60%, indicating a lower return rate per dollar invested compared to Investment A.")

# Section c: Net Present Value (NPV) at 7.8% Cost of Capital
st.header('c. Net Present Value (NPV) at 7.8% Cost of Capital')

# NPV for Investment A
npv_A = (cash_flow_A / cost_of_capital) - initial_investment
st.subheader('Investment A:')
st.write(f'NPV: ${npv_A:.2f} million')
st.write("At a cost of capital of 7.8%, Investment A creates a net value of $15.97 million.")

# NPV for Investment B
npv_B = (cash_flow_B_initial / (cost_of_capital - growth_rate_B)) - initial_investment
st.subheader('Investment B:')
st.write(f'NPV: ${npv_B:.2f} million')
st.write("At a cost of capital of 7.8%, Investment B creates a net value of $18.47 million.")

# Section d: Cost of Capital for Higher IRR to Be the Correct Choice
st.header('d. Cost of Capital for Higher IRR to Be the Correct Choice')

# Calculating the cost of capital where NPVs are equal
# NPV_A = NPV_B
# (cash_flow_A / k) - initial_investment = (cash_flow_B_initial / (k - growth_rate_B)) - initial_investment
# cash_flow_A / k = cash_flow_B_initial / (k - growth_rate_B)
# cash_flow_A * (k - growth_rate_B) = cash_flow_B_initial * k
# cash_flow_A * k - cash_flow_A * growth_rate_B = cash_flow_B_initial * k
# cash_flow_A * k - cash_flow_B_initial * k = cash_flow_A * growth_rate_B
# k * (cash_flow_A - cash_flow_B_initial) = cash_flow_A * growth_rate_B
# k = (cash_flow_A * growth_rate_B) / (cash_flow_A - cash_flow_B_initial)

# Calculating the cost of capital where NPVs are equal
k_equal = (cash_flow_A * growth_rate_B) / (cash_flow_A - cash_flow_B_initial)
st.write(f'The cost of capital at which both investments have the same NPV is: {k_equal:.2%}')
st.write("""
If the cost of capital is below approximately 9.68%, Investment B, despite its lower IRR, will have a higher NPV and be the better choice. If the cost of capital is above 9.68%, Investment A will have a higher NPV and thus be the better choice due to its higher IRR.
""")
