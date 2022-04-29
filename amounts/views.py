from django.db.models import Q, Sum, FloatField
from django.db.models.functions import Coalesce

from rest_framework          import status
from rest_framework.views    import APIView
from rest_framework.response import Response

from .models      import Amount
import datetime


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
                CTR = Coalesce(Sum('click') * 100 / Sum('impression'),0,output_field=FloatField()),
                ROAS = Coalesce(Sum('cv') * 100 / Sum('cost'),0,output_field=FloatField()),
                CPC = Coalesce(Sum('cost') * 100 / Sum('click'),0,output_field=FloatField()),
                CVR = Coalesce(Sum('conversion') * 100 / Sum('click'),0,output_field=FloatField()),
                CPA = Coalesce(Sum('cost') * 100 / Sum('conversion'),0,output_field=FloatField())
                )
           
        else:
            Response(status=status.HTTP_400_BAD_REQUEST)
            
        amount_data = list(amount_data)
        result = {}
        for i in amount_data:
            result[i['media']] = {
                'ctr' : round( i['CTR'] ,2),
                'cpc' : round( i['CPC'] ,2),
                'roas' : round( i['ROAS'] ,2),
                'cvr' : round( i['CVR'] ,2),
                'cpa' : round( i['CPA'] ,2)
            }
            return Response(result)
        else: return Response(status=status.HTTP_204_NO_CONTENT)
