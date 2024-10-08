// 내가 쓴 글 조회 - 자유 게시판
// 내가 쓴 글이 맞는 지 확인하는 구문?

const getFreeArticleList = async () => {
    try {
        const response = await axios.get(`user/${userId}/free`);  // API 요청
        const data = response.data;

        const free_articleList = document.getElementById('free-list');
        // getElementById: 특정 ID 가진 HTML 요소를 가져오는 함수.
        // 12번째 줄 id="free-list" ul 태그에 데이터를 표시할거라는 뜻

        data.forEach(free => { // 파이썬 for...in문이랑 비슷함. free 하나씩 돌면서, 화살표함수 내용 실행
            const free_articleList = document.createElement('li');
            // createElement: 새로운 HTML 요소 만들어주는 함수. li(list item) 태그 만들었어요
            // freeListItem 변수 선언: 이게 게시글 목록의 "글 한개" 에 해당함
            free_articleList.innerHTML = `
                <a href="free_detail.html?id=${free.id}">[${free.id}] ${free.title}</a>
                <br>작성자: ${free.author.nickname}
                <br>조회수: ${free.views}
                <br>댓글수: ${free.comments_count}<hr>
            `;
            free_articleList.appendChild(free_articleListItem);
        });  // 새로 생성한 li 태그(freeListItem)를 ul 태그(freelist)에 추가하고 반복문 끝

    } catch (error) {
        console.error("Error:", error);
        alert("글 등록 실패");
    }
};

getFreeArticleList();