from django.db import models


class SportsNews(models.Model):
    title = models.CharField(max_length=255)  # 뉴스 제목
    author = models.CharField(max_length=100, null=True, blank=True)  # 기자 이름
    description = models.TextField(null=True, blank=True)  # 기사 설명
    url = models.URLField()  # 기사 링크
    published_at = models.DateTimeField()  # 발행일
    content = models.TextField(null=True, blank=True)  # 기사 내용
    image_url = models.URLField(null=True, blank=True)  # 이미지 링크

    def __str__(self):
        return self.title


class Players(models.Model):
    player_number = models.IntegerField()  # 선수 고유 번호 추가
    name = models.CharField(max_length=100)
    team_name = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    batter_hand = models.CharField(max_length=10)
    birth_date = models.DateField(null=True, blank=True)  # 날짜 필드
    school = models.CharField(max_length=100, null=True, blank=True)
    draft_info = models.CharField(max_length=100, null=True, blank=True)
    active_years = models.CharField(max_length=50, null=True, blank=True)
    active_team = models.CharField(max_length=50, null=True, blank=True)
    profile_img = models.URLField(null=True, blank=True)  # 이미지 URL 필드

    def __str__(self):
        return self.name


class PlayerRecord(models.Model):
    player_number = models.IntegerField()  # 선수 고유 번호 추가
    team_logo_url = models.URLField(max_length=255)
    name = models.CharField(max_length=100)
    opponent = models.CharField(max_length=100)
    pa = models.IntegerField(default=0)
    epa = models.IntegerField(default=0)
    ab = models.IntegerField(default=0)
    r = models.IntegerField(default=0)
    h = models.IntegerField(default=0)
    two_b = models.IntegerField(default=0)
    three_b = models.IntegerField(default=0)
    hr = models.IntegerField(default=0)
    tb = models.IntegerField(default=0)
    rbi = models.IntegerField(default=0)
    bb = models.IntegerField(default=0)
    hp = models.IntegerField(default=0)
    ib = models.IntegerField(default=0)
    so = models.IntegerField(default=0)
    gdp = models.IntegerField(default=0)
    sh = models.IntegerField(default=0)
    sf = models.IntegerField(default=0)
    avg = models.FloatField(default=0.0)
    obp = models.FloatField(default=0.0)
    slg = models.FloatField(default=0.0)
    ops = models.FloatField(default=0.0)
    np = models.IntegerField(default=0)
    avli = models.FloatField(default=0.0)
    re24 = models.FloatField(default=0.0)
    wpa = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.team_logo_url} {self.name}"

    class Meta:
        unique_together = ("name", "opponent")  # name과 opponent 조합이 유니크해야 함


class GameRecord(models.Model):
    url = models.URLField()
    date = models.DateField()
    team_1 = models.CharField(max_length=100)
    team_2 = models.CharField(max_length=100)
    inning_scores_team_1 = models.JSONField(default=list)  # JSONField 사용
    inning_scores_team_2 = models.JSONField(default=list)
    r_h_e_b_team_1 = models.JSONField(
        blank=True, default=dict
    )  # 팀 1의 R, H, E, B 값 저장
    r_h_e_b_team_2 = models.JSONField(
        blank=True, default=dict
    )  # 팀 2의 R, H, E, B 값 저장

    class Meta:
        unique_together = (("date", "team_1", "team_2"),)
        db_table = "data_gamerecord"  # 테이블 이름을 명시적으로 설정

    def __str__(self):
        return f"{self.date}: {self.team_1} vs {self.team_2}"


class TeamRank(models.Model):
    rank = models.IntegerField()  # 순위
    team_number = models.CharField(max_length=10)
    team_name = models.CharField(max_length=100)  # 팀 이름
    games_played = models.IntegerField()  # 경기 수
    wins = models.IntegerField()  # 승리 수
    draws = models.IntegerField()  # 무승부 수
    losses = models.IntegerField()  # 패배 수
    games_behind = models.FloatField()  # 게임차 (소수점 가능)
    win_rate = models.FloatField()  # 승률 (소수점 가능)
    streak = models.CharField(max_length=10)  # 연속 (e.g., "W3", "L2" 등)
    last_10_games = models.CharField(max_length=20)  # 최근 10경기 성적 (e.g., "7-3")

    def __str__(self):
        return f"{self.rank} - {self.team_name}"

    class Meta:
        verbose_name = "Team Record"
        verbose_name_plural = "Team Records"
        ordering = ["rank"]  # 순위 기준으로 정렬
        db_table = "data_teamrank"  # 테이블 이름을 명시적으로 설정


