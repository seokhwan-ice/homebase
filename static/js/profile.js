// 내 프로필 조회

const params = new URLSearchParams(location.search); // URL 파라미터 찾는 객체 만들어서
const userId = params.get('id'); 

const getProfile= async () => {
    try {  
        const response = await axios.get(`user/${username}/`);  // API 요청
        const data = response.data;

        
        document.getElementById('nickname').textContent = data.nickname;
        doucument.getElementById('free_count').textContent = data.free_count;
        doucument.getElementById('live_count').textContent = data.live_count;
        document.getElementById('comment_count').textContent = data.comment_count;
        document.getElementById('created_at').textContent = new Date(data.created_at).toLocaleString();
        docuument.getElementById('following_count').textContent = data.following_count;
        document.getElementById('followers_count').textContent = data.followers_count;
        document.getElementById('bookmark_count').textContent = data.bookmarked_count;
        // 좋아요 추가?

        // 프로필 이미지 : null인 경우 처리작업 추가해야할거같다.. 일단 텍스트로
        const profileImage = free.author.profile_image ? `<img src="${free.author.profile_image}" alt="프로필 이미지" width="50">` : "이미지 없음";
        document.getElementById('free-profile-image').innerHTML = profileImage;

        // 소개글 : null 일때 어떻게?
        const intro = free.intro? free.intro : "빈 소개글입니다.";
        document.getElementById('free-intro').textContent = intro;
        

    } catch (error) {
        console.error("Error:", error);
    }
};
