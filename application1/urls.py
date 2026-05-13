# from django.urls import path
# from application1 import views

# urlpatterns=[
#     path('index',views.index,name='index'),
#     path('category',views.category,name='category'),
#     path('dashboard',views.dashboard,name='dashboard'),
#     path('entry1',views.entry1,name='entry1'),
#     path('manage',views.manage,name='manage'),
#     path('reports',views.reports,name='reports'),
#     path('settings',views.settings,name='settings'),
#     path('vehicle_entry',views.vehicle_entry,name='vehicle_entry'),
#     path('vehicle_number',views.vehicle_number,name='vehicle_number'),
# ]
from django.contrib import admin
from django.urls import path
from application1 import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.user_login, name='login'), # ADD THIS

    path('index', views.index, name='index'),
    path('category', views.category, name='category'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('entry1', views.entry1, name='entry1'),
    path('manage', views.manage, name='manage'),
    path('reports', views.reports, name='reports'),
    path('settings', views.settings, name='settings'),
    path('vehicle_entry', views.vehicle_entry, name='vehicle_entry'),
    path('vehicle_number', views.vehicle_number, name='vehicle_number'),
]