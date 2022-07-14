# cafe_mogakco
# 1W 미니 웹프로젝트
## 프로젝트명 
- 모각코GOGO
    - 모각코: 모여서 각자 코딩

## 소개
- 모각코하기 좋은 국내 카페 리스트를 공유하고 후기를 나누는 사이트

## 와이어 프레임
- 메인 페이지 (로그인 전)
![](https://velog.velcdn.com/images/sangjin0/post/9b72c807-93f8-40f9-ae65-a3ac8ccacd6b/image.png)
- 로그인, 회원가입 페이지
![](https://velog.velcdn.com/images/sangjin0/post/b7ec9492-e855-4bcc-85c2-c03ad8123ce0/image.png)
- 메인 페이지 (로그인 후)
![](https://velog.velcdn.com/images/sangjin0/post/89140c9e-2108-4a84-850d-2cbbeae80b60/image.png)
- 글 작성 페이지
![](https://velog.velcdn.com/images/sangjin0/post/089fc281-3ea6-4cb1-be39-81aa0b2392d5/image.png)
- 정리
![](https://velog.velcdn.com/images/sangjin0/post/71eaa1b8-dece-4bdc-8a6a-7d59472e8edf/image.png)


## 개발해야 하는 기능 

### 유저 /user
- 회원 가입 
    - POST
    - /user/signup
    - request
    ```json
    {
     'email' : email, 
     'password' : password
     'name': name
    }
    ```
    - response
- 로그인 
    - POST
    - /user/login
    - request
    ```json
    {
     'email' : email, 
     'password' : password
    }
    ```
    - response

- 정보 수정 
    - PUT
    - /user
    - request
    ```json
    {
     'password' : password,
     'name': name
    }
    ```
    - response
- 내 프로필 
    - GET
    - /user/info
    - response

- 회원 탈퇴
    - DELETE
    - /user
    - response



### 게시글(카페 공유글) /board
- 게시글 작성
    - POST
    - /board
    - request
    - response
- 게시글 수정
    - PUT
    - /board/:id
    - request
    - response
- 게시글 삭제 
    - DELETE
    - /board/:id
    - request
    - response
- 게시글 목록 조회 
    - GET
    - /board
    - request
    - response

- 게시글 상세 조회
    - GET
    - /board/:id
    - request
    - response

### 댓글(후기) /comment

- 댓글 작성
    - POST
    - /comment
    - request
    - response
- 댓글 수정
    - PUT
    - /comment/:id
    - request
    - response
- 댓글 삭제 
    - DELETE
    - /comment/:id
    - request
    - response
- 댓글 조회 
    - GET
    - /comment
    - request
    - response

## github
https://github.com/sangjin-park89/cafe_mogakco
## 참고
[모각코 API 정리 내용](https://docs.google.com/spreadsheets/d/1toCprd5em9synSTaCoqakpUgBr1GsA4yYSV1byeiHQ4/edit#gid=0)
