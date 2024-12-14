# requests: HTTP 요청을 보내기 위한 라이브러리로, 서버에서 데이터를 가져오거나 보내는 데 사용합니다.
import requests
# datetime이란 현재 날짜와 시간을 가져오거나 조작하는 데 사용되는 표준 라이브러리입니다.
from datetime import datetime
# xmltodict이란 XML 형식의 데이터를 Python 딕셔너리(사전)로 변환하는 데 사용하는 라이브러리입니다.
import xmltodict

# 현재 날짜를 'yyyymmdd' 형식으로 반환하는 함수입니다. 현재 날짜를 가져와서 yyyymmdd 형식의 문자열로 반환합니다.
# API 요청 시 기준 날짜를 전달하기 위해 사용됩니다. 예시로는 현재 날짜가 2024년 12월 14일이라면, 함수는 '20241214'을 반환합니다.
# 사용 이유로는 기상청 API는 날짜를 반드시 yyyymmdd 형식으로 요구하기 때문입니다.
def get_current_date_string():
# 현재 시스템 날짜를 가져옵니다.
    current_date = datetime.now().date()
# '20241214' 같은 형식의 문자열로 변환합니다.
    return current_date.strftime("%Y%m%d")

# 현재 시간을 'hhmm' 형식으로 반환하는 함수입니다.
# 기상청 API의 'base_time'은 30분 간격으로 요청해야 합니다.
# 예를 들어, 10:00, 10:30, 11:00 등 형식으로 요청해야 유효한 응답을 받을 수 있습니다.
# 현재 시간을 'hhmm' 형식으로 반환하되, 기상청 API가 요구하는 30분 단위로 조정합니다.
def get_current_hour_string():
  
    now = datetime.now()
# 현재 분이 45분 미만이면 이전 시간의 데이터를 사용합니다.
    if now.minute < 45:  
        if now.hour == 0:
# 현재 분이 45분 미만이면 이전 시간의 데이터를 사용합니다.
            base_time = "2330" 
        else:
            pre_hour = now.hour - 1
# 이전 시간을 2자리 숫자로 포맷합니다.
            base_time = f"{pre_hour:02}30"  
    else:
# 현재 시간을 2자리 숫자로 포맷합니다.
        base_time = f"{now.hour:02}30"  

    return base_time

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
def forecast():

    keys = '발급한 키'  # 사용자가 발급받은 API 키 입력
# 기상청 초단기 실황 API의 URL(공식 문서에서 제공된 API URL) 입니다.
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'
    params = {
        'serviceKey': keys, 
        'pageNo': '1', 
        'numOfRows': '1000', 
        'dataType': 'XML', 
        'base_date': get_current_date_string(), 
        'base_time': get_current_hour_string(), 
        'nx': '55', 
        'ny': '127'
    }

# requests 라이브러리를 사용하여 HTTP GET 요청을 보냅니다.
# params는 API 호출에 필요한 모든 파라미터를 포함합니다.
    res = requests.get(url, params=params)

    # 요청 결과를 XML 형식에서 딕셔너리로 변환
    xml_data = res.text

    # XML 데이터를 Python 딕셔너리로 변환합니다.
    # xmltodict를 사용하면 XML 노드가 딕셔너리의 키-값 형태로 변환되어 편리하게 데이터 접근 가능합니다.
    dict_data = xmltodict.parse(xml_data)

    # 날씨 데이터 초기화
    weather_data = {}
    try:
        # 응답 데이터에서 'items' 항목의 'item' 리스트를 순회하며 필요한 데이터를 추출합니다.
        for item in dict_data['response']['body']['items']['item']:
            category = item['category']
            value = item['fcstValue']
        
            if category == 'T1H': 
                weather_data['tmp'] = value
            elif category == 'REH':  # 습도
                weather_data['hum'] = value
            elif category == 'SKY':  # 하늘 상태
                weather_data['sky'] = value
            elif category == 'PTY':  # 강수 형태
                weather_data['sky2'] = value
    except KeyError:
        print("데이터를 불러오는 데 문제가 발생했습니다. 응답 형식을 확인하세요.")

    return weather_data

#  날씨 데이터를 가공하여 사람이 읽을 수 있는 문자열로 반환합니다.

def proc_weather():
   
    dict_sky = forecast()

    # 하늘 상태와 강수 형태를 결합하여 표현합니다.
    str_sky = "서울 "
    if 'sky' in dict_sky or 'sky2' in dict_sky:
        str_sky += "날씨 : "
        sky = dict_sky.get('sky', None)
        sky2 = dict_sky.get('sky2', None)

        if sky2 == '0':  # 강수 없음
            if sky == '1':
                str_sky += "맑음"
            elif sky == '3':
                str_sky += "구름많음"
            elif sky == '4':
                str_sky += "흐림"
        elif sky2 == '1':
            str_sky += "비"
        elif sky2 == '2':
            str_sky += "비와 눈"
        elif sky2 == '3':
            str_sky += "눈"
        elif sky2 == '5':
            str_sky += "빗방울이 떨어짐"
        elif sky2 == '6':
            str_sky += "빗방울과 눈이 날림"
        elif sky2 == '7':
            str_sky += "눈이 날림"
        str_sky += "\n"

    # 기온 정보 추가
    if 'tmp' in dict_sky:
        str_sky += f"온도 : {dict_sky['tmp']}ºC \n"

    # 습도 정보 추가
    if 'hum' in dict_sky:
        str_sky += f"습도 : {dict_sky['hum']}%"

    return str_sky

# 최종 출력
print(proc_weather())

