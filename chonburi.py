import json

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv('C:\project\chonburi.csv')


df.columns = ['Timestamp', 'เพศ', 'อายุ', 'การศึกษา', 'อาชีพ', 'รายได้',
       'สถานภาพ',
       'เที่ยวบ่อย',
       'เที่ยวกับ',
       'ช่วงเวลา',
       'ประเภทสถานที่',
       'การใช้เงิน',
       'เกาะแสมสาร',
       'เขาระเบิด',
       'น้ำตกชันตาเถร',
       'แกรนด์แคนยอนคีรี',
       'สวนนงนุช',
       'เกาะล้าน',
       'ปราสาทสัจธรรม',
       'ชุมชนตะเคียนเตี้ย',
       'วัดญาณสังวรารามวรมหาวิหาร',
       'เขาชีจรรย์',
       'ถ้ำลอดมหาจักรพรรดิ์',
       'ตลาดน้ำสี่ภาคพัทยา',
       'สวนน้ำ Cartoon Network',
       'Pattaya Shooting Park',
       'พิพิธภัณฑ์ริบลีส์',
       'Papa Beach Pattaya',
       'ทิฟฟานี่โชว์',
       'Austin café',
       '331 bar & coffee war',
       'พิพิธภัณฑ์เกาะและทะเลไทย',
       'สถาบันวิทยาศาสตร์ทางทะเล',
       'พิพิธภัณฑ์ภาพจิตกรรม 3 มิติ' ]



df.drop('Timestamp', axis='columns', inplace=True)
#df.drop('เพศ', axis='columns', inplace=True)

df_person = df[['เพศ', 'อายุ', 'การศึกษา', 'อาชีพ', 'รายได้','สถานภาพ','เที่ยวบ่อย','เที่ยวกับ','ช่วงเวลา','ประเภทสถานที่','การใช้เงิน']]
#print(df_person)
df_place = df[[ 'เกาะแสมสาร',
       'เขาระเบิด',
       'น้ำตกชันตาเถร',
       'แกรนด์แคนยอนคีรี',
       'สวนนงนุช',
       'เกาะล้าน',
       'ปราสาทสัจธรรม',
       'ชุมชนตะเคียนเตี้ย',
       'วัดญาณสังวรารามวรมหาวิหาร',
       'เขาชีจรรย์',
       'ถ้ำลอดมหาจักรพรรดิ์',
       'ตลาดน้ำสี่ภาคพัทยา',
       'สวนน้ำ Cartoon Network',
       'Pattaya Shooting Park',
       'พิพิธภัณฑ์ริบลีส์',
       'Papa Beach Pattaya',
       'ทิฟฟานี่โชว์',
       'Austin café',
       '331 bar & coffee war',
       'พิพิธภัณฑ์เกาะและทะเลไทย',
       'สถาบันวิทยาศาสตร์ทางทะเล',
       'พิพิธภัณฑ์ภาพจิตกรรม 3 มิติ']]

#print(df_place)
df_new_user = pd.read_csv('C:\project\chonburi_new_user.csv')
#df_new_user.drop('เพศ', axis='columns', inplace=True)
df_new_user.columns = ['เพศ', 'อายุ', 'การศึกษา', 'อาชีพ', 'รายได้',
       'สถานภาพ',
       'เที่ยวบ่อย',
       'เที่ยวกับ',
       'ช่วงเวลา',
       'ประเภทสถานที่',
       'การใช้เงิน',]

col_names = ['เพศ', 'อายุ', 'การศึกษา', 'อาชีพ', 'รายได้','สถานภาพ','เที่ยวบ่อย','เที่ยวกับ','ช่วงเวลา','ประเภทสถานที่','การใช้เงิน']

dummies_df_person = pd.get_dummies(df_person[col_names])
#print(dummies_df_person)

df_person = pd.concat([df_person, dummies_df_person], axis=1)

df_person = df_person.drop(col_names, axis=1)
#print(df_person)

dummies_df_new_user = pd.get_dummies(df_new_user[col_names])

df_new_user = pd.concat([df_new_user, dummies_df_new_user], axis=1)

df_new_user = df_new_user.drop(col_names, axis=1)
#print(df_new_user)

df_all = df_person.append(df_new_user, ignore_index=True, sort=False)
#print(df_all)

df_all = df_all.fillna(0)
#print(df_all)

x_user = cosine_similarity(df_all)
#print(x_user)
#print(x_user[-1].round(2))


def travel_reccomender(df_all, df_place, x_user, user_ix=-1, k=403, top_n=10):
    user_similarities = x_user[user_ix]

    most_similar_users = df_all.index[user_similarities.argpartition(-k)[-k:]]
    most_similar_users = most_similar_users[:-1]
    #print(most_similar_users)

    rec_place = df_place.iloc[most_similar_users].mean(0).sort_values(ascending=False)
    rec_place_top = rec_place.head(top_n)
    print(rec_place_top)

    return rec_place_top


travel_reccomender(df_all, df_place, x_user, user_ix=-1, k=6, top_n=6)
