from django.conf.urls import include 
from django.urls import path,re_path as url 
from log_app import views, api_views, auth_views 
from django.contrib.auth import views as dj_auth_views 


urlpatterns = [
    url(r'^announcements/$',api_views.Announcements.as_view(),name="announcements"),
    url(r'^all-announcements/$',api_views.AllAnnouncements.as_view(),name="all_announcements"),
    url(r'^stations/$',auth_views.AllUserStations.as_view(),name="stations"),
    url(r'^profiles/$',auth_views.AllProfiles.as_view(),name="profiles"),
    url(r'^user-profile/$',auth_views.UserProfile.as_view(),name="user_profile"),
    url(r'^all-users/$',auth_views.UserProfiles.as_view(),name="all_users"),
    url(r'^register/$', auth_views.RegisterView.as_view(),name="register"),
    url(r'^login/$', auth_views.LoginView.as_view(),name="login"),
    url(r'^user/$', auth_views.UserView.as_view(),name="user"),
    url(r'^logout/$', auth_views.LogoutView.as_view(),name="logout"),
    url(r'^our-fuels/$', api_views.RegisteredFuels.as_view(),name='our_fuels'),
    url(r'^diesel-info/$', api_views.DieselInfo.as_view(),name='diesel_info'),
    url(r'^gas-info/$', api_views.GasInfo.as_view(),name='gas_info'),
    url(r'^petrol-info/$', api_views.PetrolInfo.as_view(),name='petrol_info'), 
    url(r'^pump-one-info/$', api_views.PumpOneInfo.as_view(),name='pump_one_info'),
    url(r'^pump-two-info/$', api_views.PumpTwoInfo.as_view(),name='pump_two_info'),
    url(r'^pump-three-info/$', api_views.PumpThreeInfo.as_view(),name='pump_three_info'), 
    url(r'^pump-four-info/$', api_views.PumpFourInfo.as_view(),name='pump_four_info'), 
    url(r'^all-logs/$', api_views.AllLogs.as_view(),name='all_logs'),
    url(r'^logs-today/$', api_views.TodayLogs.as_view(),name='logs_today'),
    url(r'^user-logs/(\d+)$', api_views.UserLogs.as_view(),name='user_logs'),
    url(r'^petrol-summary-today/',api_views.PetrolSummaryToday.as_view(),name='petrol_summary'),
    url(r'^diesel-summary-today/',api_views.DieselSummaryToday.as_view(),name='diesel_summary'),
    url(r'^gas-summary-today/',api_views.GasSummaryToday.as_view(),name='gas_summary'),
    url(r'^fuel-logs-today/(\d+)$', api_views.TodayFuelLogs.as_view(),name='fuel_logs_today'),
    url(r'^fuel-logs-ii-today/(\d+)$', api_views.TodayFuelLogsTwo.as_view(),name='fuel_logs_ii_today'),
    url(r'^fuel-logs-iii-today/(\d+)$', api_views.TodayFuelLogsThree.as_view(),name='fuel_logs_iii_today'),
    url(r'^fuel-logs-iv-today/(\d+)$', api_views.TodayFuelLogsFour.as_view(),name='fuel_logs_iv_today'),
    url(r'^all-mpesa-logs/$', api_views.AllMpesaLogs.as_view(),name='all_mpesa_logs'),
    url(r'^all-credit-card-logs/$', api_views.AllCreditCardLogs.as_view(),name='all_credit_card_logs'),
    url(r'^mpesa-logs-today/(\d+)$', api_views.TodayMpesaLogs.as_view(),name='mpesa_logs_today'),
    url(r'^credit-card-logs-today/(\d+)$', api_views.TodayCreditCardLogs.as_view(),name='credit_card_logs_today'),
    url(r'^user-mpesa-logs/(\d+)$', api_views.UserMpesaLogs.as_view(),name='user_mpesa_logs'),
    url(r'^user-credit-card-logs/(\d+)$', api_views.UserCreditCardLogs.as_view(),name='user_credit_card_logs'),
    url(r'^all-fuel-received-today/$', api_views.AllFuelReceivedToday.as_view(),name='fuel_received_today'),
    url(r'^petrol-received-today/info/(\d+)$', api_views.PetrolReceivedTodayInfo.as_view(),name='petrol_received_today-info'),
    url(r'^total-petrol-received-today/(\d+)$', api_views.TotalPetrolReceivedToday.as_view(),name='total_petrol_received_today'),
    url(r'^diesel-received-today/info/(\d+)$', api_views.DieselReceivedTodayInfo.as_view(),name='diesel_received_today-info'),
    url(r'^total-diesel-received-today/(\d+)$', api_views.TotalDieselReceivedToday.as_view(),name='total_diesel_received_today'),
    url(r'^gas-received-today/info/(\d+)$', api_views.GasReceivedTodayInfo.as_view(),name='gas_received_today-info'),
    url(r'^total-gas-received-today/(\d+)$', api_views.TotalGasReceivedToday.as_view(),name='total_gas_received_today'),
    url(r'^log-details/(\d+)$', api_views.LogDetails.as_view(),name='log_details'),
    url(r'^mpesa-log-details/(\d+)$', api_views.MpesaLogDetails.as_view(),name='mpesa_log_details'),
    url(r'^credit-card-log-details/(\d+)$', api_views.CreditCardLogDetails.as_view(),name='credit_card_log_details'),
    url(r'^past-logs/(\d{4}-\d{2}-\d{2})$',api_views.PastLogs.as_view(),name='past_logs'),
    url(r'^past-mpesa-logs/(\d{4}-\d{2}-\d{2})$',api_views.PastMpesaLogs.as_view(),name='past_mpesa_logs'),
    url(r'^past-credit-card-logs/(\d{4}-\d{2}-\d{2})$',api_views.PastCreditCardLogs.as_view(),name='past_credit_card_logs'),
    url(r'^email-report/$',api_views.EmailReport.as_view(),name='email_report'),
    url(r'^email-mpesa-report/$',api_views.EmailMpesaReport.as_view(),name='email_mpesa_report'),
    url(r'^email-credit-card-report/$',api_views.EmailCreditCardReport.as_view(),name='email_credit_card_report'),
    url(r'^incident-report/$',api_views.IncidentReport.as_view(),name='incident_report'),
    url(r'^contact-admin/$',api_views.ContactAdmin.as_view(),name='contact_admin'),

    path('change-password/',dj_auth_views.PasswordChangeView.as_view(template_name='auth/change-password.html',success_url='/user/profile/'),name='change_password'),
    path('password-reset/',dj_auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html',subject_template_name='auth/email/password_reset_subject.txt',email_template_name='auth/email/password_reset_email.html',),name='password_reset'),
    path('password-reset/done/',dj_auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_mail_sent.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',dj_auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirmation.html'),name='password_reset_confirm'),
    path('password-reset-complete/',dj_auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_completed.html'),name='password_reset_complete'),
]