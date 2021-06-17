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

from django.db.models import Count,Sum

from django.utils import timezone

from .forms import DataForm

import asyncio#asynchronous library
from django.http import HttpResponse

def mainPage(request):

    userData = UserData.objects.order_by('-received_date')[:1000]

    allUsersInDB = UserData.objects.all().count()

    lastUserID =int(UserData.objects.order_by('-received_date')[0].id)

    form = DataForm()

    return render(request,'mainPage.html',{'userData':userData,'allUsersInDB':allUsersInDB,'lastUserID':lastUserID,'form':form})

def loadOneUserData(param):# function that makes api request,param = id of vk user,we use this func in another function

    URL = 'https://api.vk.com/method/users.get'

    PARAMS = {'fields':'sex,status,city,bdate,about,activities,books,career,connections,contacts,country,domain,education,home_town,photo_max_orig','user_id':param,'v':5.52,'access_token':'43ce5a0d661b79858eb31a0aecc69201db4025cae396066b1832b6f9f729553c35447910b2ad4429801eb'}
    #https://oauth.vk.com/authorize?client_id=5490057&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends&response_type=token&v=5.52 get token

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
            if  requestData.get('response')[0].get('photo_max_orig'):
                new_data.photo = requestData.get('response')[0].get('photo_max_orig')
            new_data.save()



def loadUserData(request):

    s = sched.scheduler(time.time,time.sleep)
    userData1 =int(UserData.objects.order_by('-received_date')[0].id) + 1

    while True:
        s.enter(0.5,0.5,loadOneUserData,(userData1,))
        s.run()
        userData1 += 1

    return redirect('mainPage')

# async def loadUserData(request):
#
#     async def l(request):
#         userData1 =int(UserData.objects.order_by('-received_date')[0].id) + 1
#
#         while True:
#             await asyncio.sleep(1)
#             loadOneUserData(userData1)
#             userData1 += 1
#
#     await asyncio.run(l())
#
#
#
#     return HttpResponse('mainPage')

def calculate_age(data):

    bd = data.split('.')

    if len(bd) == 3:
        today = date.today()

        return today.year - int(bd[2]) - ((today.month, today.day) < (int(bd[1]), (int(bd[0]))))#interesting solution))

