from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View

from rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd



# User = get_user_model()

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'charts.html', {"customers": 10})



def get_data(request, *args, **kwargs):
    data = {
        "sales": 100,
        "customers": 10,
    }
    return JsonResponse(data) # http response


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        # qs_count = User.objects.all().count()
        status = request.query_params.get("status")
        countries = request.query_params.get("countries")


        print(status, "--------")

        path = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/12-25-2020.csv'
        df = pd.read_csv(path)

        df.drop(['FIPS', 'Admin2','Last_Update','Province_State', 'Combined_Key'], axis=1, inplace=True)
        df.rename(columns={'Country_Region': "Country"}, inplace=True)

        world = df.groupby("Country")['Confirmed','Active','Recovered','Deaths'].sum().reset_index()


        top_20 = world.sort_values(by=[status], ascending=False).head(int(countries))

        labels = top_20['Country']
        default_items = top_20[status]
        data = {
                "labels": labels,
                "default": default_items,
                "status":status
        }


        return Response(data)

