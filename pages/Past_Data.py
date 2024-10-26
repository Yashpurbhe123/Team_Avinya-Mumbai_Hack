import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load your data (ensure the file path is correct)
data = pd.read_excel("pages/hyperlocal_demand_forecasting_with_grocery_items.xlsx")

# Convert 'Month' to datetime
data['Month'] = pd.to_datetime(data['Month'])

# Create a list of months sorted correctly
months_list = ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December']

# Streamlit user inputs for month and product selection
selected_month = st.selectbox("Select Month", months_list)
selected_product = st.selectbox("Select Product", data['Product Name'].unique())

# Filter data for the selected month
month_data = data[data['Month'].dt.strftime('%B') == selected_month]

if not month_data.empty:
    # Create a bar chart for sales comparison of products in the selected month
    fig = go.Figure()

    # Add bars for each product
    for product in month_data['Product Name']:
        color = 'blue' if product == selected_product else 'lightgray'  # Highlight selected product
        opacity = 1 if product == selected_product else 0.5  # Set opacity for blur effect
        fig.add_trace(go.Bar(
            x=[product],
            y=month_data[month_data['Product Name'] == product]['Monthly_Sales'],
            name=product,
            marker_color=color,
            opacity=opacity,
            width=0.4  # Adjust the width of the bars (value between 0 and 1)
        ))

    fig.update_layout(
        title=f"Monthly Sales Comparison for {selected_month}",
        xaxis_title='Product',
        yaxis_title='Sales',
        showlegend=False
    )

    st.plotly_chart(fig)

else:
    st.write(f"No data available for the month: {selected_month}.")

# Additional visualization: Sales trends over the past year for the selected product
st.subheader(f"Sales Trends for {selected_product} Over the Past Year")
last_year_data = data[data['Month'].dt.year == data['Month'].dt.year.max()]
product_last_year_data = last_year_data[last_year_data['Product Name'] == selected_product]

fig_trend = px.line(
    product_last_year_data,
    x='Month',
    y='Monthly_Sales',
    title=f"Sales Trends for {selected_product} Over the Past Year",
    labels={'Monthly_Sales': 'Sales', 'Month': 'Month'}
)
st.plotly_chart(fig_trend)
