// 내가 쓴 글 조회 - 자유 게시판
// 내가 쓴 글이 맞는 지 확인하는 구문?

const getMyFreeArticles = async () => {
    try {
        const response = await axios.get(`user/${userId}/my_free`);  // 내 게시물 조회 API 요청
        const data = response.data;

        // const my_free_articleList = document.getElementById('my-free-list');
        // 내 프로필에서 작성한 게시물을 표시할 ul 태그를 가져옴 (id="my-free-list")
        const profileImage = free.author.profile_image ? `<img src="${free.author.profile_image}" alt="프로필 이미지" width="50">` : "이미지 없음";
        document.getElementById('free-profile-image').innerHTML = profileImage;
        document.getElementById('free-profile-nickname').textContent = free.author.nickname;

        data.forEach(free => {  // 내 게시물 목록을 하나씩 처리
            const my_free_articleListItem = document.createElement('li');
            // li 태그를 생성하여 내 게시물 목록의 한 항목을 만듦
            my_free_articleListItem.innerHTML = `
                <a href="free_detail.html?id=${free.id}">[${free.id}] ${free.title}</a>
                <br>작성자: ${free.author.nickname}
                <br>조회수: ${free.views}
                <br>댓글수: ${free.comments_count}<hr>
            `;
            my_free_articleList.appendChild(my_free_articleListItem);
            location.href = `free_list.html?id=${freeId}`;  // 내가 쓴 글 목록으로 이동
        });
    } catch (error) {
        console.error('게시물 불러오기 실패:', error);
    }
};

window.onload = () => {
    getMyFreeArticles();  // 페이지 로드 시 내가 작성한 게시물을 불러오는 함수 호출
};