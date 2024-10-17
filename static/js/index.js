document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await axios.get('community/main/');
        const data = response.data;

        // 자유 게시판 (Free)
        const topViewedFree = data.top_viewed_free;
        const topViewedFreeList = document.getElementById('top-viewed-free');
        topViewedFree.forEach(free => {
            const li = document.createElement('li');
            li.innerHTML = `
                <a href="free_detail.html?id=${free.id}">${free.title}</a>
                <div class="author-meta">
                    <span class="author">작성: ${free.author.nickname}</span>
                    <div class="meta-info">
                        <span><i class="fas fa-eye"></i> ${free.views}</span>
                        <span><i class="fas fa-comments"></i> ${free.comments_count}</span>
                    </div>
                </div>
            `;
            topViewedFreeList.appendChild(li);
        });

        const topCommentedFree = data.top_commented_free;
        const topCommentedFreeList = document.getElementById('top-commented-free');
        topCommentedFree.forEach(free => {
            const li = document.createElement('li');
            li.innerHTML = `
                <a href="free_detail.html?id=${free.id}">${free.title}</a>
                <div class="author-meta">
                    <span class="author">작성: ${free.author.nickname}</span>
                    <div class="meta-info">
                        <span><i class="fas fa-eye"></i> ${free.views}</span>
                        <span><i class="fas fa-comments"></i> ${free.comments_count}</span>
                    </div>
                </div>
            `;
            topCommentedFreeList.appendChild(li);
        });


        // 직관인증 게시판 (Live)
        const defaultImageLive = '../images/live_image.png';

        const topLikedLive = data.top_liked_live;
        const topLikedLiveList = document.getElementById('top-liked-live');
        topLikedLive.forEach(live => {
            const imageUrl = live.live_image || defaultImageLive; // 기본 이미지 설정
            const li = document.createElement('li');
            li.innerHTML = `
                <a href="live_detail.html?id=${live.id}">
                    <div class="profile-section">
                        <div class="author">
                            <img src="${live.author.profile_image || '../images/kinggoddino.jpg'}" alt="${live.author.nickname}">
                            <span>${live.author.nickname}</span>
                        </div>
                        <span class="date">${new Date(live.created_at).toLocaleDateString('ko-KR', { month: '2-digit', day: '2-digit' })}</span>
                    </div>
                    <div class="image-section">
                        <img src="${imageUrl}" alt="${live.home_team} vs ${live.away_team}">
                    </div>
                    <div class="info-section">
                        <p class="team">${live.home_team} vs ${live.away_team}</p>
                        <div class="bottom-info">
                            <span class="stadium">${live.stadium}</span>
                            <div class="meta-info">
                                <span><i class="fas fa-heart"></i> ${live.likes_count}</span>
                                <span><i class="fas fa-comment"></i> ${live.comments_count}</span>
                            </div>
                        </div>
                    </div>
                </a>
            `;
            topLikedLiveList.appendChild(li);
        });

        const topCommentedLive = data.top_commented_live;
        const topCommentedLiveList = document.getElementById('top-commented-live');
        topCommentedLive.forEach(live => {
            const imageUrl = live.live_image || defaultImageLive; // 기본 이미지 설정
            const li = document.createElement('li');
            li.innerHTML = `
                <a href="live_detail.html?id=${live.id}">
                    <div class="profile-section">
                        <div class="author">
                            <img src="${live.author.profile_image || '../images/kinggoddino.jpg'}" alt="${live.author.nickname}">
                            <span>${live.author.nickname}</span>
                        </div>
                        <span class="date">${new Date(live.created_at).toLocaleDateString('ko-KR', { month: '2-digit', day: '2-digit' })}</span>
                    </div>
                    <div class="image-section">
                        <img src="${imageUrl}" alt="${live.home_team} vs ${live.away_team}">
                    </div>
                    <div class="info-section">
                        <p class="team">${live.home_team} vs ${live.away_team}</p>
                        <div class="bottom-info">
                            <span class="stadium">${live.stadium}</span>
                            <div class="meta-info">
                                <span><i class="fas fa-heart"></i> ${live.likes_count}</span>
                                <span><i class="fas fa-comment"></i> ${live.comments_count}</span>
                            </div>
                        </div>
                    </div>
                </a>
            `;
            topCommentedLiveList.appendChild(li);
        });

        // 채팅방 (Chat)
        const defaultImageChat = '../images/baseball.png';

        const topChatrooms = data.top_participated_chatrooms;
        const topChatroomList = document.getElementById('top-participated-chatrooms');
        topChatrooms.forEach(chatroom => {
            const imageUrl = chatroom.image || defaultImageChat;
            const li = document.createElement('li');
            li.innerHTML = `
                <a href="chatroom_detail.html?roomId=${chatroom.id}">
                    <div class="left-section">
                        <img src="${imageUrl}" alt="${chatroom.title}" class="chatroom-image">
                        <div class="chatroom-info">
                            <span class="title">${chatroom.title}</span>
                            <span class="description">${chatroom.description}</span>
                        </div>
                    </div>
                    <div class="right-section">
                        <span class="latest-message">${new Date(chatroom.latest_message_time).toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })}</span>
                        <i class="fas fa-user"></i>
                        <span class="participants">${chatroom.participants_count}</span>
                    </div>
                </a>
            `;
            topChatroomList.appendChild(li);
        });

        // 최신 뉴스 (News)
        const latestNews = data.latest_news;
        const newsList = document.getElementById('news-list');
        latestNews.forEach(news => {
            const formattedDate = formatDate(news.published_at);
            const li = document.createElement('li');
            li.innerHTML = `
                <a href="${news.url}" target="_blank">
                    <p>${formattedDate}</p>
                    <img src="${news.image_url}" alt="뉴스 이미지">
                    <h3>${news.title}</h3>
                </a>
            `;
            newsList.appendChild(li);
        });

        // 팀 랭킹 (Team Rank)
        const teamRank = data.team_rank;
        const teamRankList = document.getElementById('team-rank-list');
        teamRank.forEach((team) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${team.rank}위</td>
                <td>${team.team_name}</td>
                <td>${team.win_rate}</td>
                <td>${team.wins}승 ${team.draws}무 ${team.losses}패</td>
                <td>${team.games_played}</td>
                <td>${team.games_behind}</td>
            `;
            teamRankList.appendChild(row);
        });

    } catch (error) {
        console.error('데이터 로드 실패:', error);
    }
});


// 날짜 포맷 -> 'M월 D일 H시 m분'
function formatDate(dateString) {
    const date = new Date(dateString);
    const month = String(date.getMonth() + 1);  // 월은 0부터 시작하므로 +1
    const day = String(date.getDate());
    const hours = String(date.getHours());
    const minutes = String(date.getMinutes());
    return `${month}월 ${day}일 ${hours}:${minutes}`;
}