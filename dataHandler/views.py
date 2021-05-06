from django.shortcuts import render
from django.shortcuts import redirect
from .models import UserData

import requests # для запросов к api

import time,sched



def mainPage(request):

    userData = UserData.objects.order_by('-received_date')

    amountOfUsers = UserData.objects.all().count()

    moskow = UserData.objects.filter(city_id = '1').count()
    st_petersburg = UserData.objects.filter(city_id = '2').count()

    return render(request,'mainPage.html',{'userData':userData,'all':amountOfUsers,'moskow':moskow,'st_petersburg':st_petersburg})
# {'dataList':dataList,}

# TemplateResponse(request,'mainPage.html',{'dataList':dataList,})
# t = TemplateResponse(request,'mainPage.html',{'script':fuuu})
# t.render()
# return t
def load(param=100):

    URL = 'https://api.vk.com/method/users.get'

    PARAMS = {'fields':'sex,status,city,bdate,about,activities,books,career,connections,contacts,country,domain,education,home_town','user_id':param,'v':5.52,'access_token':'b5b6d031c6fe67acac183a1fa8238ac532130d82355bfb8dff764455d43309c35b1fac9aa64b3e70d657d'}

    req = requests.get(url = URL,params = PARAMS)

    requestData = req.json()
    print(requestData)
    if requestData is not None or requestData.get('response')[0].get('first_name') != 'DELETED' :
        new_data = UserData()
        new_data.id = requestData.get('response')[0].get('id')
        new_data.first_name = requestData.get('response')[0].get('first_name')
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
        new_data.save()


def loadData():
    # t = TemplateResponse(request,'mainPage.html',{})
    URL = 'https://api.vk.com/method/users.get'

    PARAMS = {'fields':'sex,status,city,bdate,about,activities,books,career,connections,contacts,country,domain,education,home_town','user_id':1,'v':5.52,'access_token':'b5b6d031c6fe67acac183a1fa8238ac532130d82355bfb8dff764455d43309c35b1fac9aa64b3e70d657d'}

    # PARAMS['user_id'] += 1
    # req = requests.get(url = URL,params = PARAMS)
    #
    # requestData = req.json()

    dataList = []

    # def add() :
    #     for i in range(4):
    #         req = requests.get(url = URL,params = PARAMS)
    #
    #         requestData = req.json()
    #
    #         if not requestData.get('response')[0].get('deactivated') :
    #             dataList.append(requestData)
    #             PARAMS['user_id'] += 1
    #
    # set_interval(add,1)

    # for i in range(10):
    #     req = requests.get(url = URL,params = PARAMS)
    #
    #     requestData = req.json()
    #
    #     if requestData.get('response')[0].get('first_name') != 'DELETED' :
    #         dataList.append(requestData)
    #         time.sleep(1)
    #
    #     PARAMS['user_id'] += 1

    for i in range(10,20):
        set_interval(load(i),1)
        PARAMS['user_id'] += 1

    #a = requestData.get('response')[0].get('first_name') # получение данных из переменной
    # PARAMS['user_id'] = 10 изменение данных переменной
    # b = PARAMS.get('user_id') получение данных

def p():
    print('kek')
def kek(request):
    # print('kek')
    s = sched.scheduler(time.time,time.sleep)
    user_id = 1
    while True:
        s.enter(1,1,load,(user_id,))
        s.run()
        user_id += 1
        # set_interval(p,1,i)
    return redirect('mainPage')

def lol():
    # print('kek')
    s = sched.scheduler(time.time,time.sleep)
    user_id = 1
    while user_id <20   :
        s.enter(1,1,load,(user_id,))
        s.run()
        user_id += 1
        # set_interval(p,1,i)
