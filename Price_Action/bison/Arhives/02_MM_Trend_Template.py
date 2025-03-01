# import streamlit as st
# import pandas as pd
# import yfinance as yf
# import ta
# import os
# import time  # Importing the time module

# # Function to apply the scanner conditions to a single stock
# @st.cache_data
# def apply_scanner_conditions(stock_data):
#     # Calculate 52-week high and low
#     lo = stock_data['Low'].min()
#     hi = stock_data['High'].max()

#     # Calculate thresholds for conditions 6 and 7
#     x = 1.3 * lo # 30% above its 52-week low
#     y = 0.75 * hi # 25% of its 52-week high

#     # Calculate RSI
#     stock_data['RSI'] = ta.momentum.rsi(stock_data['Close'])
#     rsi_condition = stock_data['RSI'].iloc[-1] > 60

#     # Check conditions
#     condition_1 = stock_data['Close'].iloc[-1] > stock_data['Close'].rolling(window=200).mean().iloc[-1]
#     condition_2 = stock_data['Close'].rolling(window=150).mean().iloc[-1] > stock_data['Close'].rolling(window=200).mean().iloc[-1]
#     condition_3 = stock_data['Close'].rolling(window=50).mean().iloc[-1] > stock_data['Close'].rolling(window=150).mean().iloc[-1]
#     condition_4 = stock_data['Close'].rolling(window=50).mean().iloc[-1] > stock_data['Close'].rolling(window=200).mean().iloc[-1]
#     condition_5 = stock_data['Close'].iloc[-1] > stock_data['Close'].rolling(window=50).mean().iloc[-1]
#     condition_6 = stock_data['Close'].iloc[-1] >= x
#     condition_7 = stock_data['Close'].iloc[-1] >= y

#     return (
#         condition_1 and condition_2 and condition_3 and condition_4 and
#         condition_5 and condition_6 and condition_7 and rsi_condition
#     )

# # Function to read stock symbols from a CSV file
# def read_stock_symbols_from_csv(file):
#     df = pd.read_csv(file)
#     return df['Symbol'].tolist()

# # Streamlit app
# st.title('Mark Minervini Trend Template')

# # User input for CSV file
# uploaded_file = st.file_uploader("Upload CSV file with stock symbols", type=['csv'])

# # Form for date input and submit button
# with st.form(key='my_form'):
#     # User input for start and end dates
#     start_date = st.date_input("Select start date", pd.to_datetime('2023-01-01'))
#     end_date = st.date_input("Select end date", pd.to_datetime('2024-03-17'))
#     submit_button = st.form_submit_button(label='Submit')

# if submit_button:
#     if uploaded_file is not None:
#         # Read stock symbols from the uploaded CSV file
#         stock_symbols = read_stock_symbols_from_csv(uploaded_file)
#         total_rows = len(stock_symbols)

#         # Define progress bar
#         progress_bar = st.progress(0)

#         # Apply scanner conditions to each stock
#         scanner_results = {}
#         for i, symbol in enumerate(stock_symbols, start=1):
#             try:
#                 # Get stock data from yfinance
#                 stock_data = yf.download(symbol, start=start_date, end=end_date)
#                 result = apply_scanner_conditions(stock_data)
#                 scanner_results[symbol] = 'Pass' if result else 'Fail'
#             except Exception as e:
#                 st.error(f"Error processing {symbol}: {e}")

#             # Update progress bar
#             progress_percent = int(i / total_rows * 100)
#             progress_bar.progress(progress_percent)

#         # Create a DataFrame from the scanner results
#         df_results = pd.DataFrame(list(scanner_results.items()), columns=['Symbol', 'Result'])

#         # Filter DataFrame to include only pass results
#         pass_results = df_results[df_results['Result'] == 'Pass']

#         # Display pass results
#         st.subheader("Stocks that passed the scanner conditions:")
#         st.write(pass_results)

#         # Save the pass results to a CSV file with the same name as the input file
#         input_file_name = uploaded_file.name
#         output_file_path = os.path.join("./Data", f"MM_{input_file_name}")
#         pass_results.to_csv(output_file_path, index=False)
#         st.success(f"Results saved to {output_file_path}")

import streamlit as st
import pandas as pd
import yfinance as yf
import ta
import os
import time  # Importing the time module
from datetime import datetime, timedelta

