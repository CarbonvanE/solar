import requests, json

with open('solar/secrets.json', 'r') as f:
    API_KEY = json.load(f)['SOLAREDGE']['API_KEY']

with open('solar/secrets.json', 'r') as f:
    SITE_ID = json.load(f)['SOLAREDGE']['SITE_ID']

def get_power_quarterly():
    time = 'startTime=2018-09-01%2000:00:00&endTime=2018-10-01%2000:00:00'
    url = f'https://monitoringapi.solaredge.com/site/{SITE_ID}/power?{time}&api_key={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.content)
        data = data['power']['values']
        for d in data:
            date, time = d['date'].split(' ')
            year, month, day = date.split('-')
            hour, minute, second = time.split(':')
            avg_power = d['value']
            print(year, month, day, hour, minute, second, avg_power)
    else:
        print(response.status_code)


if __name__ == "__main__":
    get_power_quarterly()
