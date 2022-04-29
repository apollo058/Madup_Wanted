![image](https://user-images.githubusercontent.com/88444944/165882989-e44d606f-3c62-468d-b21a-e8794ee2dd28.png)


# Wanted team_B #1매드업 기업과제



주어진 데이터 셋을 요구사항 대로 서빙하기 위한 관계형 데이터베이스 테이블을 설계하고,

주어진 기능을 제공하는 REST API 서버를 개발합니다.



## Team process:

|성명|업무|비고|
|------|---|---|
|최승리|Dockerize / 기획|팀장⭐ |
|하정현|test code 설계 / 작성 및 test|.|
|남기윤|앱 필수 기능 구현|.|

## Directory Info.
```
├─amounts              -amount django앱 디렉토리
│  ├─migrations
│  │  └─__pycache__
│  ├─tests             -amount app 테스트코드소스
│  │  ├─inputs
│  │  └─test_tools
│  └─__pycache__
├─clients              -client django앱 디렉토리
│  ├─migrations
│  │  └─__pycache__
│  ├─tests             -amount app 테스트코드소스
│  │  ├─inputs
│  │  └─test_tools
│  └─__pycache__
└─madup                -django 프로젝트 실행 파일 디렉토리
    └─__pycache__
```


## MADUP dev. 요구사항

* 필수 개발조건
  * 테이블 인덱스 설정
  * REST API를 지원하는 웹 프레임워크 사용
  * 테스트코드 작성
  * API기능만 구현
  * RESTful 하게 구현(Endpoint URL, HTTP Method)
  * Response는 JSON 형식으로 리턴
  * SQL Alchemy, Peewee, Django ORM, JPA, Hibernate 등 ORM 을 사용하고, Raw 는 사용할 수 없음.

* 구현할 시 가산점
  * 요구된 사항만 구현되는 서버가 아니라, 다른 많은 기능이 함께 있는 서버라고 생각하고, 폴더, 파일, 코드 스트럭처의 짜임새를 정리
  * DB migration tool 사용 시 가산점
  * Dockerize

## MADUP project 요구사항
* 시작 후 72내 제출
* 광고주의 정보를 담을 수 있는 테이블을 추가로 만들고, 그 광고주와 제공되는 데이터셋을 연결해서 광고주 CRUD기능 구현
* 광고주의 Unique ID와 기간으로 검색해 해당 광고주의 매체별 CTR,ROAS,CPC,CVR,CPA 리턴

```
#출력 예시
2 "naver": {
3 "ctr": 0.51,
4 "cpc": 990.55,
5 "roas": 265.38,
6 "cvr": 8.33,
7 "cpa": 881.01
8 },
9 "facebook": {
10 "ctr": 0.51,
11 "cpc": 990.55,
12 "roas": 265.38,
13 "cvr": 8.33,
14 "cpa": 881.01
15 },
```

## API info.

### 광고주 정보 CRUD api
* CREATE : 광고주의 기업명, 담당자, 연락처, 주소, 상세주소를 입력받아 저장합니다.
![image](https://user-images.githubusercontent.com/88444944/165883858-c67ab3af-7726-4e67-b48a-0be599c1842a.png)

* READ : 저장되어있는 전체 광고주 정보를 보여줍니다.
![image](https://user-images.githubusercontent.com/88444944/165883982-d9a6f944-364b-4e5a-a9a0-808671034e08.png)

* UPDATE : PK(id), 광고주의 기업명, 담당자, 연락처, 주소, 상세주소를 입력받아 수정합니다.
![image](https://user-images.githubusercontent.com/88444944/165884091-15686c8a-786c-4aed-84b6-db4db06dbe19.png)

* DELETE : PK(id) 를 입력받아 DB에서 삭제합니다
![image](https://user-images.githubusercontent.com/88444944/165884140-c997ad4a-9904-45c3-bcbc-13bc466a9fbf.png)

### 광고주의 매체별 CTR,ROAS,CPC,CVR,CPA 검색 api

* 광고주의 uid와 기간(시작일,종료일)을 입력받아 조회합니다.
![image](https://user-images.githubusercontent.com/88444944/165884250-a8865aa7-08d8-4230-8064-279d91383a89.png)

## DB info.
![매드업DB설계](https://user-images.githubusercontent.com/88444944/165886236-823e45fd-9a71-47ee-a51e-9bdd1b9e323c.png)

---

## Docker Compose 사용법

1. docker-compose.yml과 같은 경로에 `.env` 파일을 만든다.

2. `.env` 파일 설정
```
MYSQL_NAME = "madup"
MYSQL_HOST = "madup_db"
MYSQL_PORT = "3306"
MYSQL_ROOT_PASSWORD = root 패스워드
MYSQL_DATABASE = "madup"
MYSQL_USER = 컨테이너 DB_user name
MYSQL_PASSWORD = 컨테이너 DB_user password
MYSQL_LOCAL_PASSWORD = local root 패스워드
SECRET_KEY = django secret key
```
를 설정하고 저장한다.

3. docker-compose.yml 경로에서 `sudo docker-compose up -d`를 실행한다.


## wait-for-it.sh의 용도
![GitHub](https://github.com/apollo058/wait-for-it.git)
해당 스크립트의 용도는 `sudo docker-compose up -d` 명령어 실행시에 DB가 완전히 가동되기전 django migrate가 실행되는 것을 방지하기 위함입니다.
