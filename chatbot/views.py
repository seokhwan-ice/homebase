import openai
from homebase import config
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Conversation
from .serializers import ConversationSerializer
from data.models import Players, PlayerRecord, GameRecord, TeamRank


def get_openai_response(
    user_input, data_players=None, data_gamerecord=None, data_teamrank=None
):
    """
    OpenAI API를 사용해 GPT 모델로 응답 생성 (데이터베이스에서 가져온 정보 포함)
    """
    openai.api_key = config.OPENAI_API_KEY

    # 데이터베이스에서 가져온 정보가 있으면, 이를 프롬프트에 추가
    player_info = (
        f"선수 이름: {data_players['name']}, 나이: {data_players['birth_date']}, 포지션: {data_players['position']}, 팀: {data_players['team']}, 지명순위: {data_players['draft_info']}, 활동팀: {data_players['active_team']},"
        if data_players
        else None
    )
    schedule_info = (
        f"팀: {data_gamerecord['team_1']} vs {data_gamerecord['team_2']}, 날짜: {data_gamerecord['date']}"
        if data_gamerecord
        else None
    )
    team_rank = (
        f"팀 이름: {data_teamrank['team_name']}, 순위: {data_teamrank['rank']}, 승: {data_teamrank['wins']}, 무: {data_teamrank['draws']}, 패: {data_teamrank['losses']}"
        if data_teamrank
        else None
    )

    # 시스템 메시지와 유저 입력을 포함한 프롬프트 생성
    messages = [
        {
            "role": "system",
            "content": "당신은 한국 야구 전문가 챗봇입니다. 선수들의 통계와 경기 일정에 대한 정보를 200자 이내로 정확하게 답변하세요.",
        },
        {"role": "user", "content": user_input},
    ]

    if player_info:
        messages.append({"role": "user", "content": f"선수 프로필: {player_info}"})

    if schedule_info:
        messages.append({"role": "user", "content": f"경기 일정: {schedule_info}"})

    if team_rank:
        messages.append({"role": "user", "content": f"팀 순위: {team_rank}"})

    response = openai.ChatCompletion.create(
        model="gpt-4", messages=messages, max_tokens=200, temperature=0.4
    )

    return response.choices[0].message["content"]


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
                return Response(
                    {"ai_response": ai_response, "data": data},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "요청하신 경기를 찾을 수 없습니다."},
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
                return Response(
                    {"ai_response": ai_response, "data": stats},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "선수 이름을 찾을 수 없습니다."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(
            {"error": "선수 이름이 입력되지 않았습니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def get_team_rank(self, user_input):
        team_name = self.extract_team_name(user_input)

        if team_name:
            team_rank = TeamRank.objects.filter(team_name=team_name).values(
                "team_name",
                "rank",
                "wins",
                "draws",
                "losses",
            ).first()

            if team_rank:
                # 데이터베이스에서 조회한 팀 순위 정보를 OpenAI에 전송
                ai_response = get_openai_response(user_input, data_teamrank=team_rank)
                return Response(
                    {"ai_response": ai_response, "data": team_rank},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": f"{team_name} 의 순위 정보를 찾을 수 없습니다."},
                    status=status.HTTP_404_NOT_FOUND,
                )

    def get_player_profile(self, user_input):
        player_name = self.extract_player_name(user_input)

        if player_name:
            player_profile = Players.objects.filter(name=player_name).values(
                "name",
                "birth_date",
                "position",
                "team",
                "active_team",
                "draft_info",
                "profile_img",
            )

            if player_profile.exists():
                profile_data = list(player_profile)
                # 선수 프로필 데이터를 OpenAI에 전달
                ai_response = get_openai_response(user_input, profile_data)
                return Response(
                    {"ai_response": ai_response, "data": profile_data},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "message": f"{player_name} 선수의 프로필 정보를 찾을 수 없습니다."
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

        return Response(
            {"error": "선수 이름이 입력되지 않았습니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def extract_team_name(self, user_input):
        """
        사용자의 입력에서 팀 이름을 추출하는 메소드
        """
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
        player1_games = player1_stats.values(
            "game__opponent", "goals", "assists", "points"
        )
        player2_games = player2_stats.values(
            "game__opponent", "goals", "assists", "points"
        )

        stats = {
            "player1": player1_stats.first().player.name,
            "player2": player2_stats.first().player.name,
            "player1_games": player1_games,
            "player2_games": player2_games,
        }
        return stats
