import pandas as pd


def bouwplan_2022():
    excel_data = pd.read_excel("./app/data/bouwplan_26_01_2022.xlsx")
    df = pd.DataFrame(excel_data)
    df = df.fillna('')
    df = df.to_dict(orient="records")
    return df
