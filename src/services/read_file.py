import pandas as pd
from datetime import datetime

from src.utils.generator import generate_subscription


def processing_file():
    df_customer = pd.read_csv(
        'C:\\Users\\argfh\\PycharmProjects\\telmark-quiros-test\\src\\resource\\maven_music_customers.csv')
    df_history = pd.read_excel(
        'C:\\Users\\argfh\\PycharmProjects\\telmark-quiros-test\\src\\resource\\maven_music_listening_history.xlsx')
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
    print(df_customer.dtypes)
