import pandas as pd
import sqlite3

# Read csv file.
df = pd.read_csv("평균 칼로리, 영양성분.csv", encoding='cp949')

# Map CSV columns to Django 모델 fields
column_mapping = {
    "나이 범위": "age",
    "성별": "gender",
    "칼로리 (kcal)": "calorie",
    "탄수화물 (g)": "carbohydrates",
    "단백질 (g)": "protein",
    "지방 (g)": "fat",
    "당류 (g) 이하": "sugar",
    "나트륨 (mg) 이하": "sodium",
}


df = df.rename(columns=column_mapping)

df['id'] = range(1, len(df) + 1)


database = "db.sqlite3"
conn = sqlite3.connect(database)


df.to_sql(name='sprintapp_nutritiondata', con=conn, if_exists='replace', index=True)


conn.close()

df = pd.read_csv("foodDB.csv", encoding='cp949')

# Map CSV columns to Django 모델 fields
column_mapping = {
    "음 식 명": "name",
    "중량(g)": "weight",
    "에너지(kcal)": "calorie",
    "탄수화물(g)": "carbohydrates",
    "단백질(g)": "protein",
    "지방(g)": "fat",
    "당류(g)": "sugar",
    "나트륨(mg)": "sodium",
}


df = df.rename(columns=column_mapping)

df['id'] = range(1, len(df) + 1)


database = "db.sqlite3"
conn = sqlite3.connect(database)


df.to_sql(name='sprintapp_fooddata', con=conn, if_exists='replace', index=True)


conn.close()
