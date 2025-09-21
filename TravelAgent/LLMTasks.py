import pandas as pd
# Conceptual Example: Parallel Execution
from google.adk.agents import ParallelAgent, LlmAgent
from google import genai

import warnings
warnings.filterwarnings("ignore")
# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()


def CurateItinerary(profile, destination, days, role, budget):
    prompt = f"Curate an {profile} itinerary for {destination} for {days} days with a budget of {budget}. Curate this itinerary for a {role} traveler."
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
    )
    return response.text


def WeatherForecast(location, days, travel_date):
    prompt = f"Provide a detailed weather forecast for {location} for the next {days} days starting from {travel_date}. Include temperature highs and lows, precipitation chances, and any significant weather events."
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
    )
    return response.text

'''

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Curate an adventure travel itinerary for Japan for 5 days with a budeget of 2500 per couple."
)
print("Response from Gemini:\n", response.text)
'''