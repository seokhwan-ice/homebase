import openai
from homebase import config
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Conversation
from .serializers import ConversationSerializer
from data.models import Players, PlayerRecord, GameRecord, TeamRank


def get_openai_response(user_input, data=None):
    openai.api_key = config.OPENAI_API_KEY

    # 데이터가 있으면 OpenAI에 추가 정보로 전달
    messages = [
        {"role": "system", "content": "You are a baseball expert chatbot. You have access to detailed information about Korean baseball players, their stats, and game schedules. Answer all questions in a concise and accurate manner, especially when it involves player stats or match data.",},
        {"role": "user", "content": user_input},
    ]
    
    if data:
        messages.append({"role": "system", "content": f"Here is additional data: {data}"})

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=150,
        temperature=0.7,
        n=1,
    )

    return response.choices[0].message["content"].strip()


class ChatbotAPIView(APIView):

    def post(self, request, *args, **kwargs):
        user_input = request.data.get("user_input")
        if user_input:
            if "경기 일정" in user_input:
                return self.get_game_schedule(user_input)
            elif "상대 전적" in user_input:
                return self.get_rival_stats(user_input)
            elif "팀 순위" in user_input:
                return self.get_team_rank(user_input)
            elif "선수 프로필" in user_input:
                return self.get_player_profile(user_input)
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
            game_schedules = GameRecord.objects.filter(
                Q(team_1=team_name) | Q(team_2=team_name)
            ).values("date", "team_1", "team_2")

            if game_schedules.exists():
                data = list(game_schedules)
                # 데이터베이스에서 조회한 경기 일정 정보를 OpenAI에 전달
                ai_response = get_openai_response(user_input, data)
                return Response({"ai_response": ai_response, "data": data}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "No games found for the given team."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(
            {"error": "team_name not found in input"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def get_rival_stats(self, user_input):
        players = self.extract_players_from_input(user_input)
        if players and len(players) == 2:
            player1_stats = PlayerRecord.objects.filter(player__name=players[0])
            player2_stats = PlayerRecord.objects.filter(player__name=players[1])

            if player1_stats.exists() and player2_stats.exists():
                stats = self.calculate_rival_stats(player1_stats, player2_stats)
                # OpenAI에 상대 전적 데이터를 전달
                ai_response = get_openai_response(user_input, stats)
                return Response({"ai_response": ai_response, "data": stats}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "선수 이름을 찾을 수 없습니다."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(
            {"error": "선수 이름이 입력되지 않았습니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def get_player_profile(self, user_input):
        player_name = self.extract_player_name(user_input)

        if player_name:
            player_profile = Players.objects.filter(name=player_name).values(
                "name", "age", "position", "team", "career_stats"
            )

            if player_profile.exists():
                profile_data = list(player_profile)
                # 선수 프로필 데이터를 OpenAI에 전달
                ai_response = get_openai_response(user_input, profile_data)
                return Response({"ai_response": ai_response, "data": profile_data}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": f"{player_name} 선수의 프로필 정보를 찾을 수 없습니다."},
                    status=status.HTTP_404_NOT_FOUND,
                )

        return Response(
            {"error": "선수 이름이 입력되지 않았습니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def extract_team_name(self, user_input):
        team_names = TeamRank.objects.values_list("team_name", flat=True)
        for team_name in team_names:
            if team_name in user_input:
                return team_name
        return None

    def extract_players_from_input(self, user_input):
        player_names = Players.objects.values_list("name", flat=True)
        players = [name for name in player_names if name in user_input]
        return players if len(players) == 2 else None

    def calculate_rival_stats(self, player1_stats, player2_stats):
        player1_games = player1_stats.values("game__opponent", "goals", "assists", "points")
        player2_games = player2_stats.values("game__opponent", "goals", "assists", "points")

        stats = {
            "player1": player1_stats.first().player.name,
            "player2": player2_stats.first().player.name,
            "player1_games": player1_games,
            "player2_games": player2_games,
        }
        return stats

