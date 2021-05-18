from django.shortcuts import render,get_object_or_404
from django.shortcuts import redirect
from .models import UserData

import requests # для запросов к api

import time,sched

from datetime import date # for age

import pandas as pd
import plotly
import plotly.express as px
import plotly.io as pio # vor grafics

from operator import itemgetter#for visualisationAge to sort list of dicts by age

from django.db.models import Count

from django.utils import timezone

from .forms import DataForm

def mainPage(request):

    userData = UserData.objects.order_by('-received_date')[:1000]

    allUsersInDB = UserData.objects.all().count()

    form = DataForm()

    return render(request,'mainPage.html',{'userData':userData,'allUsersInDB':allUsersInDB,'form':form})

def loadOneUserData(param):# function that makes api request,param = id of vk user,we use this func in another function

    URL = 'https://api.vk.com/method/users.get'

    PARAMS = {'fields':'sex,status,city,bdate,about,activities,books,career,connections,contacts,country,domain,education,home_town','user_id':param,'v':5.52,'access_token':'b5b6d031c6fe67acac183a1fa8238ac532130d82355bfb8dff764455d43309c35b1fac9aa64b3e70d657d'}

    req = requests.get(url = URL,params = PARAMS)

    requestData = req.json()

    if requestData is not None and requestData.get('response')[0].get('first_name') != 'DELETED':
        if UserData.objects.filter(id = requestData.get('response')[0].get('id')).exists():
            print(str(requestData.get('response')[0].get('id')) + ' already exists')
        else:
            print(requestData)
            new_data = UserData()
            new_data.id = requestData.get('response')[0].get('id')
            new_data.first_name = requestData.get('response')[0].get('first_name')
            new_data.last_name = requestData.get('response')[0].get('last_name')
            new_data.sex = requestData.get('response')[0].get('sex')
            new_data.status = requestData.get('response')[0].get('status')
            if requestData.get('response')[0].get('city'):
                new_data.city_id = requestData.get('response')[0].get('city').get('id')
                new_data.city_title = requestData.get('response')[0].get('city').get('title')
            new_data.bdate = requestData.get('response')[0].get('bdate')
            new_data.about = requestData.get('response')[0].get('about')
            new_data.activities = requestData.get('response')[0].get('activities')
            new_data.books = requestData.get('response')[0].get('books')
            new_data.career = requestData.get('response')[0].get('career')
            new_data.connections = requestData.get('response')[0].get('connections')
            new_data.contacts = requestData.get('response')[0].get('contacts')
            if requestData.get('response')[0].get('country'):
                new_data.country_id = requestData.get('response')[0].get('country').get('id')
                new_data.country_title = requestData.get('response')[0].get('country').get('title')
            new_data.domain = requestData.get('response')[0].get('domain')
            new_data.education = requestData.get('response')[0].get('education')
            new_data.home_town = requestData.get('response')[0].get('home_town')
            new_data.received_date = timezone.now()
            new_data.save()



def loadUserData(request):

    s = sched.scheduler(time.time,time.sleep)
    userData1 =int(UserData.objects.order_by('-received_date')[0].id) + 1

    while True:
        s.enter(0.5,0.5,loadOneUserData,(userData1,))
        s.run()
        userData1 += 1


    return redirect('mainPage')

def calculate_age(data):

    bd = data.split('.')

    if len(bd) == 3:
        today = date.today()

        return today.year - int(bd[2]) - ((today.month, today.day) < (int(bd[1]), (int(bd[0]))))#interesting solution))

def visualisation(request):
    # df = pd.DataFrame(UserData.objects.values('city_title','city_id'))#кол во жителей в каждом городе
    usersInBiggestCities = UserData.objects.values('city_title').annotate(total = Count('city_title')).order_by('-total')[:5]
    allUsersInCities = UserData.objects.values('city_title').annotate(total = Count('city_title')).order_by('-total')


    if usersInBiggestCities:
        df = pd.DataFrame(usersInBiggestCities.values('city_title','total'))
        circleDiagram = px.pie(
            data_frame = df,
            values = 'total',#размер куска круга
            # names = 'city_title',
            color = 'city_title',
        )
        circleDiagram = circleDiagram.to_html()
    else:
        circleDiagram = 'no data to analise yet'

    return render(request,'visualisation.html',{'circleDiagram':circleDiagram,'allUsersInCities':allUsersInCities,})

def visualisationCountries(request):
    usersInBiggestCountries = UserData.objects.values('country_title').annotate(total = Count('country_title')).order_by('-total')[:5]
    allUsersInCountries = UserData.objects.values('country_title').annotate(total = Count('country_title')).order_by('-total')

    if usersInBiggestCountries:
        df = pd.DataFrame(usersInBiggestCountries.values('country_title','total'))
        circleDiagram = px.pie(
            data_frame = df,
            values = 'total',#размер куска круга
            # names = 'country_title',иконки с обозначением справа
            color = 'country_title',
        )
        circleDiagram = circleDiagram.to_html()
    else:
        circleDiagram = 'no data to analise yet'

    return render(request,'visualisationCountries.html',{'circleDiagram':circleDiagram,'allUsersInCountries':allUsersInCountries,})

