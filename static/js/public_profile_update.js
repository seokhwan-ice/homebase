// 프로필 데이터를 불러오기
async function loadProfileData() {
    try {
        // 'me/' 경로를 사용해 로그인한 사용자의 정보 요청
        const response = await axios.get(`user/me/`);
        const data = response.data;

        // 프로필 정보를 입력 폼에 반영
        document.getElementById("email").value = data.email;
        document.getElementById("phone_number").value = data.phone_number;
        document.getElementById("nickname").value = data.nickname;
        document.getElementById("bio").value = data.bio;
    } catch (error) {
        console.error("프로필 정보를 불러오는 중 오류 발생:", error);
        alert("프로필 정보를 불러오는 중 오류가 발생했습니다.");
    }
}

// 프로필 수정 데이터 전송
async function updateProfileData() {
    const email = document.getElementById("email").value;
    const phone_number = document.getElementById("phone_number").value;
    const nickname = document.getElementById("nickname").value;
    const bio = document.getElementById("bio").value;

    const updateData = {
        email,
        phone_number,
        nickname,
        bio
    };

    try {
        const response = await axios.put(`user/me/`, updateData);
        alert("프로필이 성공적으로 수정되었습니다.");
    } catch (error) {
        console.error("프로필 수정 중 오류 발생:", error);
        alert("프로필 수정 중 오류가 발생했습니다.");
    }
}

// 페이지 로드 시 프로필 데이터 불러오기
document.addEventListener("DOMContentLoaded", loadProfileData);

// 수정 버튼 클릭 시 프로필 업데이트
document.getElementById("update-profile-button").addEventListener("click", updateProfileData);

