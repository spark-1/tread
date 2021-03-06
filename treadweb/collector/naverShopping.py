import math
import urllib.request
from datetime import datetime, timedelta
from dateutil import parser

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'}

class NaverShopping:
    # 쇼핑 카테고리를 한글로 입력하면 categoryID로 변환하여 리턴하는 함수
    # https://shopping.naver.com/  에 접속 후 카테고리 더보기에서 카테고리 이름 확인할 수 있음
    # 남 / 여 공통으로 있는 카테고리의 경우 여성은 '여성 '을 남성은 '남성 '을 추가해서 입력해야함.   ex) '티셔츠' -> '여성 티셔츠' or '남성 티셔츠'
    def getCategoryID(self, name):
        categoryID = {'패션의류': '50000000', '여성의류': '50000167', '여성 니트/스웨터': '50000805', '여성 카디건': '50000806',
                      '여성 원피스': '50000807', '여성 티셔츠': '50000803', '여성 블라우스/셔츠': '50000804', '여성 점퍼': '50000814',
                      '여성 재킷': '50000815', '여성 코트': '50000813', '여성 청바지': '50000809', '여성 스커트': '50000808',
                      '여성 레깅스': '50000812', '여성 바지': '50000810', '여성 트레이닝복': '50000818', '여성 조끼': '50000817',
                      '여성 정장세트': '50000816', '남성의류': '50000169', '남성 니트/스웨터': '50000831', '남성 티셔츠': '50000830',
                      '남성 셔츠/남방': '50000833', '남성 카디건': '50000832', '남성 점퍼': '50000837', '남성 재킷': '50000838',
                      '남성 코트': '50000839', '남성 청바지': '50000835', '남성 바지': '50000836', '남성 조끼': '50000834',
                      '남성 정장세트': '50000840', '남성 트레이닝복': '50000841', '여성 언더웨어/잠옷': '50000168', '여성 브라': '50000823',
                      '여성 팬티': '50000824', '여성 브라팬티세트': '50000825', '여성 보정속옷': '50001452', '여성 잠옷/홈웨어': '50000826',
                      '여성 슬립': '50000827', '여성 러닝/캐미솔': '50000828', '여성 속치마/속바지': '50000829', '여성 시즌성내의': '50001453',
                      '여성 언더웨어소품': '50001454', '남성 언더웨어/잠옷': '50000170', '남성 팬티': '50000845', '남성 러닝': '50000846',
                      '남성 러닝팬티세트': '50000847', '남성 잠옷/홈웨어': '50000848', '남성 보정속옷': '50001455', '남성 시즌성내의': '50001456',
                      '여성신발': '50000173', '여성 부츠': '50001462', '여성 부티': '50000779', '여성 워커': '50001461',
                      '여성 단화': '50001459', '여성 힐/펌프스': '50001460', '여성 운동화': '50001463', '여성 실내화': '50000781',
                      '지갑': '50000179', '머니클립': '50000661', '여성지갑': '50001471', '남성지갑': '50001472', '카드/명함지갑': '50000662',
                      '동전지갑': '50000664', '남성신발': '50000174', '남성 운동화': '50001466', '남성 부츠': '50000792',
                      '남성 워커': '50000791', '남성 모카신/털신': '50000784', '남성 스니커즈': '50000788', '남성 구두': '50000787',
                      '남성 실내화': '50000666', '시계': '50000186', '패션시계': '50001487', '아동시계': '50000426', '커플시계': '50000425',
                      '시계소품': '50001488', '시계수리용품': '50000435', '여성가방': '50000176', '여성 백팩': '50000644',
                      '여성 크로스백': '50000641', '여성 숄더백': '50000639', '여성 토트백': '50000640', '여성 파우치': '50000643',
                      '여성 클러치백': '50000642', '여성 힙색': '50000645', '여성 가방소품': '50001468', '주얼리': '50000189',
                      '반지': '50001489', '귀걸이': '50001490', '목걸이': '50001491', '펜던트': '50001492', '팔찌': '50001495',
                      '발찌': '50006174', '남성가방': '50000177', '백팩': '50000651', '크로스백': '50000648', '숄더백': '50000646',
                      '토트백': '50000647', '브리프케이스': '50000650', '클러치백': '50000649', '힙색': '50000652', '모자': '50000181',
                      '스냅백': '50001475', '베레모': '50006868', '야구모자': '50001474', '군모': '50000541', '비니': '50000543',
                    '귀달이모자': '50000548', '방울털모자': '50000549', '귀마개': '50000550', '여행용': '50000178', '하드캐리어': '50001469',
                    '소프트캐리어': '50001470', '보스턴가방': '50000653', '여행소품케이스': '50000658', '선글라스/안경테': '50000183',
                    '캐리어소품': '50005464', '캐리어커버': '50006908', '기타잡화': '50000185', '패션소품': '50000185', '스카프': '50001479',
                    '머플러': '50000565', '넥타이': '50001481', '넥워머': '50000566', '장갑': '50000182', '벨트': '50000180',
                    '양말': '50000166', '패션잡화': '50000001', '스킨케어': '50000190', '스킨/토너': '50000437', '로션': '50000438',
                    '에센스': '50000439', '크림': '50000440', '아이케어': '50000441', '넥케어': '50000342', '미스트': '50000442',
                    '마스크': '50000193', '마스크시트': '50000463', '필오프팩': '50000464', '워시오프팩': '50000465', '코팩': '50000466',
                    '수면팩': '50000467', '마사지크림/젤': '50000468', '마스크/팩세트': '50000469', '남성화장품': '50000202',
                    '선케어': '50000191', '선크림': '50000445', '선스프레이': '50000446', '선스틱': '50000447', '선파우더/쿠션': '50000448',
                    '태닝': '50001496', '애프터선': '50000449', '선케어세트': '50000450', '헤어케어': '50000198', '샴푸': '50000297',
                  '린스': '50000298', '트리트먼트': '50000299', '헤어에센스': '50000300', '헤어팩': '50000301', '헤어미스트': '50000302',
                  '두피케어': '50000303', '향수': '50000200', '베이스메이크업': '50000194', 'BB크림': '50000470', 'CC크림': '50000471',
                  '프라이머': '50000472', '메이크업베이스': '50000345', '파우더': '50001369', '트윈케이크': '50000346',
                  '파운데이션': '50001370', '헤어스타일링': '50000199', '헤어왁스': '50000306', '헤어스프레이': '50000307',
                  '헤어무스': '50000308', '헤어젤': '50000309', '헤어글레이즈': '50000310', '염색약': '50000311', '파마약': '50001372',
                  '뷰티소품': '50000201', '색조메이크업': '50000195', '립스틱': '50000391', '립케어': '50000392', '립글로스': '50000393',
                  '립틴트': '50000394', '립라이너': '50000395', '아이섀도': '50000396', '아이라이너': '50001371', '바디케어': '50000197',
                  '바디로션': '50000408', '바디크림': '50000281', '바디오일': '50000282', '바디미스트': '50000283', '바디파우더': '50000284',
                  '바디클렌저': '50000285', '데오드란트': '50000293', '클렌징': '50000192', '클렌징폼': '50000451', '클렌징오일': '50000452',
                  '클렌징크림': '50000453', '클렌징로션': '50000454', '클렌징젤': '50000455', '클렌징워터': '50000456',
                  '클렌징티슈': '50000457', '네일케어': '50000196', '매니큐어': '50000402', '네일아트': '50000403', '네일영양제': '50000404',
                  '네일리무버': '50000405', '네일케어도구': '50000406', '네일케어세트': '50000407', '화장품 / 미용': '50000002',
                  '휴대폰': '50000204', '휴대폰': '50000205', '휴대폰 케이스': '50001377', '휴대폰 보호필름': '50001378',
                  '휴대폰 배터리': '50001380', '휴대폰 충전기': '50001379', '계절가전': '50000212', '에어컨': '50001421',
                  '선풍기': '50001420', '냉풍기': '50001419', '제습기': '50001427', '가습기': '50001425', '공기정화기': '50001426',
                  '전기장판/담요/방석': '50001429', '전기매트': '50001428', '전기히터': '50001852', '온풍기': '50001422',
                  '노트북': '50000151', '카메라': '50000206', 'DSLR 카메라': '50000265', '미러리스 디카': '50000266',
                  '일반 디카': '50000267', '카메라 렌즈': '50001381', '생활가전': '50000210', '세탁기': '50001408', '청소기': '50001410',
                  '다리미': '50001411', '디지털 도어록': '50001412', '주방가전': '50000213', '냉장고': '50001430', '가스레인지': '50001305',
                  '전기밥솥': '50001306', '커피메이커': '50001708', '태블릿PC': '50000152', '영상가전': '50000208', 'TV': '50001395',
                  '프로젝터': '50001397', '영상플레이어': '50001399', '디지털 액자': '50002014', '음향가전': '50000209',
                  '홈시어터': '50001400', '이어폰': '50001976', '헤드폰': '50001977', '블루투스셋': '50001406', '이미용가전': '50000211',
                  '면도기': '50001417', '드라이어': '50001986', '매직기': '50001988', '피부케어기기': '50001995', 'PC': '50000089',
                  'PC주변기기': '50000094', '마우스': '50001203', '키보드': '50001204', '복합기': '50001206', '프린터': '50001207',
                  '저장장치': '50000096', '외장HDD': '50001600', '외장SSD': '50001601', 'SSD': '50001617', 'USB메모리': '50001615',
                  '게임': '50000088', '가정용 게임기': '50001733', '휴대용 게임기': '50001734', '게임 타이틀': '50001736',
                  'PC 게임': '50001735', '모니터': '50000153', 'PC부품': '50000097', 'CPU': '50001620', 'RAM': '50001218',
                  '그래픽카드': '50001219', '메인보드': '50001220', '네트워크': '50000098', '공유기': '50001226', '랜카드': '50001227',
                  '스위칭허브': '50001506', '블루투스동글': '50001504', '자동차기기': '50000214', '블랙박스/액세서리': '50001188',
                  '내비게이션/액세서리': '50001189', '하이패스/GPS': '50001190', '전방/후방 카메라': '50001191', '디지털 / 가전': '50000003',
                  '침실가구': '50000100', '침대': '50001228', '매트리스': '50001229', '장롱/붙박이장': '50001230', '화장대': '50001231',
                  '거울': '50001232', '서랍장': '50007189', '거실가구': '50000101', '소파': '50001234', '테이블': '50001235',
                  'TV거실장': '50001310', '장식장': '50001311', '아동': '50000104', '주방가구': '50000102', '식탁/의자': '50001236',
                  '레인지대': '50001313', '왜건/카트': '50001315', '주방수납장': '50001316', '그릇장/컵보드': '50001317',
                  '기타주방가구': '50001318', '서재': '50000105', '책상': '50001238', '책장': '50001346', '책꽂이': '50001347',
                  '의자': '50001239', '사무/교구용 가구': '50001240', '아웃도어가구': '50000106', '수납가구': '50000103', '행거': '50001319',
                  '수납장': '50001320', '선반': '50001321', '공간박스': '50001322', '코너장': '50001329', '소품수납함': '50001330',
                  'DIY자재': '50000107', '목재': '50001060', '반제품': '50001061', '가구부속품': '50001113', '바닥재': '50001114',
                  '벽지': '50001116', '손잡이': '50001062', '인테리어소품': '50000108', '침구단품': '50000109', '매트/침대커버': '50001123',
                  '베개': '50001124', '스프레드': '50000969', '차렵이불': '50000970', '홑이불': '50000971', '패드': '50001125',
                  '침구세트': '50000110', '침대커버세트': '50001127', '매트커버세트': '50001128', '이불베개세트': '50001129',
                  '이불패드세트': '50001130', '요이불세트': '50001131', '한실예단세트': '50000977', '솜류': '50000111', '커튼': '50000113',
                  '커튼': '50001136', '로만셰이드': '50000857', '커튼/로만세트': '50000858', '블라인드': '50000859', '버티컬': '50000860',
                  '롤스크린': '50000861', '홈데코': '50000154', '커버류': '50001137', '주방데코': '50001138', '쿠션/방석': '50001139',
                  '카페트': '50000112', '수예': '50000114', '가구 / 인테리어': '50000004', '분유': '50000115', '국내분유': '50000854',
                  '수입분유': '50000855', '특수분유': '50000856', '수유용품': '50000120', '젖병': '50000743', '젖꼭지': '50000745',
                  '노리개젖꼭지': '50000746', '유축기': '50000673', '분유케이스': '50000674', '보틀워머': '50000675', '스킨': '50000125',
                  '유아가구': '50000131', '기저귀': '50000116', '국내기저귀': '50000729', '수입기저귀': '50000730', '기능성기저귀': '50001143',
                  '유모차': '50000121', '초경량/휴대용': '50000686', '절충형/디럭스형': '50000687', '쌍둥이용': '50005406',
                  '유모차/카시트 세트': '50005407', '유모차 용품': '50001147', '위생': '50000126', '이유식용품': '50000132',
                  '물티슈': '50000117', '캡형': '50005401', '리필형': '50005402', '휴대용': '50005403', '혼합세트': '50005405',
                  '카시트': '50000122', '바구니형': '50005408', '일체형': '50005409', '분리형': '50005410', '카시트용품': '50001148',
                  '구강': '50000127', '임부복': '50000133', '이유식': '50000118', '분말이유식': '50000733', '반고형이유식': '50000736',
                  '레토르트이유식': '50000737', '수제이유식': '50001144', '외출용품': '50000123', '아기띠': '50000692', '힙시트': '50000697',
                  '아기띠침받이': '50000694', '망토/워머': '50000702', '슬링': '50000701', '아기띠쿨러/패드': '50000693',
                  '기저귀가방': '50000695', '소독': '50000129', '유아동의류': '50000138', '아기간식': '50000119', '유아과자': '50000739',
                  '유아두유': '50000738', '유아유제품': '50005467', '유아음료': '50005468', '목욕용품': '50000124', '유아욕조': '50000705',
                  '유아목욕의자': '50000706', '유아목욕가운': '50000707', '유아목욕타월': '50000708', '유아샴푸캡': '50000709',
                  '유아목욕장갑/스펀지': '50000710', '유아세면대/수도꼭지': '50000711', '유아동잡화': '50000139', '유아동언어웨어': '50007135',
                  '출산 / 육아': '50000005', '축산': '50000145', '돼지고기': '50001170', '쇠고기': '50001171', '닭고기': '50001172',
                  '양고기': '50000280', '오리고기': '50000279', '알류': '50001173', '축산가공식품': '50001174', '음료': '50000148',
                  '생수': '50002032', '탄산수': '50002033', '청량/탄산음료': '50001079', '주스/과즙음료': '50001080', '커피': '50001081',
                  '차류': '50001082', '건강식품': '50000023', '수산': '50000159', '생선': '50001175', '김/해초': '50001176',
                  '해산물/어패류': '50001049', '젓갈': '50001050', '건어물': '50001051', '과자': '50000149', '스낵': '50001998',
                  '쿠키': '50001999', '초콜릿': '50002000', '사탕': '50002001', '엿': '50001762', '껌': '50002002',
                  '젤리': '50001763', '다이어트식품': '50000024', '농산물': '50000160', '쌀': '50001052', '잡곡/혼합곡': '50001053',
                  '과일': '50000960', '채소': '50001077', '견과류': '50001078', '건과류': '50001093', '아이스크림': '50000025',
                  '아이스크림': '50001865', '빙수/빙수재료': '50001866', '전통주': '50006349', '반찬': '50000146', '절임류': '50002015',
                  '조림류': '50002016', '장아찌': '50001916', '장조림': '50001917', '반찬세트': '50002017', '기타반찬류': '50002018',
                  '가공식품': '50000150', '라면': '50001083', '면류': '50001084', '우유': '50002006', '두유': '50002007',
                  '요구르트': '50001756', '치즈': '50001085', '생크림': '50001757', '쿠킹박스': '50006808', '김치': '50000147',
                  '포기김치': '50002019', '갓김치': '50002020', '총각김치': '50002021', '깍두기': '50002022', '겉절이': '50002023',
                  '나박김치': '50002024', '동치미': '50002025', '냉동': '50000026', '피자': '50001867', '핫도그': '50001868',
                  '햄버거': '50001869', '딤섬': '50001870', '만두': '50001871', '채식푸드': '50001872', '샐러드': '50001873',
                  '식품': '50000006', '등산': '50000027', '등산의류': '50001096', '등산잡화': '50001097', '등산화': '50001768',
                  '등산가방': '50001769', '등산장비': '50001098', '낚시': '50000163', '낚싯대': '50000990', '낚시릴': '50000991',
                  '낚싯줄': '50000992', '루어낚시': '50000993', '민물낚시': '50000994', '바다낚시': '50000995', '낚시용품': '50000996',
                  '캠핑': '50000028', '텐트': '50001099', '천막': '50001771', '랜턴': '50001100', '다용도칼': '50001772',
                  '취사용품': '50001101', '타프': '50001770', '캠핑의자': '50001776', '해먹': '50001304', '수영': '50000164',
                  '남성수영복': '50000998', '여성수영복': '50000999', '비치웨어': '50001000', '수영용품': '50001001', '골프': '50000029',
                  '골프클럽': '50001102', '골프백': '50001103', '골프의류': '50001104', '골프화': '50001740', '골프공': '50001741',
                  '골프연습용품': '50001106', '골프필드용품': '50001107', '헬스': '50000030', '러닝머신': '50001002', '헬스사이클': '50001603',
                  '줄넘기': '50001605', '훌라후프': '50001606', '스텝퍼': '50001608', '아령/덤벨': '50001604', '복근운동기구': '50001523',
                  '자전거': '50000161', '자전거/MTB': '50001108', '자전거용품': '50001109', '자전거부품': '50001110',
                  '자전거의류/잡화': '50001111', '스케이트': '50000034', '스케이트보드': '50001538', '핑거보드': '50005286',
                  '스케이트보드용품': '50001540', '스네이크보드': '50001541', '아이스스케이트': '50001542', '스포츠액세서리': '50000053',
                  '스포츠선글라스': '50001297', '스포츠토시': '50001302', '스포츠마스크': '50006374', '아이스머플러/스카프': '50006376',
                  '요가': '50000031', '요가복': '50001005', '요가용품': '50001528', '오토바이': '50000035', '오토바이': '50001546',
                  '스쿠터': '50001547', '오토바이부품': '50001007', '전동휠': '50006189', '스포츠 / 레저': '50000007',
                  '자동차용품': '50000055', '인테리어용품': '50000943', '익스테리어용품': '50000942', '세차용품': '50000938',
                  '타이어/휠': '50000947', '튜닝용품': '50000948', 'DIY용품': '50000933', '램프': '50000934', '생활용품': '50000078',
                  '해충퇴치용품': '50000914', '생활잡화': '50000915', '보안용품': '50000916', '화장지': '50000908',
                  '제습/방향/탈취': '50000913', '생리대': '50000909', '성인용기저귀': '50000910', '주방용품': '50000061',
                  '보관밀폐용기': '50000886', '식기류': '50000881', '잔/컵': '50000882', '냄비/솥': '50000883', '주방잡화': '50000894',
                  '프라이팬': '50000884', '주전자/티포트': '50000885', '공구': '50000165', '전동공구': '50001027', '전기용품': '50001032',
                  '측정공구': '50001029', '수작업공구': '50001026', '포장용품': '50001038', '운반용품': '50001037', '안전용품': '50001031',
                  '세탁용품': '50000062', '빨래건조대': '50000901', '빨래바구니': '50002036', '세탁망': '50002041', '다림판': '50002034',
                  '빨래삶통': '50002037', '빨래집게': '50002039', '빨래판': '50002040', '화방용품': '50000054', '붓': '50000928',
                  '물감/포스터컬러': '50000929', '페인트/염료/잉크': '50000927', '미술보조용품': '50000925', '전문지류/미술지류': '50000926',
                  '우드락/폼보드': '50000636', '스케치/드로잉용품': '50000930', '수납': '50000076', '선반/진열대': '50000904',
                  '정리함': '50000905', '옷걸이': '50000906', '바구니': '50001835', '소품걸이': '50001836', '옷커버': '50001837',
                  '압축팩': '50001838', '악기': '50000156', '기타(guitar)': '50000868', '음향기자재': '50000874', '타악기': '50000872',
                  '관악기': '50000871', '피아노': '50000959', '건반악기': '50000869', '현악기': '50000870', '문구': '50000158',
                  '다이어리/플래너': '50001039', '필기도구': '50001041', '용지': '50001047', '이벤트/파티용품': '50000922',
                  '기타문구/사무용품': '50001046', '노트/수첩': '50001040', '앨범': '50001042', '반려동물': '50000155',
                  '강아지 사료': '50006630', '고양이 사료': '50006678', '햄스터용품': '50000229', '고슴도치용품': '50000230',
                  '토끼용품': '50000231', '조류용품': '50000232', '기타반려동물용품': '50000233', '생활 / 건강': '50000008',
                  '공연': '50000082', '뮤지컬': '50001690', '콘서트': '50001691', '연극': '50001692', '스포츠': '50005310',
                  '전시/행사': '50001693', '클래식': '50001694', '오페라': '50001695', '발레/무용': '50001696', '국악/전통예술': '50001697',
                  '모바일쿠폰': '50000085', '영화/공연관람권': '50001746', '백화점/마트': '50001747', '편의점': '50006204',
                  '헤어/뷰티/건강': '50001749', '주유': '50001750', '뷔페/레스토랑': '50001751', '치킨/배달음식': '50001752',
                  '패스트푸드': '50001625', '카페/베이커리': '50001626', '피자': '50001627', '아이스크림': '50001628', '쇼핑상품': '50001629',
                  '통화/문자/데이터': '50001630', '도서/문화': '50001631', '사진촬영': '50001632', '학습/생활서비스': '50001633',
                  '게임/E머니': '50001634', '지류': '50000084', '백화점상품권': '50001700', '구두상품권': '50001701',
                  '도서/문화상품권': '50001702', '마트상품권': '50001703', '영화상품권': '50001704', '외식상품권': '50001705',
                  '주유상품권': '50001743', '기타상품권': '50001744', '기프트카드': '50001745', '여행': '50000011', '국내여행': '50001644',
                  '해외여행': '50001645', '국내숙박': '50001646', '해외숙박': '50001647', '국내항공권': '50001648', '해외항공권': '50001649',
                  '렌터카': '50001650', '레저이용권': '50000086', '스키/보드': '50000920', '눈썰매장': '50001636', '워터파크': '50001637',
                  '아쿠아리움': '50001638', '테마/놀이동산': '50001639', '래프팅': '50001640', '체험': '50006869', '수상레저': '50001642',
                  'e컨텐츠': '50000012', 'VOD': '50001651', '강좌': '50001652', '전자도서': '50001653', '만화': '50001654',
                  '오디오북': '50001655', '기타e컨텐츠': '50001656', '꽃': '50000083', '꽃배달': '50001698', '케이크배달': '50001699',
                  '장기렌터카': '50006929', '여행 / 문화': '50000009', '화장품': '50000013', '스킨케어': '50000793',
                  '스킨/토너': '50002886', '에센스': '50002887', '크림': '50002889', '미스트': '50002890', '아이케어': '50002891',
                  '립케어': '50002892', '마스크/팩': '50002893', '스페셜케어': '50002894', '페이스오일': '50002895', '메이크업': '50000794',
                  '클렌징': '50001657', '선케어': '50001658', '바디케어': '50001659', '헤어케어': '50001660', '남성화장품': '50001661',
                  '아동화장품': '50001662', '주얼리': '50000016', '귀걸이': '50001673', '목걸이': '50001674', '반지': '50001675',
                  '펜던트': '50001676', '팔찌': '50001677', '발찌': '50001678', '헤어': '50001679', '넥타이핀': '50001680',
                  '커프스': '50001681', '브로치': '50001682', '키홀더': '50001683', '휴대폰줄': '50001684', '장식소품': '50001685',
                  '시계': '50000015', '시계': '50000795', '정장시계': '50002900', '캐주얼시계': '50002901', '아동시계': '50002902',
                  '필기도구': '50001667', '라이터': '50001668', '크리스탈': '50001670', '수첩/다이어리': '50001671', '생활소품': '50001672',
                  '패션': '50000017', '가방': '50000796', '지갑': '50000797', '벨트': '50001686', '선글라스': '50001687',
                  '안경': '50001688', '넥타이': '50001561', '스카프/머플러': '50001562', '의류': '50000798', '신발': '50000799',
                  '모자': '50001564', '장갑': '50001565', '언더웨어': '50001563', '양말': '50001566', '우산/양산': '50001567',
                  '패션소품': '50001568', '여행소품': '50001569', '전자제품': '50000018', '노트북/주변기기': '50001570',
                  '카메라/캠코더': '50000800', '가전제품': '50000801', '면도기': '50003080', '이미용가전': '50003081', '전동칫솔': '50003082',
                  'MP3/이어폰/헤드폰': '50000802', '기타 전자제품': '50001611', '향수': '50000014', '여성향수': '50001663',
                  '남성향수': '50001664', '면세점': '50000010'}
        return categoryID[name]

    # 네이버 쇼핑에서 해당 카테고리의 검색 빈도를 보여주는 함수
    # list 형태로 리턴
    # keyword_search와 사용법 동일
    # ages -> 검색 연령대 설정 (입력 안하면 전 연령대 결과 출력, 여러 연령대 결과 출력하고 싶을 때는 ["1","2","3"] 이런 식으로 리스트 입력)
    # - 10: 10∼19세
    # - 20: 20∼29세
    # - 30: 30∼39세
    # - 40: 40∼49세
    # - 50: 50∼59세
    # - 60: 60세 이상
    def trend_search(self, categoryName, device='', ages='0', gender=''):
        client_id = "gDb5rUUUu3cNZt3fIhxy"
        client_secret = "HWP6j_9S6w"
        url = "https://openapi.naver.com/v1/datalab/shopping/categories";
        endTime = datetime.now().date().strftime("%Y-%m-%d")
        startTime = (parser.parse(endTime) - timedelta(days=30)).strftime("%Y-%m-%d")
        body = "{\"startDate\":\"" + startTime + "\",\"endDate\":\"" + endTime + "\",\"timeUnit\":\"date\",\"category\":[{\"name\":\"" + categoryName + "\",\"param\":[\"" + self.getCategoryID(categoryName) + "\"]}]"

        if device != '':
            body += (",\"device\":\"" + device + "\"")
        if ages != '0':
            if len(ages) == 1:
                body += (",\"ages\":[\"" + ages[0] + "\"")
            else:
                body += (",\"ages\":[\"" + ages[0] + "\"")
            for i in range(1, len(ages)):
                body  += (",\"" + ages[i] + "\"")
            body += "]"

        if gender != '':
            body += (",\"gender\":\"" + gender + "\"")
        body += "}"

        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        request.add_header("Content-Type", "application/json")
        response = urllib.request.urlopen(request, data=body.encode("utf-8"))
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            tmp = response_body.decode('utf-8')
            ret = self.str_to_list(tmp, categoryName)
            return ret
        else:
            print("Error Code:" + rescode)

    # 네이버 쇼핑에서 해당 카테고리의 검색 빈도를 성별을 나눠서 보여주는 함수
    # list 형태로 리턴
    # trend_search와 사용법 동일
    def trend_search_gender(self, categoryName):
        client_id = "gDb5rUUUu3cNZt3fIhxy"
        client_secret = "HWP6j_9S6w"
        url = "https://openapi.naver.com/v1/datalab/shopping/category/gender"
        endTime = datetime.now().date().strftime("%Y-%m-%d")
        startTime = (parser.parse(endTime) - timedelta(days=30)).strftime("%Y-%m-%d")
        body = "{\"startDate\":\"" + startTime + "\",\"endDate\":\"" + endTime + "\",\"timeUnit\":\"date\",\"category\":\"" + self.getCategoryID(categoryName) + "\"}"

        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        request.add_header("Content-Type", "application/json")
        response = urllib.request.urlopen(request, data=body.encode("utf-8"))
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            tmp = response_body.decode('utf-8')
            ret = self.str_to_list_gender(tmp, categoryName)
            return ret
        else:
            print("Error Code:" + rescode)

    # 네이버 쇼핑에서 해당 카테고리의 검색 빈도를 연령대별로 보여주는 함수
    # list 형태로 리턴
    # trend_search와 사용법 동일
    def trend_search_age(self, categoryName):
        client_id = "gDb5rUUUu3cNZt3fIhxy"
        client_secret = "HWP6j_9S6w"
        url = "https://openapi.naver.com/v1/datalab/shopping/category/age"
        endTime = datetime.now().date().strftime("%Y-%m-%d")
        startTime = (parser.parse(endTime) - timedelta(days=30)).strftime("%Y-%m-%d")
        body = "{\"startDate\":\"" + startTime + "\",\"endDate\":\"" + endTime + "\",\"timeUnit\":\"date\",\"category\":\"" + self.getCategoryID(categoryName) + "\"}"

        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        request.add_header("Content-Type", "application/json")
        response = urllib.request.urlopen(request, data=body.encode("utf-8"))
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            tmp = response_body.decode('utf-8')
            ret = self.str_to_list_age(tmp, categoryName)
            return ret
        else:
            print("Error Code:" + rescode)

    # api 결과를 dict 형태로 변환해주는 함수
    def str_to_list(self, str, keyword):
        d_list = ['x']
        v_list = [keyword]
        cnt = 0
        idx = 0
        tmp = str
        while idx != -1:
            idx = tmp.find("period")
            if idx == -1:
                break
            date = tmp[idx+9:idx+19]
            tmp = tmp[idx:]
            idx = tmp.find("ratio")
            if idx == -1:
                break
            value = tmp[idx+7:idx+11]
            if value[-1] == ',' or value[-1] == '}':
                value = value[0:-1]
            value = math.ceil(float(value))
            tmp = tmp[idx:]
            d_list.append(date)
            v_list.append(value)
            cnt += 1
        ret = [d_list, v_list]
        return ret

    def str_to_list_age(self, str, keyword):
        dic = dict()
        cnt = 0
        idx = 0
        tmp = str
        while idx != -1:
            idx = tmp.find("period")
            if idx == -1:
                break
            date = tmp[idx + 9:idx + 19]
            tmp = tmp[idx:]
            idx = tmp.find("ratio")
            value = tmp[idx+7:idx+11]
            if value[-1] == ',' or value[-1] == '}':
                value = value[0:-1]
            value = math.ceil(float(value))
            idx = tmp.find("group")
            age = tmp[idx+8:idx+10]
            tmp = tmp[idx:]
            dic[cnt] = [date, age, value]
            cnt += 1
        total = dic[cnt - 6][2] + dic[cnt - 5][2] + dic[cnt - 4][2] + dic[cnt - 3][2] + dic[cnt - 2][2] + dic[cnt - 1][2]
        ret = [['x', '10대', '20대', '30대', '40대', '50대', '60대 이상'], [keyword, round(dic[cnt - 6][2] / total * 100), round(dic[cnt - 5][2] / total * 100), round(dic[cnt - 4][2] / total * 100), round(dic[cnt - 3][2] / total * 100), round(dic[cnt - 2][2] / total * 100), round(dic[cnt - 1][2] / total * 100)]]
        return ret

    def str_to_list_gender(self, str, keyword):
        dic = dict()
        cnt = 0
        idx = 0
        tmp = str
        while idx != -1:
            idx = tmp.find("period")
            if idx == -1:
                break
            date = tmp[idx+9:idx+19]
            tmp = tmp[idx:]
            idx = tmp.find("ratio")
            value = tmp[idx+7:idx+11]
            if value[-1] == ',' or value[-1] == '}':
                value = value[0:-1]
            value = round(float(value))
            idx = tmp.find("group")
            gender = tmp[idx+8]
            tmp = tmp[idx:]
            dic[cnt] = [date, gender, value]
            cnt += 1
        total = dic[cnt-2][2] + dic[cnt-1][2]
        ret = [['x', 'm', 'f'],[keyword, round(dic[cnt-1][2]/total * 100), round(dic[cnt-2][2]/total * 100)]]
        return ret

if __name__=='__main__':
    naver = NaverShopping()
    # a = naver.trend_search("여성 티셔츠")
    a = naver.trend_search_age("여성 티셔츠")
    # a = naver.trend_search_gender("여성 티셔츠")
    print(a)