from django.urls import path
from . import views

urlpatterns = [
    path('',views.mainPage,name='mainPage'),
    path('loadUserData',views.loadUserData,name='loadUserData'),
    path('visualisation',views.visualisation,name='visualisation'),
    path('<int:pk>/',views.extendedInfo,name='extendedInfo'),
    path('visualisationCountries',views.visualisationCountries,name='visualisationCountries'),
    path('visualisationSex',views.visualisationSex,name='visualisationSex'),
    path('visualisationAge',views.visualisationAge,name='visualisationAge'),
    path('visualisationNames',views.visualisationNames,name='visualisationNames'),
    path('technical',views.technical,name='technical'),
    path('loadUserDataLimited',views.loadUserDataLimited,name='loadUserDataLimited'),
    path('printInConsole',views.printInConsole,name='printInConsole'),
]
