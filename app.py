import streamlit as st
import joblib
import pandas as pd

# 1. PAGE CONFIG (Must be the first Streamlit command)
st.set_page_config(
    page_title="Real Estate Predictor",
    page_icon="🏠",
    layout="centered" # "wide" ya "centered"
)
# 2. BACKGROUND COLOR (Light Red)
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #ffebee; /*  Red */
}
[data-testid="stSidebar"] {
    background-color: #f5f5f5; /* Light Grey for Sidebar */
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)
# --- Saved Model ko Load Karna ---
try:
    model = joblib.load("xgboost_house_price_model.pkl")
except FileNotFoundError:
    st.error("Model file not found!")
    st.stop()

# 2. CUSTOM STYLING (Title ke liye)
st.markdown("""
<style>
.title-style {
    font-size:42px !important;
    font-weight: bold;
    color: #2E86C1;
    text-align: center;
    text-shadow: 2px 2px 4px #f2f2f2;
}
.subtitle-style {
    text-align: center;
    font-style: italic;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title-style">California House Price Predictor</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-style">Enter the details to get an estimated price.</p>', unsafe_allow_html=True)


# --- SIDEBAR INPUTS ---
st.sidebar.header("Input Features")
st.sidebar.info("⬅️ Enter all details here to predict the price.")

med_inc = st.sidebar.number_input("Median Income (in tens of thousands)", min_value=0.0, max_value=20.0, value=3.5, step=0.1)
house_age = st.sidebar.number_input("House Age (in years)", min_value=1, max_value=60, value=25, step=1)
ave_rooms = st.sidebar.number_input("Average Number of Rooms", min_value=1.0, max_value=20.0, value=5.0, step=0.5)
ave_bedrms = st.sidebar.number_input("Average Number of Bedrooms", min_value=0.5, max_value=10.0, value=1.0, step=0.1)
population = st.sidebar.number_input("Block Population", min_value=1, max_value=40000, value=1500, step=100)
ave_occup = st.sidebar.number_input("Average Occupancy", min_value=1.0, max_value=20.0, value=3.0, step=0.1)
latitude = st.sidebar.number_input("Latitude", min_value=32.0, max_value=42.0, value=37.0, step=0.1)
longitude = st.sidebar.number_input("Longitude", min_value=-125.0, max_value=-114.0, value=-122.0, step=0.1)


# --- PREDICTION LOGIC ---
if st.sidebar.button("Predict House Price", type="primary"):
    input_features = pd.DataFrame(
        [[med_inc, house_age, ave_rooms, ave_bedrms, population, ave_occup, latitude, longitude]],
        columns=['MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 'Population', 'AveOccup', 'Latitude', 'Longitude']
    )
    
    prediction = model.predict(input_features)
    
    st.header("Prediction Result")
    st.success(f"The estimated price of the house is: ${prediction[0] * 100000:,.2f}")