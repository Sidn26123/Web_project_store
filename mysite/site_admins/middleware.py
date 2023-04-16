from django.shortcuts import redirect

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





