from django.test import TestCase, Client
from clients.models import Client
import json
from clients.tests.test_tools.test_tools import print_err_msg
from typing import Dict

class TestClientsUnittest(TestCase):
    """
        작성자: 하정현
        Summary: Client CRUD Test
    """

    """ Variables """
    URI         = "/api/clients"
    INPUTS_ROOT = "clients/tests/inputs"    # 테스트 할 때 사용되는 케이스들

    def tearDown(self) -> None:
        try:
            Client.objects.delete()
        except AttributeError as e:
            # Client에 레코드가 없는 경우 발생?
            pass

    """ Test Functions """
    def mod_create(self, case: Dict[str, object], test: bool = True) -> int:
        """
            CREATE 테스트 함수

            return: id 출력
        """
        case_idx, case_data, case_answer = \
            case["test-topic"], case['data'], case['answer']
        res = self.client.post(self.URI, data=case_data, format="json")
        
            
        # 테스트 목적일 경우 assert까지 확인한다.
        if test:
            # Status Code 테스트
            self.assertEqual(
                res.status_code, case_answer['code'],
                msg = print_err_msg(case_idx, case_answer['code'], res.status_code)
            )
            
            # Client가 실제로 생성되어있는 지 테스트
            # 인원 수로 계산
            cnt = Client.objects.count()
            self.assertEqual(
                cnt, case_answer['client-count'],
                msg = print_err_msg(case_idx, case_answer['client-count'], cnt)
            )

        if res.status_code == 200:
            return res.data['id']

    def mod_read(self, case: Dict[str, object], id: int, test: bool = True):
        """
            READ 테스트 함수:
        """
        case_topic, _, case_answer = \
            case["test-topic"], case['data'], case['answer']
        res = self.client.get(f"{self.URI}?id={id}")

        # 테스트가 필요한 경우
        if test:
            # Status Code Test
            self.assertEqual(
                res.status_code, case_answer['code'],
                msg = print_err_msg(case_topic, case_answer['code'], res.status_code))

            if res.status_code == 200:
                # 정상적으로 읽기에 성공한 경우 Data 검토
                for k, v in case_answer.items():
                    """
                        name, manager 등, response의 Data가 제대로
                        맞는 지 검토
                    """
                    if k == "code":
                        # status code는 이미 확인함
                        continue
                    self.assertEqual(res.data[k], v, 
                        msg = print_err_msg(f"{case_topic} -> Key: {k}", case_answer[k], res.data[k]))

    def mod_update(self, case: Dict[str, object], id: int, test: bool = True):
        """
            UPDATE 테스트 함수:
        """
        case_topic, case_data, case_answer = \
            case["test-topic"], case['data'], case['answer']

        # 수정 할 데이터 수집
        req_data = {k:v for k, v in case_data.items() if k != 'id'}
        # Request to api
        res = self.client.patch(f"{self.URI}/{id}", data=req_data, format="json")

        if test:
            self.assertEqual(
                res.status_code, case_answer['code'],
                msg = print_err_msg(case_topic, case_answer['code'], res.status_code))
            if res.status_code == 200:
                # 수정된 데이터 매칭
                for k, v in req_data.items():
                    self.assertEqual(res.data[k], v, 
                        msg = print_err_msg(f"{case_topic} -> Key: {k}", req_data[k], res.data[k]))
            

    def mod_delete(self, case: Dict[str, object], id: int, test: bool = True):
        """
            DELETE 테스트 함수:
        """
        case_topic, case_data, case_answer = \
            case["test-topic"], case['data'], case['answer']

        res = self.client.delete(f"{self.URI}/{id}")

        if test:
            self.assertEqual(
                res.status_code, case_answer['code'],
                msg = print_err_msg(case_topic, case_answer['code'], res.status_code))
            
            if res.status_code == 200:
                # 검색해서 더이상 검색이 안 되는 지 확인
                res = self.client.get(f"{self.URI}/{id}", format="json")
                self.assertEqual(404, res.status_code, 
                    msg=print_err_msg(f"{case_topic}: not deleted", 404, res.status_code))
        
    
    """ Create Functions """

    def test_create(self):
        """
            Testing Client 'CREATE'
        """
        with open(f"{self.INPUTS_ROOT}/create.json") as f:
            # 테스트 케이스가 들어있는 Json 파일 불러오기
            for case in json.load(f)['case']:
                # test case 데이터 불러오면서 테스트
                self.mod_create(case)

    def test_read(self):
        """
            Testing Client 'READ'
        """
        created_id: int = 0
        with open(f"{self.INPUTS_ROOT}/read.json") as f:
            # 테스트 케이스가 들어있는 Json 파일 불러오기
            for case in json.load(f)['case']:
                if case['command'] == 'create':
                    created_id = self.mod_create(case, test=False)
                elif case['command'] == "read":
                    if 'id' in case['data']:
                        self.mod_read(case, id=case['data']['id'])
                    else:
                        self.mod_read(case, id=created_id)

    def test_update(self):
        """
            Testing Client "UPDATE"
        """
        created_id: int = 0
        with open(f"{self.INPUTS_ROOT}/update.json") as f:
            # 테스트 케이스가 들어있는 Json 파일 불러오기
            for case in json.load(f)['case']:
                if case['command'] == 'create':
                    created_id = self.mod_create(case, test=False)
                elif case['command'] == "update":
                    if 'id' in case['data']:
                        self.mod_update(case, id=created_id)
                    else:
                        self.mod_update(case, id=case['data']['id'])

    def test_delete(self):
        """
            Testing Client: "DELETE"
        """
        created_id: int = 0
        with open(f"{self.INPUTS_ROOT}/delete.json") as f:
            # 테스트 케이스가 들어있는 Json 파일 불러오기
            for case in json.load(f)['case']:
                if case['command'] == 'create':
                    self.mod_create(case, test=False)
                elif case['command'] == "delete":
                    if 'id' in case['data']:
                        self.mod_delete(case, id=created_id)
                    else:
                        self.mod_delete(case, id=case['data']['id'])
