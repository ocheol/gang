import requests

url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"
params = {
    'serviceKey':' %2FLqgJiy2ddbDwCCO5BbKA1Rq%2FYUounM0%2B%2FTw2%2F94WPbRQGjxODuySL46A8V10U%2F2XHIjlVFdefSCvysQ8WON7w%3D%3D',
    'pageNo': '1',
    'numOfRows': '10',
    'dataType': 'XML',
    'base_date': '20241214',
    'base_time': '1430',
    'nx': '55',
    'ny': '127'
}

res = requests.get(url, params)
print(res.status_code)
print(res.text)