def visualisation(request):
    # df = pd.DataFrame(UserData.objects.values('city_title','city_id'))#кол во жителей в каждом городе
    usersInBiggestCities = UserData.objects.values('city_title').annotate(total = Count('city_title')).order_by('-total')[:5]
    allUsersInCities = UserData.objects.values('city_title').annotate(total = Count('city_title')).order_by('-total')

    usersInOtherCities = UserData.objects.values('city_title').annotate(total = Count('city_title')).order_by('-total')[5:].aggregate(other = Sum('total')).get("other")
    #
    # allCities = UserData.objects.filter(city_title__isnull = False).count()
    listOfCitiesForDiagram = []

    for i in usersInBiggestCities:#add 5 biggest cities to the list
        listOfCitiesForDiagram.append(i)

    listOfCitiesForDiagram.append({'city_title':'others', 'total':usersInOtherCities})# add other cities

    if usersInBiggestCities:
        df = pd.DataFrame(listOfCitiesForDiagram)
        # df2 = pd.DataFrame({'city_title': 'other cities','total': usersInOtherCities},index = [5])
        # print(df1,'\n')
        # print(df2,'\n')
        # df1.append(df2,ignore_index = True)
        # print(df1,'\n')

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

    usersInOtherCountries = UserData.objects.values('country_title').annotate(total = Count('country_title')).order_by('-total')[5:].aggregate(other = Sum('total')).get("other")

    listOfCountriesForDiagram = []

    for i in usersInBiggestCountries:
        listOfCountriesForDiagram.append(i)

    listOfCountriesForDiagram.append({'country_title':'others', 'total':usersInOtherCountries})

    if usersInBiggestCountries:
        df = pd.DataFrame(listOfCountriesForDiagram)
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
    allUsersMonth = []
    allUsersMonthFiltered = []
    allUsersMonthFilteredSorted = []


    for i in UserData.objects.all():
        if i.bdate:
            j = i.bdate
            if calculate_age(j) != None:
                age = calculate_age(j)
                month = j.split('.')[1]
                allUsersAge.append({'id':i.id,'age':age})
                allUsersMonth.append({'id':i.id,'month':month})

    if allUsersAge:
        for i in range(200):
            arr = [x['age'] for x in allUsersAge if x['age'] == i]
            allUsersAgeFiltered.append({'age':i,'total':len(arr)})

        allUsersAgeFilteredSorted = sorted(allUsersAgeFiltered,key=itemgetter('total'),reverse = True)

        allUsersAgeFiltered = [i for i in allUsersAgeFiltered if not (i['total'] == 0)]

        otherUsersAge = 0
        listOfAgesForDiagram = []

        for i in allUsersAgeFilteredSorted[5:]:
            otherUsersAge += i['total']

        for i in allUsersAgeFilteredSorted[:5]:
            listOfAgesForDiagram.append(i)

        listOfAgesForDiagram.append({'age':'others','total':otherUsersAge})

        if allUsersAgeFilteredSorted:
            # df = pd.DataFrame(allUsersAge)
            df = pd.DataFrame(listOfAgesForDiagram)
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

    if allUsersMonth:
        months = ['january','february','march','april','may','june','july','august','september','october','november','december']
        for i,j in zip(range(1,13),months):
            arr = [x['month'] for x in allUsersMonth if int(x['month']) == i]
            allUsersMonthFiltered.append({'month':j,'total':len(arr)})

        allUsersMonthFilteredSorted = sorted(allUsersMonthFiltered,key=itemgetter('total'),reverse = True)

        allUsersMonthFiltered = [i for i in allUsersMonthFiltered if not (i['total'] == 0)]


        if allUsersMonthFilteredSorted:

            if allUsersMonthFiltered:
                df = pd.DataFrame(allUsersMonthFiltered)
                figMonth = px.bar(df,x='month',y='total')
                figMonth.update_xaxes(type='category')
                figMonth = figMonth.to_html()

    else:
        figMonth = 'no data to analise yet'


    #
    # allUsersInCountries = UserData.objects.values('country_title').annotate(total = Count('country_title'))
    #
    # df = pd.DataFrame(allUsersInCountries)
    # fig1 = px.scatter_geo(df, locations="country_title",hover_name="country_title", size="total",projection="natural earth")
    # fig1 = fig1.to_html()


    return render(request,'visualisationAge.html',{'circleDiagram':circleDiagram,'allUsersAgeFilteredSorted':allUsersAgeFilteredSorted,'fig':fig,'figMonth':figMonth,})

def visualisationNames(request):

    menData = UserData.objects.filter(sex = 2).values('first_name').annotate(total = Count('first_name')).order_by('-total')
    womenData = UserData.objects.filter(sex = 1).values('first_name').annotate(total = Count('first_name')).order_by('-total')

    listOfMenNamesForDiagram = []
    listOfWomenNamesForDiagram = []
    otherMen = 0
    otherWomen = 0

    for i in menData[:10]:#add 5 biggest cities to the list
        listOfMenNamesForDiagram.append(i)

    for i in menData[10:]:
        otherMen += i['total']

    listOfMenNamesForDiagram.append({'first_name':'others','total':otherMen})

    for i in womenData[:10]:#add 5 biggest cities to the list
        listOfWomenNamesForDiagram.append(i)

    for i in womenData[10:]:
        otherWomen += i['total']

    listOfWomenNamesForDiagram.append({'first_name':'others','total':otherWomen})

    if menData:
        df = pd.DataFrame(listOfMenNamesForDiagram)
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
        df = pd.DataFrame(listOfWomenNamesForDiagram)
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



async def main():
    userData1 =int(UserData.objects.order_by('-received_date')[0].id) + 1
    while True:
        await asyncio.sleep(1)
        loadOneUserData(userData1)
        userData1 += 1

async def printInConsole(request):
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # loop.create_task(main())
    # while True:
    #     await asyncio.sleep(1)
    #     print('kek')
    loop = asyncio.new_event_loop()
    ss = loop.run_until_complete(print('kek'))
    loop.close()
    return HttpResponse(ss,content_type='text/plain')
