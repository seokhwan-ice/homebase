"""
ASGI config for homebase project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

# django가 사용할 설정 파일 지정 -> 우리 프로젝트 설정 정보 불러오기!
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homebase.settings")
# django ASGI 앱 초기화 -> 이걸 해야 ORM 모델 불러올때 문제 안생김.
django_asgi_app = get_asgi_application()

from chat.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(  # 허용된 호스트에서만 허용
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),  # 사용자 인증 처리하고 WebSocket 요청의 URL 경로를 라우팅
    }
)
