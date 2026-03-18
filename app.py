import streamlit as st
import random
import time

# ==========================================
# 1. PBA 선수 데이터베이스
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
    "강동궁": {"TS%": 63.5, "BS%": 24.9, "HR": 14, "BRS%": 69.6, "5HS%": 11.5, "PHR": 1, "PFR": 50.0, "PSR": 0.0}
}

# ==========================================
# 2. 시뮬레이션 클래스 및 함수 (웹용 로그 반환 구조)
# ==========================================
class PBAOfficialPlayer:
    def __init__(self, name, stats):
        self.name = name
        self.ts_pct = stats['TS%'] / 100
        self.bs_pct = stats['BS%'] / 100
        self.hr = int(stats['HR'])
        self.brs_pct = stats['BRS%'] / 100
        self.five_hs_pct = stats['5HS%'] / 100
        self.phr = int(stats['PHR'])
        self.pfr = stats['PFR'] / 100
        self.psr = stats['PSR'] / 100

    def play_inning(self, is_break_shot=False):
        points = 0
        current_prob = self.brs_pct if is_break_shot else self.ts_pct
        while random.random() < current_prob and points < self.hr:
            if random.random() < self.bs_pct:
                points += 2
                current_prob = self.ts_pct
            else:
                points += 1
                current_prob = min(0.90, self.ts_pct + 0.02)
            if points >= 4:
                current_prob = min(0.95, current_prob + (self.five_hs_pct * 0.4))
        return points

    def play_shootout(self, is_first_turn):
        mental_bonus = (self.pfr - 0.5) * 0.1 if is_first_turn else (self.psr - 0.5) * 0.1
        points = 0
        current_prob = min(0.95, max(0.1, self.brs_pct + mental_bonus))
        while random.random() < current_prob and points < self.phr:
            if random.random() < self.bs_pct:
                points += 2
                current_prob = self.ts_pct + mental_bonus
            else:
                points += 1
                current_prob = self.ts_pct + mental_bonus + 0.02
        return points

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
                pts = p1.play_inning(is_break_shot=is_break)
                p1_score += pts
                if get_log and pts > 0: logs.append(f" - {inning:2d}이닝 | {p1.name}: **{pts}득점** (누적 {min(p1_score, target_score)}점)")
                if p1_score >= target_score: p1_sets += 1; break
                turn = 2
            else:
                pts = p2.play_inning(is_break_shot=is_break)
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
                winner = 1
                break
            elif p2_pen > p1_pen:
                winner = 2
                break
            round_num += 1

    if get_log: logs.append(f"\n🏆 **최종 승리: {p1.name if winner == 1 else p2.name}**")
    
    return winner, "\n".join(logs)

# ==========================================
# 3. Streamlit UI 렌더링
# ==========================================
st.set_page_config(page_title="PBA 승률 예측기", page_icon="🎱", layout="wide")
st.title("🎱 PBA 승률 예측 시뮬레이터")
st.markdown("선수를 선택하고 스탯을 조절하여 **가상 매치업의 승률과 적정 배당률**을 확인하세요.")

# 선수 선택 및 스탯 조절 UI
col1, col2 = st.columns(2)

with col1:
    st.subheader("Player 1")
    p1_name = st.selectbox("선수 선택", list(PBA_PLAYERS.keys()), index=0, key='p1_sel')
    p1_stats = PBA_PLAYERS[p1_name].copy()
    
    with st.expander(f"🛠️ {p1_name} 스탯 미세조정"):
        p1_stats['TS%'] = st.slider("공격성공률 (TS%)", 0.0, 100.0, p1_stats['TS%'], key='p1_ts')
        p1_stats['BS%'] = st.slider("뱅크샷 비율 (BS%)", 0.0, 50.0, p1_stats['BS%'], key='p1_bs')
        p1_stats['BRS%'] = st.slider("초구 성공률 (BRS%)", 0.0, 100.0, p1_stats['BRS%'], key='p1_brs')
        p1_stats['5HS%'] = st.slider("장타율 (5HS%)", 0.0, 30.0, p1_stats['5HS%'], key='p1_5hs')

with col2:
    st.subheader("Player 2")
    # P1과 다른 선수를 기본값으로 선택
    p2_name = st.selectbox("선수 선택", list(PBA_PLAYERS.keys()), index=3, key='p2_sel')
    p2_stats = PBA_PLAYERS[p2_name].copy()
    
    with st.expander(f"🛠️ {p2_name} 스탯 미세조정"):
        p2_stats['TS%'] = st.slider("공격성공률 (TS%)", 0.0, 100.0, p2_stats['TS%'], key='p2_ts')
        p2_stats['BS%'] = st.slider("뱅크샷 비율 (BS%)", 0.0, 50.0, p2_stats['BS%'], key='p2_bs')
        p2_stats['BRS%'] = st.slider("초구 성공률 (BRS%)", 0.0, 100.0, p2_stats['BRS%'], key='p2_brs')
        p2_stats['5HS%'] = st.slider("장타율 (5HS%)", 0.0, 30.0, p2_stats['5HS%'], key='p2_5hs')

st.divider()

# 시뮬레이션 설정 및 실행
iter_count = st.slider("시뮬레이션 반복 횟수 (횟수가 많을수록 정교해집니다)", 1000, 20000, 10000, step=1000)

if st.button("🚀 시뮬레이션 실행", use_container_width=True):
    player1 = PBAOfficialPlayer(p1_name, p1_stats)
    player2 = PBAOfficialPlayer(p2_name, p2_stats)
    
    p1_wins = 0
    
    # 진행 상태 바
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(iter_count):
        # UI 업데이트 최적화를 위해 10%마다 렌더링
        if i % (iter_count // 10) == 0:
            progress_bar.progress(i / iter_count)
            status_text.text(f"연산 중... ({i}/{iter_count})")
            
        winner, _ = simulate_pba_match(player1, player2, get_log=False)
        if winner == 1:
            p1_wins += 1
            
    progress_bar.progress(1.0)
    status_text.text("✅ 시뮬레이션 완료!")
    time.sleep(0.5)
    progress_bar.empty()
    status_text.empty()
    
    # 결과 계산
    p1_win_rate = (p1_wins / iter_count) * 100
    p2_win_rate = 100 - p1_win_rate
    
    p1_odds = 100 / p1_win_rate if p1_win_rate > 0 else 0
    p2_odds = 100 / p2_win_rate if p2_win_rate > 0 else 0

    # 결과 UI 표시
    st.subheader("📊 시뮬레이션 결과")
    res_col1, res_col2 = st.columns(2)
    
    with res_col1:
        st.metric(label=f"🏆 {p1_name} 승률", value=f"{p1_win_rate:.1f}%", delta=f"적정 배당: {p1_odds:.2f}배")
    with res_col2:
        st.metric(label=f"🏆 {p2_name} 승률", value=f"{p2_win_rate:.1f}%", delta=f"적정 배당: {p2_odds:.2f}배", delta_color="inverse")

    st.divider()
    
    # 가상 경기 1게임 중계 로그 보여주기
    st.subheader("📺 가상 매치 샘플 (1게임 중계 로그)")
    _, sample_log = simulate_pba_match(player1, player2, get_log=True)
    with st.expander("경기 상세 로그 보기", expanded=False):
        st.markdown(sample_log)
