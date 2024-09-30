from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "nickname",
            "name",
        ]


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "profile_image",
            "nickname",
            "bio",
            "created_at",
        ]


# 추가적인 커뮤니티, 코멘트, 좋아요 구현 후 필드추가.


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "phone_number", "nickname", "bio"]


# account- 내 계정(개인정보) 수정 페이지 추후 비번필드도 보여줌?


class UserProfileTitleSerializer(serializers.ModelSerializer):
    community_free_title = serializers.SerializerMethodField()

    def get_community_free_title(self, obj):
        user_free_article = obj.free_title.all()
        title = []

        for free in user_free_article:
            if free.title:
                title.append(free.title)
        return title

    class Meta:
        model = User
        fields = ["community_free_title", "nickname", "created_at"]


class UserProfileliveViewSerializer(serializers.ModelSerializer):
    community_live_image = serializers.SerializerMethodField()

    def get_community_live_image(self, obj):
        user_live_image = obj.author_live.all()
        images = []

        for live_image in user_live_image:
            if live_image.live_image:
                live_image.append(live_image.title)
        return images

    class Meta:
        model = User
        fields = ["community_live_image", "nickname", "created_at"]


class FollowingListSerializer(serializers.ModelSerializer):
    following_count = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    following_list = serializers.SerializerMethodField()

    def get_following_list(self, obj):
        following = obj.followings.all()
        nicknames = []

        for following_users in following:
            nicknames.append(following_users.nickname)
        return nicknames

    def get_following_count(self, obj):
        return obj.followings.count()

    def get_follower_count(self, obj):
        return obj.followers.count()

    class Meta:
        model = User
        fields = [
            "nickname",
            "profile_image",
            "nickname",
            "bio",
            "created_at",
            "following_count",
            "follower_count",
            "following_list",
        ]
