# 항해일지 [미니 프로젝트]

![issue badge](https://img.shields.io/github/issues/player31-kks/logBook)
![star badge](https://img.shields.io/github/stars/Joon-Kim-Lang/kiosk_spring_project)
![forks badge](https://img.shields.io/github/forks/player31-kks/logBook)

> ### 99일간의 항해를 위한 항해일지를 작성한다.!!
>
> <br>

## Team

- **금교석** : Full-Stack
  - `back & front`
  - `AWS deploy`
- **김남석** : Back-end
  - `MongoDB management `
  - `python,Flask Server`
- **임다빈** : Front-end
  - `client ajax management `
  - `html,css, javascript,jquery`

## Environment

- **python**
- **Flask**
- **Mongodb**
- **JWT**
- **html css javascript jquery**

## Description

## flow chart

## client

### 1. 로그인 페이지

- 회원 가입
- 로그인 하기(JWT 사용)

 <img src="https://user-images.githubusercontent.com/57718605/109966693-e55fd880-7d33-11eb-8464-5028b4ff6cd9.png" width="250" height="300">
 <img src="https://user-images.githubusercontent.com/57718605/109966809-06282e00-7d34-11eb-8a2b-493ac70e07bd.png" width="250" height="300">
 <img src="https://user-images.githubusercontent.com/57718605/109966693-e55fd880-7d33-11eb-8464-5028b4ff6cd9.png" width="250" height="300">

### 2. 메인 페이지

- 로그아웃
- 마이페이지
- 친구 등록,조회,삭제
- 개인별 99개의 상세페이지 이동 및 친구 메인페이지 이동

<img src="https://user-images.githubusercontent.com/57718605/109966987-3a9bea00-7d34-11eb-837e-d65b88f0744b.png" width="400" height="300">
<img src="https://user-images.githubusercontent.com/57718605/109966987-3a9bea00-7d34-11eb-837e-d65b88f0744b.png" width="400" height="300">

### 3. 상세 페이지

- 이전페이지 다음페이지 이동
- 개인 메인페이지 이동
- 글작성, 이미지 upload (본인꺼만)
- 좋아요, 및 삭제기능 (본인꺼만)

<img src="https://user-images.githubusercontent.com/57718605/109967390-b007ba80-7d34-11eb-9b96-30337c455c57.png" width="500" height="300">

## Server

### mongoDB

- 친구 collections : 내 이메일, 친구 이메일
- 회원 collections : 이름,이메일,생년월일,비밀번호(hash)
- 이미지 맵 collections : 99개의 해당하는 이미지 좌표값
- 카드 collections : 작성자 개정,일차,좋아요,이미지 url,글 작성 목록

### flask

- jwt를 이용한 회원정보 인증관리
- hash함수를 이용한 암호화 복호화
- jinja2를 이용한 render templates
- Restful API 관리

### JSON

- ajax json 요청처리
- json 데이터 전송
