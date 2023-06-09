# internetProgrammingFinalProject
교과목 중 하나인 인터넷 프로그래밍 기말 프로젝트입니다.

초콜릿을 주제로 한 쇼핑몰을 제작하였습니다.
<br> 

## 개발 기간
* 22년 12월 16일 - 22년 12월 19일

## 개발 환경
- `Python 3.10`
- **IDE**: PyCharm 2022.2.1
- **Framework**: Django 3.2
- **Database** : Sqlite3
- 부트스트랩을 사용하였습니다.

## 웹 사이트 구성
- 홈 페이지
- 상품 목록 페이지
- 상품 상세 페이지
- My 페이지
- 회사 소개 페이지

## 주요 기능
#### 회원가입
- 이메일로 회원가입을 할 수 있습니다.
#### 로그인
- 구글 계정, 이메일, 네이버 계정으로 로그인할 수 있습니다.
#### 상품 목록 페이지에서의 상품 보여주기
- 게시된 순서대로 상품을 보여줍니다.
- 상품명, 카테고리, 상품이미지, 가격, 간단한 설명 등을 보여줍니다.
- 모든 카테고리에 대한 정보를 보여주고, 카테고리 페이지와 연결합니다.
- 모든 제조사에 대한 정보를 보여주고, 제조사 페이지와 연결합니다. 
- 상품 목록은 여러 페이지에 나눠 보여줍니다. (Pagnation)
#### 상품 상세 페이지에서의 상품 보여주기
- 모든 카테고리에 대한 정보를 보여주고, 카테고리 페이지와 연결합니다.
- 모든 제조사에 대한 정보를 보여주고, 제조사 페이지와 연결합니다. 

#### 상품 등록, 상품 수정
- 로그인한 superuser와 staff만 상품을 등록할 수 있습니다.
- crispy-form으로 폼을 작성할 수 있습니다.

#### 댓글
- 로그인한 모든 사용자는 댓글을 작성할 수 있습니다.
- 댓글을 작성한 사용자만 댓글을 수정할 수 있습니다. 
- 댓글을 작성한 사용자만 댓글을 삭제할 수 있습니다.
- 모달창으로 삭제를 확인한 후 댓글을 삭제할 수 있습니다.

#### 상품 검색
- 상품명으로 제품을 검색할 수 있습니다.

#### 아바타 보여주기
- 로그인 사용자와 댓글 작성자의 아바타를 보여줍니다.

#### 홈 페이지의 기능
- 쇼핑몰을 대표할 수 있는 이미지와 멘트를 보여줍니다.
- 최근 게시된 상품 3개를 이미지, 상품명, 가격 등과 함께 보여줍니다. 

#### 회사 소개 페이지의 기능
- 쇼핑몰에 대한 소개를 보여줍니다.
- 상품에 대한 통계정보를 모달창으로 보여줍니다.

#### My 페이지의 기능
- 로그인한 사용자만 접근 가능합니다.
- 사용자의 username과 이메일을 보여줍니다.
- 사용자가 작성한 댓글을 보여줍니다. 댓글을 클릭하면 댓글이 달린 상품 상세 페이지로 이동합니다.

#### Markdown
- 상품의 상세한 설명을 Markdown으로 작성할 수 있습니다.

#### 장바구니 기능
- 로그인한 사용자만 가능합니다.
- My 페이지에서 찜한 상품의 목록을 확인할 수 있습니다. 




