import streamlit as st
import random
import time

# ==========================================
# 1. PBA 선수 데이터베이스 (Top 25 대량 추출)
# ==========================================
# 데이터 기반으로 ELO 점수는 순위에 따라 1850~1550 사이로 가설정해 두었습니다.
PBA_PLAYERS = {
    "산체스": {"TS%": 63.4, "BS%": 18.0, "HR": 15, "BRS%": 78.8, "5HS%": 9.9, "PHR": 3, "PFR": 100.0, "PSR": 0.0, "ELO": 1850},
    "마민껌": {"TS%": 60.1, "BS%": 24.6, "HR": 14, "BRS%": 65.8, "5HS%": 9.9, "PHR": 3, "PFR": 66.7, "PSR": 33.3, "ELO": 1830},
    "모리": {"TS%": 60.6, "BS%": 28.7, "HR": 14, "BRS%": 75.8, "5HS%": 10.5, "PHR": 6, "PFR": 66.7, "PSR": 0.0, "ELO": 1820},
    "조재호": {"TS%": 63.8, "BS%": 20.9, "HR": 13, "BRS%": 81.9, "5HS%": 11.4, "PHR": 4, "PFR": 0.0, "PSR": 75.0, "ELO": 1810},
    "마르티네스": {"TS%": 62.7, "BS%": 28.3, "HR": 13, "BRS%": 75.4, "5HS%": 11.2, "PHR": 1, "PFR": 50.0, "PSR": 100.0, "ELO": 1800},
    "이승진": {"TS%": 58.1, "BS%": 24.5, "HR": 14, "BRS%": 65.3, "5HS%": 8.6, "PHR": 5, "PFR": 71.4, "PSR": 50.0, "ELO": 1780},
    "최성원": {"TS%": 60.3, "BS%": 25.7, "HR": 11, "BRS%": 77.9, "5HS%": 10.2, "PHR": 5, "PFR": 100.0, "PSR": 0.0, "ELO": 1770},
    "김영원": {"TS%": 61.6, "BS%": 21.0, "HR": 13, "BRS%": 54.7, "5HS%": 9.6, "PHR": 0, "PFR": 0.0, "PSR": 0.0, "ELO": 1760},
    "레펀스": {"TS%": 61.8, "BS%": 20.0, "HR": 13, "BRS%": 61.9, "5HS%": 10.1, "PHR": 5, "PFR": 75.0, "PSR": 0.0, "ELO": 1750},
    "김재근": {"TS%": 58.4, "BS%": 25.8, "HR": 13, "BRS%": 60.7, "5HS%": 8.9, "PHR": 7, "PFR": 83.3, "PSR": 100.0, "ELO": 1740},
    "강동궁": {"TS%": 63.5, "BS%": 24.9, "HR": 14, "BRS%": 69.6, "5HS%": 11.5, "PHR": 1, "PFR": 50.0, "PSR": 0.0, "ELO": 1730},
    "Q.응우옌": {"TS%": 61.3, "BS%": 24.6, "HR": 12, "BRS%": 67.2, "5HS%": 10.3, "PHR": 6, "PFR": 50.0, "PSR": 0.0, "ELO": 1720},
    "D.응우옌": {"TS%": 58.0, "BS%": 23.2, "HR": 12, "BRS%": 61.7, "5HS%": 7.9, "PHR": 4, "PFR": 75.0, "PSR": 80.0, "ELO": 1710},
    "응오": {"TS%": 62.2, "BS%": 20.6, "HR": 15, "BRS%": 65.5, "5HS%": 9.8, "PHR": 1, "PFR": 50.0, "PSR": 0.0, "ELO": 1700},
    "모랄레스": {"TS%": 60.7, "BS%": 19.4, "HR": 11, "BRS%": 77.6, "5HS%": 8.8, "PHR": 3, "PFR": 100.0, "PSR": 100.0, "ELO": 1690},
    "사파타": {"TS%": 60.4, "BS%": 21.1, "HR": 12, "BRS%": 78.6, "5HS%": 8.1, "PHR": 4, "PFR": 33.3, "PSR": 66.7, "ELO": 1680},
    "조건휘": {"TS%": 61.1, "BS%": 23.8, "HR": 11, "BRS%": 74.1, "5HS%": 9.1, "PHR": 3, "PFR": 33.3, "PSR": 0.0, "ELO": 1670},
    "이충복": {"TS%": 61.6, "BS%": 24.6, "HR": 14, "BRS%": 66.7, "5HS%": 9.7, "PHR": 3, "PFR": 100.0, "PSR": 50.0, "ELO": 1660},
    "초클루": {"TS%": 59.6, "BS%": 27.7, "HR": 13, "BRS%": 72.1, "5HS%": 9.1, "PHR": 5, "PFR": 50.0, "PSR": 33.3, "ELO": 1650},
    "사이그너": {"TS%": 60.5, "BS%": 21.8, "HR": 13, "BRS%": 62.5, "5HS%": 9.9, "PHR": 6, "PFR": 100.0, "PSR": 50.0, "ELO": 1640},
    "체네트": {"TS%": 61.5, "BS%": 21.7, "HR": 13, "BRS%": 66.1, "5HS%": 10.8, "PHR": 2, "PFR": 50.0, "PSR": 0.0, "ELO": 1630},
    "김임권": {"TS%": 58.1, "BS%": 26.9, "HR": 13, "BRS%": 58.9, "5HS%": 7.9, "PHR": 5, "PFR": 100.0, "PSR": 0.0, "ELO": 1620},
    "김종원": {"TS%": 58.3, "BS%": 25.9, "HR": 11, "BRS%": 67.9, "5HS%": 8.0, "PHR": 4, "PFR": 0.0, "PSR": 100.0, "ELO": 1610},
    "엄상필": {"TS%": 58.0, "BS%": 23.5, "HR": 14, "BRS%": 64.8, "5HS%": 8.3, "PHR": 2, "PFR": 0.0, "PSR": 50.0, "ELO": 1600},
    "팔라손": {"TS%": 59.5, "BS%": 26.2, "HR": 14, "BRS%": 64.2, "5HS%": 10.4, "PHR": 4, "PFR": 66.7, "PSR": 100.0, "ELO": 1590}
}

