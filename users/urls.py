from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView


from .views import RegisterUserView, ActivateView, ForgotPasswordView, RestorePasswordView

urlpatterns = [
    path('register/', RegisterUserView.as_view()),
    path('activate/', ActivateView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('forgot/', ForgotPasswordView.as_view()),
    path('restore/', RestorePasswordView.as_view()),
]
