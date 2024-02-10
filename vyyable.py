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

def get_google_trends_data(keywords, timeframe='today 12-m'):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(keywords, timeframe=timeframe)
    interest_over_time_df = pytrends.interest_over_time()

    related_queries_dict = {}
    for keyword in keywords:
        pytrends.build_payload([keyword], timeframe=timeframe)
        related_queries_dict[keyword] = pytrends.related_queries()[keyword]['top']

    return interest_over_time_df, related_queries_dict

def plot_trends(interest_over_time_df):
    plt.figure(figsize=(10, 6))
    for column in interest_over_time_df.columns:
        plt.plot(interest_over_time_df.index, interest_over_time_df[column], label=column)

    plt.title('Google Trends Over Time')
    plt.xlabel('Date')
    plt.ylabel('Interest')
    plt.legend()
    st.pyplot()

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
