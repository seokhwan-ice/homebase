import openai
from homebase import config
from rest_framework.response import Response
from rest_framework.decorators import api_view
from data.models import Players, PlayerRecord, TeamRank, GameRecord
import datetime

# OpenAI API 키 설정
openai.api_key = config.OPENAI_API_KEY

# @api_view(['POST'])
# def get_info(request):
#     user_input = request.data.get('user_input')

#     if not user_input:
#         return Response({'response': '질문을 입력해주세요.'}, status=400)

#     # 팀 이름 목록을 데이터베이스에서 동적으로 가져옴
#     team_names = TeamRank.objects.values_list('team_name', flat=True)

#     # "상대전적" 또는 "상대팀" 관련 질문 처리
#     if "상대전적" in user_input or "상대팀" in user_input:
#         player_names = user_input.replace("상대전적", "").replace("상대팀", "").strip().split() 
#         '''
#         질문 예시)
#         문동주 김도영 상대전적
#         '''


#         if len(player_names) < 2:
#             return Response({'response': '선수 이름과 상대팀을 모두 입력해주세요.'}, status=400)

#         player_name = player_names[0]
#         opponent_name = player_names[1]

#         # 해당 선수와 상대팀에 대한 기록을 필터링
#         player_record = PlayerRecord.objects.filter(name__icontains=player_name, opponent__icontains=opponent_name).first()

#         if player_record:
#             player_rival_info = (
#                 f"선수: {player_record.name}, 상대팀: {player_record.opponent}, "
#                 f"타석: {player_record.pa}, 타수: {player_record.ab}, "
#                 f"안타: {player_record.h}, 홈런: {player_record.hr}, "
#                 f"타점: {player_record.rbi}, 타율: {player_record.avg}, OPS: {player_record.ops}"
#             )
#             return Response({'response': player_rival_info})
#         else:
#             return Response({'response': f"{player_name} 선수와 {opponent_name} 선수와의 경기 정보가 없습니다."})

#     # "팀 정보" 조회를 위한 분기, 팀 이름이 데이터베이스에 있는지 확인
#     elif "팀" in user_input or any(team in user_input for team in team_names):
#         team_name = user_input.strip()  # 공백 제거
#         '''
#         질문 예시)
#         한화, 삼성
#         '''

#         teams = TeamRank.objects.filter(team_name__icontains=team_name)

#         if teams.exists():
#             team = teams.first()
#             team_info = (
#                 f"팀: {team.team_name}, 순위: {team.rank}, "
#                 f"경기 수: {team.games_played}, 승리: {team.wins}, "
#                 f"패배: {team.losses}, 무승부: {team.draws}, "
#                 f"승률: {team.win_rate}, 게임차: {team.games_behind}, "
#                 f"연속: {team.streak}, 최근 10경기: {team.last_10_games}"
#             )
#             return Response({'response': team_info})
#         else:
#             return Response({'response': "해당 팀에 대한 정보를 찾을 수 없습니다."})

#     # 선수 프로필 조회
#     else:
#         player = Players.objects.filter(name__icontains=user_input).first()
#         '''
#         질문 예시)
#         문동주
#         '''

#         if player:
#             player_info = (
#                 f"이름: {player.name}, 팀: {player.team}, 포지션: {player.position}, "
#                 f"타석: {player.batter_hand}, 나이: {player.birth_date}, "
#                 f"학교: {player.school}, 드래프트 정보: {player.draft_info}, "
#                 f"활동 팀: {player.active_team}, 프로필 이미지: {player.profile_img}"
#             )
#             return Response({'response': player_info})
#         else:
#             return Response({'response': "해당 선수에 대한 정보를 찾을 수 없습니다."})


