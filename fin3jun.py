import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Define exercise prices and premiums
buy_call_exercise_price = 65
buy_call_premium = 9
sell_call_exercise_price = 75
sell_call_premium = 4

# Function to calculate payoffs and profits
def option_strategy(stock_price):
    buy_call_payoff = max(0, stock_price - buy_call_exercise_price)
    sell_call_payoff = -max(0, stock_price - sell_call_exercise_price)

    total_payoff = buy_call_payoff + sell_call_payoff
    total_profit = total_payoff - buy_call_premium + sell_call_premium

    return total_payoff, total_profit

# Streamlit App
st.title('Option Strategy Analysis')

# Part 1: Value at expiration (payoffs) and profit under different outcomes
st.header('1. Value at Expiration and Profit')

stock_prices = [78, 69, 62]
results = {"Stock Price": [], "Payoff": [], "Profit": []}

for price in stock_prices:
    payoff, profit = option_strategy(price)
    results["Stock Price"].append(price)
    results["Payoff"].append(payoff)
    results["Profit"].append(profit)

st.write("a. Stock Price at Expiration: $78")
st.write(f"Payoff: {results['Payoff'][0]}")
st.write(f"Profit: {results['Profit'][0]}")
st.write("Equation: Payoff = max(0, 78 - 65) - max(0, 78 - 75)")
st.write("Profit: Payoff - 9 + 4")
st.markdown(f"**Final Answer: Profit = {results['Profit'][0]}**")

st.write("b. Stock Price at Expiration: $69")
st.write(f"Payoff: {results['Payoff'][1]}")
st.write(f"Profit: {results['Profit'][1]}")
st.write("Equation: Payoff = max(0, 69 - 65) - max(0, 69 - 75)")
st.write("Profit: Payoff - 9 + 4")
st.markdown(f"**Final Answer: Profit = {results['Profit'][1]}**")

st.write("c. Stock Price at Expiration: $62")
st.write(f"Payoff: {results['Payoff'][2]}")
st.write(f"Profit: {results['Profit'][2]}")
st.write("Equation: Payoff = max(0, 62 - 65) - max(0, 62 - 75)")
st.write("Profit: Payoff - 9 + 4")
st.markdown(f"**Final Answer: Profit = {results['Profit'][2]}**")

# Part 2: Maximum profit and maximum loss
st.header('2. Maximum Profit and Maximum Loss')

max_profit = (sell_call_premium - buy_call_premium) + (sell_call_exercise_price - buy_call_exercise_price)
max_loss = buy_call_premium - sell_call_premium

st.write("a. Maximum Profit")
st.write("Equation: Maximum Profit = (Sell call premium - Buy call premium) + (Sell call exercise price - Buy call exercise price)")
st.markdown(f"**Final Answer: Maximum Profit = {max_profit}**")

st.write("b. Maximum Loss")
st.write("Equation: Maximum Loss = Buy call premium - Sell call premium")
st.markdown(f"**Final Answer: Maximum Loss = {max_loss}**")

# Part 3: Breakeven stock price at expiration
st.header('3. Breakeven Stock Price')

breakeven_price = buy_call_exercise_price + (buy_call_premium - sell_call_premium)

st.write("Equation: Breakeven Stock Price = Buy call exercise price + (Buy call premium - Sell call premium)")
st.markdown(f"**Final Answer: Breakeven Stock Price = {breakeven_price}**")

# Part 4: Payoff and Profit Diagrams
st.header('4. Payoff and Profit Diagrams')

# Generate a range of stock prices
stock_prices_range = np.linspace(50, 90, 400)
payoffs = []
profits = []

for price in stock_prices_range:
    payoff, profit = option_strategy(price)
    payoffs.append(payoff)
    profits.append(profit)

# Plotting using Seaborn
sns.set(style="whitegrid")

# Payoff diagram
fig1, ax1 = plt.subplots(figsize=(10, 4))
sns.lineplot(x=stock_prices_range, y=payoffs, ax=ax1)
ax1.set_title('Option Strategy Payoff Diagram')
ax1.set_xlabel('Stock Price at Expiration')
ax1.set_ylabel('Payoff')
st.pyplot(fig1)

# Profit diagram
fig2, ax2 = plt.subplots(figsize=(10, 4))
sns.lineplot(x=stock_prices_range, y=profits, ax=ax2)
ax2.set_title('Option Strategy Profit Diagram')
ax2.set_xlabel('Stock Price at Expiration')
ax2.set_ylabel('Profit')
st.pyplot(fig2)
