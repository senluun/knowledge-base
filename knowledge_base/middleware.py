"""
Дополнительный middleware для заголовков безопасности (CSP/Permissions-Policy).
"""

import logging
from django.conf import settings


logger = logging.getLogger(__name__)


class PermissionsPolicyMiddleware:
    """Минимальный и корректный middleware для настройки заголовков."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Permissions-Policy (минимально необходимая настройка)
        response['Permissions-Policy'] = 'unload=*'

        # Разрешаем необходимые CDN для CSS/JS/шрифтов
        csp_policy = (
            "default-src 'self'; "
            "img-src 'self' data: https: blob:; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
            "connect-src 'self'; "
            "frame-ancestors 'self'; "
            "media-src 'self' data: blob:; "
            "worker-src 'self' blob:"
        )

        # Для страниц редактора/админки оставляем те же мягкие правила
        if request.path.startswith('/knowledge/create-article/') or request.path.startswith('/admin/'):
            pass

        # Сбрасываем и устанавливаем заголовки CSP
        for header in ('Content-Security-Policy', 'X-Content-Security-Policy', 'X-WebKit-CSP'):
            response.headers.pop(header, None)
            response[header] = csp_policy

        # Админка: снимаем строгий COOP
        if request.path.startswith('/admin/'):
            response.headers.pop('Cross-Origin-Opener-Policy', None)
            response['Cross-Origin-Opener-Policy'] = 'same-origin-allow-popups'
            response['Cross-Origin-Embedder-Policy'] = 'unsafe-none'

        if settings.DEBUG:
            logger.info(f"CSP установлен для {request.path}")

        return response













