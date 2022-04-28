from clients.models import Client
from amounts.models import Amount
from amounts.tests.test_tools.test_tools import *
import json
import csv
import datetime
from rest_framework.test import APITestCase
from typing import List, Dict

class TestAmmountUnittest(APITestCase):
    """
        작성자: 하정현
        Summary: Amount CRUD Test

        TODO: 아직 테스트 X
    """

    INPUTS_ROOT = "amounts/tests/inputs"    # 테스트 할 때 사용되는 케이스들
    URI         = "/api/amounts"            # uri
    CLIENT_URI  = "/api/clients"
    cid_list: List[str]

    def setUp(self) -> None:
        """
            테스트에 사용될 클라이언트 3개 생성
        """
        self.cid_list = [] # 초기화
        for i in range(3):
            name = f"client-{i}"
            res = self.client.post(self.CLIENT_URI, format="json", data={
                "name"      : name,
                "manager"   : "manager1",
                "contact"   : "010-1111-1111",
                "address_code"  : "13403",
                "address_detail": "Unknown Address"
            })

            # id 저장
            self.cid_list.append(res.json()['id'])

    def mod_create(self, case: Dict[str, object], test = True) -> str:
        """
            CREATE 테스트 함수
            params:
                case: 테스트 케이스
            return:
                id: 생성된 amount의 ID
        """        
        
        # 케이스 데이터 가져오기
        case_topic, case_data, case_answer = \
            case["test-topic"], case['data'], case['answer']

        # advertiser부분의 id를 변경한다 (id가 있는 경우만)
        if 'id' in case['data']:
            case['data']['id'] = self.cid_list[case['data']['id']]
        # api request
        res = self.client.post(self.URI, data=case_data, format="json")

        if not test:
            # 테스트를 하지 않음
            # 근데 정상적으로 업로드 안되면 호출
            self.assertEqual(201, res.status_code,
                msg = print_err_msg("read test를 위한 create중 에러 발생", 201, res.status_code))
            return res.json()

        # Status Code 테스트
        self.assertEqual(
            res.status_code, case_answer['code'],
            msg = print_err_msg(case_topic, case_answer['code'], res.status_code)
        )
            
        # Client가 실제로 생성되어있는 지 테스트
        # 인원 수로 계산
        cnt = Amount.objects.count()
        self.assertEqual(
            cnt, case_answer['amount-count'],
            msg = print_err_msg(case_topic, case_answer['amount-count'], cnt)
        )

        if res.status_code == 201:
            """
                추가에 성공했다면
                다른 테스트를 위해 id값 리턴
            """
            return res.json()['id']

    def mod_read(self, case: Dict[str, object], advertises: List[Dict[str, object]]):
        """
            UPDATE 테스트 함수

            params:
                case: 테스트 케이스
                advertises: 모든 advertises 관련된 데이터들이 들어 있다.
        """
        case_topic, case_data, case_answer = \
            case['test-topic'], case['data'], case['answer']
        
        # uri param 작성
        uri_param = "?"
        if 'uid' in case_data:
            uri_param += f"uid={case_data['uid']}"
        if 'start_date' in case_data:
            uri_param += f"&start_date={case_data['start_date']}"
        if 'end_date' in case_data:
            uri_param += f"&end_date={case_data['end_date']}"

        # uri 합치기
        uri = self.URI + uri_param

        # request
        res = self.client.get(f"{uri}", format="json")

        # status code 검증
        self.assertEqual(
            res.status_code, case_answer['code'],
            msg = print_err_msg(case_topic, case_answer['code'], res.status_code))

        if res.status_code == 200:
            
            # 데이터 검증
            # 데이터 검증을 위한 정답 데이터 생성
            
            DATE_FORMAT = '%Y.%m.%d'
            start_date  = datetime.datetime.strptime(case_data['start_date'], DATE_FORMAT)
            end_date    = datetime.datetime.strptime(case_data['end_date'], DATE_FORMAT)

            def __filter_func(e):
                """
                    기간, uid 필터링 함수
                """
                uid = e['uid']
                create_date = datetime.datetime.strptime(e['create_date'], DATE_FORMAT)
                return (uid == case_data['uid']) and (start_date <= create_date <= end_date)
            
            filtered = list(filter(__filter_func, advertises))
            data_map = {}

            for e in filtered:
                # 데이터 수집
                if e['media'] not in data_map:
                    data_map[e['media']] = {
                        "click": 0, "cost": 0,
                        "cv": 0, "conversion": 0,
                        "impression": 0
                    }
                data_map[e['media']]['click']       += e['click']
                data_map[e['media']]['cost']        += e['cost']
                data_map[e['media']]['cv']          += e['cv']
                data_map[e['media']]['conversion']  += e['conversion']
                data_map[e['media']]['impression']  += e['impression']

            # 단위 계산
            for k in data_map.keys():
                click, impression, cost, conversion, cv = \
                    data_map[k]['click'], data_map[k]['impression'], data_map[k]['cost'],   \
                    data_map[k]['conversion'], data_map[k]['cv']

                data_map[k]['ctr']  = 0 if not impression else (click * 100) / impression
                data_map[k]['cpc']  = 0 if not click else cost / click
                data_map[k]['cvr']  = 0 if not click else conversion * 100 / click
                data_map[k]['roas'] = 0 if not cost else cv * 100 / cost

            test_cases  = {'ctr', 'cpc', 'cvr', 'roas'}
            res_data    = res.json()

            # 단위 검증
            for media in res_data:
                # media: 회사명
                for k in test_cases:
                    # 테스트 케이스
                    # 소수 둘째 짜리 밑으로 버림
                    # == -0.01 까지 허용
                    self.assertLess(
                        data_map[media][k]-float(res_data[media][k]),
                        0.01
                    )
    

    def mod_update(self, case: Dict[str, object], id: str):
        """
            UPDATE 테스트 함수

            params:
                case: 테스트 케이스
                id: 테스트 대상 아이디
        """
        case_topic, case_data, case_answer = \
            case['test-topic'], case['data'], case['answer']
        # 수정 할 데이터 수집, id는 이미 있으므로 제외
        req_data = {k:v for k,v in case_data.items() if k != 'id'}
        # request to api
        res = self.client.patch(f"{self.URI}/{id}", data=req_data, format="json")

        # 검증
        self.assertEqual(
            res.status_code, case_answer['code'],
            msg = print_err_msg(case_topic, case_answer['code'], res.status_code))
        
        if res.status_code == 200:
            # 수정된 데이터가 제대로 수정되었는지 테스트
            for k, v in req_data.items():
                self.assertEqual(req_data[k], v,
                    msg = print_err_msg(f"{case_topic} -> Key: {k}", req_data[k], res.data[k]))
        

    def mod_delete(self, case: Dict[str, object]):
        """
            DELETE 테스트 함수:
            
            params:
                case: 테스트 케이스
                id: 삭제 대상 id
        """
        case_topic, _, case_answer = \
            case["test-topic"], case['data'], case['answer']

        res = self.client.delete(f"{self.URI}/{id}")

        self.assertEqual(
            res.status_code, case_answer['code'],
            msg = print_err_msg(case_topic, case_answer['code'], res.status_code))
            
        if res.status_code == 200:
            # 검색해서 더이상 검색이 안 되는 지 확인
            res = self.client.get(f"{self.URI}/{id}", format="json")
            self.assertEqual(404, res.status_code, 
                msg=print_err_msg(f"{case_topic}: not deleted", 404, res.status_code))
                
    def tearDown(self) -> None:
        try:
            Amount.objects.delete()
            Client.objects.delete()
        except AttributeError as e:
            # 레코드 없는 경우 발생
            pass
    
    def test_create(self):
        """
            TEST: CREATE
        """
        if True:
            return
        with open(f"{self.INPUTS_ROOT}/create.json") as f:
            # 테스트 케이스가 들어있는 Json 파일 불러오기
            for case in json.load(f)['case']:
                self.mod_create(case)

    def test_read(self):
        """
            TEST: READ
            TEST: CTR/ROADS/CPC/CVR/CPA 읽기 테스트
        """

        if True:
            return
        
        advertises = []

        # 테스트진행을 위해 데이터를 채운다
        with open(f"{self.INPUTS_ROOT}/read.csv") as f:
            reader = csv.reader(f)
            for idx,    uid,    \
                media,  date,   \
                cost,   imporession,    \
                click,  conversion,     \
                cv      in reader:

                # 제목 부분 제외
                if uid == "uid":
                    continue

                # advertise 정보 추가
                advertises.append(
                    # 동시에 DB에도 업로드 (테스트 X)
                    self.mod_create(
                        test=False,
                        case={
                            "test-topic": None,
                            "answer": None,
                            "data": {
                                "advertiser"    : self.cid_list[int(idx)],
                                "uid"           : uid,
                                "media"         : media,
                                "date"          : date,
                                "cost"          : int(cost),
                                "impression"    : int(imporession),
                                "click"         : int(click),
                                "conversion"    : int(conversion),
                                "cv"            : int(cv)
                            }
                        }
                    )
                )
        
        # Case 돌면서 테스트 시작
        with open(f"{self.INPUTS_ROOT}/read.json") as f:
            for case in json.load(f)['case']:
                if case['command'] == 'read':
                    self.mod_read(case, advertises)

    def test_update(self):
        """
            TEST: UPDATE
        """
        if True:
            return

        amount_ids = [int('9'*11)]  # 첫부분은 존재하지 않는 ID다
        with open(f"{self.INPUTS_ROOT}/update.json") as f:
            for case in json.load(f)['case']:
                if case['command'] == 'create':
                    self.mod_create(case)
                elif case['command'] == 'update':
                    self.mod_update(case, id=amount_ids[case['data']['advertiser_idx']])

    def test_delete(self):
        """
            TEST: DELETE
        """
        if True:
            return
        amount_ids = [int('9'*11)]  # 첫부분은 존재하지 않는 ID다
        with open(f"{self.INPUTS_ROOT}/delete.json") as f:
            for case in json.load(f)['case']:
                if case['command'] == 'create':
                    self.mod_create(case)
                elif case['command'] == 'delete':
                    self.mod_delete(case, id=amount_ids[case['data']['advertiser_idx']])