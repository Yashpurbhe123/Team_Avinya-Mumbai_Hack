import streamlit as st
import pandas as pd
from prophet import Prophet
import plotly.express as px
import speech_recognition as sr
import pyttsx3

# Load the data (Ensure the file path is correct)
data = pd.read_excel("pages/hyperlocal_demand_forecasting_with_grocery_items.xlsx")

# Data preprocessing
data['Month'] = pd.to_datetime(data['Month'])
data['Product Name'] = data['Product Name'].astype(str)
data = data.sort_values('Month')

# Define seasons/festivals with corresponding months
seasons = {
    "None": [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ],
    "Diwali": ["October", "November"],
    "Christmas": ["December"],
    "Summer": ["April", "May", "June"],
    "Monsoon": ["July", "August", "September"],
    "New Year": ["January"]
}

months_list = list(seasons["None"])  # Create a list of months for validation

# Sidebar selection for product, season/festival, and specific month
st.sidebar.title("Product Demand Forecasting")
selected_product = st.sidebar.selectbox("Select a product", data['Product Name'].unique())
selected_season = st.sidebar.selectbox("Select a season or festival", list(seasons.keys()))
selected_month = st.sidebar.selectbox("Select a month", seasons[selected_season])

# Filter data for the selected product
product_data = data[data['Product Name'] == selected_product]
product_data = product_data[['Month', 'Monthly_Sales']].rename(columns={'Month': 'ds', 'Monthly_Sales': 'y'})

# Ensure no NaN values in product_data
product_data.dropna(inplace=True)

# Build the forecasting model
model = Prophet(growth='linear')  # Use linear growth
model.fit(product_data)
future = model.make_future_dataframe(periods=12, freq='MS')  # Predict for next 12 months
forecast = model.predict(future)

# Clip the predictions to ensure no negative values
forecast['yhat'] = forecast['yhat'].clip(lower=0).round().astype(int)
forecast['yhat_lower'] = forecast['yhat_lower'].clip(lower=0).round().astype(int)
forecast['yhat_upper'] = forecast['yhat_upper'].clip(lower=0).round().astype(int)

# Separate past data and forecasted data
historical_data = product_data.copy()
forecast_data = forecast[forecast['ds'] > product_data['ds'].max()]  # Only future months

# Add a 'Month' column with month names for easier season and month filtering
forecast_data['Month'] = forecast_data['ds'].dt.strftime('%B')
forecast_data['Year'] = forecast_data['ds'].dt.year

# Filter forecast data based on selected season and month
if selected_season != "None":
    season_months = seasons[selected_season]
    season_forecast_data = forecast_data[forecast_data['Month'].isin(season_months)]
else:
    season_forecast_data = forecast_data  # Show all months when "None" is selected

# Further filter by the selected month if applicable
selected_month_forecast_data = season_forecast_data[season_forecast_data['Month'] == selected_month]

# Layout setup
st.title("📈 Product Demand Forecasting")
st.write(f"This app presents a forecast of future demand for {selected_product}.")

