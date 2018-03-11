import json
import logging
from rest_framework.response import Response
from libs import baseview
from libs import con_database
from core.models import DatabaseList

CUSTOM_ERROR = logging.getLogger('Yearning.core.views')


class serach(baseview.BaseView):

    '''
    sql查询接口, 过滤非查询语句并返回查询结果
    '''

    def post(self, request, args=None):
        sql = request.data['sql']
        check = str(sql).strip().rstrip(';').split('\n')
        if check[-1].lower().find('s') != 0:
            return Response({'error': '只支持查询功能!'})
        else:
            address = json.loads(request.data['address'])
            _c = DatabaseList.objects.filter(id=address['id']).first()
            try:
                with con_database.SQLgo(
                        ip=_c.ip,
                        password=_c.password,
                        user=_c.username,
                        port=_c.port,
                        db=address['basename']
                ) as f:
                    dataset = f.search(sql=check[-1] + '  limit 1000')
                    return Response(dataset)
            except Exception as e:
                return Response({'error': str(e)})