from django.urls import path
from . import views
from . views import LikeView


urlpatterns = [
    path('mine/', views.ManagePodListView.as_view(), name='manage_pod_list'),
    path('create/', views.PodCreateView.as_view(), name='pod_create'),
    path('<pk>/edit/', views.PodUpdateView.as_view(), name='pod_edit'),
    path('<pk>/delete/', views.PodDeleteView.as_view(), name='pod_delete'),
    path('<pk>/module/', views.PodModuleUpdateView.as_view(), name='pod_module_update'),
    path('module/<int:module_id>/content/<model_name>/create/', views.ContentCreateUpdateView.as_view(), name='module_content_create'),
    path('module/<int:module_id>/content/<model_name>/<id>/', views.ContentCreateUpdateView.as_view(), name='module_content_update'),
    path('content/<int:id>/delete/', views.ContentDeleteView.as_view(), name='module_content_delete'),
    path('module/<int:module_id>', views.ModuleContentListView.as_view(), name='module_content_list'),
    path('module/order/', views.ModuleOrderView.as_view(), name='module_order'),
    path('content/order/',views.ContentOrderView.as_view(),name='content_order'),
    path('tags/<slug:tag_slug>/', views.TagListView.as_view(), name='pods_by_tag'),
    path('<slug:slug>/', views.PodDetailView.as_view(), name='pod_detail'),
    ##
    path('search_pods', views.search_pods , name='search_pods'),
    path('like/<int:pk>', LikeView, name= 'like_pod'),
    

    
       
]