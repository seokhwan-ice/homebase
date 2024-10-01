from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'', views.UserViewSet, basename='user')

urlpatterns = [
    path("", include(router.urls)),
#     path("signup/", views.UserCreateView.as_view()),
#     path("signin/", views.UserLoginView.as_view()),
#     path("signout/", views.UserSignoutView.as_view()),
#     path("password/", views.UserPasswordChangeView.as_view()),
#     path("withdraw/", views.UserDeleteView.as_view()),
#     path("<str:username>/", views.UserProfileView.as_view()),
#     path("<str:username>/free/", views.UserProfileTitleView.as_view()),
#     path("<str:username>/live/", views.UserProfileliveView.as_view()),
#     path("<str:username>/follow/", views.FollowAPIView.as_view()),
#     path("<str:username>/followinglist/", views.FollowingListAPIView.as_view()),
#     path("<str:username>/followerslist/", views.FollowerslistAPIView.as_view()),
#     path("<str:username>/commentlist/", views.CommentsListAPIView.as_view()),
#     path("<str:username>/bookmark/", views.BookMarkListAPIView.as_view()),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
