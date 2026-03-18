import streamlit as st
import random
import time

# ==========================================
# 1. PBA 선수 데이터베이스 (Top 25)
# ==========================================
PBA_PLAYERS = {
    "산체스": {"TS%": 63.4, "BS%": 18.0, "HR": 15, "BRS%": 78.8, "5HS%": 9.9, "PHR": 3, "PFR": 100.0, "PSR": 0.0},
    "마민껌": {"TS%": 60.1, "BS%": 24.6, "HR": 14, "BRS%": 65.8, "5HS%": 9.9, "PHR": 3, "PFR": 66.7, "PSR": 33.3},
    "모리": {"TS%": 60.6, "BS%": 28.7, "HR": 14, "BRS%": 75.8, "5HS%": 10.5, "PHR": 6, "PFR": 66.7, "PSR": 0.0},
    "조재호": {"TS%": 63.8, "BS%": 20.9, "HR": 13, "BRS%": 81.9, "5HS%": 11.4, "PHR": 4, "PFR": 0.0, "PSR": 75.0},
    "마르티네스": {"TS%": 62.7, "BS%": 28.3, "HR": 13, "BRS%": 75.4, "5HS%": 11.2, "PHR": 1, "PFR": 50.0, "PSR": 100.0},
    "이승진": {"TS%": 58.1, "BS%": 24.5, "HR": 14, "BRS%": 65.3, "5HS%": 8.6, "PHR": 5, "PFR": 71.4, "PSR": 50.0},
    "최성원": {"TS%": 60.3, "BS%": 25.7, "HR": 11, "BRS%": 77.9, "5HS%": 10.2, "PHR": 5, "PFR": 100.0, "PSR": 0.0},
    "김영원": {"TS%": 61.6, "BS%": 21.0, "HR": 13, "BRS%": 54.7, "5HS%": 9.6, "PHR": 0, "PFR": 0.0, "PSR": 0.0},
    "레펀스": {"TS%": 61.8, "BS%": 20.0, "HR": 13, "BRS%": 61.9, "5HS%": 10.1, "PHR": 5, "PFR": 75.0, "PSR": 0.0},
    "김재근": {"TS%": 58.4, "BS%": 25.8, "HR": 13, "BRS%": 60.7, "5HS%": 8.9, "PHR": 7, "PFR": 83.3, "PSR": 100.0},
    "강동궁": {"TS%": 63.5, "BS%": 24.9, "HR": 14, "BRS%": 69.6, "5HS%": 11.5, "PHR": 1, "PFR": 50.0, "PSR": 0.0},
    "Q.응우옌": {"TS%": 61.3, "BS%": 24.6, "HR": 12, "BRS%": 67.2, "5HS%": 10.3, "PHR": 6, "PFR": 50.0, "PSR": 0.0},
    "D.응우옌": {"TS%": 58.0, "BS%": 23.2, "HR": 12, "BRS%": 61.7, "5HS%": 7.9, "PHR": 4, "PFR": 75.0, "PSR": 80.0},
    "응오": {"TS%": 62.2, "BS%": 20.6, "HR": 15, "BRS%": 65.5, "5HS%": 9.8, "PHR": 1, "PFR": 50.0, "PSR": 0.0},
    "모랄레스": {"TS%": 60.7, "BS%": 19.4, "HR": 11, "BRS%": 77.6, "5HS%": 8.8, "PHR": 3, "PFR": 100.0, "PSR": 100.0},
    "사파타": {"TS%": 60.4, "BS%": 21.1, "HR": 12, "BRS%": 78.6, "5HS%": 8.1, "PHR": 4, "PFR": 33.3, "PSR": 66.7},
    "조건휘": {"TS%": 61.1, "BS%": 23.8, "HR": 11, "BRS%": 74.1, "5HS%": 9.1, "PHR": 3, "PFR": 33.3, "PSR": 0.0},
    "이충복": {"TS%": 61.6, "BS%": 24.6, "HR": 14, "BRS%": 66.7, "5HS%": 9.7, "PHR": 3, "PFR": 100.0, "PSR": 50.0},
    "초클루": {"TS%": 59.6, "BS%": 27.7, "HR": 13, "BRS%": 72.1, "5HS%": 9.1, "PHR": 5, "PFR": 50.0, "PSR": 33.3},
    "사이그너": {"TS%": 60.5, "BS%": 21.8, "HR": 13, "BRS%": 62.5, "5HS%": 9.9, "PHR": 6, "PFR": 100.0, "PSR": 50.0},
    "체네트": {"TS%": 61.5, "BS%": 21.7, "HR": 13, "BRS%": 66.1, "5HS%": 10.8, "PHR": 2, "PFR": 50.0, "PSR": 0.0},
    "김임권": {"TS%": 58.1, "BS%": 26.9, "HR": 13, "BRS%": 58.9, "5HS%": 7.9, "PHR": 5, "PFR": 100.0, "PSR": 0.0},
    "김종원": {"TS%": 58.3, "BS%": 25.9, "HR": 11, "BRS%": 67.9, "5HS%": 8.0, "PHR": 4, "PFR": 0.0, "PSR": 100.0},
    "엄상필": {"TS%": 58.0, "BS%": 23.5, "HR": 14, "BRS%": 64.8, "5HS%": 8.3, "PHR": 2, "PFR": 0.0, "PSR": 50.0},
    "팔라손": {"TS%": 59.5, "BS%": 26.2, "HR": 14, "BRS%": 64.2, "5HS%": 10.4, "PHR": 4, "PFR": 66.7, "PSR": 100.0}
}

