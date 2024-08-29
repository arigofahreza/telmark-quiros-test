import math

import numpy as np
import pandas as pd
from datetime import datetime

from src.utils.generator import generate_subscription


def processing_file():
    df_customer = pd.read_csv(
        'C:\\Users\\Arigo\\PycharmProjects\\telmark-quiros-test\\src\\resource\\maven_music_customers.csv')
    df_customer['email_clean'] = df_customer['Email'].str.replace('Email: ', '')
    df_customer['Discount?'] = df_customer['Discount?'].fillna('No')
    df_customer['Subscription Plan'] = df_customer['Subscription Plan'].fillna('')
    df_customer['formatted_member_since'] = df_customer['Member Since'].apply(
        lambda x: datetime.strptime(x, "%m/%d/%y").strftime("%Y-%m-%d"))
    df_customer['clean_subscription_rate'] = df_customer['Subscription Rate'].apply(lambda x: float(x.replace('$', '')))
    df_customer[['Subscription Plan', 'clean_subscription_rate', 'Discount?']] = df_customer.apply(
        lambda x: generate_subscription(x['Subscription Plan'], x['clean_subscription_rate'], x['Discount?']),
        axis=1, result_type='expand')
    df_customer['clean_subscription_rate'] = df_customer['clean_subscription_rate'].apply(lambda x: f"{x:.2f}")
    df_customer['Cancellation Date'] = df_customer['Cancellation Date'].fillna('')
    df_customer['formatted_cancellation_date'] = df_customer['Cancellation Date'].apply(
        lambda x: datetime.strptime(x, "%m/%d/%y").strftime("%Y-%m-%d") if x else '1900-01-01')

    df_history = pd.read_excel(
        'C:\\Users\\Arigo\\PycharmProjects\\telmark-quiros-test\\src\\resource\\maven_music_listening_history.xlsx',
        sheet_name='listening_history')

    data_count = aggregate_count(df_history)
    data_duration = aggregate_min_max(df_history)

    agg_df = pd.merge(data_count, data_duration, on='Customer ID')
    print(agg_df)

    df_audio = pd.read_excel(
        'C:\\Users\\Arigo\\PycharmProjects\\telmark-quiros-test\\src\\resource\\maven_music_listening_history.xlsx',
        sheet_name='audio_files')
    df_audio['Audio ID'] = df_audio['ID'].str.extract(r'(\d+)')
    df_audio['Audio ID'] = df_audio['Audio ID'].astype(int)
    details_df = pd.merge(agg_df, df_audio, on='Audio ID')

    finals_df = pd.merge(df_customer, details_df, on='Customer ID')
    print(finals_df)


def aggregate_count(df_history):
    category_count = df_history.groupby(['Customer ID', 'Audio ID']).size().reset_index(name='Count')
    most_played = category_count.loc[category_count.groupby('Customer ID')['Count'].idxmax()]
    return most_played


def aggregate_min_max(df_history):
    df_session = pd.read_excel(
        'C:\\Users\\Arigo\\PycharmProjects\\telmark-quiros-test\\src\\resource\\maven_music_listening_history.xlsx',
        sheet_name='session_login_time')
    df_session['Session Log In Time'] = pd.to_datetime(df_session['Session Log In Time'])

    df_merged = pd.merge(df_history, df_session, on='Session ID')

    customer_login_times = df_merged.groupby('Customer ID').agg({'Session Log In Time': ['min', 'max']})

    customer_login_times['Total Duration'] = customer_login_times['Session Log In Time']['max'] - \
                                             customer_login_times['Session Log In Time']['min']
    customer_login_times['Total Duration'] = np.floor(
        customer_login_times['Total Duration'].dt.total_seconds() / 3600).astype(int)
    customer_login_times.columns = customer_login_times.columns.droplevel(0)
    customer_login_times = customer_login_times.reset_index()
    customer_login_times = customer_login_times.rename(columns={'': 'Total Duration'})

    return customer_login_times[['Customer ID', 'Total Duration']]
