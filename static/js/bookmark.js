// Axios를 이용해 백엔드에서 북마크한 글 목록 가져오기

const username = '로그인된 유저의 이름';

document.addEventListener('DOMContentLoaded', function() {
    const bookmarksListElement = document.getElementById('bookmark-list');

    // 북마크한 글 목록을 가져오는 API 엔드포인트
    const apiUrl = `user/${username}/bookmark/`;  // 실제 API 엔드포인트로 변경

    axios.get(apiUrl)
    .then(response => {
        const bookmarks = response.data;  // 응답이 바로 배열일 경우
        if (!Array.isArray(bookmarks)) {
            console.error('북마크 목록이 배열이 아닙니다.');
            return;
        }
        
        bookmarks.forEach(bookmark => {
            const listItem = document.createElement('li');
            listItem.textContent = bookmark.title;
            bookmarksListElement.appendChild(listItem);
        });
    })
    .catch(error => {
        console.error('API 요청 중 오류 발생:', error);
    });
});