@api_view(['POST'])
def get_info(request):
    user_input = request.data.get('user_input')

    if not user_input:
        return Response({'response': '질문을 입력해주세요.'}, status=400)

    try:
        # OpenAI ChatCompletion 호출하여 질문 처리
        openai_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful baseball chatbot."},
                {"role": "user", "content": user_input}
            ]
        )

        # OpenAI 응답에서 처리된 메시지를 가져옵니다.
        chatbot_reply = openai_response['choices'][0]['message']['content']

        # 경기 일정 관련 질문 처리
        if "경기 일정" in user_input or "경기" in user_input:
            # 질문에서 날짜나 팀 이름을 추출하여 필터링
            # "한화 경기 일정", "10월 15일 경기" 등의 질문을 처리
            if "팀" in user_input:
                team_name = user_input.replace("경기 일정", "").strip()
                games = GameRecord.objects.filter(
                    team_1__icontains=team_name
                ) | GameRecord.objects.filter(team_2__icontains=team_name)

                if games.exists():
                    game_info_list = []
                    for game in games:
                        game_info = (
                            f"날짜: {game.date}, {game.team_1} vs {game.team_2}, "
                            f"링크: {game.url}"
                        )
                        game_info_list.append(game_info)
                    return Response({'response': "\n".join(game_info_list)})
                else:
                    return Response({'response': "해당 팀에 대한 경기 일정을 찾을 수 없습니다."})

            elif "일정" in user_input:
                date_str = user_input.replace("경기 일정", "").strip()
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    games = GameRecord.objects.filter(date=date)

                    if games.exists():
                        game_info_list = []
                        for game in games:
                            game_info = (
                                f"날짜: {game.date}, {game.team_1} vs {game.team_2}, "
                                f"링크: {game.url}"
                            )
                            game_info_list.append(game_info)
                        return Response({'response': "\n".join(game_info_list)})
                    else:
                        return Response({'response': "해당 날짜에 대한 경기 일정이 없습니다."})
                except ValueError:
                    return Response({'response': '올바른 날짜 형식을 입력해주세요. (예: 2024-10-15)'}, status=400)

        # 기존 상대전적, 팀 정보, 선수 정보 조회 로직 유지
        if "상대전적" in user_input or "상대팀" in user_input:
            player_names = user_input.replace("상대전적", "").replace("상대팀", "").strip().split()

            if len(player_names) < 2:
                return Response({'response': '선수 이름과 상대팀을 모두 입력해주세요.'}, status=400)

            player_name = player_names[0]
            opponent_name = player_names[1]

            player_record = PlayerRecord.objects.filter(name__icontains=player_name, opponent__icontains=opponent_name).first()

            if player_record:
                player_rival_info = (
                    f"선수: {player_record.name}, 상대팀: {player_record.opponent}, "
                    f"타석: {player_record.pa}, 타수: {player_record.ab}, "
                    f"안타: {player_record.h}, 홈런: {player_record.hr}, "
                    f"타점: {player_record.rbi}, 타율: {player_record.avg}, OPS: {player_record.ops}"
                )
                return Response({'response': player_rival_info})
            else:
                return Response({'response': f"{player_name} 선수와 {opponent_name} 선수와의 경기 정보가 없습니다."})

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
                return Response({'response': team_info})
            else:
                return Response({'response': "해당 팀에 대한 정보를 찾을 수 없습니다."})

        elif "선수" in user_input or "선수 정보" in user_input:
            player = Players.objects.filter(name__icontains=user_input).first()

            if player:
                player_info = (
                    f"이름: {player.name}, 팀: {player.team}, 포지션: {player.position}, "
                    f"타석: {player.batter_hand}, 나이: {player.birth_date}, "
                    f"학교: {player.school}, 드래프트 정보: {player.draft_info}, "
                    f"활동 팀: {player.active_team}, 프로필 이미지: {player.profile_img}"
                )
                return Response({'response': player_info})
            else:
                return Response({'response': "해당 선수에 대한 정보를 찾을 수 없습니다."})

        return Response({'response': chatbot_reply})

    except Exception as e:
        return Response({'response': 'OpenAI API 호출에 실패했습니다.', 'error': str(e)}, status=500)
