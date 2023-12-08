import pandas as pd


def prepare_data(df):
    df.rename(columns={'PAY_0': 'PAY_1', 'default.payment.next.month': 'default'}, inplace=True)
    df.drop('ID', axis=1, inplace=True)

    df['bill_amt_mean'] = df[['BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6']] \
        .mean(axis=1)
    df['bill_amt_std'] = df[['BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6']].std(axis=1)
    df['pay_amt_mean'] = df[['PAY_AMT1', 'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6']].mean(axis=1)
    df['pay_amt_sum'] = df[['PAY_AMT1', 'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6']].mean(axis=1)
    df['pay_amt_std'] = df[['PAY_AMT1', 'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6']].std(axis=1)
    df['pay_limit'] = df['PAY_AMT1'] / df['LIMIT_BAL']

    # all PAY columns = 0, -1, -2 mean payments without delay
    df[(df['PAY_1'] == -1) | (df['PAY_1'] == -2)] = 0
    df[(df['PAY_2'] == -1) | (df['PAY_2'] == -2)] = 0
    df[(df['PAY_3'] == -1) | (df['PAY_3'] == -2)] = 0
    df[(df['PAY_4'] == -1) | (df['PAY_4'] == -2)] = 0
    return df
