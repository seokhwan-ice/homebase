import openai
from homebase import config
from rest_framework.response import Response
from rest_framework.decorators import api_view
from data.models import Players  # Player 모델 가져오기

# OpenAI API 키 설정
openai.api_key = config.OPENAI_API_KEY

@api_view(['POST'])
def get_player_info(request):
    
    # 요청에서 선수 이름 받기
    name = request.data.get('player_name')

    if not name:
        return Response({'response': '선수 이름을 입력해주세요.'}, status=400)

    # 데이터베이스에서 해당 선수 정보 검색
    try:
        player = Players.objects.filter(name__icontains=name).first()  # 첫 번째 선수만 가져오기
        if player is None:
            return Response({'response': '해당 선수에 대한 정보를 찾을 수 없습니다.'}, status=404)
        player_info = (
            f"이 선수는 {player.name}이고, 팀은 {player.team}, "
            f"포지션은 {player.position}, 타석은 {player.batter_hand} 입니다."
        )
    except Players.DoesNotExist:
        return Response({'response': '해당 선수에 대한 정보를 찾을 수 없습니다.'}, status=404)

    # OpenAI API 호출에 선수 정보를 프롬프트로 전달
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"선수 정보: {player_info}. 이 선수에 대해 자세히 설명해주세요.",
            max_tokens=100,
            temperature=0.7
        )
        openai_response = response.choices[0].text.strip()
        return Response({'response': openai_response})
    except Exception as e:
        return Response({'response': 'OpenAI API 호출에 실패했습니다.', 'error': str(e)}, status=500)