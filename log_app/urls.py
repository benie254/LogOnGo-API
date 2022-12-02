from django.conf.urls import include 
from django.urls import path,re_path as url 
from log_app import views, api_views, auth_views 
from knox import views as knox_views

urlpatterns = [
    #auth & user URLS
    path('password/change/<int:pk>',auth_views.ChangePasswordView.as_view(),name='change-password'),
    url(r'^password/reset/request/$',auth_views.PasswordResetRequest.as_view(),name='reset-password-request'),
    path('password/reset/confirmed/<int:pk>',auth_views.ResetPasswordView.as_view(),name='reset-password-confirmed'),
    path('password/reset/complete/<slug:uidb64>/<slug:token>/',auth_views.activate,name='reset-password-complete'),
    url(r'^auth/', include('knox.urls')),
    url(r'^auth/register$', auth_views.RegisterView.as_view(),name="register"),
    url(r'^auth/login$', auth_views.LoginView.as_view(),name="login"),
    url(r'^auth/logout/$', knox_views.LogoutView.as_view(),name="knox-logout"),
    url(r'^user/$', auth_views.UserView.as_view(),name="user"),
    url(r'^profiles/$',auth_views.AllProfiles.as_view(),name="profiles"),
    url(r'^user/profile/$',auth_views.UserProfile.as_view(),name="user-profile"),
    url(r'^all-users/$',auth_views.UserProfiles.as_view(),name="all-users"),
    url(r'^all/admins/$',auth_views.AllAdmins.as_view(),name='all-admins'),
    url(r'^stations/$',auth_views.AllUserStations.as_view(),name="stations"),

    # content URLS
    url(r'^announcements/latest/$',api_views.LatestAnnouncements.as_view(),name="latest-announcements"),
    url(r'^announcements/all/$',api_views.AllAnnouncements.as_view(),name="all-announcements"),
    url(r'^announcements/update/(\d+)$',api_views.UpdateAnnouncement.as_view(),name="update-announcement"),
    url(r'^fuels/all/$', api_views.AllFuels.as_view(),name='all-fuels'),
    url(r'^fuel/info/(\d+)$', api_views.FuelInfo.as_view(),name='fuel-info'),
    url(r'^petrol/info/$', api_views.PetrolInfo.as_view(),name='petrol-info'),
    url(r'^diesel/info/$', api_views.DieselInfo.as_view(),name='diesel-info'),
    url(r'^gas/info/$', api_views.GasInfo.as_view(),name='gas-info'),
    url(r'^fuel/summary/today/(\d+)',api_views.FuelSummaryToday.as_view(),name='fuel-summary'),
    url(r'^fuel/received/today/all/$', api_views.AllFuelReceivedToday.as_view(),name='fuel-received-today'),
    url(r'^fuel/received/today/info/(\d+)$', api_views.FuelReceivedTodayInfo.as_view(),name='fuel-received-today-info'),
    url(r'^fuel/received/details/(\d+)$', api_views.FuelReceivedDetails.as_view(),name='fuel-received-details'),
    url(r'^fuel/received/today/total/(\d+)$', api_views.TotalFuelReceivedToday.as_view(),name='total-fuel-received-today'),
    url(r'^logs/all/$', api_views.AllLogs.as_view(),name='all-logs'),
    url(r'^logs/today/$', api_views.LogsToday.as_view(),name='logs-today'),
    url(r'^logs/user/(\d+)$', api_views.UserLogs.as_view(),name='user-logs'),
    url(r'^logs/today/fuel/(\d+)$', api_views.FuelLogsToday.as_view(),name='fuel-logs-today'),
    url(r'^logs/yesterday/fuel/(\d+)$', api_views.FuelLogsYesterday.as_view(),name='fuel-logs-yesterday'),
    url(r'^log/details/(\d+)$', api_views.LogDetails.as_view(),name='log-details'),
    url(r'^logs/summary/$', api_views.LogSummary.as_view(),name='logs-summary'),
    url(r'^logs/past/(\d{4}-\d{2}-\d{2})$',api_views.PastLogs.as_view(),name='past-logs'),
    url(r'^log/email/report/$',api_views.EmailReport.as_view(),name='email-report'),
    url(r'^log/delete/request/$',api_views.DeleteLogRequest.as_view(),name='delete-log-request'),
    url(r'^logs/mpesa/all/$', api_views.AllMpesaLogs.as_view(),name='all-mpesa-logs'),
    url(r'^logs/mpesa/today/(\d+)$', api_views.MpesaLogsToday.as_view(),name='mpesa-logs-today'),
    url(r'^logs/mpesa/user/(\d+)$', api_views.UserMpesaLogs.as_view(),name='user_mpesa_logs'),
    url(r'^log/mpesa/details/(\d+)$', api_views.MpesaLogDetails.as_view(),name='mpesa-details'),
    url(r'^logs/mpesa/summary/$', api_views.MpesaSummary.as_view(),name='mpesa-summary'),
    url(r'^logs/mpesa/past/(\d{4}-\d{2}-\d{2})$',api_views.PastMpesaLogs.as_view(),name='past-mpesa-logs'),
    url(r'^log/mpesa/email/report/$',api_views.EmailMpesaReport.as_view(),name='email-mpesa-report'),
    url(r'^log/mpesa/delete/request/$',api_views.DeleteMpesaRequest.as_view(),name='delete-mpesa-request'),
    url(r'^logs/card/all/$', api_views.AllCreditCardLogs.as_view(),name='all-card-logs'),
    url(r'^logs/card/today/(\d+)$', api_views.CreditCardLogsToday.as_view(),name='card-logs-today'),
    url(r'^logs/card/user/(\d+)$', api_views.UserCreditCardLogs.as_view(),name='user-card-logs'),
    url(r'^log/card/details/(\d+)$', api_views.CreditCardLogDetails.as_view(),name='card-details'),
    url(r'^logs/card/summary/$', api_views.CardSummary.as_view(),name='card-summary'),
    url(r'^logs/card/past/(\d{4}-\d{2}-\d{2})$',api_views.PastCreditCardLogs.as_view(),name='past-card-logs'),
    url(r'^log/card/email/report/$',api_views.EmailCreditCardReport.as_view(),name='email-card-report'),
    url(r'^log/card/delete/request/$',api_views.DeleteCreditCardRequest.as_view(),name='delete-card-request'),
    url(r'^incident/report/$',api_views.IncidentReport.as_view(),name='incident-report'),
    url(r'^contact/admin/$',api_views.ContactAdmin.as_view(),name='contact-admin'),
    url(r'^contact/details/(\d+)$',api_views.ContactDetails.as_view(),name='contact-details'),
    url(r'^incident/details/(\d+)$',api_views.IncidentDetails.as_view(),name='contact-details'),
]