# Voice input and response
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.sidebar.write("Say the product name followed by the month you want to predict the sales for...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        st.write("You said: " + text)
        return text
    except sr.UnknownValueError:
        st.sidebar.write("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError:
        st.sidebar.write("Could not request results.")
        return None

def respond(prediction):
    engine = pyttsx3.init()
    engine.say(f"The predicted sales for {selected_product} in {selected_month} are {prediction}")
    engine.runAndWait()

# Voice control - Place the button in the sidebar for left alignment
if st.sidebar.button("Click to speak", key="speak_button"):
    text = recognize_speech()
    if text:
        words = text.split()
        if len(words) < 2:
            st.sidebar.write("Please provide both a product name and a month.")
        else:
            # Extracting the product name and month
            month_mentioned = words[-1]  # Last word as month
            product_mentioned = ' '.join(words[:-1])  # All but the last word as product
            
            # Update product selection if the recognized product is valid
            if product_mentioned in data['Product Name'].unique():
                selected_product = product_mentioned
                # Update the sidebar selection
                st.sidebar.selectbox("Select a product", data['Product Name'].unique(), index=list(data['Product Name'].unique()).index(selected_product))

            # Update month selection if the recognized month is valid
            if month_mentioned in months_list:
                selected_month = month_mentioned
                # Update the sidebar selection
                st.sidebar.selectbox("Select a month", months_list, index=months_list.index(selected_month))
            else:
                st.sidebar.write(f"Month '{month_mentioned}' not recognized. Please try again.")
            
            # Re-fetch the forecast data based on the updated selection
            selected_month_forecast_data = season_forecast_data[season_forecast_data['Month'] == selected_month]
            
            # Update the metrics display
            if not selected_month_forecast_data.empty:
                selected_month_prediction = selected_month_forecast_data['yhat'].iloc[0]
                respond(selected_month_prediction)  # Announce the prediction
            else:
                st.write(f"No forecast data available for the product: {selected_product} and month: {selected_month}.")

# Show metrics for selected season and month
if not selected_month_forecast_data.empty:
    selected_month_prediction = selected_month_forecast_data['yhat'].iloc[0]
    selected_lower = selected_month_forecast_data['yhat_lower'].iloc[0]
    selected_upper = selected_month_forecast_data['yhat_upper'].iloc[0]
    
    st.subheader(f"Predicted Demand for {selected_product} - {selected_season} ({selected_month})")
    col1, col2, col3 = st.columns(3)
    col1.metric("Prediction", f"{selected_month_prediction}")
    col2.metric("Lower Estimate", f"{selected_lower}")
    col3.metric("Upper Estimate", f"{selected_upper}")
else:
    st.write(f"No forecast data available for the selected season: {selected_season} and month: {selected_month}.")

# Visualize past and predicted future sales for the selected season and month
st.subheader(f"Past Sales vs. Forecasted Demand during {selected_season} ({selected_month})")

# Line chart for past sales and predictions for the season and specific month
fig_line = px.line(
    x=pd.concat([historical_data['ds'], season_forecast_data['ds']]),
    y=pd.concat([historical_data['y'], season_forecast_data['yhat']]),
    labels={'x': 'Month', 'y': 'Sales'},
    title=f"Past Sales and Forecasted Demand for {selected_product} during {selected_season} ({selected_month})"
)
fig_line.add_scatter(
    x=season_forecast_data['ds'],
    y=season_forecast_data['yhat'],
    mode="lines",
    name="Predicted",
    line=dict(dash="dash")
)
st.plotly_chart(fig_line)

# Display the forecast table for the selected season and month
st.subheader(f"Predicted Future Demand for {selected_product} ({selected_season} - {selected_month})")
selected_month_forecast_table = selected_month_forecast_data[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].rename(
    columns={'ds': 'Date', 'yhat': 'Predicted Sales', 'yhat_lower': 'Lower Estimate', 'yhat_upper': 'Upper Estimate'}
)
selected_month_forecast_table['Predicted Sales'] = selected_month_forecast_table['Predicted Sales'].astype(int)
selected_month_forecast_table['Lower Estimate'] = selected_month_forecast_table['Lower Estimate'].astype(int)
selected_month_forecast_table['Upper Estimate'] = selected_month_forecast_table['Upper Estimate'].astype(int)
st.dataframe(selected_month_forecast_table)

# Summary of predictions
st.write(
    f"The above tables and charts provide a visual representation of the past sales and predicted future demand for "
    f"{selected_product} during {selected_season} in {selected_month}. This information can guide stock levels and ordering needs."
)

# Additional visualizations

# Pie chart for sales distribution by month (last year's sales)
last_year_data = data[data['Month'].dt.year == data['Month'].dt.year.max()]

fig_pie = px.pie(
    last_year_data,
    names='Month',
    values='Monthly_Sales',
    title=f"Sales Distribution for {selected_product} in Last Year"
)
st.plotly_chart(fig_pie)
