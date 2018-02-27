import pandas as pd
import requests, json


def get_score(data_file='测试数据_0201'):
    api = 'http://103.28.215.253:10170/demo/intelliTrain/makeScore.do'
    data = pd.read_excel(data_file + '.xlsx')
    headers = {
        'Content-Type': 'text/plain;charset=UTF-8'
    }
    for idx, row in data.iterrows():
        keys = [s for s in row['必答关键句'].split('；')]
        weight = [1] * len(keys)
        params = {
            "question": "",
            "stdAnswer": row['参考答案'],
            "userAnswer": row['客户回答'],
            "strictKeys": [
                {"sentence": k, "weight": w} for k, w in zip(keys, weight)
            ],
            "looseKeys": [
                {"sentence": None, "weight": 1}
            ]
        }
        res = requests.post(api, data=json.dumps(params), headers=headers).json()
        try:
            scoreTotal = res['resp']['scoreTotal']
        except KeyError:
            scoreTotal = -1

        print(scoreTotal)
        data.set_value(idx, '最后得分', scoreTotal)

    writer = pd.ExcelWriter(data_file + '_output.xlsx')
    data.to_excel(writer, 'Sheet1', index=False)
    writer.save()


if __name__ == '__main__':
    get_score()