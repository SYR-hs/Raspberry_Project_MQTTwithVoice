# Raspberry_Project_MQTTwithVoice

소스코드는 각각 노트북ver_날씨.py, 라즈베리ver_날씨.py 파일에 정리되어 있습니다.

음성인식 시연 영상 링크: https://youtu.be/UHX83wy6cI4
----

# 추가적으로 찾아본 내용

## 📚 참고 자료 및 추가 학습 (References & Learnings)

본 프로젝트를 진행하며 오디오 제어 및 통신 아키텍처 구축을 위해 참고한 주요 자료와 이를 통해 파생된 추가 학습 내용.

### 1. 파이썬 음성 합성(TTS) 엔진 아키텍처 비교
Reference: [Speech engines with python tutorial - Pythonspot](https://pythonspot.com/speech-engines-with-python-tutorial/)

학습 내용: 파이썬 환경에서 구동 가능한 대표적인 TTS 엔진들의 작동 방식과 장단점을 비교 분석하여, 본 프로젝트 환경에 가장 적합한 엔진을 선정하는 데 참고.

`pyttsx3`: (본 프로젝트 노트북 노드에 적용) 오프라인 환경에서 동작하며 Mac, Windows, Linux 크로스 플랫폼을 지원. (로컬 연산)

`espeak`: 라즈베리파이와 같은 리눅스 환경에서 가볍게 동작하는 기본 명령어 기반 TTS 도구입니다.

`gTTS (Google TTS)`: 구글 클라우드 기반으로 매우 자연스러운 사람의 음성을 제공하지만, API 호출을 위해 상시 인터넷 연결이 필수적이라는 차이점을 확인.

### 2. 터미널 기반 챗봇의 Web GUI 확장 가능성 확인
Reference: [Streamlit, PyAudio, SpeechRecognition, pyttsx3로 간단한 대화형 챗봇 만들어서 배포하기 (Velog)](https://velog.io/@koominji/python-streamlit-pyaudio-speechrecognition-pyttsx3-%EB%A1%9C-%EA%B0%84%EB%8B%A8%ED%95%9C-%EB%8C%80%ED%99%94%ED%98%95-%EC%B1%97%EB%B4%87-%EB%A7%8C%EB%93%A4%EC%96%B4%EC%84%9C-%EB%B0%B0%ED%8F%AC%ED%95%98%EA%B8%B0)

학습 내용: 현재 터미널 백그라운드 환경에서 동작하는 STT/TTS 시스템을 한 단계 발전시켜, 파이썬 기반 웹 프레임워크인 `Streamlit`을 활용해 사용자 친화적인 웹 UI를 입히는 방법론을 참고하였습니다. 향후 이 프로젝트를 로컬 터미널 제어에서 웹 브라우저 기반 대화형 AIoT 인터페이스로 고도화할 수 있는 방향성을 확보.

### 3. 음성 인식(STT) 환경 구축 및 트러블슈팅
Reference: [Python 기반 음성 인식 기술 블로그 (Naver Blog)](https://blog.naver.com/rlrkcka/223573566887)

학습 내용: 로컬 PC 환경에 `PyAudio` 및 마이크 제어 모듈을 설치하는 과정에서 발생할 수 있는 컴파일 에러, 패키지 의존성 문제를 해결하기 위한 커뮤니티 트러블슈팅 노하우 및 실무적인 파이썬 환경 설정 예제를 참고.
