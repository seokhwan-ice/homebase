import random
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import transaction
from community.models import Free, Live, Comment, Like
from chat.models import ChatRoom, ChatParticipant

User = get_user_model()


class Command(BaseCommand):

    @transaction.atomic
    def handle(self, *args, **kwargs):

        # 유저 10
        users = []
        for i in range(10):
            user = User.objects.create_user(
                username=f"username{i}",
                password="password123",
                nickname=f"Kinggoddino{i}",
                name=f"User{i}",
            )
            users.append(user)
            self.stdout.write(self.style.SUCCESS(f"User {user.username} created!"))

        # free 10 + 댓글 30
        free_posts = []
        for i in range(10):
            free_post = Free.objects.create(
                title=f"Sample Free Title {i}",
                content=f"This is a sample free {i}.",
                author=random.choice(users),
                views=random.randint(0, 50),
            )
            free_posts.append(free_post)
            self.stdout.write(self.style.SUCCESS(f"Free {free_post.title} created!"))

        for i in range(30):
            free_post = random.choice(free_posts)
            comment = Comment.objects.create(
                author=random.choice(users),
                content=f"This is a comment {i} on Free {free_post.id}.",
                content_type=ContentType.objects.get_for_model(free_post),
                object_id=free_post.id,
            )
            free_post.update_comments_count()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Comment {comment.id} created on Free {free_post.id}!"
                )
            )

        # live 10 + 댓글 30
        live_posts = []
        for i in range(10):
            live_post = Live.objects.create(
                review=f"Sample review for live community {i}.",
                game_date=timezone.now(),
                home_team=random.choice([team[0] for team in Live.TEAM_CHOICES]),
                away_team=random.choice([team[0] for team in Live.TEAM_CHOICES]),
                stadium=random.choice([stadium[0] for stadium in Live.STADIUM_CHOICES]),
                author=random.choice(users),
                likes_count=random.randint(0, 50),
            )
            live_posts.append(live_post)
            self.stdout.write(self.style.SUCCESS(f"Live {live_post.id} created!"))

        for i in range(30):
            live_post = random.choice(live_posts)
            comment = Comment.objects.create(
                author=random.choice(users),
                content=f"This is a comment {i} on Live {live_post.id}.",
                content_type=ContentType.objects.get_for_model(live_post),
                object_id=live_post.id,
            )
            live_post.update_comments_count()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Comment {comment.id} created on Live {live_post.id}!"
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
            participants_count = random.randint(0, 20)
            participants = random.sample(users, k=min(participants_count, len(users)))
            for participant in participants:
                ChatParticipant.objects.create(user=participant, room=chat_room)
            self.stdout.write(
                self.style.SUCCESS(
                    f"{participants_count} participants joined in {chat_room.title}!"
                )
            )

        self.stdout.write(self.style.SUCCESS("Database seeding completed!"))

        print("\n\n" + "-" * 50)
        print(
            self.style.SUCCESS(
                "이제 테스트 할 때마다 샘플 노가다 안해도 된다. test code 만들줄 알았으면 이런일도 없었겠지"
            )
        )
