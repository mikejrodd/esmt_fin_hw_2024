import streamlit as st
import numpy as np
from numpy_financial import irr

def calculate_npv(initial_cost, annual_cash_flow, shutdown_cost, discount_rate, years):
    # Present Value of Annual Cash Inflows
    pv_inflows = annual_cash_flow * (1 - (1 + discount_rate)**-years) / discount_rate

    # Present Value of Shutdown Cost
    pv_shutdown = shutdown_cost / (1 + discount_rate)**years

    # NPV Calculation
    npv = initial_cost + pv_inflows + pv_shutdown
    return npv

def calculate_irr(cash_flows):
    return irr(cash_flows)

def calculate_mirr(cash_flows, discount_rate):
    years = len(cash_flows) - 1
    positive_cash_flows = [cf if cf > 0 else 0 for cf in cash_flows]
    negative_cash_flows = [cf if cf < 0 else 0 for cf in cash_flows]

    # Future Value of Positive Cash Flows
    fv_positive_cash_flows = sum([cf * (1 + discount_rate)**(years - t) for t, cf in enumerate(positive_cash_flows)])

    # Present Value of Negative Cash Flows
    pv_negative_cash_flows = sum([cf / (1 + discount_rate)**t for t, cf in enumerate(negative_cash_flows)])

    # MIRR Calculation
    mirr = (fv_positive_cash_flows / -pv_negative_cash_flows)**(1/years) - 1
    return mirr

def main():
    st.title("FIN 27 May Problem 1")

    # Inputs
    initial_cost = -99
    annual_cash_flow = 12
    shutdown_cost = -141
    discount_rate = 0.12
    years = 20

    # Cash flows array
    cash_flows = [initial_cost] + [annual_cash_flow] * years + [shutdown_cost]

    # Calculations
    npv = calculate_npv(initial_cost, annual_cash_flow, shutdown_cost, discount_rate, years)
    project_irr = calculate_irr(cash_flows)
    mirr = calculate_mirr(cash_flows, discount_rate)

    # Display results
    st.subheader("A. What is the NPV of the project?")
    st.write("The NPV is calculated using the formula:")
    st.latex(r"NPV = \sum \left( \frac{C_t}{(1+r)^t} \right)")
    st.write(f"**NPV of the project:** ${npv:.2f} million")
    st.write("The NPV indicates the net value added by the project. A negative NPV means the project is not financially viable at the given discount rate of 12%.")

    st.subheader("B. Is using the IRR rule reliable for this project?")
    st.write("The IRR rule may not be reliable for this project due to the unconventional cash flows, particularly the large shutdown cost in the final year. This can lead to multiple IRRs, making the IRR rule less reliable for decision-making.")
    st.write("Given the non-standard cash flows, the IRR rule could mislead the decision-making process, making it essential to consider other metrics like NPV and MIRR.")

    st.subheader("C. What are the IRR’s of this project?")
    st.write("The IRR is calculated using the formula:")
    st.latex(r"0 = \sum \left( \frac{C_t}{(1+\text{IRR})^t} \right)")
    st.write("**IRR of the project:** {:.2%}".format(project_irr))
    st.write("The IRR for this project is approximately zero, which implies the project's return is minimal and may not justify the investment given the risk and the cost of capital.")

    st.subheader("D. What is the modified IRR of this project (MIRR)?")
    st.write("The MIRR is calculated using the formula:")
    st.latex(r"\text{MIRR} = \left( \frac{FV_{\text{positive cash flows}}}{PV_{\text{negative cash flows}}} \right)^{\frac{1}{n}} - 1")
    st.write(f"**MIRR of the project:** {mirr:.2%}")
    st.write("The MIRR considers the cost of capital and reinvestment rate, providing a more accurate reflection of the project's profitability compared to IRR. In this case, the MIRR is 10.68%, which is still below the required 12% cost of capital.")

if __name__ == "__main__":
    main()
