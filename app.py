import csv
import json

from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask,  request, jsonify
import pandas as pd
import chonburi

response = ''

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route("/res", methods=["GET", "POST"])
def hello():

    global response
    global responsing
    if request.method == "POST":
        request_data = request.data
        request_data = json.loads(request_data.decode('utf-8'))
        data = request_data["res"]
        for i in data.keys():
            x = i
            print(x)
            break
        json_data = data[x]
        csv_file = open("chonburi_new_user.csv", 'w', encoding='utf8', newline='')
        csv_writer = csv.writer(csv_file)
        count = 0
        for element in json_data:
            if count == 0:
                header = element.keys()
                csv_writer.writerow(header)
                count += 1
            csv_writer.writerow(element.values())
        csv_file.close()

        old_user = chonburi.df_person
        new_user = chonburi.pd.read_csv("chonburi_new_user.csv")
        new_user.columns = ['เพศ', 'อายุ', 'การศึกษา', 'อาชีพ', 'รายได้', 'สถานภาพ', 'เที่ยวบ่อย', 'เที่ยวกับ','ช่วงเวลา','ประเภทสถานที่','การใช้เงิน',]
        col_names = ['เพศ', 'อายุ', 'การศึกษา', 'อาชีพ', 'รายได้', 'สถานภาพ', 'เที่ยวบ่อย', 'เที่ยวกับ', 'ช่วงเวลา', 'ประเภทสถานที่', 'การใช้เงิน']
        dummies_df_new_user = pd.get_dummies(new_user[col_names])

        new_user = pd.concat([new_user, dummies_df_new_user], axis=1)

        new_user = new_user.drop(col_names, axis=1)
        all_user = old_user.append(new_user, ignore_index=True, sort=False)
        all_user = all_user.fillna(0)
        place = chonburi.df_place
        x = cosine_similarity(all_user)
        we = chonburi.travel_reccomender(df_all=all_user, df_place=place, x_user=x, user_ix=-1, k=5, top_n=5).index
        sr = pd.Series(we)
        result = sr.to_json(force_ascii=False)
        response = f'{result}'
        return ""
    else:
        return response




if __name__ ==  "__main__":
    app.run(debug=True)