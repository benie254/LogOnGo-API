from django.conf.urls import include 
from django.urls import path,re_path as url 
from log_app import views, api_views, auth_views 


urlpatterns = [
    path('',views.home,name='home'),
    url(r'^register/$', auth_views.RegisterView.as_view()),
    url(r'^login/$', auth_views.LoginView.as_view()),
    url(r'^user/$', auth_views.UserView.as_view()),
    url(r'^logout/$', auth_views.LogoutView.as_view()),
    url(r'^our-fuels/$', api_views.RegisteredFuels.as_view(),name='our_fuels'),
    url(r'^diesel-info/$', api_views.DieselInfo.as_view(),name='diesel_info'),
    url(r'^gas-info/$', api_views.GasInfo.as_view(),name='gas_info'),
    url(r'^petrol-info/$', api_views.PetrolInfo.as_view(),name='petrol_info'), 
    url(r'^all-logs/$', api_views.AllLogs.as_view(),name='all_logs'),
    url(r'^logs-today/$', api_views.TodayLogs.as_view(),name='logs_today'),
    url(r'^user-logs/(\d+)$', api_views.UserLogs.as_view(),name='user_logs'),
    url(r'^fuel-logs-today/(\d+)$', api_views.TodayFuelLogs.as_view(),name='fuel_logs_today'),
    url(r'^fuel-logs-ii-today/(\d+)$', api_views.TodayFuelLogsTwo.as_view(),name='fuel_logs_ii_today'),
    url(r'^fuel-logs-iii-today/(\d+)$', api_views.TodayFuelLogsThree.as_view(),name='fuel_logs_iii_today'),
    url(r'^fuel-logs-iv-today/(\d+)$', api_views.TodayFuelLogsFour.as_view(),name='fuel_logs_iv_today'),
    url(r'^fuel-logs-yesterday/(\d+)$', api_views.YesterdayFuelLogs.as_view(),name='fuel_logs_yesterday'),
    url(r'^all-mpesa-logs/$', api_views.AllMpesaLogs.as_view(),name='all_mpesa_logs'),
    url(r'^mpesa-logs-today/$', api_views.TodayMpesaLogs.as_view(),name='mpesa_logs_today'),
    url(r'^user-mpesa-logs/(\d+)$', api_views.UserMpesaLogs.as_view(),name='user_mpesa_logs'),
    url(r'^mpesa-cumulative/$', api_views.MpesaCumulative.as_view(),name='mpesa_cumulative'),
    url(r'^mpesa-total-today/$', api_views.MpesaTodayTotal.as_view(),name='mpesa_total_today'),
    url(r'^total-fuel-received-today/(\d+)$', api_views.TotalFuelReceivedToday.as_view(),name='total_fuel_today'),
    url(r'^fuel-received-today/info/(\d+)$', api_views.FuelReceivedTodayInfo.as_view(),name='fuel_received_today'),
    url(r'^log-details/(\d+)$', api_views.LogDetails.as_view(),name='log_details'),
    url(r'^mpesa-log-details/(\d+)$', api_views.MpesaLogDetails.as_view(),name='mpesa_log_details'),
    url(r'^past-logs/(\d{4}-\d{2}-\d{2})/$',api_views.PastLogs.as_view(),name='past_logs'),
]