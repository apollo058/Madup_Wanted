from tkinter.tix import InputOnly
from django.test import TestCase, Client
from clients.models import Client
from amounts.models import Amount
import csv

from typing import Dict

class TestAmmountUnittest(TestCase):
    """
        작성자: 하정현
        Summary: Account CRUD Test

        TODO: 추가 작성 예정
    """

    INPUTS_ROOT = "amounts/tests/inputs"    # 테스트 할 때 사용되는 케이스들

    """
    def setUp(self):
        # CSV 데이터 로드
        with open(f'{self.INPUTS_ROOT}/Madup_Wanted_Data_set.csv', 'rt') as f:
            reader = csv.reader(f)

            i = 0
            for advertiser, uid,        \
                media,      data,       \
                cost,       impression, \
                click,      conversion, \
                cv          in reader:

                if cv == 'cv':
                    continue

                # TODO: 유저 생성 및 Amount 생성
                self.client.post(f"/api/clients", format="json", data={
                    "id": advertiser,
                    "name": f"user-{advertiser}",
                    "manager": f"compnay-{advertiser}",
                    "contact": "010-1111-1111",
                    "address_code": "13403",
                    "address_detail": "Unknown Address"
                })

                # TODO: AD LOAD
                self.client.post(f"/api/amounts")
    """
                
    def tearDown(self) -> None:
        # TODO 모든 데이터 삭제
        try:
            Amount.objects.delete()
            Client.objects.delete()
        except AttributeError as e:
            # 레코드 없는 경우 발생
            pass
    
    def test_process(self):
        pass
