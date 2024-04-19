
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('freedom.urls')),
#     re_path(r'ws/my_websocket/$', consumers.MyConsumer.as_asgi()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# websocket_urlpatterns = [
#     re_path(r'ws/my_websocket/$', consumers.MyConsumer.as_asgi()),
# ]

# application = ProtocolTypeRouter(
#     {
#         'http': get_asgi_application(),
#         'websocket': URLRouter(websocket_urlpatterns)
#     }
# )
