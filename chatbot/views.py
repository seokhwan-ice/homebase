import openai
from homebase import config
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Conversation
from .serializers import ConversationSerializer
from data.models import Players, PlayerRecord, GameRecord, TeamRank


def get_openai_response(user_input):
    openai.api_key = config.OPENAI_API_KEY

    # OpenAI Chat API를 사용하여 응답 생성
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input},
        ],
        max_tokens=150,
        temperature=0.7,
        n=1,
    )

    return response.choices[0].message['content'].strip()


class ChatbotAPIView(APIView):

    def post(self, request, *args, **kwargs):
        user_input = request.data.get("user_input")
        if user_input:
            # 경기 일정 요청 처리
            if "경기 일정" in user_input:
                return self.get_game_schedule(user_input)
            # 선수 통계 요청 처리
            elif "선수 통계" in user_input:
                return self.get_player_stats(user_input)
            # 팀 순위 요청 처리
            elif "팀 순위" in user_input:
                return self.get_team_rank(user_input)
            # 그 외에는 OpenAI 응답
            else:
                ai_response = get_openai_response(user_input)
                conversation = Conversation.objects.create(
                    user_input=user_input, ai_response=ai_response
                )
                serializer = ConversationSerializer(conversation)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            {"error": "user_input is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    def get_game_schedule(self, user_input):
        team_name = self.extract_team_name(user_input)
        if team_name:
            game_schedules = GameRecord.objects.filter(team_1=team_name).values(
                "date", "team_2"
            )
            if game_schedules.exists():
                return Response(game_schedules, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "No games found for the given team."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(
            {"error": "team_name not found in input"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def get_player_stats(self, user_input):
        player_name = self.extract_player_name(user_input)
        if player_name:
            player_stats = PlayerRecord.objects.filter(player__name=player_name).values(
                "game__date", "game__opponent", "goals", "assists", "points"
            )
            if player_stats.exists():
                return Response(player_stats, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "No stats found for the given player."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(
            {"error": "player_name not found in input"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def get_team_rank(self, user_input):
        team_name = self.extract_team_name(user_input)
        if team_name:
            team_rank = TeamRank.objects.filter(team_name=team_name).values(
                "rank", "points", "goal_difference"
            )
            if team_rank.exists():
                return Response(team_rank, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "No rank found for the given team."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(
            {"error": "team_name not found in input"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def extract_team_name(self, user_input):
        # 팀 이름 목록
        team_names = ["한화", "삼성", "두산", "LG", "롯데", "기아", "SSG", "NC", "키움", "KT"]
        
        # 사용자 입력에서 팀 이름이 포함되어 있는지 확인
        for team_name in team_names:
            if team_name in user_input:
                return team_name
        return None

    def extract_player_name(self, user_input):
        # 선수 이름 목록
        player_names = Players.objects.values_list('name', flat=True)
        
        # 사용자 입력에서 선수 이름이 포함되어 있는지 확인
        for player_name in player_names:
            if player_name in user_input:
                return player_name
        return None
