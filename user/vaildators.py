from .models import User

def validate_user_data(user_data):
    username = user_data.get("username")
    nickname = user_data.get("nickname")
    name = user_data.get("name")
    password = user_data.get("password")
    bio = user_data.get("bio")
    profile_image = user_data.get("profile_image")
    phone_number = user_data.get("phone_number")

    err_message = []

    if len(nickname) > 15:
        err_message.append("닉네임은 15글자 이하여야 합니다.")
        
    if len(password) < 8:
        err_message.append("비밀번호를 8글자 이상 입력해주세요.")
        
    if User.objects.filter(username=username).exists():
        err_message.append("이미 존재하는 아이디입니다.")
        
    if User.objects.filter(nickname=nickname).exists():
        err_message.append("이미 존재하는 닉네임입니다.")
        
    if not name:
        err_message.append("이름을 필수로 입력해주세요!")

    if err_message:
        return err_message
    return None