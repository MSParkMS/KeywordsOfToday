# KeywordsOfToday

## 개발 환경 설정 (처음)
1. Python3 설치
2. git clone https://github.com/MSParkMS/KeywordsOfToday.git
3. 생성된 폴더에 들어가서 `python -m venv env`
    * [about venv](https://docs.python.org/ko/3/tutorial/venv.html)
4. `env\scripts\activate.bat` (가상환경 실행)
5. `python -m pip install --upgrade pip` (최신 pip 설치)
6. `pip install -r requirements.txt` (requirements.txt에 기록되어 있는 패키지들 설치)
7. `env\scripts\deactivate.bat` (가상환경 종료)

## 평소 개발 흐름
1. `env\scripts\activate.bat` (가상환경 실행)
2. 추가된 패키지가 있을 경우 `pip install -r requirements.txt` (requirements.txt에 기록되어 있는 패키지들 설치)
    * 설치시 pip 버전 업그레이드가 필요할 시 `python -m pip install --upgrade pip` (최신 pip 설치)
3. 개발
4. `env\scripts\deactivate.bat` (가상환경 종료)

## 패키지 추가
1. 가상환경 실행 상태에서 패키지 인스톨
2. `pip freeze > requirements.txt` (requirements.txt에 현재 패키지 정보들을 기록)
3. requirements.txt 파일을 올림
