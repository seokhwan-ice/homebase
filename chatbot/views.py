# import openai
# from homebase.config import OPENAI_API_KEY
from rest_framework.response import Response
from rest_framework.decorators import api_view
from data.models import Players, PlayerRecord, TeamRank 

# OpenAI API 키 설정
# openai.api_key = OPENAI_API_KEY

@api_view(['POST'])
def get_info(request):
    user_input = request.data.get('user_input')

    if not user_input:
        return Response({'response': '질문을 입력해주세요.'}, status=400)

    # 팀 이름 목록을 데이터베이스에서 동적으로 가져옴
    team_names = TeamRank.objects.values_list('team_name', flat=True)

    # "상대전적" 또는 "상대팀" 관련 질문 처리
    if "상대전적" in user_input or "상대팀" in user_input:
        player_names = user_input.replace("상대전적", "").replace("상대팀", "").strip().split() 
        '''
        질문 예시)
        문동주 김도영 상대전적
        '''


        if len(player_names) < 2:
            return Response({'response': '선수 이름과 상대팀을 모두 입력해주세요.'}, status=400)

        player_name = player_names[0]
        opponent_name = player_names[1]

        # 해당 선수와 상대팀에 대한 기록을 필터링
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

    # "팀 정보" 조회를 위한 분기, 팀 이름이 데이터베이스에 있는지 확인
    elif "팀" in user_input or any(team in user_input for team in team_names):
        team_name = user_input.strip()  # 공백 제거
        '''
        질문 예시)
        한화, 삼성
        '''

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

    # 선수 프로필 조회
    else:
        player = Players.objects.filter(name__icontains=user_input).first()
        '''
        질문 예시)
        문동주
        '''

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


# @api_view(['POST'])
# def get_player_info(request):
#     # 요청에서 선수 이름 받기
#     name = request.data.get('player_name')

#     if not name:
#         return Response({'response': '선수 이름을 입력해주세요.'}, status=400)

#     # 데이터베이스에서 해당 선수 정보 검색 (get() 사용)
#     try:
#         player = Players.objects.get(name__icontains=name)  # 대소문자 구분 없이 검색
#         player_info = (
#             f"이 선수는 {player.name}이고, 팀은 {player.team}, "
#             f"포지션은 {player.position}, 타석은 {player.batter_hand} 입니다."
#         )
#     except Players.DoesNotExist:
#         return Response({'response': '해당 선수에 대한 정보를 찾을 수 없습니다.'}, status=404)

#     # OpenAI API 호출에 선수 정보를 프롬프트로 전달
#     try:
#         response = openai.Completion.create(
#             engine="text-davinci-003",
#             prompt=f"선수 정보: {player_info}. 이 선수에 대해 자세히 설명해주세요.",
#             max_tokens=100,
#             temperature=0.7
#         )
#         openai_response = response.choices[0].text.strip()
#         return Response({'response': openai_response})
#     except Exception as e:
#         return Response({'response': 'OpenAI API 호출에 실패했습니다.', 'error': str(e)}, status=500)