def visualisationSex(request):
    allUsersSex = UserData.objects.values('sex').annotate(total = Count('sex'))

    if allUsersSex:
        df = pd.DataFrame(allUsersSex.values('sex','total'))
        circleDiagram = px.pie(
            data_frame = df,
            values = 'total',#размер куска круга
            # names = 'sex',
            color = 'sex',
            color_discrete_sequence = ['sky blue','pink']
        )
        circleDiagram = circleDiagram.to_html()
    else:
        circleDiagram = 'no data to analise yet'

    return render(request,'visualisationSex.html',{'circleDiagram':circleDiagram,'allUsersSex':allUsersSex,})


def extendedInfo(request,pk):

    userData = get_object_or_404(UserData,pk = pk)

    return render(request,'extendedInfo.html',{'userData':userData})

def visualisationAge(request):

    # allUsersBD = UserData.objects.values('bdate')
    # print(allUsersBD)
    allUsersAge = []
    allUsersAgeFiltered = []
    allUsersAgeFilteredSorted = []


    for i in UserData.objects.all():
        if i.bdate:
            j = i.bdate
            if calculate_age(j) != None:
                age = calculate_age(j)
                allUsersAge.append({'id':i.id,'age':age})

    if allUsersAge:
        for i in range(200):
            arr = [x['age'] for x in allUsersAge if x['age'] == i]
            allUsersAgeFiltered.append({'age':i,'total':len(arr)})

        allUsersAgeFilteredSorted = sorted(allUsersAgeFiltered,key=itemgetter('total'),reverse = True)

        allUsersAgeFiltered = [i for i in allUsersAgeFiltered if not (i['total'] == 0)]


        if allUsersAgeFilteredSorted:
            # df = pd.DataFrame(allUsersAge)
            df = pd.DataFrame(allUsersAgeFilteredSorted[:5])
            circleDiagram = px.pie(
                data_frame = df,
                values = 'total',#размер куска круга
                names = 'age',
                color = 'age',
            )
            circleDiagram = circleDiagram.to_html()
        else:
            circleDiagram = 'no data to analise yet'

        if allUsersAgeFiltered:
            df = pd.DataFrame(allUsersAgeFiltered)
            fig = px.bar(df,x='age',y='total')
            fig.update_xaxes(type='category')
            fig = fig.to_html()

    else:
        allUsersAgeFilteredSorted = 'no data to analise yet'
        circleDiagram = 'no data to analise yet'
        fig = 'no data to analise yet'

    #
    # allUsersInCountries = UserData.objects.values('country_title').annotate(total = Count('country_title'))
    #
    # df = pd.DataFrame(allUsersInCountries)
    # fig1 = px.scatter_geo(df, locations="country_title",hover_name="country_title", size="total",projection="natural earth")
    # fig1 = fig1.to_html()


    return render(request,'visualisationAge.html',{'circleDiagram':circleDiagram,'allUsersAgeFilteredSorted':allUsersAgeFilteredSorted,'fig':fig,})

def visualisationNames(request):

    menData = UserData.objects.filter(sex = 2).values('first_name').annotate(total = Count('first_name')).order_by('-total')
    womenData = UserData.objects.filter(sex = 1).values('first_name').annotate(total = Count('first_name')).order_by('-total')

    if menData:
        df = pd.DataFrame(menData.values('first_name','total')[:10])
        circleDiagramMen = px.pie(
            data_frame = df,
            values = 'total',#размер куска круга
            names = 'first_name',
            color = 'first_name',
        )
        circleDiagramMen = circleDiagramMen.to_html()
    else:
        circleDiagramMen = 'no data to analise yet'

    if womenData:
        df = pd.DataFrame(womenData.values('first_name','total')[:10])
        circleDiagramWomen = px.pie(
            data_frame = df,
            values = 'total',#размер куска круга
            names = 'first_name',
            color = 'first_name',
        )
        circleDiagramWomen = circleDiagramWomen.to_html()
    else:
        circleDiagramWomen = 'no data to analise yet'


    return render(request,'visualisationNames.html',{'circleDiagramMen':circleDiagramMen,'circleDiagramWomen':circleDiagramWomen,'womenData':womenData,'menData':menData,})

def technical(request):

    form = DataForm()

    return render(request,'technical.html',{'form':form,})

def loadUserDataLimited(request):


    if request.method == 'POST':
        form = DataForm(request.POST)
        if form.is_valid():

            amountOfUsers =int( form.cleaned_data.get('amountOfUsers'))
            userData1 =int(UserData.objects.order_by('-received_date')[0].id) + 1
            userData2 = userData1 + amountOfUsers

            s = sched.scheduler(time.time,time.sleep)

            while userData1 < userData2:
                s.enter(0.5,0.5,loadOneUserData,(userData1,))
                s.run()
                userData1 +=1

    return redirect('mainPage')
