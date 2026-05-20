import speech_recognition as sr  # 마이크 제어 및 음성 인식(STT)을 위한 라이브러리
import paho.mqtt.client as mqtt  # MQTT 통신(발행/구독)을 위한 라이브러리
import pyttsx3                   # 텍스트를 음성으로 변환(TTS)하여 스피커로 출력하기 위한 라이브러리

# 1. 텍스트 음성 변환(TTS) 엔진 초기화
engine = pyttsx3.init()  # 노트북의 스피커를 사용하기 위해 TTS 엔진 객체를 생성하고 초기화
# 2. MQTT 수신 콜백 함수 정의 (라즈베리파이의 응답이 도착했을 때 자동 실행)
def on_message(client, userdata, msg):
    # msg.payload에 담긴 바이트(Byte) 형태의 데이터를 읽을 수 있는 'utf-8' 문자열로 디코딩
    weather_text = msg.payload.decode('utf-8')
    # 디코딩된 날씨 문장을 터미널(화면)에 출력하여 확인
    print("\n[라즈베리파이 응답]: " + weather_text)
    # 수신된 문자열 텍스트를 노트북 스피커(음성)로 읽어주도록 TTS 엔진의 큐에 추가함
    engine.say(weather_text)
    # 큐에 추가된 음성 출력이 끝날 때까지 대기함 (말을 끝까지 하도록 보장)
    engine.runAndWait()

# 3. MQTT 클라이언트 기본 설정
broker_address = "xxx.xxx.xxx.xxx"  # 접속할 우체국(MQTT 브로커)인 라즈베리파이의 IP 주소
# 기기 간 충돌을 막기 위해 노트북 클라이언트만의 고유한 ID("Laptop_Node") 부여
client = mqtt.Client(client_id="Laptop_Node")
# 메시지가 도착했을 때(on_message 이벤트 발생) 실행할 함수를 위에서 만든 함수로 연결함
client.on_message = on_message
# 설정한 브로커 주소로 실제 네트워크 접속 시도
client.connect(broker_address)

# 4. 수신 대기 및 멀티스레딩 설정
# 라즈베리파이가 날씨 정보를 보내줄 채널인 "weather_info" 토픽을 구독(Subscribe)
client.subscribe("weather_info", 1)

# 백그라운드 네트워크 통신 스레드 시작
# 메인 루프(음성 인식)가 멈춰서 기다리는 동안에도 라즈베리파이의 응답을 놓치지 않고 비동기 수신하기 위함
client.loop_start() 

# 5. 메인 루프 (마이크 음성 인식 및 데이터 요청 발행)
try:
    while True: # 프로그램이 종료될 때까지 무한 반복
        r = sr.Recognizer()  # 음성을 인식하고 분석할 객체 생성
        
        with sr.Microphone() as source:  # 노트북에 내장된 기본 마이크를 입력 소스로 사용
            print("\n[대기 중] '날씨'라고 말씀해주세요 :")
            # 마이크가 켜진 직후 0.5초 동안 주변 소음(배경음)의 크기를 측정하여 인식 기준점을 자동으로 보정함
            r.adjust_for_ambient_noise(source, duration=0.5)
            # 사용자가 말하는 음성을 듣고 오디오 데이터(audio)로 메모리에 저장함 (이때 프로그램은 대기 상태)
            audio = r.listen(source)
            
        try:
            # 구글의 음성 인식 서버(API)로 오디오를 보내 한국어('ko-KR') 텍스트로 변환하여 받아옴
            text = r.recognize_google(audio, language='ko-KR')
            print("인식된 음성: [" + text + "]")  # 화면에 인식된 글자 출력
            # 인식된 텍스트 문자열 안에 "날씨"라는 단어가 포함되어 있는지 검사함
            if "날씨" in text:
                # "날씨"가 맞다면 브로커의 "voice_weather" 토픽으로 "날씨"라는 텍스트를 발행(Publish)함
                client.publish("voice_weather", "날씨")
                print("-> 라즈베리파이에 날씨 데이터를 요청했습니다.")
                
        # 음성을 들었으나 무슨 말인지 판별하지 못한 경우 발생하는 예외 처리
        except sr.UnknownValueError:
            print("음성을 인식하지 못했습니다.")
        # 구글 서버 장애나 와이파이 단절 등으로 API 접속에 실패한 경우 발생하는 예외 처리
        except sr.RequestError as e:
            print(f"네트워크 에러 발생: {e}")

# 터미널에서 사용자가 Ctrl+C를 눌러 강제 종료(KeyboardInterrupt) 신호를 보낸 경우
except KeyboardInterrupt:
    client.loop_stop()  # 백그라운드에서 돌고 있던 네트워크 수신 스레드를 안전하게 종료함
    client.disconnect() # MQTT 브로커와의 접속을 끊고 프로그램을 마침
