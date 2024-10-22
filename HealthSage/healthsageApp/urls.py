from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('',views.home, name = "home"),
    path('diabetes/',views.diabetes,name = "diabetes"),
    path('pneumonia/',views.pneumonia,name = "pneumonia"),
    path('Diabetic Retinopathy/',views.DR, name = "DR"),
    path('remedies/', views.remedies,name = "remedies"),
    # path('signup/',views.user_signup,name = "signup"),
    # path('login/',views.user_login,name = "login"),
    # path('Breast-cancer/',views.breast_cancer,name = "breast_cancer" )
    # path('diabetes-detection/',diabetes_detection,name = "diabetes-detection"),
]