class TeamRecord(models.Model):
    team_name = models.CharField(max_length=50)
    team_number = models.CharField(max_length=10)
    rival = models.CharField(max_length=50)
    wins = models.IntegerField()
    draws = models.IntegerField()
    losses = models.IntegerField()
    win_rate = models.FloatField()

    def __str__(self):
        return f"{self.team_name} vs {self.rival}"


class TeamDetail(models.Model):
    team_number = models.CharField(max_length=10)
    team = models.CharField(max_length=100)  # 팀 이름
    year = models.FloatField()  # 연도
    war = models.FloatField()  # WAR
    owar = models.FloatField()  # oWAR
    dwar = models.FloatField()  # dWAR
    games = models.FloatField()  # 경기 수
    plate_appearances = models.FloatField()  # 타석 수
    effective_pa = models.FloatField()  # 유효 타석 수
    at_bats = models.FloatField()  # 타수
    runs = models.FloatField()  # 득점
    hits = models.FloatField()  # 안타
    two_b = models.FloatField()  # 2루타
    three_b = models.FloatField()  # 3루타
    home_runs = models.FloatField()  # 홈런
    total_bases = models.FloatField()  # 총 베이스
    rbi = models.FloatField()  # 타점
    stolen_bases = models.FloatField()  # 도루
    caught_stealing = models.FloatField()  # 도루 실패
    walks = models.FloatField()  # 볼넷
    hit_by_pitch = models.FloatField()  # 몸에 맞는 볼
    intentional_walks = models.FloatField()  # 고의 볼넷
    strikeouts = models.FloatField()  # 삼진
    grounded_into_double_play = models.FloatField()  # 병살 타구
    sacrifice_hits = models.FloatField()  # 희생타
    sacrifice_flies = models.FloatField()  # 희생플라이
    batting_average = models.FloatField()  # 타율
    on_base_percentage = models.FloatField()  # 출루율
    slugging_percentage = models.FloatField()  # 장타율
    on_base_plus_slugging = models.FloatField()  # OPS
    runs_per_effective_pa = models.FloatField()  # 유효 타석당 득점
    wrc_plus = models.FloatField()  # wRC+

    class Meta:
        verbose_name = "팀 통계"
        verbose_name_plural = "팀 통계"

    def __str__(self):
        return f"{self.year} {self.team} "


class WeatherData(models.Model):
    base_date = models.CharField(max_length=8)  # YYYYMMDD
    base_time = models.CharField(max_length=4)  # HHMM
    location = models.CharField(max_length=50)  # 지점 이름 추가
    temperature = models.FloatField()  # 기온 (TMP)
    humidity = models.FloatField()  # 습도 (REH)
    wind_speed = models.FloatField()  # 풍속 (WSD)
    wind_direction = models.CharField(max_length=10)  # 풍향 (VEC)
    rain_status = models.CharField(max_length=10)  # 강수 상태 (PTY)
    rain_probability = models.FloatField(null=True, blank=True)  # 강수 확률 (POP)
    sky_status = models.CharField(
        max_length=10, null=True, blank=True
    )  # 하늘 상태 (SKY)
    precipitation = models.FloatField(null=True, blank=True)  # 강수량 (PCP)
    min_temperature = models.FloatField(null=True, blank=True)  # 일 최저기온 (TMN)
    max_temperature = models.FloatField(null=True, blank=True)  # 일 최고기온 (TMX)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.location} ({self.base_date} {self.base_time}) - 온도: {self.temperature}℃, 습도: {self.humidity}%, 풍향: {self.wind_direction}, 강수 상태: {self.rain_status}"


class Video(models.Model):
    video_id = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    publish_time = models.DateTimeField()
    video_url = models.URLField()

    def __str__(self):
        return self.title
