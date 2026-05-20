import paho.mqtt.client as mqtt  # MQTT 통신(발행/구독)을 위한 라이브러리
import requests                  # 외부 웹 서버(API)와 HTTP 통신을 하여 데이터를 가져오기 위한 라이브러리

# 1. OpenWeatherMap API 통신 설정
# 기상청 역할을 하는 OpenWeatherMap 서버에 접근하기 위한 개인 고유 발급 열쇠(API KEY)
API_KEY = "ENTER_YOUR_API_KEY"
# 접속할 URL 조립 (q=Seoul: 서울 날씨 요청, appid={API_KEY}: 내 인증키, units=metric: 섭씨온도 기준)
url = f"https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={API_KEY}&units=metric"

# 2. MQTT 수신 콜백 함수 정의 (노트북에서 명령이 도착했을 때 자동 실행됨)
def on_message(client, userdata, msg):
    # 노트북에서 넘어온 바이트(Byte) 형태의 메시지를 읽을 수 있는 문자열(utf-8)로 디코딩
    text = msg.payload.decode('utf-8')
    print("\n수신된 명령: " + text)
   
    # 수신된 문자열이 "날씨"인지 조건문으로 확인
    if "날씨" in text:
        print("OpenWeatherMap API 정보를 불러옵니다...")
        try:
            # 설정해둔 url로 HTTP GET 요청을 보내 응답 객체를 받아옴
            response = requests.get(url)
            # 받아온 응답 객체의 내용을 다루기 쉬운 딕셔너리 형태의 JSON 데이터로 변환함
            data = response.json()
            # JSON 데이터 구조 안에서 ["main"] 그룹에 있는 현재 기온["temp"] 숫자를 추출함
            temp = data["main"]["temp"]
            # JSON 데이터 구조 안에서 ["main"] 그룹에 있는 현재 습도["humidity"] 숫자를 추출함
            humi = data["main"]["humidity"]
            # 노트북으로 보낼 직관적인 한국어 문장을 조립함 (int(temp)를 통해 소수점 온도를 정수로 깔끔하게 자름)
            msg_text = f"현재 서울의 기온은 {int(temp)}도, 습도는 {humi}퍼센트 입니다."
            print("전송할 내용:", msg_text) # 라즈베리파이 화면에도 로그로 띄워줌
            # 완성된 문장 데이터를 브로커의 "weather_info" 토픽으로 발행(Publish)함 -> 노트북으로 전송됨
            client.publish("weather_info", msg_text)
            print("-> 노트북으로 날씨 데이터를 전송했습니다.")
           
        # API 통신에 실패하거나 JSON 구조가 달라 에러가 발생했을 때 프로그램이 뻗지 않도록 예외 처리
        except Exception as e:
            print("API 요청 또는 데이터 처리 중 에러 발생:", e)

# 3. MQTT 클라이언트 기본 설정
# 서버 역할을 명확히 알 수 있도록 고유한 ID("PiWeatherServer")를 부여함
client = mqtt.Client(client_id="PiWeatherServer")
# 메시지가 도착했을 때 실행할 콜백 함수를 위에서 만든 on_message 함수로 매핑함
client.on_message = on_message
# 라즈베리파이 내부(자기 자신)에서 백그라운드로 돌고 있는 Mosquitto 브로커에 접속함 (127.0.0.1 = 자기 자신)
client.connect("127.0.0.1") 
# 노트북이 명령을 보낼 채널인 "voice_weather" 토픽을 구독(Subscribe)
client.subscribe("voice_weather", 1)

print("날씨 요청 대기 중...")
try:
    # 메인 스레드 통신 루프 유지
    # 프로그램이 종료되지 않도록 무한히 멈춰서(Blocking) 네트워크 수신 대기 상태를 유지함
    client.loop_forever()
    
# 사용자가 Ctrl+C를 눌러 강제 종료를 시도하면 안전하게 빠져나감
except KeyboardInterrupt:
    pass
