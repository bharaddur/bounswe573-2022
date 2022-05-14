from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.SuserRegistrationView.as_view(),name='suser_registration'),
    path('enroll-course/',views.SuserEnrollCourseView.as_view(),name='suser_enroll_course'),
    path('courses/', views.SuserCourseListView.as_view(), name='suser_course_list'),
    path('course/<pk>/', views.SuserCourseDetailView.as_view(), name='suser_course_detail'),
    path('course/<pk>/<module_id>/', views.SuserCourseDetailView.as_view(),name='suser_course_detail_module'),
]