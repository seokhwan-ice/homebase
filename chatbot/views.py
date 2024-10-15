import openai
from homebase import config
from rest_framework.response import Response
from rest_framework.decorators import api_view
from data.models import Players, PlayerRecord, TeamRank, GameRecord
import datetime
from django.utils.timezone import now
from django.db.models import Q

# OpenAI API 키 설정
openai.api_key = config.OPENAI_API_KEY


@api_view(["POST"])
def get_info(request):
    user_input = request.data.get("user_input")

    if not user_input:
        return Response({"response": "질문을 입력해주세요."}, status=400)

    try:
        # OpenAI ChatCompletion 호출하여 질문 처리
        openai_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "너는 친절하고 정확한 야구 챗봇이야. 우리 데이터베이스를 바탕으로 대답하고, 추가적인 내용은 검색을 통해 대답해줘.",
                },
                {"role": "user", "content": user_input},
            ],
        )

        # OpenAI 응답에서 처리된 메시지를 가져옵니다.
        chatbot_reply = openai_response["choices"][0]["message"]["content"]

        # 날짜 없이 경기 일정을 묻는 질문 처리
        if "경기 일정" in user_input:
            # 사용자가 날짜를 제공하지 않았다면 오늘 날짜로 기본값 설정
            today = now().date()  # 현재 날짜
            team_name = user_input.replace("경기 일정", "").strip()  # 팀 이름만 추출

            if not team_name:
                return Response({"response": "팀 이름을 입력해주세요."}, status=400)

            # 해당 팀의 최근 경기 일정 조회 (오늘 날짜 또는 가장 최근 경기)
            recent_game = (
                GameRecord.objects.filter(
                    (Q(team_1__icontains=team_name) | Q(team_2__icontains=team_name))
                    & Q(date__lte=today)
                )
                .order_by("-date")
                .first()
            )

            if recent_game:
                game_info = (
                    f"팀: {recent_game.team_1} vs {recent_game.team_2}, "
                    f"날짜: {recent_game.date}, "
                    # f"팀 1 점수: {recent_game.inning_scores_team_1}, "
                    # f"팀 2 점수: {recent_game.inning_scores_team_2}, "
                    f"링크: {recent_game.url}"
                )
                return Response({"response": game_info})
            else:
                return Response(
                    {"response": f"{team_name} 팀의 최근 경기 일정을 찾을 수 없습니다."}
                )

        # 기존 상대전적, 팀 정보, 선수 정보 조회 로직 유지
        if "상대전적" in user_input or "상대팀" in user_input:
            player_names = (
                user_input.replace("상대전적", "").replace("상대팀", "").strip().split()
            )

            if len(player_names) < 2:
                return Response(
                    {"response": "선수 이름과 상대팀을 모두 입력해주세요."}, status=400
                )

            player_name = player_names[0]
            opponent_name = player_names[1]

            player_record = PlayerRecord.objects.filter(
                name__icontains=player_name, opponent__icontains=opponent_name
            ).first()

            if player_record:
                player_rival_info = (
                    f"선수: {player_record.name}, 상대팀: {player_record.opponent}, "
                    f"타석: {player_record.pa}, 타수: {player_record.ab}, "
                    f"안타: {player_record.h}, 홈런: {player_record.hr}, "
                    f"타점: {player_record.rbi}, 타율: {player_record.avg}, OPS: {player_record.ops}"
                )
                return Response({"response": player_rival_info})
            else:
                return Response(
                    {
                        "response": f"{player_name} 선수와 {opponent_name} 선수와의 경기 정보가 없습니다."
                    }
                )

        elif "팀" in user_input or "팀 정보" in user_input:
            team_name = user_input.strip()
            teams = TeamRank.objects.filter(team_name__icontains=team_name)

            if teams.exists():
                team = teams.first()
                team_info = (
                    f"팀: {team.team_name}, 순위: {team.rank}, "
                    f"경기 수: {team.games_played}, 승리: {team.wins}, "
                    f"패배: {team.losses}, 무승부: {team.draws}, "
                    f"승률: {team.win_rate}, 게임차: {team.games_behind}, "
                    f"연속: {team.streak}, 최근 10경기: {team.last_10_games}"
                )
                return Response({"response": team_info})
            else:
                return Response({"response": "해당 팀에 대한 정보를 찾을 수 없습니다."})

        elif "선수" in user_input or "선수 정보" in user_input:
            player = Players.objects.filter(name__icontains=user_input).first()

            if player:
                player_info = (
                    f"이름: {player.name}, 팀: {player.team}, 포지션: {player.position}, "
                    f"타석: {player.batter_hand}, 나이: {player.birth_date}, "
                    f"학교: {player.school}, 드래프트 정보: {player.draft_info}, "
                    f"활동 팀: {player.active_team}, 프로필 이미지: {player.profile_img}"
                )
                return Response({"response": player_info})
            else:
                return Response(
                    {"response": "해당 선수에 대한 정보를 찾을 수 없습니다."}
                )

        return Response({"response": chatbot_reply})

    except Exception as e:
        return Response(
            {"response": "OpenAI API 호출에 실패했습니다.", "error": str(e)}, status=500
        )