# ==========================================
# 2. 마르코프 체인 시뮬레이션 클래스
# ==========================================
class MarkovPBAPlayer:
    def __init__(self, name, stats):
        self.name = name
        self.ts_pct = stats['TS%'] / 100
        self.brs_pct = stats['BRS%'] / 100
        self.bs_pct = stats['BS%'] / 100
        self.hr = int(stats['HR'])
        self.five_hs_pct = stats['5HS%'] / 100
        self.phr = int(stats['PHR'])
        self.pfr = stats['PFR'] / 100
        self.psr = stats['PSR'] / 100

    def play_inning_markov(self, is_break_shot=False, is_penalty=False):
        """마르코프 체인(Markov Chain) 상태 전이 모델 적용"""
        state = 0
        points = 0
        max_cap = self.phr if is_penalty else self.hr
        
        while state != 3 and points < max_cap:
            if state == 0:
                hit_prob = self.brs_pct if is_break_shot else self.ts_pct
            elif state == 1:
                hit_prob = min(0.90, self.ts_pct + 0.02)
            elif state == 2:
                hit_prob = min(0.95, self.ts_pct + 0.02 + (self.five_hs_pct * 0.4))
                
            if random.random() < hit_prob:
                if random.random() < self.bs_pct:
                    points += 2
                    state = 1 
                else:
                    points += 1
                    state = 2 if points >= 4 else 1 
            else:
                state = 3 
                
        return points

    def play_shootout(self, is_first_turn):
        # 승부치기는 선공/후공 데이터(PFR, PSR)로 심리적 보정
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
st.set_page_config(page_title="PBA 예측 엔진", page_icon="🎱", layout="wide")
st.title("🎱 PBA 경기 승률 예측기 (마르코프 모델)")
st.markdown("PBA 공식 기록을 기반으로 선수의 **모멘텀(상태 전이)**과 **물리적 스탯**을 결합하여 실제 경기를 정밀하게 시뮬레이션합니다.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Player 1")
    p1_name = st.selectbox("선수 선택 (Top 25)", list(PBA_PLAYERS.keys()), index=0, key='p1_sel')
    p1_stats = PBA_PLAYERS[p1_name].copy()
    
with col2:
    st.subheader("Player 2")
    p2_name = st.selectbox("선수 선택 (Top 25)", list(PBA_PLAYERS.keys()), index=3, key='p2_sel')
    p2_stats = PBA_PLAYERS[p2_name].copy()

st.divider()
iter_count = st.slider("몬테카를로 시뮬레이션 반복 횟수", 1000, 20000, 10000, step=1000)

if st.button("🚀 예측 시뮬레이션 실행", use_container_width=True):
    player1 = MarkovPBAPlayer(p1_name, p1_stats)
    player2 = MarkovPBAPlayer(p2_name, p2_stats)
    
    st.info(f"🧠 시뮬레이션 엔진 구동 중... ({iter_count:,}경기 분량 연산)")
    
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
