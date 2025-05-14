# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('about/', views.about, name='about'),
# ]




from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('predict-ajax/', views.predict_ajax, name='predict_ajax'),
]
