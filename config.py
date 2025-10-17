import streamlit as st

CARD_RANKS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
CARD_SUITS = ["♠️", "♥️", "♦️", "♣️"]
POSITIONS = ["UTG", "MP", "CO", "BTN", "SB", "BB"]
STEPS = ["Pre-Flop", "Flop", "Turn", "River"]
ACTIONS = ["Check", "Bet", "Call"]
STACK = 100

PAGES = [
    st.Page("pages/home.py", title="首頁", icon="🏠", default = True),
    st.Page("pages/six_max_cashgame.py", title="六人現金桌", icon="🃏"),
]