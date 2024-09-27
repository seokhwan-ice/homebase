from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    
    path("signup/", views.UserCreateView.as_view()),
    path("signin/", views.UserLoginView.as_view()),
    path("signout/", views.UserSignoutView.as_view()),
    path("password/", views.UserPasswordChangeView.as_view()),
    path("withdraw/", views.UserDeleteView.as_view()),
    path("<str:username>/", views.UserProfileView.as_view()),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
