import random
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import transaction
from community.models import Free, Live, Comment
from chat.models import ChatRoom, ChatParticipant

User = get_user_model()


class Command(BaseCommand):

    @transaction.atomic
    def handle(self, *args, **kwargs):

        # 유저네임 리스트
        usernames = [
            "Spino",
            "Allo",
            "Tyranno",
            "Brachio",
            "Elasmo",
            "Mosa",
            "Raptor",
            "Ankylo",
            "Stego",
            "Trice",
        ]

        # 유저 10
        users = []
        for i, username in enumerate(usernames):
            user = User.objects.create_user(
                username=username,
                password="password123",
                nickname=f"{username}_nickname",
                name=f"User{i}",
            )
            users.append(user)
            self.stdout.write(self.style.SUCCESS(f"User {user.username} created!"))

        # 팔로우
        for user in users:
            others = [u for u in users if u != user]
            following_count = random.randint(0, 5)
            following_users = random.sample(others, following_count)
            for follow in following_users:
                user.followings.add(follow)
            self.stdout.write(
                self.style.SUCCESS(f"{user.username} followed {following_count} users!")
            )

        # free 10 + 댓글 30
        free_articles = []
        for i in range(10):
            free_article = Free.objects.create(
                title=f"Sample Free Title {i}",
                content=f"This is a sample free {i}.",
                author=random.choice(users),
                views=random.randint(0, 50),
            )
            free_articles.append(free_article)
            self.stdout.write(self.style.SUCCESS(f"Free {free_article.title} created!"))

        for i in range(30):
            free_article = random.choice(free_articles)
            comment = Comment.objects.create(
                author=random.choice(users),
                content=f"This is a comment {i} on Free {free_article.id}.",
                content_type=ContentType.objects.get_for_model(free_article),
                object_id=free_article.id,
            )
            free_article.update_comments_count()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Comment {comment.id} created on Free {free_article.id}!"
                )
            )

        # live 10 + 댓글 30
        live_articles = []
        for i in range(10):
            live_article = Live.objects.create(
                review=f"Sample review for live community {i}.",
                game_date=timezone.now(),
                home_team=random.choice([team[0] for team in Live.TEAM_CHOICES]),
                away_team=random.choice([team[0] for team in Live.TEAM_CHOICES]),
                stadium=random.choice([stadium[0] for stadium in Live.STADIUM_CHOICES]),
                author=random.choice(users),
                likes_count=random.randint(0, 50),
            )
            live_articles.append(live_article)
            self.stdout.write(self.style.SUCCESS(f"Live {live_article.id} created!"))

        for i in range(30):
            live_article = random.choice(live_articles)
            comment = Comment.objects.create(
                author=random.choice(users),
                content=f"This is a comment {i} on Live {live_article.id}.",
                content_type=ContentType.objects.get_for_model(live_article),
                object_id=live_article.id,
            )
            live_article.update_comments_count()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Comment {comment.id} created on Live {live_article.id}!"
                )
            )

        # 채팅방 10
        chat_rooms = []
        for i in range(10):
            chat_room = ChatRoom.objects.create(
                title=f"Chat Room {i}",
                description=f"This is the description for ChatRoom {i}.",
                creator=random.choice(users),
            )
            chat_rooms.append(chat_room)
            self.stdout.write(
                self.style.SUCCESS(f"ChatRoom {chat_room.title} created!")
            )

            # 채팅방 참여자 수 0~20
            participants_count = random.randint(0, 10)
            participants = random.sample(users, k=min(participants_count, len(users)))
            for participant in participants:
                ChatParticipant.objects.create(user=participant, room=chat_room)
            self.stdout.write(
                self.style.SUCCESS(
                    f"{participants_count} participants joined in {chat_room.title}!"
                )
            )

        self.stdout.write(self.style.SUCCESS("Database seeding completed!!!!!"))

        print("\n\n" + "-" * 50)
        print(self.style.SUCCESS("또 추가하고 싶은 샘플 있우면 말해주세요"))
