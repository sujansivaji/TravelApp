import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import base64
from io import BytesIO
import json

from TravelAgent import LLMTasks

# Page configuration
st.set_page_config(
    page_title="TravelEase - Your Travel Companion",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for travel-themed design
st.markdown("""
<style>
    .feature-box.tips {
        background: purple;
        color: white;
    }
    .feature-box.weather {
        background: purple;
        color: white;
        padding: 1rem;
    }
    .main {
        padding-top: 2rem;
    }
    .stApp {
        background: url('travel_app_wallpaper.svg') no-repeat center center fixed;
        background-size: cover;
    }
    .travel-header {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: purple;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .destination-card {
        background: purple;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        border-left: 4px solid #4ECDC4;
    }
    .price-tag {
        background: linear-gradient(45deg, #FF6B6B, #FF8E53);
        color: purple;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: bold;
        display: inline-block;
        margin: 0.5rem 0;
    }
    .feature-box {
        background: rgba(255, 255, 255, 0.9);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        color: green;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: orange;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="travel-header">
    <h1>✈️ TravelEase - Your Ultimate Travel Companion</h1>
    <p>Discover amazing destinations, plan your perfect trip, and create unforgettable memories!</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🧳 Trip Planner")
    
    # Travel preferences
    travel_type = st.selectbox(
        "Travel Type",
        ["Adventure", "Relaxation", "Cultural", "Business", "Family", "Couple"]
    )

# Side bar
with st.sidebar:
    #st.header("🧳 Destination:")
    data = pd.read_csv('/Users/sujansivaji/Documents/TravelApp/data/world_countries_travel_csv.txt', delimiter=',')
    country = st.selectbox("Select Destination Country", data['Country'].unique())
    #country_info = data[data['Country'] == country].iloc[0]
 
    
    # Travel mood
    travel_mood = st.selectbox(
        "Travel Mood",
        ["Thrill seeking", "Relaxation & Wellness", "Cultural Exploration", "Experience & Memory mood", "The Romantic mood", "customized", ]
    )

    budget = st.slider("Budget (USD)", 300, 15000, 2500, 100)

    duration = st.select_slider(
        "Trip Duration (days)",
        options=[3, 5, 7, 10, 14, 21, 30],
        value=7
    )
    
    departure_date = st.date_input(
        "Departure Date",
        min_value=datetime.now().date(),
        value=datetime.now().date() + timedelta(days=30)
    )
    
    travelers = st.number_input("Number of Travelers", 1, 10, 2)

# Sample data for destinations
destinations_data = {
    "Destination": ["Paris, France", "Tokyo, Japan", "Bali, Indonesia", "New York, USA", 
                   "Rome, Italy", "Santorini, Greece", "Dubai, UAE", "Barcelona, Spain"],
    "Price": [1800, 2200, 1200, 1600, 1500, 2000, 1900, 1400],
    "Rating": [4.8, 4.9, 4.7, 4.6, 4.8, 4.9, 4.5, 4.7],
    "Days": [7, 10, 8, 5, 6, 7, 6, 7],
    "Type": ["Cultural", "Cultural", "Relaxation", "Business", "Cultural", "Romantic", "Adventure", "Cultural"],
    "Highlights": [
        "Eiffel Tower, Louvre Museum, Seine River",
        "Cherry Blossoms, Temples, Modern Culture",
        "Beaches, Temples, Rice Terraces",
        "Statue of Liberty, Times Square, Central Park",
        "Colosseum, Vatican City, Roman Forum",
        "Sunset Views, White Architecture, Volcanic Beaches",
        "Burj Khalifa, Desert Safari, Luxury Shopping",
        "Sagrada Familia, Park Güell, Gothic Quarter"
    ]
}

df_destinations = pd.DataFrame(destinations_data)

# Filter destinations based on preferences
filtered_destinations = df_destinations[
    (df_destinations['Type'] == travel_type) & 
    (df_destinations['Price'] <= budget) &
    (df_destinations['Days'] <= duration)
]



# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🌍 Trending Destinations")
    
    if not filtered_destinations.empty:
        for idx, row in filtered_destinations.iterrows():
            st.markdown(f"""
            <div class="destination-card">
                <h3>🏖️ {row['Destination']}</h3>
                <div class="price-tag">${row['Price']} for {row['Days']} days</div>
                <p><strong>⭐ Rating:</strong> {row['Rating']}/5.0</p>
                <p><strong>🎯 Highlights:</strong> {row['Highlights']}</p>
                <p><strong>📅 Perfect for:</strong> {row['Type']} travelers</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Our models are tweaking the recommendations. Please adjust your preferences.")
    
    # Travel analytics
    st.header("📊 Travel Analytics")
    
    # Price comparison chart
    fig_price = px.bar(
        df_destinations, 
        x="Destination", 
        y="Price",
        color="Type",
        title="Destination Price Comparison",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_price.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig_price, use_container_width=True)
    
    # Rating vs Price scatter plot
    fig_scatter = px.scatter(
        df_destinations,
        x="Price",
        y="Rating",
        size="Days",
        color="Type",
        hover_data=["Destination"],
        title="Price vs Rating Analysis",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_scatter.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.header("🛡️ Travel Itinerary")
    if st.button("Generate Itinerary using LLM"):
        st.write("Stay tight! Generating your personalized itinerary...")
        itinerary = LLMTasks.CurateItinerary(
            profile=travel_mood,
            destination=country,
            days=duration,
            role=travel_type,
            budget=f"${budget} for {travelers} travelers"
        )
        #st.write(itinerary)

        st.subheader("Your Curated Itinerary:")
        st.text_area("Itinerary", itinerary, height=500)


with col2:
    st.header("📈 Quick Stats")
    
    # Metrics
    total_destinations = len(df_destinations)
    avg_price = df_destinations['Price'].mean()
    avg_rating = df_destinations['Rating'].mean()
    
    st.markdown(f"""
    <div class="metric-card">
        <h3>{total_destinations}</h3>
        <p>Total Destinations</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="metric-card">
        <h3>${avg_price:.0f}</h3>
        <p>Average Price</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="metric-card">
        <h3>{avg_rating:.1f}⭐</h3>
        <p>Average Rating</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Travel tips
    st.markdown("""
    <div class="feature-box tips">
        <h4>💡 Travel Tips</h4>
        <ul>
            <li>Book flights 6-8 weeks in advance</li>
            <li>Check visa requirements early</li>
            <li>Get travel insurance</li>
            <li>Research local customs</li>
            <li>Pack light and smart</li>
            <li>Stay hydrated and healthy</li>
            <li>Use apps for navigation and translation</li>
            <li>Keep digital and physical copies of important documents</li>
            <li>Inform your bank of travel plans to avoid card blocks</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button("💡 Country specific Visa Requirements"):
        st.info("Please check the official government website for the most accurate and up-to-date visa information.")

    


# Booking simulation
st.header("🎫 Book Your Trip")

booking_col1, booking_col2, booking_col3 = st.columns(3)

with booking_col1:
    selected_destination = st.selectbox(
        "Select Destination",
        df_destinations['Destination'].tolist()
    )

with booking_col2:
    flight_class = st.selectbox(
        "Flight Class",
        ["Economy", "Premium Economy", "Business", "First Class"]
    )

with booking_col3:
    hotel_rating = st.selectbox(
        "Hotel Rating",
        ["1-star","2-star","3-star", "4-star", "5-star", "Luxury Resort","customized"]
    )

# Generate trip summary
if st.button("🚀 Generate Trip Summary", type="primary"):
    selected_row = df_destinations[df_destinations['Destination'] == selected_destination].iloc[0]
    
    # Calculate total cost
    base_price = selected_row['Price']
    flight_multiplier = {"Economy": 1.0, "Premium Economy": 1.3, "Business": 1.8, "First Class": 2.5}
    hotel_multiplier = {"3 Star": 1.0, "4 Star": 1.2, "5 Star": 1.5, "Luxury Resort": 2.0}
    
    total_cost = base_price * flight_multiplier[flight_class] * hotel_multiplier[hotel_rating] * travelers
    
    trip_summary = {
        "Trip Details": {
            "Destination": selected_destination,
            "Departure Date": departure_date.strftime("%Y-%m-%d"),
            "Duration": f"{duration} days",
            "Travelers": travelers,
            "Travel Type": travel_type
        },
        "Bookings": {
            "Flight Class": flight_class,
            "Hotel Rating": hotel_rating,
            "Total Cost": f"${total_cost:.2f}",
            "Cost Per Person": f"${total_cost/travelers:.2f}"
        },
        "Destination Info": {
            "Rating": f"{selected_row['Rating']}/5.0",
            "Highlights": selected_row['Highlights'],
            "Recommended Duration": f"{selected_row['Days']} days"
        }
    }
    
    st.success("🎉 Trip Summary Generated!")
    st.json(trip_summary)
    
    # Download functionality
    def create_download_link(data, filename):
        json_str = json.dumps(data, indent=2)
        b64 = base64.b64encode(json_str.encode()).decode()
        href = f'<a href="data:application/json;base64,{b64}" download="{filename}">📥 Download Trip Summary (JSON)</a>'
        return href
    
    st.markdown(create_download_link(trip_summary, f"trip_summary_{selected_destination.replace(', ', '_')}.json"), unsafe_allow_html=True)
    
    # Create PDF-style report
    report_data = []
    report_data.append(f"TravelEase Trip Summary")
    report_data.append(f"======================")
    report_data.append(f"Destination: {selected_destination}")
    report_data.append(f"Departure: {departure_date}")
    report_data.append(f"Duration: {duration} days")
    report_data.append(f"Travelers: {travelers}")
    report_data.append(f"Flight Class: {flight_class}")
    report_data.append(f"Hotel Rating: {hotel_rating}")
    report_data.append(f"Total Cost: ${total_cost:.2f}")
    report_data.append(f"Cost Per Person: ${total_cost/travelers:.2f}")
    report_data.append(f"Highlights: {selected_row['Highlights']}")
    
    report_text = "\n".join(report_data)
    
    st.download_button(
        label="📋 Download Trip Report (TXT)",
        data=report_text,
        file_name=f"trip_report_{selected_destination.replace(', ', '_')}.txt",
        mime="text/plain"
    )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: white; padding: 2rem;">
    <h4>✈️ TravelEase - Making Travel Dreams Come True</h4>
    <p>Contact us: info@travelease.com | Phone: +1-800-TRAVEL</p>
    <p>Follow us on social media for travel inspiration and deals!</p>
</div>
""", unsafe_allow_html=True)

# Sidebar additional features
with st.sidebar:
    st.markdown("---")
    st.header("🔧 App Features")
    
    if st.button("🔄 Refresh Data"):
        st.rerun()
    
    # Export destinations data
    csv = df_destinations.to_csv(index=False)
    st.download_button(
        label="📊 Download Destinations Data (CSV)",
        data=csv,
        file_name="destinations_data.csv",
        mime="text/csv"
    )
    
    # Weather widget (simulated)
    st.header("🌤️ Weather Update")
    if st.button("Get Weather Forecast"):
        weather_data = LLMTasks.WeatherForecast(country, duration, departure_date.strftime("%Y-%m-%d"))

        st.text_area("Weather Forecast", weather_data, height=300)

