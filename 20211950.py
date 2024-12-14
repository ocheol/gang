import requests
import json

# API 키와 기본 설정
apikey = "39ce00f348bab0f4c0a86507d1fc762d"
city = "Seoul"
lang = "kr"

# API URL 생성
api = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&lang={lang}&units=metric"

# API 요청 및 JSON 데이터 변환
result = requests.get(api)
data = json.loads(result.text)

# 날씨 데이터 출력
print(data["name"], "의 날씨입니다.")
print("날씨는 ", data["weather"][0]["description"], "입니다.")
print("현재 온도는 ", data["main"]["temp"], "입니다.")
print("하지만 체감 ", data["main"]["feels_like"], "일 거에요.")
print("최저 기온은 ", data["main"]["temp_min"], "입니다.")
print("최고 기온은 ", data["main"]["temp_max"], "입니다.")
print("습도는 ", data["main"]["humidity"], "입니다.")
print("기압은 ", data["main"]["pressure"], "입니다.")
print("풍향은 ", data["wind"]["deg"], "입니다.")
print("풍속은 ", data["wind"]["speed"], "입니다.")

# 날씨 상태에 따른 메시지 출력
# 날씨 설명 가져오기
weather_description = data["weather"][0]["description"]

# 날씨 상태에 따른 메시지 출력
if "비" in weather_description:
    print("비가 와요. 우산을 챙겨주세요!")
elif "눈" in weather_description and "비" in weather_description:
    print("비 또는 눈이 와요. 따뜻하게 입고 우산을 챙기세요!")
elif "눈" in weather_description:
    print("눈이 와요. 장갑을 꼭 챙기세요!")
else:
    print("날씨가 좋네요!")
