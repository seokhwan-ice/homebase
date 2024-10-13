document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await axios.get('community/main/');
        const data = response.data;

        // 자유 게시판 (Free)
        const topViewedFree = data.top_viewed_free;
        const topViewedFreeList = document.getElementById('top-viewed-free');
        topViewedFree.forEach(free => {
            const li = document.createElement('li');
            li.innerHTML = `<a href="free_detail.html?id=${free.id}">${free.title}</a> (조회수: ${free.views})`;
            topViewedFreeList.appendChild(li);
        });

        const topCommentedFree = data.top_commented_free;
        const topCommentedFreeList = document.getElementById('top-commented-free');
        topCommentedFree.forEach(free => {
            const li = document.createElement('li');
            li.innerHTML = `<a href="free_detail.html?id=${free.id}">${free.title}</a> (댓글 수: ${free.comments_count})`;
            topCommentedFreeList.appendChild(li);
        });

        // 직관인증 게시판 (Live)
        const topLikedLive = data.top_liked_live;
        const topLikedLiveList = document.getElementById('top-liked-live');
        topLikedLive.forEach(live => {
            const li = document.createElement('li');
            li.innerHTML = `<a href="live_detail.html?id=${live.id}">${live.image}</a> (좋아요: ${live.likes_count})`;
            topLikedLiveList.appendChild(li);
        });

        const topCommentedLive = data.top_commented_live;
        const topCommentedLiveList = document.getElementById('top-commented-live');
        topCommentedLive.forEach(live => {
            const li = document.createElement('li');
            li.innerHTML = `<a href="live_detail.html?id=${live.id}">${live.image}</a> (댓글 수: ${live.comments_count})`;
            topCommentedLiveList.appendChild(li);
        });

        // 채팅방 (Chat)
        const topChatrooms = data.top_participated_chatrooms;
        const topChatroomList = document.getElementById('top-participated-chatrooms');
        topChatrooms.forEach(chatroom => {
            const li = document.createElement('li');
            li.innerHTML = `<a href="chatroom_detail.html?roomId=${chatroom.id}">${chatroom.title}</a> (참여자 수: ${chatroom.participants_count})`;
            topChatroomList.appendChild(li);
        });

    } catch (error) {
        console.error('데이터 로드 실패:', error);
    }
});
