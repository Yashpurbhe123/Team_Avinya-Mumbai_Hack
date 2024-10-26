import streamlit as st

# Set page configuration
st.set_page_config(page_title="Product Demand Forecasting", layout="wide")

# Title and Introductory Message
st.title("Product Demand Forecasting Application")
st.markdown("""
    Welcome to the **Product Demand Forecasting Application**! 🌟

    This application utilizes advanced data analysis techniques to assist businesses in understanding and predicting product demand based on historical sales data. With intuitive visualizations and predictive modeling, users can make informed decisions to optimize inventory management and enhance sales strategies.

    ## Key Features:
    - **User-Friendly Interface**: Navigate easily through the application for a seamless experience.
    - **Interactive Data Visualizations**: Engage with dynamic graphs and charts for insightful data analysis.
    - **Accurate Demand Forecasting**: Leverage machine learning algorithms for precise demand predictions.

    ## How It Works:
    1. **Data Input**: Upload your sales data in the specified format to kickstart the analysis.
    2. **Forecasting**: Select the product and month for which you wish to forecast demand.
    3. **Visualization**: Explore detailed graphs and charts that illustrate your data and forecasts, aiding in strategic decision-making.

    ## About This Project:
    Our goal is to provide businesses with a robust tool for predictive analytics, enabling alignment of inventory management with actual consumer demand. By harnessing data-driven insights, we aim to empower businesses in navigating market fluctuations effectively.
    
    Thank you for using our application, and we hope it serves you well in your decision-making process!
""")

# Create two columns for images
col1, col2 = st.columns(2)

# Add images to the columns
with col1:
    st.image("https://media.licdn.com/dms/image/v2/C4D12AQFB-LCvXBaoNA/article-cover_image-shrink_600_2000/article-cover_image-shrink_600_2000/0/1619619546670?e=2147483647&v=beta&t=8eHOWwIN7DPk9ucHRU5V1xnYHDdv-1Lk4v8c2Aax0N0", width=500)

with col2:
    st.image("https://tridentinfo.com/wp-content/uploads/2023/04/demand-forecasting-machine-learning-use-cases.webp", width=500)

st.image("https://miro.medium.com/v2/resize:fit:1400/1*yFjlQejWS5s_IwWGmRGjYQ.png", width=1026)  # Replace with the actual path to your logo or image
