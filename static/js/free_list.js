
// 자유게시판 글 목록 (free_list)

const getFreeList = async (query = '') => {
    try {
        const response = await axios.get(`community/free/?q=${query}`);
        const data = response.data;

        const freeList = document.getElementById('free-list');
        freeList.innerHTML = '';

        data.forEach(free => {
            const freeListItem = document.createElement('tr');
            freeListItem.innerHTML = `
                <td><a href="free_detail.html?id=${free.id}">${free.title}</a></td>
                <td>${free.views}</td>
                <td>${free.author.nickname}</td>
                <td>${new Date(free.created_at).toLocaleDateString()}</td>
            `;
            freeList.appendChild(freeListItem);
        });

    } catch (error) {
        console.error("Error:", error);
    }
};

getFreeList();

// 검색 버튼 클릭 이벤트
document.getElementById('search-button').addEventListener('click', () => {
    const searchInput = document.getElementById('search-input').value;
    getFreeList(searchInput);
});

// 글쓰기 버튼 클릭
document.getElementById('create-button').addEventListener('click', () => {
    if (!checkSignin()) return;
    location.href = 'free_create.html';
});