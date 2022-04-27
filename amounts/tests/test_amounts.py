from tkinter.tix import InputOnly
from clients.models import Client
from amounts.models import Amount
import csv
from rest_framework.test import APITestCase
from typing import List

from typing import Dict

class TestAmmountUnittest(APITestCase):
    """
        작성자: 하정현
        Summary: Account CRUD Test

        TODO: 추가 작성 예정
    """

    INPUTS_ROOT = "amounts/tests/inputs"    # 테스트 할 때 사용되는 케이스들
    cid_list: List[str]

    def setUp(self) -> None:
        """
            테스트에 사용될 클라이언트 3개 생성
        """
        self.cid_list = [] # 초기화
        for i in range(3):
            name = f"client-{i}"
            res = self.client.post(f"/api/clients", format="json", data={
                "name"      : name,
                "manager"   : "manager1",
                "contact"   : "010-1111-1111",
                "address_code"  : "13403",
                "address_detail": "Unknown Address"
            })

            # id 저장
            self.cid_list.append(res.json()['id'])

                
    def tearDown(self) -> None:
        # TODO 모든 데이터 삭제
        try:
            Amount.objects.delete()
            Client.objects.delete()
        except AttributeError as e:
            # 레코드 없는 경우 발생
            pass
    
    def test_create(self):
        pass

    def test_read(self):
        pass

    def test_update(self):
        pass

    def test_delete(self):
        pass