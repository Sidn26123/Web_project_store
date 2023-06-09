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
        # next_url = request.path_info
        # condition = True
        # class_name = request.user.__class__.__name__
        # if class_name == 'Doctor' and (next_url[1:3] != "do"):
        #     condition = False
        # elif class_name == 'Patient' and (next_url[1:3] != "pa"):
        #     condition = False
        # elif class_name == 'Site_admin' and (next_url[1:3] != "ad"):
        #     condition = False
        return response




class ClassRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        response = self.get_response(request)
        class_name = request.user.__class__.__name__
        print(class_name)
        next_url = request.path_info
        previous_page = request.META.get('HTTP_REFERER', '/')
        context = {
            'previous_page': previous_page
        }
        if (class_name == 'Doctor' and (next_url[1:3] in ["ad", "pa"])) or (class_name == 'Patient' and (next_url[1:3] in ["ad", "do"])) or (class_name == 'Site_admin' and (next_url[1:3] in ["pa", "do"])):
            return render(request, settings.PAGE_NOT_AVAILABLE, context)
        # # Kiểm tra điều kiện của bạn



        # if condition == False:
        #     return redirect('page_not_allowed')  # Chuyển hướng đến trang không cho phép
        return response