# ==========================================
# 2. 마르코프 체인 시뮬레이션 클래스
# ==========================================
class MarkovPBAPlayer:
    def __init__(self, name, stats, opp_elo):
        self.name = name
        self.elo = stats['ELO']
        
        # ELO 기반 멘탈 보정 (최대 ±5%)
        elo_diff = self.elo - opp_elo
        mental_modifier = max(-0.05, min(0.05, (elo_diff / 100) * 0.015))
        
        self.ts_pct = max(0.1, (stats['TS%'] / 100) + mental_modifier)
        self.brs_pct = max(0.1, (stats['BRS%'] / 100) + mental_modifier)
        self.bs_pct = stats['BS%'] / 100
        self.hr = int(stats['HR'])
        self.five_hs_pct = stats['5HS%'] / 100
        self.phr = int(stats['PHR'])
        self.pfr = stats['PFR'] / 100
        self.psr = stats['PSR'] / 100

    def play_inning_markov(self, is_break_shot=False, is_penalty=False):
        """마르코프 체인(Markov Chain) 상태 전이 모델 적용"""
        # [상태 정의]
        # State 0: 타격 준비 (초구 또는 일반 첫 샷)
        # State 1: 일반 득점 흐름 (1~3점) - 포지션 플레이 이점 소폭 적용
        # State 2: 장타(몰입) 흐름 (4점 이상) - 5HS% 모멘텀 적용
        # State 3: 턴 종료 (Miss)
        
        state = 0
        points = 0
        max_cap = self.phr if is_penalty else self.hr
        
        while state != 3 and points < max_cap:
            # 1. 현재 상태(State)에 따른 확률(Transition Probability) 도출
            if state == 0:
                hit_prob = self.brs_pct if is_break_shot else self.ts_pct
            elif state == 1:
                hit_prob = min(0.90, self.ts_pct + 0.02)
            elif state == 2:
                hit_prob = min(0.95, self.ts_pct + 0.02 + (self.five_hs_pct * 0.4))
                
            # 2. 전이 판별 (Hit vs Miss)
            if random.random() < hit_prob:
                # 득점 시 뱅크샷 여부에 따라 상태 전이 다르게 처리
                if random.random() < self.bs_pct:
                    points += 2
                    state = 1 # 뱅크샷 후엔 공이 흩어지므로 '몰입 흐름'이 끊기고 '일반 흐름'으로 회귀
                else:
                    points += 1
                    state = 2 if points >= 4 else 1 # 4득점 이상이면 '장타 흐름'으로 전이
            else:
                state = 3 # 미스 발생 -> 턴 종료 상태로 전이
                
        return points

    def play_shootout(self, is_first_turn):
        # 승부치기는 마르코프 체인을 돌리되, 승부치기 제한(PHR)과 멘탈 보정을 부여
        mental_bonus = (self.pfr - 0.5) * 0.1 if is_first_turn else (self.psr - 0.5) * 0.1
        self.ts_pct += mental_bonus
        self.brs_pct += mental_bonus
        pts = self.play_inning_markov(is_break_shot=True, is_penalty=True)
        # 보정치 원상복구
        self.ts_pct -= mental_bonus
        self.brs_pct -= mental_bonus
        return pts


