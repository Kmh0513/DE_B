from bs4 import BeautifulSoup

html = """
<option value="(주) 금성오토텍" >(주) 금성오토텍</option>
<option value="(주) 금성정공 2공장" >(주) 금성정공 2공장</option>
<option value="(주) 세원이엔아이" >(주) 세원이엔아이</option>
<option value="(주) 제이브엠" >(주) 제이브엠</option>
<option value="(주)YMP" >(주)YMP</option>
<option value="(주)고려자동차" >(주)고려자동차</option>
<option value="(주)금성정공" >(주)금성정공</option>
<option value="(주)동선씨에스" >(주)동선씨에스</option>
<option value="(주)동신유압" >(주)동신유압</option>
<option value="(주)마이크로컴퓨팅" >(주)마이크로컴퓨팅</option>
<option value="(주)세양" >(주)세양</option>
<option value="(주)알앤유" >(주)알앤유</option>
<option value="(주)우리텍" >(주)우리텍</option>
<option value="(주)우성케미칼" >(주)우성케미칼</option>
<option value="(주)우성케미칼 제2공장" >(주)우성케미칼 제2공장</option>
<option value="(주)원하이테크" >(주)원하이테크</option>
<option value="(주)제이에스글로벌" >(주)제이에스글로벌</option>
<option value="(주)제이에스테크" >(주)제이에스테크</option>
<option value="(주)중앙테크" >(주)중앙테크</option>
<option value="(주)진양 오일씰" >(주)진양 오일씰</option>
<option value="(주)창림이엔지" >(주)창림이엔지</option>
<option value="(주)케이메디칼" >(주)케이메디칼</option>
<option value="(주)퓨쳐스테크놀러지" >(주)퓨쳐스테크놀러지</option>
<option value="(주)한주정공" >(주)한주정공</option>
<option value="HS테크" >HS테크</option>
<option value="JYS태양광발전소" >JYS태양광발전소</option>
<option value="KTS(주)" >KTS(주)</option>
<option value="가야산업" >가야산업</option>
<option value="경진기계(주)" >경진기계(주)</option>
<option value="금성" >금성</option>
<option value="금성산업" >금성산업</option>
<option value="금오특수프라스틱" >금오특수프라스틱</option>
<option value="뉴텍디에스" >뉴텍디에스</option>
<option value="다안테크" >다안테크</option>
<option value="대구 솔라시티 주식회사" >대구 솔라시티 주식회사</option>
<option value="대안산업" >대안산업</option>
<option value="도양산업" >도양산업</option>
<option value="도진산업" >도진산업</option>
<option value="동국정밀(주)" >동국정밀(주)</option>
<option value="동진정밀" >동진정밀</option>
<option value="레송무역" >레송무역</option>
<option value="부성회사" >부성회사</option>
<option value="비젼테크" >비젼테크</option>
<option value="삼정에이엔피" >삼정에이엔피</option>
<option value="세양" >세양</option>
<option value="세종산업" >세종산업</option>
<option value="세진테크" >세진테크</option>
<option value="승리자동차상사" >승리자동차상사</option>
<option value="승보오토 모티브(주)" >승보오토 모티브(주)</option>
<option value="신세기산업" >신세기산업</option>
<option value="신일전자 공업사" >신일전자 공업사</option>
<option value="에이치씨에이에스 주식회사 구미지점" >에이치씨에이에스 주식회사 구미지점</option>
<option value="에프씨에스코리아" >에프씨에스코리아</option>
<option value="영원산업" >영원산업</option>
<option value="용산프라스틱" >용산프라스틱</option>
<option value="우석이엔지" >우석이엔지</option>
<option value="우성정공" >우성정공</option>
<option value="우영테크" >우영테크</option>
<option value="원일정공" >원일정공</option>
<option value="월드트렌드" >월드트렌드</option>
<option value="유림테크" >유림테크</option>
<option value="이안테크" >이안테크</option>
<option value="인성산업" >인성산업</option>
<option value="일신프라스틱(주)" >일신프라스틱(주)</option>
<option value="재원 모델" >재원 모델</option>
<option value="재원테크" >재원테크</option>
<option value="정화이엠에스 주식회사" >정화이엠에스 주식회사</option>
<option value="제이에스 파워테크" >제이에스 파워테크</option>
<option value="주식회사 대영알앤티" >주식회사 대영알앤티</option>
<option value="주식회사 부광정밀" >주식회사 부광정밀</option>
<option value="주식회사 오토라이팅" >주식회사 오토라이팅</option>
<option value="주식회사 제이씨티" >주식회사 제이씨티</option>
<option value="주식회사디케이" >주식회사디케이</option>
<option value="주은산업" >주은산업</option>
<option value="진성산업" >진성산업</option>
<option value="창영정밀주식회사" >창영정밀주식회사</option>
<option value="칸토 디자인" >칸토 디자인</option>
<option value="케이알 무역" >케이알 무역</option>
<option value="태승화학" >태승화학</option>
<option value="퍼지텍(주)" >퍼지텍(주)</option>
<option value="하나정밀금형" >하나정밀금형</option>
<option value="한국전력공사" >한국전력공사</option>
<option value="한양테크" >한양테크</option>
<option value="진양오일씰" >진양오일씰</option>
<option value="태광폴리머" >태광폴리머</option>
<option value="신성알엔피" >신성알엔피</option>
<option value="영진소재" >영진소재</option>
<option value="KTR" >KTR</option>
<option value="크라이버그티피이코리아" >크라이버그티피이코리아</option>
<option value="삼박LFT" >삼박LFT</option>
<option value="BASF" >BASF</option>
<option value="성덕케미컬" >성덕케미컬</option>
<option value="우성폴리머" >우성폴리머</option>
<option value="오성금속" >오성금속</option>
<option value="라임TEST" >라임TEST</option>
<option value="주식회사 다담" >주식회사 다담</option>
<option value="한화 토탈" >한화 토탈</option>
<option value="test" >test</option>
<option value="삼성전자" >삼성전자</option>
<option value="신성델타테크" >신성델타테크</option>
<option value="팬케미칼" >팬케미칼</option>
<option value="(주)한국티알" >(주)한국티알</option>
<option value="두남화학" >두남화학</option>
<option value="대영알엔티" >대영알엔티</option>
<option value="(주)다담" >(주)다담</option>
<option value="구남산업" >구남산업</option>
<option value="모아테크" >모아테크</option>
<option value="한국포장" >한국포장</option>
<option value="대구 비닐" >대구 비닐</option>
<option value="이엔지폴리머" >이엔지폴리머</option>
<option value="세원이엔아이" >세원이엔아이</option>
<option value="타이코에이엠피(TE)" >타이코에이엠피(TE)</option>
<option value="(주)티케이" >(주)티케이</option>
<option value="LG화학" >LG화학</option>
<option value="롯데케미칼" >롯데케미칼</option>
"""

soup = BeautifulSoup(html, 'html.parser')
options = soup.find_all('option')
company_names = [option.text.strip() for option in options]
print(company_names)