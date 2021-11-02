from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View

from rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd
import json



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

class TimeSeriesData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        # qs_count = User.objects.all().count()
        # status = request.query_params.get("status")
        country = request.query_params.get("country")


        print(country, "--------")

        path = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'

        df = pd.read_csv(path)
        
        clean_data = pd.DataFrame(df[df["Country/Region"] == country ]).T
        country = df["Country/Region"].unique()
        clean_data.drop(["Province/State","Country/Region","Lat","Long"], axis=0, inplace=True )

       
        result = clean_data.to_json(orient="split")

        parsed = json.loads(result)

        clean_data = []
        for i, each in enumerate(parsed['data']) :
            clean_dic = {}
            clean_dic["value"] = parsed['data'][i][0]
            new = parsed['index'][i].split('/')

            clean_dic["data"] = "20{0}-{2}-{1}".format(new[2],new[1],new[0])

            clean_data.append(clean_dic)

        response = sorted(clean_data, key = lambda i: i['value'],reverse=True)
        data = {
                "clean_data": response,
                "country":country,
        }


        return Response(data)

