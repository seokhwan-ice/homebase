from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .vaildators import validate_user_data
from .serializers import (
    UserSerializer,
    UserProfileSerializer,
    UpdateProfileSerializer,
    UserProfileTitleSerializer,
    FollowingListSerializer,
    UserProfileliveViewSerializer,
    FollowerslistSerializer,
    CommentsListSerializer,
    BookMarkListSerializer,
    MyProfileSerializer,
    UpdateMyProfileSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.generics import CreateAPIView


class UserCreateView(APIView):
    def post(self, request):
        rlt_message = validate_user_data(request.data)
        if rlt_message is not None:
            return Response({"message": rlt_message}, status=400)

        user = User.objects.create_user(**request.data)  # 코드 간소화

        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {"message": "아이디 또는 비밀번호가 틀렸습니다"}, status=400
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        if request.user == user:
            serializer = UserProfileSerializer(user)
            return Response(serializer.data)
        else:
            serializer = MyProfileSerializer(user)
            return Response(serializer.data)

    def put(self, request, username):
        user = get_object_or_404(User, username=username)
        if request.user != user:
            raise PermissionDenied("수정 권한이 없습니다")
        serializer = UpdateProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def patch(self, request, username):
        user = get_object_or_404(User, username=username)
        if request.user == user:

            serializer = UpdateMyProfileSerializer(
                user, data=request.data, partial=True
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)


class UserPasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):

        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not old_password or not new_password:
            return Response({"message": " 비밀번호 똑디 입력해주세요"}, status=400)

        if not request.user.check_password(old_password):
            return Response({"message": "이전 비밀번호가 틀렸습니다."}, status=400)

        request.user.set_password(new_password)
        request.user.save()

        # 새로운 토큰 발급
        refresh = RefreshToken.for_user(request.user)
        access_token = refresh.access_token

        return Response(
            {
                "message": "비밀번호 변경 성공!",
                "access": str(access_token),
                "refresh": str(refresh),
            },
            status=200,
        )


class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        password = request.data.get("password")
        if not request.user.check_password(password):
            return Response({"message": "비밀번호가 틀렸습니다."}, status=400)

        request.user.is_active = False
        request.user.save()
        return Response({"message": "회원 탈퇴 성공!!"}, status=200)


class UserSignoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"message": "로그아웃 실패!"}, status=400)
        token = RefreshToken(refresh_token)  # RefreshToken 객체 생성
        token.blacklist()  # 블랙리스트에 추가
        return Response({"message": "로그아웃 성공!"}, status=205)


class UserProfileTitleView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근

    def get(self, request, username):
        user = get_object_or_404(
            User, username=username
        )  # username db에서 찾기, 없으면 404 반환
        serializer = UserProfileTitleSerializer(user)
        return Response(serializer.data)


class UserProfileliveView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserProfileliveViewSerializer(user)
        return Response(serializer.data)


class FollowAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        user = get_object_or_404(User, username=username)
        if request.user == user:
            return Response("나 자신을 팔로우 할 수 없습니다.", status=status.HTTP_400_BAD_REQUEST)
        if request.user in user.followers.all():
            user.followers.remove(request.user)
            return Response("언팔로우!", status=status.HTTP_200_OK)
        else:
            user.followers.add(request.user)
            return Response("팔로우성공!", status=status.HTTP_200_OK)


class FollowingListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = FollowingListSerializer(user)
        return Response(serializer.data)


class FollowerslistAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = FollowerslistSerializer(user)
        return Response(serializer.data)


class CommentsListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = CommentsListSerializer(user)
        return Response(serializer.data)


class BookMarkListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = BookMarkListSerializer(user)
        return Response(serializer.data)

