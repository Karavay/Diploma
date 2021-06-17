# import sched,time
#
# from dataHandler.views import loadUserDataLimi
#
# def lol():
#     # print('kek')
#     s = sched.scheduler(time.time,time.sleep)
#     user_id = 1
#     while user_id <20   :
#         s.enter(1,1,load,(user_id,))
#         s.run()
#         user_id += 1
#         # set_interval(p,1,i)
#
# lol()
# maybe i will need it

async def loadUserDataLimited(request):


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