def simulate_pba_match(p1, p2, target_score=15, get_log=False):
    p1_sets, p2_sets = 0, 0
    logs = []
    
    if get_log: logs.append(f"**🎱 매치 시작: [{p1.name}] vs [{p2.name}]**")

    for set_num in range(1, 5):
        p1_score, p2_score = 0, 0
        turn = 1 if set_num % 2 != 0 else 2 
        inning = 1
        if get_log: logs.append(f"\n**▶ [세트 {set_num}] (초구: {p1.name if turn == 1 else p2.name})**")

        while p1_score < target_score and p2_score < target_score:
            is_break = (inning == 1)
            if turn == 1:
                pts = p1.play_inning_markov(is_break_shot=is_break)
                p1_score += pts
                if get_log and pts > 0: logs.append(f" - {inning:2d}이닝 | {p1.name}: **{pts}득점** (누적 {min(p1_score, target_score)}점)")
                if p1_score >= target_score: p1_sets += 1; break
                turn = 2
            else:
                pts = p2.play_inning_markov(is_break_shot=is_break)
                p2_score += pts
                if get_log and pts > 0: logs.append(f" - {inning:2d}이닝 | {p2.name}: **{pts}득점** (누적 {min(p2_score, target_score)}점)")
                if p2_score >= target_score: p2_sets += 1; break
                turn = 1
                inning += 1

    if p1_sets > p2_sets:
        winner = 1
    elif p2_sets > p1_sets:
        winner = 2
    else:
        p1_is_first = random.choice([True, False])
        if get_log: logs.append(f"\n**🚨 2:2 승부치기 돌입! (선공: {p1.name if p1_is_first else p2.name})**")
        round_num = 1
        while True:
            p1_pen = p1.play_shootout(is_first_turn=p1_is_first)
            p2_pen = p2.play_shootout(is_first_turn=not p1_is_first)
            if get_log: logs.append(f" - [승부치기 {round_num}R] {p1.name} {p1_pen}점 vs {p2.name} {p2_pen}점")
            if p1_pen > p2_pen:
                winner = 1; break
            elif p2_pen > p1_pen:
                winner = 2; break
            round_num += 1

    if get_log: logs.append(f"\n🏆 **최종 승리: {p1.name if winner == 1 else p2.name}**")
    return winner, "\n".join(logs)

# ==========================================
# 3. Streamlit UI 구성
# ==========================================
st.set_page_config(page_title="PBA 마르코프 베팅 모델", page_icon="🎱", layout="wide")
st.title("🎱 PBA 마르코프 체인 승률 예측기")
st.markdown("선수의 득점 상태 전이(State Transition)와 몬테카를로 시뮬레이션을 결합한 전문 배당 예측 엔진입니다.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Player 1")
    p1_name = st.selectbox("선수 선택 (Top 25)", list(PBA_PLAYERS.keys()), index=0, key='p1_sel')
    p1_stats = PBA_PLAYERS[p1_name].copy()
    p1_stats['ELO'] = st.number_input(f"{p1_name} ELO 점수", value=p1_stats['ELO'], step=10, key='p1_elo')

with col2:
    st.subheader("Player 2")
    p2_name = st.selectbox("선수 선택 (Top 25)", list(PBA_PLAYERS.keys()), index=3, key='p2_sel')
    p2_stats = PBA_PLAYERS[p2_name].copy()
    p2_stats['ELO'] = st.number_input(f"{p2_name} ELO 점수", value=p2_stats['ELO'], step=10, key='p2_elo')

st.divider()
iter_count = st.slider("몬테카를로 시뮬레이션 반복 횟수", 1000, 20000, 10000, step=1000)

if st.button("🚀 몬테카를로 시뮬레이션 실행", use_container_width=True):
    player1 = MarkovPBAPlayer(p1_name, p1_stats, opp_elo=p2_stats['ELO'])
    player2 = MarkovPBAPlayer(p2_name, p2_stats, opp_elo=p1_stats['ELO'])
    
    st.info(f"🧠 **마르코프 모델 세팅:** ELO 점수 차이에 의해 {p1_name}의 기본 타격 확률은 **{player1.ts_pct*100:.1f}%**, {p2_name}은 **{player2.ts_pct*100:.1f}%**로 보정되었습니다.")
    
    p1_wins = 0
    progress_bar = st.progress(0)
    
    for i in range(iter_count):
        if i % (iter_count // 10) == 0: progress_bar.progress(i / iter_count)
        if simulate_pba_match(player1, player2)[0] == 1:
            p1_wins += 1
            
    progress_bar.progress(1.0)
    
    p1_win_rate = (p1_wins / iter_count) * 100
    p2_win_rate = 100 - p1_win_rate
    p1_odds = 100 / p1_win_rate if p1_win_rate > 0 else 0
    p2_odds = 100 / p2_win_rate if p2_win_rate > 0 else 0

    st.subheader("📊 산출 결과 및 적정 배당률")
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.metric(label=f"🏆 {p1_name} 승률", value=f"{p1_win_rate:.1f}%", delta=f"적정 배당: {p1_odds:.2f}배")
    with res_col2:
        st.metric(label=f"🏆 {p2_name} 승률", value=f"{p2_win_rate:.1f}%", delta=f"적정 배당: {p2_odds:.2f}배", delta_color="inverse")

    st.divider()
    st.subheader("📺 시뮬레이션 로그 샘플 (마르코프 상태 전이 확인)")
    _, sample_log = simulate_pba_match(player1, player2, get_log=True)
    with st.expander(f"{p1_name} vs {p2_name} 1경기 상세 흐름 보기", expanded=False):
        st.markdown(sample_log)
