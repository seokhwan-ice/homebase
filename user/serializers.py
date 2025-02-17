from .models import User
from rest_framework import serializers
from community.models import Comment, Bookmark

# TODO 모두 구현 간소화진행할게요! 코멘트도 하나의 시리얼라이져만들어서 사용하는거 고민!!


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "nickname",
            "name",
            "profile_image",
            "phone_number",
            "bio",
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    free_article_count = serializers.SerializerMethodField()
    live_article_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    bookmark_count = serializers.SerializerMethodField()

    def get_bookmark_count(self, obj):
        return Bookmark.objects.filter(user=obj).count()

    def get_comment_count(self, obj):
        return Comment.objects.filter(author=obj).count()

    def get_free_article_count(self, obj):
        return obj.author_free.count()

    def get_live_article_count(self, obj):
        return obj.author_live.count()
            
    def get_following_count(self, obj):
        return obj.followings.count()

    def get_followers_count(self, obj):
        return obj.followers.count()

    class Meta:
        model = User
        fields = [
            "profile_image",
            "nickname",
            "bio",
            "email",
            "phone_number",
            "created_at",
            "following_count",
            "followers_count",
            "comment_count",
            "bookmark_count",
            "username",
            "live_article_count",
            "free_article_count",
        ]


# 타인의 프로필을 볼때 페이지
class MyProfileSerializer(serializers.ModelSerializer):
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    community_live_image = serializers.SerializerMethodField()

    def get_following_count(self, obj):
        return obj.followings.count()

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_community_live_image(self, obj):
        user_live_image = obj.author_live.all()
        images = []

        for live_image in user_live_image:
            if live_image.live_image:
                images.append(
                    {
                        "id": live_image.id,
                        "url": live_image.live_image.url,
                        "title": live_image.review,  # 또는 다른 필드
                        "created_at": live_image.created_at.strftime("%Y-%m-%d %H:%M"),
                    }
                )
        return images

    class Meta:
        model = User
        fields = [
            "profile_image",
            "nickname",
            "following_count",
            "followers_count",
            "community_live_image",
            "username",
            "bio",
        ]


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["profile_image", "nickname", "bio", "username"]


# 나만 보이는 페이지 부분 수정?
class UpdateMyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "phone_number",
            "username",
        ]


class UserProfileTitleSerializer(serializers.ModelSerializer):
    community_free_articles = serializers.SerializerMethodField()

    def get_community_free_articles(self, obj):
        user_free_articles = obj.author_free.all()  # 유저가 작성한 Free 게시물 가져오기
        article_data_list = []  # 리스트 초기화

        for free in user_free_articles:
            article_data = {
                "id": free.id,
                "title": free.title,
                "free_image": free.free_image.url if free.free_image else None,
                "created_at": free.created_at.strftime("%Y-%m-%d %H:%M"),
                "updated_at": free.updated_at.strftime("%Y-%m-%d %H:%M"),
            }
            article_data_list.append(article_data)  # 리스트에 딕셔너리 추가

        return article_data_list  # 리스트 반환

    class Meta:
        model = User
        fields = [
            "profile_image",
            "nickname",
            "community_free_articles",
            "username",
        ]


class UserProfileliveViewSerializer(serializers.ModelSerializer):
    community_live_articles = serializers.SerializerMethodField()

    def get_community_live_articles(self, obj):
        user_live_articles = obj.author_live.all()  # 유저가 작성한 Live 게시물 가져오기
        article_data = []

        for live in user_live_articles:
            article_data.append(
                {
                    "id": live.id,
                    "live_image": (
                        live.live_image.url if live.live_image else None
                    ),  # 이미지 URL
                    "review": live.review,  # 경기 리뷰
                    "created_at": live.created_at.strftime("%Y-%m-%d %H:%M"),
                    "updated_at": live.updated_at.strftime("%Y-%m-%d %H:%M"),
                }
            )

        return article_data

    class Meta:
        model = User
        fields = [
            "profile_image",
            "username",
            "nickname",
            "community_live_articles",  # live 게시글 데이터
        ]


class FollowingListSerializer(serializers.ModelSerializer):
    following_count = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    following_list = serializers.SerializerMethodField()

    def get_following_list(self, obj):
        followings = obj.followings.all()
        followings_data = []

        for following in followings:
            followings_data.append(
                {
                    "username": following.username,
                    "nickname": following.nickname,
                    "profile_image": (
                        following.profile_image if following.profile_image else None
                    ),
                }
            )
        return followings_data

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
            "username",
        ]


class FollowerslistSerializer(serializers.ModelSerializer):
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    followers_list = serializers.SerializerMethodField()

    def get_followers_list(self, obj):
        followers = obj.followers.all()
        followers_data = []

        for follower in followers:
            followers_data.append(
                {
                    "username": follower.username,
                    "nickname": follower.nickname,
                    "profile_image": (
                        follower.profile_image if follower.profile_image else None
                    ),
                }
            )
        return followers_data

    def get_following_count(self, obj):
        return obj.followings.count()

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
            "username",
        ]


# TODO 뉴스 댓글 추가해야해요.
class CommentsListSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    def get_comments(self, obj):
        comments = Comment.objects.filter(author=obj)
        comments_list = []

        for comment in comments:
            comments_data = {
                "id": comment.content_object.id,
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
        fields = ["username", "profile_image", "nickname", "comments"]


class BookMarkListSerializer(serializers.ModelSerializer):
    bookmark = serializers.SerializerMethodField()

    def get_bookmark(self, obj):
        bookmarks = Bookmark.objects.filter(user=obj)
        bookmark_list = []

        for bookmark in bookmarks:
            bookmarks_data = {
                "id": bookmark.content_object.id,
                "article_type": self.get_article_type(bookmark),
                "title": self.get_article_title(
                    bookmark
                ),  # Live에서는 review 필드로 변경됨
                "created_at": bookmark.created_at.strftime("%Y-%m-%d %H:%M"),
                "updated_at": bookmark.updated_at.strftime("%Y-%m-%d %H:%M"),
            }
            bookmark_list.append(bookmarks_data)

        return bookmark_list

    def get_article_title(self, bookmark):
        # Free와 Live 모델에 따라 다른 필드를 반환
        content_object = bookmark.content_object
        if content_object:
            if bookmark.content_type.model == "free":
                return content_object.title
            elif bookmark.content_type.model == "live":
                return content_object.review
        return None

    def get_article_type(self, bookmark):
        # 게시물의 타입 반환 (Free 또는 Live)
        if bookmark.content_type.model == "free":
            return "Free"
        elif bookmark.content_type.model == "live":
            return "Live"

    class Meta:
        model = User
        fields = ["username", "profile_image", "nickname", "bookmark"]
