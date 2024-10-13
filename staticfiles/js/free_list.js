
// 자유게시판 글 목록 (free_list)

const getFreeList = async (query = '') => {
    try {
        const response = await axios.get(`community/free/?q=${query}`);
        const data = response.data;

        const freeList = document.getElementById('free-list');
        // getElementById: 특정 ID 가진 HTML 요소를 가져오는 함수.
        // 12번째 줄 id="free-list" ul 태그에 데이터를 표시할거라는 뜻
        freeList.innerHTML = '';  // 기존 목록 초기화

        data.forEach(free => { // 파이썬 for...in문이랑 비슷함. free 하나씩 돌면서, 화살표함수 내용 실행
            const freeListItem = document.createElement('li');
            // createElement: 새로운 HTML 요소 만들어주는 함수. li(list item) 태그 만들었어요
            // freeListItem 변수 선언: 이게 게시글 목록의 "글 한개" 에 해당함
            freeListItem.innerHTML = `
                <a href="free_detail.html?id=${free.id}">[${free.id}] ${free.title}</a>
                <br>작성자: ${free.author.nickname}
                <br>조회수: ${free.views}
                <br>댓글수: ${free.comments_count}<hr>
            `;
            freeList.appendChild(freeListItem);
        });  // 새로 생성한 li 태그(freeListItem)를 ul 태그(freelist)에 추가하고 반복문 끝

    } catch (error) {
        console.error("Error:", error);
        alert("글 목록 불러오기 실패");
    }
};

getFreeList();

// 검색 버튼 클릭 이벤트
document.getElementById('search-button').addEventListener('click', () => {
    const searchInput = document.getElementById('search-input').value;
    getFreeList(searchInput);
});