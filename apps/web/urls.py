from django.urls import path, include
from django.views.generic import TemplateView

from . import views, api

app_name = 'web'
url_views = [
    path('home', views.home, name='home'),
    path('contact-us', TemplateView.as_view(template_name="web/pages/contact-us.html"), name='contact-us'),
    path('faq', TemplateView.as_view(template_name="web/pages/contact-us.html"), name='faq'),

    path('patients', views.patient_list, name='patients'),

    path('therapy', views.therapy, name='therapy'),
    path('therapy/session/<token>/c/<c_token>', views.therapy_client_site, name='therapy_client_site'),
    path('therapy/session/<token>/c/<c_token>/confirmation', views.therapy_client_confirm, name='therapy_client_confirm'),

    path('accounts/settings', views.account_settings, name='account_settings'),
    path('accounts/settings/deleting', views.account_settings_delete, name='account_settings_deleting'),
    path('accounts/settings/passwrod', views.account_settings, name='account_settings_passchange'),
    path('accounts/settings/profile', views.account_settings, name='account_settings_profilechange'),

    # Stripe
    path('accounts/subscription', include('apps.subscriptions.urls')),
    path('accounts/subscription/success', views.account_subscription_success, name='account_subscription_success'),
    path('accounts/subscription/canceled', views.account_subscription_canceled, name='account_subscription_canceled'),

    path('terms-and-conditions', TemplateView.as_view(template_name="web/pages/terms-and-conditions.html"), name='terms'),
    path('404', TemplateView.as_view(template_name='404.html'), name='404'),
    path('500', TemplateView.as_view(template_name='500.html'), name='500')
]

url_api = [
    path('api/patients', api.patients, name="api_patients"),
    path('api/patients/<patient_id>', api.patient, name="api_patient"),
    path('api/email/send', api.sending_email_to_patient, name='api_send_email'),
]

urlpatterns = url_views + url_api
