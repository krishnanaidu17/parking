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
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('category/', views.category, name='category'),
    path('delete_category/<int:id>/', views.delete_category, name='delete_category'),
    path('edit_category/<int:id>/', views.edit_category, name='edit_category'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('entry1', views.entry1, name='entry1'),
    path('manage', views.manage, name='manage'),
    path('reports', views.reports, name='reports'),
    path('settings', views.settings, name='settings'),
    path('vehicle_entry', views.vehicle_entry, name='vehicle_entry'),
    path('vehicle_number', views.vehicle_number, name='vehicle_number'),
    path('otp-verify/', views.otp_verify, name='otp_verify'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('toggle_category/<int:id>/', views.toggle_category, name='toggle_category'),
    path('search-vehicle/', views.search_vehicle, name='search_vehicle'),
    path(
    'toggle-vehicle-status/<int:id>/',
    views.toggle_vehicle_status,
    name='toggle_vehicle_status'
),
path(
    'clear-vehicle-search/',
    views.clear_vehicle_search,
    name='clear_vehicle_search'
),
path('remove-vehicle-search/<int:id>/', views.remove_vehicle_search, name='remove_vehicle_search'),
    # path('forgot-password/', views.forgot_password, name='forgot_password'),
    # path('send_otp/', views.send_otp, name='send_otp'),
]