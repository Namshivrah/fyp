# #routing websockets requests

# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.urls import path
# from freedom import consumers
# from freedom.consumers import MyConsumer
# from django.urls import re_path

# websocket_urlpatterns = [
#     re_path(r'ws/my_websocket/$', consumers.MyConsumer.as_asgi()),
# ]

# application = ProtocolTypeRouter(
#     {
#         'http': get_asgi_application(),
#         'websocket': URLRouter(websocket_urlpatterns)
#     }
# )