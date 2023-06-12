from flask import Flask, render_template, request
import sqlite3
import pandas as pd
import numpy as np

def process_data(age, gender, machine_learning_data):
    # SQLite 데이터베이스에 연결
    conn = sqlite3.connect('foodDB.db')

    # 중량을 100으로 맞추는 작업
    query = "SELECT * FROM food_table"
    food_data = pd.read_sql_query(query, conn)

    food_data['비율'] = 100 / food_data['중량(g)']

    numeric_columns = food_data.columns.drop(['음식명', '중량(g)', '비율'])
    food_data[numeric_columns] = food_data[numeric_columns].mul(food_data['비율'], axis=0)

    food_data['중량(g)'] = 100

    food_data.drop('비율', axis=1, inplace=True)

    # 머신러닝을 통해 받은 데이터와 '음 식 명' 컬럼 값을 비교하여 해당하는 영양 성분을 가져오고 더하기
    result = pd.Series(dtype=float)

    for item in machine_learning_data:
        food_name = item['음식명']
        food_amount = item['음식량']

        # 머신러닝 데이터와 '음 식 명' 컬럼 값 비교
        match = food_data[food_data['음식명'] == food_name]

        if not match.empty:
            # 머신러닝 데이터와 매칭된 영양 성분을 가져와 더하기
            match_values = match.iloc[:, 2:].values.flatten()
            match_values *= food_amount

            result = result.add(pd.Series(match_values), fill_value=0)

    # 연결 종료
    conn.close()