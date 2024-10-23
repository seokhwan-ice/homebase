import openai
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from data.models import Players, PlayerRecord, GameRecord
from homebase import config
from .models import Conversation
from .serializers import ConversationSerializer

TEAM_NAME_VARIATIONS = {
    "KIA": ["KIA", "kia", "기아", "기아타이거즈"],
    "롯데": ["롯데", "롯데자이언츠", "lotte"],
    "키움": ["키움", "키움히어로즈", "kiwoom"],
    "두산": ["두산", "두산베어스", "doosan"],
    "LG": ["LG", "lg", "엘지", "엘지트윈스", "LG트윈스"],
    "한화": ["한화", "한화이글스", "hanwha"],
    "NC": ["NC", "nc", "엔씨", "엔시", "nc다이노스"],
    "삼성": ["삼성", "삼성라이온즈", "samsung"],
    "KT": ["KT", "kt", "kt wiz", "케이티", "케티"],
    "SSG": ["SSG", "ssg", "ssg랜더스", "SSG랜더스"],
}
openai.api_key = config.OPENAI_API_KEY


def get_openai_response(user_input, additional_info=None):
    additional_info_text = ""
    if additional_info:
        additional_info_text = f"\n\n추가 정보:\n{additional_info}"

    messages = [
        {
            "role": "system",
            "content": (
                #"응답은 오직 데이터베이스에서 가져온 정보만 사용해야 합니다. "
                "당신은 한국 야구 전문가 챗봇입니다."
                "데이터베이스의 데이터만 답변합니다."
                "선수 프로필, 선수 정보는 db에 data_players에 저장되어 있습니다.db를 사용해서 응답하세요"
                "선수 상대 전적은 data_playerrecord에 저장되어 있습니다. db를 사용해서 응답하세요"
                "팀 상대 전적은 data_teamrecord에 저장되어있습니다. 이 db를 사용해서 응답하세요"
                "실시간 데이터는 데이터베이스에 저장된 데이터입니다."
                "AI는 자체적으로 정보를 찾거나 추론해서는 안 됩니다."
            ),
        },
        {"role": "user", "content": user_input + additional_info_text},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.0,  # 확률적 대답을 줄이기 위해 temperature를 낮춤
    )

    return response.choices[0]["message"]["content"]


class ChatbotAPIView(APIView):

    def post(self, request, *args, **kwargs):
        user_input = request.data.get("user_input")
        if user_input:
            if "경기 일정" in user_input:
                return self.get_game_schedule(user_input)
            elif "상대 전적" in user_input:
                return self.get_rival_stats(user_input)
            elif "전체 순위" in user_input or "순위" in user_input:
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

    def extract_player_name(self, user_input):
        # 데이터베이스에서 모든 선수 이름을 가져옴
        player_names = Players.objects.values_list("name", flat=True)

        # 입력된 user_input에서 선수 이름을 찾아 반환
        for name in player_names:
            # 괄호가 포함된 이름에서 괄호 이전 부분만 추출
            korean_name = name.split(" (")[0]
            if korean_name in user_input:
                return korean_name
        return None

    def get_game_schedule(self, user_input):
        team_name = self.extract_team_name(user_input)
        if team_name:
            game_schedules = GameRecord.objects.filter(
                Q(team_1=team_name) | Q(team_2=team_name), year=2024
            ).values("date", "team_1", "team_2")

            if game_schedules.exists():
                data = list(game_schedules)
                # AI 응답 생성 없이 데이터베이스 결과만 반환
                return Response(
                    {"data": data},
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
            player1_stats = PlayerRecord.objects.filter(
                player__name=players[0], year=2024
            )
            player2_stats = PlayerRecord.objects.filter(
                player__name=players[1], year=2024
            )

            if player1_stats.exists() and player2_stats.exists():
                stats = self.calculate_rival_stats(player1_stats, player2_stats)
                # AI 응답 생성 없이 데이터베이스 결과만 반환
                return Response(
                    {"data": stats},
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

    def get_player_profile(self, user_input):
        # 사용자 입력에서 선수 이름 추출
        player_name = self.extract_player_name(user_input)

        if player_name:
            # 선수 이름으로 프로필 정보 조회
            player_profile = Players.objects.filter(name__icontains=player_name).values(
                "year",
                "player_number",
                "name",
                "team_name",
                "position",
                "batter_hand",
                "birth_date",
                "school",
                "draft_info",
                "active_years",
                "active_team",
                "profile_img",
            )

            if player_profile.exists():
                profile_data = list(player)
                # AI 응답 생성 없이 데이터베이스 결과만 반환
                return Response(
                    {"data": profile_data},
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
        for team_name, variations in TEAM_NAME_VARIATIONS.items():
            for variation in variations:
                if variation in user_input:
                    return team_name
        return None

    def extract_players_from_input(self, user_input):
        player_names = Players.objects.values_list("name", flat=True)
        players = []

        # 사용자 입력에서 선수 이름을 검색
        for name in player_names:
            # 괄호가 포함된 이름에서 괄호 이전 부분만 추출
            korean_name = name.split(" (")[0]  # 괄호 이전 부분을 가져옴
            if korean_name in user_input:
                players.append(korean_name)

        return players if len(players) == 2 else None

    def calculate_rival_stats(self, player1_stats, player2_stats):
        player1_games = player1_stats.filter(year=2024).values(
            "opponent", "goals", "assists", "points"
        )
        player2_games = player2_stats.filter(year=2024).values(
            "opponent", "goals", "assists", "points"
        )

        stats = {
            "player1": player1_stats.first().name,
            "player2": player2_stats.first().name,
            "player1_games": player1_games,
            "player2_games": player2_games,
        }
        return stats
