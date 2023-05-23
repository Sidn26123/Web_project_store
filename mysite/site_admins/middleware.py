from django.shortcuts import redirect
from django.shortcuts import render
from django.conf import settings
class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Kiểm tra xem người dùng đã đăng nhập hay chưa
        if not request.user.is_authenticated:
            # Chuyển hướng người dùng đến trang đăng nhập
            return redirect(request.build_absolute_uri('/ad/login/'))

        response = self.get_response(request)

        return response

class Custom404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 404:
            previous_page = request.META.get('HTTP_REFERER', '/')
            context = {
                'previous_page': previous_page
            }
            return render(request, settings.PAGE_TEMPLATE_404, context, status=404)

        return response



