from django.urls import path, include
from .views import Login_view, Register_view
app_name = "patient"

urlpatterns = [
	path('login/', Login_view.as_view()),
	path('register/', Register_view.as_view()),
]