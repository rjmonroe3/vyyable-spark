"""
# My first app
Here's our first attempt at using data to create a table:
"""
from datetime import datetime
from datetime import timedelta
import numpy as np
from dateutil.relativedelta import *
import streamlit as st
from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import pandas as pd
import time

def get_google_trends_data(keywords, timeframe='today 12-m'):
    pytrends = TrendReq(hl='en-US', tz=360)

    max_retries = 5
    backoff_factor = 2
    sleep_time = 5  # Starting sleep time in seconds

    interest_over_time_df = None
    related_queries_dict = {}

    for attempt in range(max_retries):
        try:
            pytrends.build_payload(keywords, timeframe=timeframe)
            interest_over_time_df = pytrends.interest_over_time()

            for keyword in keywords:
                time.sleep(sleep_time)  # Delay between requests
                pytrends.build_payload([keyword], timeframe=timeframe)
                related_queries = pytrends.related_queries()
                if related_queries and keyword in related_queries:
                    related_queries_dict[keyword] = related_queries[keyword]['top']

            return interest_over_time_df, related_queries_dict

        except Exception as e:
            st.error(f"Request failed, attempt {attempt + 1} of {max_retries}. Retrying in {sleep_time} seconds.")
            time.sleep(sleep_time)
            sleep_time *= backoff_factor  # Exponential backoff

    st.error("Failed to fetch data from Google Trends after several attempts.")
    return None, None

def plot_trends(interest_over_time_df):
    plt.figure(figsize=(10, 6))
    for column in interest_over_time_df.columns:
        plt.plot(interest_over_time_df.index, interest_over_time_df[column], label=column)

    plt.title('Google Trends Over Time')
    plt.xlabel('Date')
    plt.ylabel('Interest')
    plt.legend()
    st.pyplot(fig)

def display_related_keywords(related_queries_dict):
    st.subheader('Related Keywords:')
    for keyword, related_keywords in related_queries_dict.items():
        st.write(f"Related to {keyword}: {', '.join(related_keywords)}")

def main():
    st.title('Google Trends Search with Streamlit and Pytrends')

    # User input for keywords
    keyword1 = st.text_input('Enter Keyword 1:', '')
    keyword2 = st.text_input('Enter Keyword 2:', '')
    keywords = [keyword1, keyword2]

    if st.button('Search Trends'):
        st.info('Fetching data... Please wait.')
        
        # Get Google Trends data
        interest_over_time_df, related_queries_dict = get_google_trends_data(keywords)

        # Display trends graph
        plot_trends(interest_over_time_df)

        # Display related keywords
        display_related_keywords(related_queries_dict)

         # Add reset button
        if st.button('Reset'):
            st.experimental_rerun()

if __name__ == '__main__':
    main()