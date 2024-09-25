from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .vaildators import validate_user_data
from .serializers import UserSerializer


class UserCreateView(APIView):
    def post(self,request):
        rlt_message = validate_user_data(request.data)
        if rlt_message is not None:
            return Response({"message": rlt_message},status=400)
        
        user = User.objects.create_user(**request.data) # 코드 간소화
        
        # user = User.objects.create_user(
        #     username=request.data.get("username"),
        #     nickname=request.data.get("nickname"),
        #     name = request.data.get("name"),
        #     password=request.data.get("password"),
        #     bio=request.data.get("bio"),
        #     profile_image=request.data.get("profile_image"),
        #     phone_number=request.data.get("phone_number"),
        # )

        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"message": "아이디 또는 비밀번호가 틀렸습니다"}, status=400)
        

        refresh = RefreshToken.for_user(user)

        return Response(
        {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        }
    )

