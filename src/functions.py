import pandas as pd

def bmi_encoding(df):
    df['bmi'] = df['bmi'].fillna(df['bmi'].mode().iloc[0])
    df["bmi"] = df["bmi"].apply(lambda x: 31.0 if x == '>=30' else x)
    df["bmi"] = df["bmi"].apply(lambda x: 18.0 if x == '<19' else x)
    df["bmi"] = df["bmi"].apply(lambda x: 26.0 if x == '>=25' else x)  # it belongs to overweight
    df["bmi"] = df["bmi"].apply(lambda x: 31 if x == '>=30' else x)
    df = df.astype({'bmi': 'float'})
    df['bmi'] = df.bmi.apply(lambda bmi: 'Underweight' if bmi < 18.5 else ('Normal' if bmi < 25 else (
        'Overweight' if bmi < 30 else 'Obese')))
    return df


if __name__ == '__main__':
    # Due to run problems with streamlit, we store for bmi beforehand.
    df = pd.read_csv('data/data_unprocessed.csv', index_col=0)
    df_demographics = df.groupby('id').first()
    df_bmi = bmi_encoding(pd.DataFrame(df_demographics['bmi']))
    df_bmi.to_csv('./data/df_bmi.csv')
    df_bmi_eng = bmi_encoding(pd.DataFrame(df))
    df_bmi_eng.to_csv('./data/df_bmi_eng.csv')
