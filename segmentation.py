import streamlit as st 
import pandas as pd 
import numpy as np 
import joblib  


# Load pre-trained KMeans clustering model and StandardScaler
# These models were trained on customer segmentation dataset with 6 clusters
kmeans = joblib.load("kmeans_model.pkl")
scaler = joblib.load("scaler.pkl")

# App title and description
st.write("Customer Segmentation App")
st.write("Enter custmoer details to predict the segment.")

# Input widgets for customer features
age = st.number_input("Age", min_value=18, max_value=100, value=35)
income = st.number_input("Income", min_value=0, max_value=200000, value=5000)
total_spending = st.number_input("Total Spending", min_value=0, max_value=5000, value=1000)
num_web_purchases = st.number_input("Total Web Purchase", min_value=0, max_value=100, value=10)
num_store_purchases = st.number_input("Total Store Purchase", min_value=0, max_value=100, value=10)
num_web_visits = st.number_input("Number of Web Visits", min_value=0, max_value=50, value=3)
recency = st.number_input("Recency (days since last Purchase)", min_value=0, max_value=365, value=30)


# Create input DataFrame with EXACT column names and order as training data
input_data = pd.DataFrame({
    "Age": [age],
    "Income": [income],
    "Total_Spending": [total_spending],
    "NumWebPurchases": [num_web_purchases],
    "NumStorePurchases": [num_store_purchases],
    "NumWebVisitsMonth": [num_web_visits],
    "Recency": [recency]
})

input_scaled = scaler.transform(input_data)


# Cluster profiles dictionary
cluster_profiles = {
    0: "👨‍💼 **Mid-age Professionals** - Age:61, Income:$54K, Spending:$588\n📈 Target: Premium wines/meat products",
    1: "👨‍👩‍👧‍👦 **Young Families** - Age:55, Income:$36K, Spending:$128\n📈 Target: Budget family promotions", 
    2: "👴 **Premium Seniors** - Age:70, Income:$74K, Spending:$1177\n📈 Target: In-store premium products",
    3: "🧑‍🎓 **Budget Young Adults** - Age:51, Income:$32K, Spending:$81\n📈 Target: Entry-level web campaigns",
    4: "🛒 **Prime Omnichannel** - Age:59, Income:$63K, Spending:$1063\n📈 Target: Cross-channel loyalty programs",
    5: "🚀 **Young High-Rollers** - Age:46, Income:$79K, Spending:$1307\n📈 Target: VIP experiences"
}

# Main Prediction logic
if st.button("Predict Segment"):

	# Predict cluster
    cluster = kmeans.predict(input_scaled)[0]
    # retruns predection
    st.success(f"Predicted Segment: Cluster {cluster}")

     # Display cluster profile
    st.markdown("### 📋 **Cluster Profile**")
    st.markdown(cluster_profiles[cluster])
    
    # Show feature comparison
    cluster_center = kmeans.cluster_centers_[cluster]
    comparison = pd.DataFrame({
        'Your Input': input_scaled[0].round(2),
        'Cluster Avg': cluster_center.round(2)
    })
    st.write("**📊 Your input vs Cluster average:**")
    st.dataframe(comparison)
