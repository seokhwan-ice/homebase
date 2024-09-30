from .models import User
from rest_framework import serializers
from community.models import Comment

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


class FollowerslistSerializer(serializers.ModelSerializer):
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    followers_list = serializers.SerializerMethodField()

    def get_followers_list(self, obj):
        followers = obj.followers.all()
        nicknames = []

        for follower in followers:
            nicknames.append(follower.nickname)
        return nicknames

    def get_following_count(self, obj):
        return obj.following.count()

    def get_followers_count(self, obj):
        return obj.followers.count()

    class Meta:
        model = User
        fields = [
            "profile_image",
            "nickname",
            "bio",
            "created_at",
            "following_count",
            "followers_count",
            "followers_list",
        ]


# TODO 뉴스 댓글 추가해야해요.
class CommentsListSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    def get_comments(self, obj):
        comments = Comment.objects.filter(author=obj)
        comments_list = []

        for comment in comments:
            comments_data = {
                "content": comment.content,
                "article_type": self.get_article_type(comment),
                "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M:"),
                "updated_at": comment.updated_at.strftime(
                    "%Y-%m-%d %H:%M:"
                ),  # strftime 데이트타입 포맷터(출력date지정)
            }
            comments_list.append(comments_data)

        return comments_list

    def get_article_type(self, comment):

        # 댓글이 작성된 게시물이 Free인지 Live인지 반환
        if comment.content_type.model == "free":
            return "Free"
        elif comment.content_type.model == "live":
            return "Live"

    class Meta:
        model = User
        fields = ["profile_image", "nickname", "comments"]