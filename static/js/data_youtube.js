let allVideos = []; // 모든 비디오 데이터를 저장할 배열
let currentPage = 1; // 현재 페이지
const videosPerPage = 9; // 페이지당 비디오 수

document.addEventListener('DOMContentLoaded', () => {
    fetchVideos(); // 페이지 로드 시 비디오 가져오기

    // 검색 버튼 클릭 시 검색어로 비디오를 필터링합니다.
    document.getElementById('search-button').addEventListener('click', filterVideos);

    // 페이지네이션 버튼 클릭 이벤트
    document.getElementById('prev-button').addEventListener('click', () => changePage(currentPage - 1));
    document.getElementById('next-button').addEventListener('click', () => changePage(currentPage + 1));
});

function fetchVideos() {
    axios.get('data/youtube/') // GET 요청할 URL
        .then(response => {
            allVideos = response.data; // 전체 비디오 데이터 저장
            displayVideos(allVideos); // 비디오 목록 표시
            updatePagination(); // 페이지네이션 업데이트
        })
        .catch(error => {
            console.error("비디오를 가져오는 데 오류 발생:", error);
            document.getElementById('video-list').innerHTML = '<p>비디오를 가져오는 데 오류가 발생했습니다.</p>';
        });
}

function filterVideos() {
    const query = document.getElementById('search-query').value.toLowerCase(); // 입력 필드에서 검색어 가져오기
    const filteredVideos = allVideos.filter(video =>
        video.title.toLowerCase().includes(query) ||
        video.description.toLowerCase().includes(query)
    ); // 제목이나 설명에 검색어가 포함된 비디오 필터링
    displayVideos(filteredVideos); // 필터링된 비디오 표시
    currentPage = 1; // 필터링 후 첫 페이지로 초기화
    updatePagination(); // 페이지네이션 업데이트
}

function displayVideos(videos) {
    const videoListDiv = document.getElementById('video-list');
    videoListDiv.innerHTML = ''; // 기존 비디오 목록 초기화

    // 페이지네이션 계산
    const start = (currentPage - 1) * videosPerPage;
    const end = start + videosPerPage;
    const paginatedVideos = videos.slice(start, end); // 현재 페이지에 해당하는 비디오 목록

    if (paginatedVideos.length === 0) {
        videoListDiv.innerHTML = '<p>저장된 비디오가 없습니다.</p>';
    } else {
        paginatedVideos.forEach(video => {
            videoListDiv.innerHTML += `
                <div class="video-item">
                    <img src="https://img.youtube.com/vi/${video.video_id}/hqdefault.jpg" alt="${video.title}" class="video-thumbnail" />
                    <h2>${video.title}</h2>
                    <p>${video.description}</p>
                    <p>게시 시간: ${new Date(video.publish_time).toLocaleString()}</p>
                    <a href="${video.video_url}" target="_blank">비디오 보기</a>
                </div>
                <hr>
            `;
        });
    }
}

function changePage(page) {
    const totalPages = Math.ceil(allVideos.length / videosPerPage); // 총 페이지 수

    // 페이지 번호가 유효한지 확인
    if (page < 1 || page > totalPages) return;

    currentPage = page; // 현재 페이지 업데이트
    displayVideos(allVideos); // 현재 페이지에 해당하는 비디오 목록 다시 표시
    updatePagination(); // 페이지네이션 업데이트
}

function updatePagination() {
    const totalPages = Math.ceil(allVideos.length / videosPerPage); // 총 페이지 수

    // 페이지 번호 버튼을 추가할 div
    const pageNumbersDiv = document.getElementById('page-numbers');
    pageNumbersDiv.innerHTML = ''; // 기존 페이지 번호 초기화

    // 현재 페이지가 속한 그룹 계산
    const groupSize = 10; // 각 그룹의 크기
    const currentGroup = Math.ceil(currentPage / groupSize); // 현재 페이지가 속한 그룹
    const startPage = (currentGroup - 1) * groupSize + 1; // 시작 페이지
    const endPage = Math.min(startPage + groupSize - 1, totalPages); // 끝 페이지

    // 페이지 번호 버튼 생성
    for (let i = startPage; i <= endPage; i++) {
        const pageButton = document.createElement('button'); // 페이지 번호 버튼 생성
        pageButton.innerText = i; // 페이지 번호 설정
        pageButton.classList.add('page-button'); // 버튼에 클래스 추가
        pageButton.disabled = (i === currentPage); // 현재 페이지 버튼 비활성화
        pageButton.addEventListener('click', () => changePage(i)); // 클릭 시 해당 페이지로 이동

        pageNumbersDiv.appendChild(pageButton); // 페이지 번호 버튼 추가
    }

    // 그룹 이전/다음 버튼 추가
    if (currentGroup > 1) {
        const prevGroupButton = document.createElement('button');
        prevGroupButton.innerText = '이전 그룹';
        prevGroupButton.addEventListener('click', () => changePage(startPage - groupSize));
        pageNumbersDiv.prepend(prevGroupButton); // 이전 그룹 버튼을 앞에 추가
    }

    if (endPage < totalPages) {
        const nextGroupButton = document.createElement('button');
        nextGroupButton.innerText = '다음 그룹';
        nextGroupButton.addEventListener('click', () => changePage(endPage + 1));
        pageNumbersDiv.appendChild(nextGroupButton); // 다음 그룹 버튼을 뒤에 추가
    }

    // 이전/다음 버튼 비활성화 (숨김)
    document.getElementById('prev-button').style.display = 'none';
    document.getElementById('next-button').style.display = 'none';
}
