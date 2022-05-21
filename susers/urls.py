from django.urls import path
from . import views 


urlpatterns = [
    path('register/',views.SuserRegistrationView.as_view(),name='suser_registration'),
    path('enroll-Pod/',views.SuserEnrollPodView.as_view(),name='suser_enroll_pod'),
    path('Pods/', views.SuserPodListView.as_view(), name='suser_pod_list'),
    path('Pod/<pk>/', views.SuserPodDetailView.as_view(), name='suser_pod_detail'),
    path('Pod/<pk>/<module_id>/', views.SuserPodDetailView.as_view(),name='suser_pod_detail_module'),
    
]