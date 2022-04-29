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

    """

    INPUTS_ROOT = "amounts/tests/inputs"    # 테스트 할 때 사용되는 케이스들
    URI         = "/api/amounts"            # uri
    CLIENT_URI  = "/api/clients"
    cid_list: List[str]
    advertises: List[Dict[str, object]]    # read 테스트에 사용될 advertise data

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
                c: Client = Client.objects.filter(id=self.cid_list[int(idx)])[0]
                input_data =  {
                    "advertiser"    : c,
                    "uid"           : uid,
                    "media"         : media,
                    "date"          : date,
                    "cost"          : int(cost),
                    "impression"    : int(imporession),
                    "click"         : int(click),
                    "conversion"    : int(conversion),
                    "cv"            : int(cv)
                }
                Amount.objects.create(**input_data)
                DATE_FORMAT = '%Y-%m-%d'
                input_data['date'] = datetime.datetime.strptime(input_data['date'], DATE_FORMAT)
                self.advertises.append(input_data)
            
    def tearDown(self) -> None:
        try:
            Amount.objects.delete()
            Client.objects.delete()
        except AttributeError as e:
            # 레코드 없는 경우 발생
            pass

    def mod_read(self, case: Dict[str, object], advertises: List[Dict[str, object]]):
        """
            READE 테스트 함수

            params:
                case: 테스트 케이스
                advertises: 모든 advertise 관련된 데이터들이 들어 있다.
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
            
            DATE_FORMAT = '%Y-%m-%d'
            start_date  = datetime.datetime.strptime(case_data['start_date'], DATE_FORMAT)
            end_date    = datetime.datetime.strptime(case_data['end_date'], DATE_FORMAT)

            def __filter_func(e):
                """
                    기간, uid 필터링 함수
                """
                uid = e['uid']
                create_date = e['date']
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
                data_map[k]['roas'] = 0 if not cost else cv * 100 / cost
                data_map[k]['cpc']  = 0 if not click else cost * 100 / click
                data_map[k]['cvr']  = 0 if not click else conversion * 100 / click
                data_map[k]['cpa']  = 0 if not conversion else cost * 100 / conversion

            test_cases  = {'ctr', 'cpc', 'cvr', 'roas', 'cpa'}
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
                        0.01,
                        msg = f"""
                            In {media}, {k}.
                            Answer: {data_map[media][k]}
                            Output: {res_data[media][k]}
                        """
                    )

    def test_read(self):
        """
            TEST: READ
            TEST: CTR/ROADS/CPC/CVR/CPA 읽기 테스트
        """

        # Case 돌면서 테스트 시작
        with open(f"{self.INPUTS_ROOT}/read.json") as f:
            for case in json.load(f)['case']:
                if case['command'] == 'read':
                    self.mod_read(case, self.advertises)