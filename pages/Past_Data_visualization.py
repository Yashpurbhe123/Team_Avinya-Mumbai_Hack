import streamlit as st
import pandas as pd
from prophet import Prophet
import plotly.graph_objects as go

# Load your data (ensure the file path is correct)
data = pd.read_excel('pages/hyperlocal_demand_forecasting_with_grocery_items.xlsx')

# Convert 'Month' to datetime
data['Month'] = pd.to_datetime(data['Month'])

# Create a list of months sorted correctly
months_list = ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December']

# Streamlit user inputs for month and product selection
selected_month = st.selectbox("Select Month", months_list)
selected_product = st.selectbox("Select Product", data['Product Name'].unique())

# Filter data for the selected product
monthly_data = data[data['Product Name'] == selected_product]

# Ensure the data is filtered for the selected month if needed
monthly_data['Month_str'] = monthly_data['Month'].dt.strftime('%B')
monthly_data = monthly_data[monthly_data['Month_str'] == selected_month]

# Calculate total stock and total sales for the selected product in the selected month
if not monthly_data.empty:  # Check if there is any data for the selected product in the selected month
    total_month_stock = monthly_data['Monthly_Stock'].sum()  # Total stock for the selected product
    total_sales = monthly_data['Monthly_Sales'].sum()  # Total sales for the selected product

    # Prepare data for prediction
    # Create a DataFrame for Prophet
    df = monthly_data[['Month', 'Monthly_Sales']].rename(columns={'Month': 'ds', 'Monthly_Sales': 'y'})
    
    # Fit the model
    model = Prophet()
    model.fit(df)

    # Create a future DataFrame for the next month
    future = model.make_future_dataframe(periods=1, freq='M')
    forecast = model.predict(future)
    
    # Get the predicted value for the next month
    predicted_value = forecast['yhat'].iloc[-1]  # Last prediction value
    
    # Prepare data for different plots
    labels = ['Total Sales', 'Total Monthly Stock', 'Predicted Sales']
    values = [total_sales, total_month_stock, predicted_value]

    # Plotting sales vs stock
    st.subheader(f"Sales vs. Stock for {selected_product} in {selected_month}")

    # Bar Plot for Sales and Stock
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=['Sales', 'Stock'], y=[total_sales, total_month_stock], 
                              marker_color=['blue', 'orange']))
    fig_bar.update_layout(title='Sales vs Stock', xaxis_title='Category', yaxis_title='Amount')
    st.plotly_chart(fig_bar)

    # Line Plot to visualize trends
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=['Sales', 'Stock'], y=[total_sales, total_month_stock], 
                                   mode='lines+markers', name='Sales & Stock', line=dict(shape='linear')))
    fig_line.update_layout(title='Sales vs Stock Trend', xaxis_title='Category', yaxis_title='Amount')
    st.plotly_chart(fig_line)

    # Area Plot to visualize cumulative sales and stock
    fig_area = go.Figure()
    fig_area.add_trace(go.Scatter(x=['Sales', 'Stock'], y=[total_sales, total_month_stock], 
                                   mode='lines', fill='tozeroy', name='Values'))
    fig_area.update_layout(title='Cumulative Sales vs Stock', xaxis_title='Category', yaxis_title='Amount')
    st.plotly_chart(fig_area)

    # Pie Chart to represent sales and stock distribution
    fig_pie = go.Figure()
    fig_pie.add_trace(go.Pie(labels=['Total Sales', 'Total Stock'], values=[total_sales, total_month_stock], 
                              name='Sales and Stock'))
    fig_pie.update_layout(title='Sales and Stock Distribution')
    st.plotly_chart(fig_pie)

else:
    st.error(f"No data available for {selected_product} in {selected_month}.")
