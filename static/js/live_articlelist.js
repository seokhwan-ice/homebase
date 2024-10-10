// // 내가 쓴 글 조회 - 직관인증 게시판

// const getMyLiveArticles = async () => {
//     try {
//         const response = await axios.get(`user/${userId}/my_live`);  // 내 게시물 조회 API 요청
//         const data = response.data;

//         const my_live_articleList = document.getElementById('my-live-list'); // 내 프로필에서 작성한 게시물을 표시할 ul 태그 가져오기
//         const profileImage = data[0]?.author.profile_image ? `<img src="${data[0].author.profile_image}" alt="프로필 이미지" width="50">` : "이미지 없음"; // 첫 게시물 작성자의 프로필 이미지 가져오기
//         document.getElementById('free-profile-image').innerHTML = profileImage;
//         document.getElementById('free-profile-nickname').textContent = data[0]?.author.nickname || "닉네임 없음"; // 첫 게시물 작성자의 닉네임 가져오기

//         data.forEach(free => {  // 내 게시물 목록을 하나씩 처리
//             const my_live_articleListItem = document.createElement('li');
//             // li 태그를 생성하여 내 게시물 목록의 한 항목을 만듦
//             my_live_articleListItem.innerHTML = `
//                 <a href="free_detail.html?id=${free.id}">[${free.id}] ${free.title}</a>
//                 <br>작성자: ${free.author.nickname}
//                 <br>조회수: ${free.views}
//                 <br>댓글수: ${free.comments_count}
//                 <br>${free.free_image ? `<img src="${free.free_image}" alt="${free.title} 이미지" width="100">` : "이미지 없음"}<hr>
//             `;
//             my_live_articleList.appendChild(my_free_articleListItem);
//         });
//     } catch (error) {
//         console.error('게시물 불러오기 실패:', error);
//     }
// };

// window.onload = () => {
//     getMyLiveArticles();  // 페이지 로드 시 내가 작성한 게시물을 불러오는 함수 호출
// };

// Axios를 이용해 백엔드에서 내가 쓴 글 목록과 썸네일 가져오기
document.addEventListener('DOMContentLoaded', function() {
    const thumbnailsContainer = document.getElementById('my-posts-thumbnails');

    // 백엔드에서 사용자의 글 목록을 가져오는 API 엔드포인트
    const apiUrl = `/api/user/${userId}/live`; // 실제 API 엔드포인트로 변경

    axios.get(apiUrl)
        .then(response => {
            const posts = response.data;
            // 가져온 데이터로 썸네일 목록 생성
            posts.forEach(post => {
                const imageElement = document.createElement('img');
                imageElement.src = post.free_image; // free_image 필드 사용
                imageElement.alt = post.title; // 이미지 대체 텍스트로 제목 사용
                imageElement.classList.add('post-thumbnail');
                thumbnailsContainer.appendChild(imageElement);
            });
        })
        .catch(error => {
            console.error('내 글 목록을 불러오는 중 오류 발생:', error);
        });
});