# Calculate 52 weeks from the current date
fifty_two_weeks_ago = datetime.now() - timedelta(weeks=52)


# Function to apply the scanner conditions to a single stock
@st.cache_resource
def apply_scanner_conditions(stock_data):
    # Calculate 52-week high and low
    lo = stock_data['Low'].min()
    hi = stock_data['High'].max()

    # Calculate thresholds for conditions 6 and 7
    x = 1.3 * lo # 30% above its 52-week low
    y = 0.75 * hi # 25% of its 52-week high

    # Calculate RSI
    stock_data['RSI'] = ta.momentum.rsi(stock_data['Close'])
    rsi_condition = stock_data['RSI'].iloc[-1] > 0

    # Check conditions
    condition_1 = stock_data['Close'].iloc[-1] > stock_data['Close'].rolling(window=200).mean().iloc[-1]
    condition_2 = stock_data['Close'].rolling(window=150).mean().iloc[-1] > stock_data['Close'].rolling(window=200).mean().iloc[-1]
    condition_3 = stock_data['Close'].rolling(window=50).mean().iloc[-1] > stock_data['Close'].rolling(window=150).mean().iloc[-1]
    condition_4 = stock_data['Close'].rolling(window=50).mean().iloc[-1] > stock_data['Close'].rolling(window=200).mean().iloc[-1]
    condition_5 = stock_data['Close'].iloc[-1] > stock_data['Close'].rolling(window=50).mean().iloc[-1]
    condition_6 = stock_data['Close'].iloc[-1] >= x
    condition_7 = stock_data['Close'].iloc[-1] >= y

    return (
        condition_1 and condition_2 and condition_3 and condition_4 and
        condition_5 and condition_6 and condition_7 and rsi_condition
    )

# Function to read stock symbols and additional columns from a CSV file
def read_stock_data_from_csv(file):
    df = pd.read_csv(file)
    return df['Symbol'].tolist(), df[['Symbol', 'Close','ADR Value', 'ADR %', 'Mod_ADR %', 'RSI']]

# Streamlit app
st.title('Mark Minervini Trend Template')

# User input for CSV file
uploaded_file = st.file_uploader("Upload CSV file with stock symbols and additional columns", type=['csv'])

# Form for date input and submit button
with st.form(key='my_form'):
    # User input for start and end dates
    # User input for start and end dates
    start_date = st.date_input("Select start date", pd.to_datetime(fifty_two_weeks_ago))
    end_date = st.date_input("Select end date", pd.to_datetime(datetime.now()))
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    if uploaded_file is not None:
        # Read stock symbols and additional columns from the uploaded CSV file
        stock_symbols, additional_columns = read_stock_data_from_csv(uploaded_file)
        total_rows = len(stock_symbols)

        # Define progress bar
        progress_bar = st.progress(0)

        # Apply scanner conditions to each stock
        scanner_results = {}
        for i, symbol in enumerate(stock_symbols, start=1):
            try:
                # Get stock data from yfinance
                stock_data = yf.download(symbol, start=start_date, end=end_date)
                result = apply_scanner_conditions(stock_data)
                scanner_results[symbol] = 'Pass' if result else 'Fail'
            except Exception as e:
                st.error(f"Error processing {symbol}: {e}")

            # Update progress bar
            progress_percent = int(i / total_rows * 100)
            progress_bar.progress(progress_percent)

        # Create a DataFrame from the scanner results
        df_results = pd.DataFrame(list(scanner_results.items()), columns=['Symbol', 'Result'])

        # Filter DataFrame to include only pass results
        pass_results = df_results[df_results['Result'] == 'Pass']

        # Merge pass results with additional columns
        pass_results_with_additional_columns = pd.merge(pass_results, additional_columns, on='Symbol', how='left')

        # Display pass results
        st.subheader("Stocks that passed the scanner conditions:")
        st.write(pass_results_with_additional_columns)

        # Save the pass results to a CSV file with the same name as the input file
        input_file_name = uploaded_file.name
        output_file_path = os.path.join("./Data", f"MM_{input_file_name}")
        pass_results_with_additional_columns.to_csv(output_file_path, index=False)
        st.success(f"Results saved to {output_file_path}")
