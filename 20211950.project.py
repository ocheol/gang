# requests: HTTP 요청을 보내기 위한 라이브러리로, 서버에서 데이터를 가져오거나 보내는 데 사용합니다.
import requests

# datetime이란 현재 날짜와 시간을 가져오거나 조작하는 데 사용되는 표준 라이브러리입니다.
from datetime import datetime

# xmltodict이란 XML 형식의 데이터를 Python 딕셔너리(사전)로 변환하는 데 사용하는 라이브러리입니다.
import xmltodict

# 현재 날짜를 'yyyymmdd' 형식으로 반환하는 함수입니다. 현재 날짜를 가져와서 yyyymmdd 형식의 문자열로 반환합니다.
# API 요청 시 기준 날짜를 전달하기 위해 사용됩니다. 예시로는 현재 날짜가 2024년 12월 14일이라면, 함수는 '20241214'을 반환합니다.
# 사용 이유로는 기상청 API는 날짜를 반드시 yyyymmdd 형식으로 요구하기 때문입니다.
def get_current_date():
# 현재 시스템 날짜를 가져옵니다.
    current_date = datetime.now().date()  
# '20241214' 같은 형식의 문자열로 변환합니다.
    return current_date.strftime("%Y%m%d")  

# 현재 시간을 'hhmm' 형식으로 반환하는 함수입니다.
# 기상청 API의 'base_time'은 30분 간격으로 요청해야 합니다.
# 예를 들어, 10:00, 10:30, 11:00 등 형식으로 요청해야 유효한 응답을 받을 수 있습니다.
def get_current_hour():
# 현재 시스템 시간을 가져옵니다.
    now = datetime.now()  
# '1045' 같은 형식으로 시간과 분 반환
    return datetime.now().strftime("%H%M")  

# 강수 형태를 나타내는 숫자 코드를 사람이 읽을 수 있는 텍스트로 변환하기 위한 딕셔너리입니다.
int_to_weather = {
    "0": "맑음",        # 강수 없음
    "1": "비",         # 비가 오는 상태
    "2": "비/눈",      # 비와 눈이 섞여서 내리는 상태
    "3": "눈",         # 눈이 오는 상태
    "5": "빗방울",      # 가볍게 빗방울이 떨어지는 상태
    "6": "빗방울눈날림", # 빗방울과 눈이 흩날리는 상태
    "7": "눈날림"       # 눈이 흩날리는 상태
}

# 초단기 실황 데이터를 요청하고 결과를 처리하는 함수입니다.

#   기상청 초단기 실황 데이터를 가져오는 함수입니다.
#   입력된 API 파라미터를 이용해 서버에서 데이터를 요청한 후, 결과를 처리하여 온도와 날씨 상태를 반환합니다.
#   매개변수 params는 dict로 API 호출에 필요한 요청 파라미터를 포함하는 딕셔너리
#   반환값은 tuple(현재 온도, 날씨 상태) 예를 들어 ('15', '맑음')과 같은 형식으로 반환됩니다.
#   처리 과정
#   1. 기상청 API URL로 HTTP GET 요청을 보냅니다.
#   2. XML 형식의 응답 데이터를 가져옵니다.
#   3. XML 데이터를 Python 딕셔너리로 변환합니다.
#   4. 필요한 데이터('T1H'와 'PTY')를 추출합니다.
#   5. 'PTY' 코드를 텍스트로 변환하여 결과를 반환합니다.
def forecast(params):
    # 기상청 초단기 실황 API의 URL(공식 문서에서 제공된 API URL) 입니다.
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'

    # requests 라이브러리를 사용하여 HTTP GET 요청을 보냅니다.
    # params는 API 호출에 필요한 모든 파라미터를 포함합니다.
    res = requests.get(url, params)
    
    # API 서버로부터 받은 응답 데이터를 XML 형식의 텍스트로 저장합니다.
    xml_data = res.text
    
    # XML 데이터를 Python 딕셔너리로 변환합니다.
    # xmltodict를 사용하면 XML 노드가 딕셔너리의 키-값 형태로 변환되어 편리하게 데이터 접근 가능합니다.
    dict_data = xmltodict.parse(xml_data)

    # 딕셔너리에서 필요한 데이터('T1H'와 'PTY')를 추출하기 위한 반복문입니다.
    for item in dict_data['response']['body']['items']['item']:
        # 'T1H'는 현재 온도를 나타냅니다
        if item['category'] == 'T1H':
        # 현재 온도를 저장합니다.
            temp = item['obsrValue']  
        # 'PTY'는 강수 형태를 나타냅니다.
        if item['category'] == 'PTY':
        # 강수 형태를 코드로 저장합니다.
            sky = item['obsrValue']  
    # 강수 형태 코드(sky)를 사람이 읽을 수 있는 텍스트로 변환합니다.
    sky = int_to_weather[sky]
    
    # 최종적으로 온도와 날씨 상태를 튜플 형태로 반환합니다.
    return temp, sky

# 기상청 API 호출 시 필요한 인증 키 (기상청에서 발급) 입니다.
keys = '%2FLqgJiy2ddbDwCCO5BbKA1Rq%2FYUounM0%2B%2FTw2%2F94WPbRQGjxODuySL46A8V10U%2F2XHIjlVFdefSCvysQ8WON7w%3D%3D'

# API 호출에 필요한 모든 요청 파라미터를 딕셔너리 형태로 구성합니다.
params = {
# 기상청에서 발급받은 API 인증 키입니다.
    'serviceKey': keys,          
# 조회할 페이지 번호, 기본적으로 첫 페이지를 요청합니다.
    'pageNo': '1',               
# 조회할 데이터의 개수입니다. 
    'numOfRows': '10',            
# 응답 데이터의 형식(XML 또는 JSON 중 선택) 입니다.
    'dataType': 'XML',            
# 기준 날짜 (yyyymmdd 형식)입니다.
    'base_date': get_current_date(),  
# 기준 시간 (hhmm 형식, 30분 단위로 제공됨) 입니다.
    'base_time': get_current_hour(),  
# 조회할 지역의 격자 X 좌표 (서울: 55) 입니다.
    'nx': '55',                   
 # 조회할 지역의 격자 Y 좌표 (서울: 127) 입니다.
    'ny': '127'                  
}

# 위에서 정의한 forecast 함수를 호출하여 온도와 날씨 데이터를 가져옵니다.
 # API 응답으로부터 데이터를 받아 처리합니다.
forecast_data = forecast(params)  
# 결과를 출력합니다.
print(f"현재 온도: {forecast_data[0]}°C, 현재 날씨: {forecast_data[1]}")  
