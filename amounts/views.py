from http.client import BAD_REQUEST
from tracemalloc import start
from django.db.models import Q, Count, F, Sum, Case, When
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404

from rest_framework          import status
from rest_framework.views    import APIView
from rest_framework.response import Response
from yaml import serialize

from .models      import Amount
import datetime

import json

def Date(str):
    return datetime.datetime.strptime(str, '%Y-%m-%d').date()

class AmountsListView(APIView):
    '''
    작성자 : 남기윤
    (GET) /Amounts
    '''

    def get(self,request):
        '''
        작성자:남기윤
        '''
        #우선 uid로 검색할지 결정합니다
        #이유:해당 uid가 존재하면 첫번째 조회시 대상을 대폭 줄일 수 있을 것이라 가정
        #그 후 기간을 나눔 (DateFilter)
        uid = request.GET.get("uid", None)
        start_date = request.GET.get("start_date", None)
        end_date = request.GET.get("end_date", None)

        q = Q()

        if uid:
            q &= Q(uid=uid)
        if start_date:
            q &= Q(date__gte=Date(start_date))
        if end_date:
            q &= Q(date__lte=Date(end_date))
        if  uid: 
            amount_data = Amount.objects.filter(q).values('media').annotate(
                CTR = Coalesce(Sum('click') * 100 / Sum('impression'),0),
                ROAS = Coalesce(Sum('cv') * 100 / Sum('cost'),0),
                CPC = Coalesce(Sum('cost') * 100 / Sum('click'),0),
                CVR = Coalesce(Sum('conversion') * 100 / Sum('click'),0),
                CPA = Coalesce(Sum('cost') * 100 / Sum('conversion'),0)
                )
            #eg.[{'media': 'naver', 'CTR': 0, 'ROAS': 1449, 'CPC': 29750, 'CVR': 12, 'CPA': 238000}]
        else:
            Response(status=status.HTTP_400_BAD_REQUEST)
            
        amount_data = list(amount_data)
        result = {}
        for i in amount_data:
            result[i['media']] = {
                'ctr' : i['CTR'],
                'cpc' : i['CPC'],
                'roas' : i['ROAS'],
                'cvr' : i['CVR'],
                'cpa' : i['CPA']
            }
            print()
            return Response(result)
        else: return Response(status=status.HTTP_204_NO_CONTENT)
