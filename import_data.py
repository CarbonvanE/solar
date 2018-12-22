""" Imports all the initial data from the API to the database """
import json
import requests

with open('solar/secrets.json', 'r') as f:
    DATA = json.load(f)
    API_KEY = DATA['SOLAREDGE']['API_KEY']
    SITE_ID = DATA['SOLAREDGE']['SITE_ID']


def get_average(values, index_range):
    if len(values) >= index_range:
        index_to_set = int(-(index_range + 1) / 2)
        total = 0.0
        for i in range(-index_range, 0):
            total += values[i]['p_q']
        avg = round(total / index_range, 3)
        return avg


def get_power_quarterly():
    time = 'startTime=2018-11-19%2000:00:00&endTime=2018-12-19%2000:00:00'
    url = f'https://monitoringapi.solaredge.com/site/{SITE_ID}/power?{time}&api_key={API_KEY}'
    response = requests.get(url)
    all_values = []
    if response.status_code == 200:
        data = json.loads(response.content)
        data = data['power']['values']
        for datum in data:
            date, time = datum['date'].split(' ')
            y, m, d = date.split('-')
            h, min, s = time.split(':')
            avg_power = (0.000 if datum['value'] is None else round(datum['value'], 3))
            data = {'y': y, 'm':m, 'd':d, 'h': h, 'min': min, 's': s, 'p_q': avg_power}
            all_values.append(data)
            # get_average(all_values, 5)
            if len(all_values) >= 5:
                all_values[-3]['p_1'] = get_average(all_values, 5)
            if len(all_values) >= 13:
                all_values[-7]['p_3'] = get_average(all_values, 13)
            if len(all_values) >= 97:
                all_values[-49]['p_24'] = get_average(all_values, 97)
            if len(all_values) >= 673:
                all_values[-337]['p_7'] = get_average(all_values, 673)
            if len(all_values) >= 1441:
                all_values[-721]['p_30'] = get_average(all_values, 1441)
        for i in all_values:
            # print(i)
            try:
                print(i['p_1'], ';', i['p_3'], ';', i['p_24'], ';', i['p_7'])
            except:
                print('')
    else:
        print(response.status_code)


if __name__ == "__main__":
    get_power_quarterly()
