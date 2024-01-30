from django.urls import path
from . import views
from django.conf import settings

urlpatterns =[
    path('v1/tasks',views.handleData),
    path('v1/tasks/<int:pk>',views.GetDeleteById),
]