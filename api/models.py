from django.db import models
from tastypie.resources import ModelResource
from django.db.models import Q
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpBadRequest
from datetime import datetime, timedelta
from dateutil.parser import parse
from django.urls import re_path
from tastypie.utils import trailing_slash
from tastypie.authorization import Authorization
from .autification import CustomAuthentication

class Finances(models.Model):
    datetime = models.DateTimeField()
    gross = models.FloatField()  # 'грязные'
    tax = models.FloatField()    # 'налог'
    net = models.FloatField()    # 'чистые'


class FinanceResource(ModelResource):
    class Meta:
        queryset = Finances.objects.all()
        resource_name = 'finances'
        allowed_methods = ['get', 'post']
        use_in = 'list'
        authentication = CustomAuthentication()
        authorization = Authorization()


    def prepend_urls(self):
        from django.urls import re_path

        return [
            re_path(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()),
                    self.wrap_view('search'),
                    name="api_search"),
        ]

    def search(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        self.throttle_check(request)

        # Парсим данные из POST-запроса
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))

        # Проверяем наличие необходимых полей в данных
        if 'timeslots' not in data or 'column' not in data:
            raise ImmediateHttpResponse(HttpBadRequest("Missing timeslots or column in request data"))

        timeslots = data['timeslots']
        column = data['column']

        # Создаем условия для запроса
        result = []
        for timeslot, dates in timeslots.items():
            start_time_str, end_time_str = timeslot.split('-')
            start_time = datetime.strptime(start_time_str, "%H:%M")
            end_time = datetime.strptime(end_time_str, "%H:%M")
            dates = map(parse, dates)
            for date in dates:
                # Добавляем временной промежуток к дате
                start_datetime = datetime.combine(date, start_time.time())
                end_datetime = datetime.combine(date, end_time.time())
                queries = Q(datetime__range=(start_datetime, end_datetime))

                # Выполняем запрос к базе данных
                columns_to_search = column.split(',')
                query_result = list(Finances.objects.filter(queries).values(*columns_to_search))
                result.extend(query_result)

        return self.create_response(request, {'result': result})
