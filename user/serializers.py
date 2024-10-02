from .models import User
from rest_framework import serializers
from community.models import Comment, Bookmark

# TODO 모두 구현 간소화진행할게요! 코멘트도 하나의 시리얼라이져만들어서 사용하는거 고민!!


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)
        super().__init__(*args, **kwargs)
        # 파라쿼리미터로(뷰에서 불러올 필드) 제어
        if fields is not None:
            allowed = set(fields)  # 요청된
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


# TODO 직관 이미지 추가해보고 실험 images.append(live_image.live_image)
class UserProfileSerializer(DynamicFieldsModelSerializer):
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    article_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    bookmark_count = serializers.SerializerMethodField()
    community_free_title = serializers.SerializerMethodField()
    community_live_image = serializers.SerializerMethodField()

    def get_bookmark_count(self, obj):
        return Bookmark.objects.filter(user=obj).count()

    def get_comment_count(self, obj):
        return Comment.objects.filter(author=obj).count()

    def get_article_count(self, obj):
        free_article = obj.author_free.count()
        live_article = obj.author_live.count()
        return free_article + live_article

    def get_following_count(self, obj):
        return obj.followings.count()

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_community_free_title(self, obj):
        user_free_article = obj.author_free.all()
        title = []

        for free in user_free_article:
            if free.title:
                title.append(free.title)
        return title

    def get_community_live_image(self, obj):
        user_live_image = obj.author_live.all()
        images = []

        for live_image in user_live_image:
            if live_image.live_image:
                images.append(live_image.live_image)
        return images

    class Meta:
        model = User
        fields = [
            "email",
            "phone_number",
            "profile_image",
            "nickname",
            "bio",
            "created_at",
            "following_count",
            "followers_count",
            "article_count",
            "comment_count",
            "bookmark_count",
            "community_free_title",
            "community_live_image",
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "nickname",
            "name",
        ]


# class FollowingListSerializer(serializers.ModelSerializer):
#     following_count = serializers.SerializerMethodField()
#     follower_count = serializers.SerializerMethodField()
#     following_list = serializers.SerializerMethodField()

#     def get_following_list(self, obj):
#         following = obj.followings.all()
#         nicknames = []

#         for following_users in following:
#             nicknames.append(following_users.nickname)
#         return nicknames

#     def get_following_count(self, obj):
#         return obj.followings.count()

#     def get_follower_count(self, obj):
#         return obj.followers.count()

#     class Meta:
#         model = User
#         fields = [
#             "nickname",
#             "profile_image",
#             "nickname",
#             "bio",
#             "created_at",
#             "following_count",
#             "follower_count",
#             "following_list",
#         ]


# class FollowerslistSerializer(serializers.ModelSerializer):
#     following_count = serializers.SerializerMethodField()
#     followers_count = serializers.SerializerMethodField()
#     followers_list = serializers.SerializerMethodField()

#     def get_followers_list(self, obj):
#         followers = obj.followers.all()
#         nicknames = []

#         for follower in followers:
#             nicknames.append(follower.nickname)
#         return nicknames

#     def get_following_count(self, obj):
#         return obj.followings.count()

#     def get_followers_count(self, obj):
#         return obj.followers.count()

#     class Meta:
#         model = User
#         fields = [
#             "profile_image",
#             "nickname",
#             "bio",
#             "created_at",
#             "following_count",
#             "followers_count",
#             "followers_list",
#         ]


# # TODO 뉴스 댓글 추가해야해요.
# class CommentsListSerializer(serializers.ModelSerializer):
#     comments = serializers.SerializerMethodField()

#     def get_comments(self, obj):
#         comments = Comment.objects.filter(author=obj)
#         comments_list = []

#         for comment in comments:
#             comments_data = {
#                 "content": comment.content,
#                 "article_type": self.get_article_type(comment),
#                 "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M:"),
#                 "updated_at": comment.updated_at.strftime(
#                     "%Y-%m-%d %H:%M:"
#                 ),  # strftime 데이트타입 포맷터(출력date지정)
#             }
#             comments_list.append(comments_data)

#         return comments_list

#     def get_article_type(self, comment):

#         # 댓글이 작성된 게시물이 Free인지 Live인지 반환
#         if comment.content_type.model == "free":
#             return "Free"
#         elif comment.content_type.model == "live":
#             return "Live"

#     class Meta:
#         model = User
#         fields = ["profile_image", "nickname", "comments"]


# class BookMarkListSerializer(serializers.ModelSerializer):
#     bookmark = serializers.SerializerMethodField()

#     def get_bookmark(self, obj):
#         bookmarks = Bookmark.objects.filter(user=obj)
#         bookmark_list = []

#         for bookmark in bookmarks:
#             bookmarks_data = {
#                 "article_type": self.get_article_type(bookmark),
#                 "title": self.get_article_title(bookmark),
#                 "created_at": bookmark.created_at.strftime("%Y-%m-%d %H:%M:"),
#                 "updated_at": bookmark.updated_at.strftime(
#                     "%Y-%m-%d %H:%M:"
#                 ),  # strftime 데이트타입 포맷터(출력date지정)
#             }
#             bookmark_list.append(bookmarks_data)

#         return bookmark_list

#     def get_article_title(self, bookmark):
#         # 기사 제목 가져오기
#         if bookmark.content_object:  # content_object가 존재하는지 확인
#             return bookmark.content_object.title  # 제목 반환
#         else:
#             return None  # 존재하지 않으면 None 반환

#     def get_article_type(self, bookmark):

#         # 댓글이 작성된 게시물이 Free인지 Live인지 반환
#         if bookmark.content_type.model == "free":
#             return "Free"
#         elif bookmark.content_type.model == "live":
#             return "Live"

#     class Meta:
#         model = User
#         fields = ["profile_image", "nickname", "bookmark"]
