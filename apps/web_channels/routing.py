from django.urls import path

from apps.web_channels.consumers import TherapyConsumer

ws_urlpatterns = [
    path('ws/asgi/', TherapyConsumer.as_asgi())
]

