import streamlit as st
import openai
import config as c
import time


# Constants
OTHER_PLAYER_WIDTH = 5
ACTION_WIDTH = 4
openai.api_key = st.secrets["OPENAI_API_KEY"]
ai_model = "gpt-4o" # gpt-4o is much more efficient then gpt-5
# system_message = "你扮演德州撲克GTO，我打的是六人現金桌，我會給你我的手牌、位置、籌碼，\
#                   各個玩家的位置及籌碼，以及各個玩家的行動線及籌碼，依照GTO給我各行動線的比例，\
#                   注意指需要給我比例不需要分析，例如Check(60%)、Bet1/3Pot(30%)、Bet1/2Pot(10%)。"
system_message="Act as a Texas Hold’em GTO solver for a 6-max cash game.\
                Given my hole cards, position, stack size, and the other players’ positions, stacks, and action lines,\
                output only the GTO action frequencies for my spot.\
                Output format only:\
                Action (percentage)\
                No explanations, no reasoning."

# Session state
if "Flop" not in st.session_state:
    st.session_state.Flop = False
if "Turn" not in st.session_state:
    st.session_state.Turn = False
if "River" not in st.session_state:
    st.session_state.River = False
if "positions" not in st.session_state:
    st.session_state.positions = []
if "stacks" not in st.session_state:
    st.session_state.stacks = []
if "actions" not in st.session_state:
    st.session_state.actions = {
        "Pre-Flop": {"Position": [], "Action": [], "Amount": []},
        "Flop": {"Position": [], "Action": [], "Amount": []},
        "Turn": {"Position": [], "Action": [], "Amount": []},
        "River": {"Position": [], "Action": [], "Amount": []},
    }
if "history" not in st.session_state:
    st.session_state.history = [{"role": "system", "content": system_message}]


st.title("6-MAX CASH GAME")


# Player
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
with col1:
    st.write("#### Player:")
with col2:
    player_cardrank1 = st.selectbox("Rank1", c.CARD_RANKS, index=0)
with col3:
    player_cardsuit1 = st.selectbox("Suit1", c.CARD_SUITS, index=0)
with col4:
    player_cardrank2 = st.selectbox("Rank2", c.CARD_RANKS, index=0)
with col5:
    player_cardsuit2 = st.selectbox("Suit2", c.CARD_SUITS, index=1)
with col6:
    player_position = st.selectbox("Position", c.POSITIONS, index=0)
with col7:
    player_stack = st.number_input("Stack", min_value=1, value=c.STACK, step=1)

st.write("#### Other:")
cols = st.columns(OTHER_PLAYER_WIDTH + 1)
for i, col in enumerate(cols):
    with col:
        if i == len(st.session_state.positions):
            if (
                st.button("Add", key=f"add_player_{i}")
                and len(st.session_state.positions) < OTHER_PLAYER_WIDTH
            ):
                st.session_state.positions.append(c.POSITIONS[0])
                st.session_state.stacks.append(c.STACK)
                st.rerun()
            if (
                st.button("🗑️", key=f"delete_player_{i}")
                and len(st.session_state.positions) > 0
            ):
                if len(st.session_state.positions) > 0:
                    st.session_state.positions.pop()
                    st.session_state.stacks.pop()
                    st.rerun()
        elif i < len(st.session_state.positions):
            st.session_state.positions[i] = st.selectbox(
                f"Position {i+1}", c.POSITIONS, index=0, key=f"position_{i}"
            )
            st.session_state.stacks[i] = st.number_input(
                f"Stack {i+1}", min_value=1, value=c.STACK, step=1, key=f"stack_{i}"
            )


# Community Cards
st.write("----")
st.write("#### Community Cards:")
col1, col2, col3, col4, col5 = st.columns(5)
with col2:
    if st.button("Flop"):
        st.session_state.Flop = not st.session_state.Flop
with col4:
    if st.button("Turn"):
        st.session_state.Turn = not st.session_state.Turn
with col5:
    if st.button("River"):
        st.session_state.River = not st.session_state.River

col1, col2, col3, col4, col5 = st.columns(5)
if st.session_state.Flop:
    with col1:
        flop_cardrank1 = st.selectbox("Flop Rank1", c.CARD_RANKS, index=0)
        flop_cardsuit1 = st.selectbox("Flop Suit1", c.CARD_SUITS, index=0)
    with col2:
        flop_cardrank2 = st.selectbox("Flop Rank2", c.CARD_RANKS, index=0)
        flop_cardsuit2 = st.selectbox("Flop Suit2", c.CARD_SUITS, index=1)
    with col3:
        flop_cardrank3 = st.selectbox("Flop Rank3", c.CARD_RANKS, index=0)
        flop_cardsuit3 = st.selectbox("Flop Suit3", c.CARD_SUITS, index=2)
if st.session_state.Turn:
    with col4:
        turn_cardrank = st.selectbox("Turn Rank", c.CARD_RANKS, index=0)
        turn_cardsuit = st.selectbox("Turn Suit", c.CARD_SUITS, index=3)
if st.session_state.River:
    with col5:
        river_cardrank = st.selectbox("River Rank", c.CARD_RANKS, index=0)
        river_cardsuit = st.selectbox("River Suit", c.CARD_SUITS, index=0)


# Actions
st.write("----")
st.write("#### Actions:")
for j in range(len(c.STEPS)):
    cols = st.columns(ACTION_WIDTH + 2)
    for i, col in enumerate(cols):
        with col:
            if i == 0:
                st.write(f"#### {c.STEPS[j]}:")
            elif i == len(st.session_state.actions[c.STEPS[j]]["Position"]) + 1:
                if (
                    st.button("Add", key=f"add_action_{c.STEPS[j]}_{i}")
                    and len(st.session_state.actions[c.STEPS[j]]["Position"])
                    < ACTION_WIDTH
                ):
                    st.session_state.actions[c.STEPS[j]]["Position"].append(
                        c.POSITIONS[0]
                    )
                    st.session_state.actions[c.STEPS[j]]["Action"].append(c.ACTIONS[0])
                    st.session_state.actions[c.STEPS[j]]["Amount"].append(c.STACK)
                    st.rerun()
                if (
                    st.button("🗑️", key=f"delete_action_{c.STEPS[j]}_{i}")
                    and len(st.session_state.actions[c.STEPS[j]]["Position"]) > 0
                ):
                    st.session_state.actions[c.STEPS[j]]["Position"].pop()
                    st.session_state.actions[c.STEPS[j]]["Action"].pop()
                    st.session_state.actions[c.STEPS[j]]["Amount"].pop()
                    st.rerun()

            elif i <= len(st.session_state.actions[c.STEPS[j]]["Position"]):
                st.session_state.actions[c.STEPS[j]]["Position"][i - 1] = st.selectbox(
                    f"Position {i}",
                    c.POSITIONS,
                    index=0,
                    key=f"action_{c.STEPS[j]}_Position_{i}",
                )
                st.session_state.actions[c.STEPS[j]]["Action"][i - 1] = st.selectbox(
                    f"Action {i}",
                    c.ACTIONS,
                    index=0,
                    key=f"action_{c.STEPS[j]}_Action_{i}",
                )
                st.session_state.actions[c.STEPS[j]]["Amount"][i - 1] = st.number_input(
                    f"Amount {i}",
                    min_value=0,
                    value=0,
                    step=1,
                    key=f"action_{c.STEPS[j]}_Amount_{i}",
                )


# AI Suggestions
st.write("----")
player_words = f"{player_position} {player_cardrank1}{player_cardsuit1}{player_cardrank2}{player_cardsuit2}({player_stack})"
for i in range(len(st.session_state.positions)):
    player_words += f", {st.session_state.positions[i]}({st.session_state.stacks[i]})"

preflop_words = ""
for i in range(len(st.session_state.actions["Pre-Flop"]["Position"])):
    if st.session_state.actions["Pre-Flop"]["Action"][i] == "Bet":
        preflop_words += f", {st.session_state.actions['Pre-Flop']['Position'][i]} Bet {st.session_state.actions['Pre-Flop']['Amount'][i]}"
    else:
        preflop_words += f", {st.session_state.actions['Pre-Flop']['Position'][i]} {st.session_state.actions['Pre-Flop']['Action'][i]}, "

flop_words = ""
if st.session_state.Flop:
    flop_words += f", flop {flop_cardrank1}{flop_cardsuit1}{flop_cardrank2}{flop_cardsuit2}{flop_cardrank3}{flop_cardsuit3}"
    for i in range(len(st.session_state.actions["Flop"]["Position"])):
        if st.session_state.actions["Flop"]["Action"][i] == "Bet":
            flop_words += f", {st.session_state.actions['Flop']['Position'][i]} Bet {st.session_state.actions['Flop']['Amount'][i]}"
        else:
            flop_words += f", {st.session_state.actions['Flop']['Position'][i]} {st.session_state.actions['Flop']['Action'][i]}"

turn_words = ""
if st.session_state.Turn:
    turn_words += f", turn {turn_cardrank}{turn_cardsuit}"
    for i in range(len(st.session_state.actions["Turn"]["Position"])):
        if st.session_state.actions["Turn"]["Action"][i] == "Bet":
            turn_words += f", {st.session_state.actions['Turn']['Position'][i]} Bet {st.session_state.actions['Turn']['Amount'][i]}"
        else:
            turn_words += f", {st.session_state.actions['Turn']['Position'][i]} {st.session_state.actions['Turn']['Action'][i]}"

river_words = ""
if st.session_state.River:
    river_words += f", river {river_cardrank}{river_cardsuit}"
    for i in range(len(st.session_state.actions["River"]["Position"])):
        if st.session_state.actions["River"]["Action"][i] == "Bet":
            river_words += f", {st.session_state.actions['River']['Position'][i]} Bet {st.session_state.actions['River']['Amount'][i]}"
        else:
            river_words += f", {st.session_state.actions['River']['Position'][i]} {st.session_state.actions['River']['Action'][i]}"

words = f"\n{player_words}{preflop_words}{flop_words}{turn_words}{river_words}"
st.markdown(f"目前牌局：\n{words}")

col1, col2 = st.columns([1, 5])
with col1:
    if st.button("打法建議"):
        st.session_state.history.append({"role": "user", "content": words})

        with st.spinner("計算中..."):
            response = openai.chat.completions.create(
                model=ai_model,
                messages=st.session_state.history,
            )
            time.sleep(1)

        assistant_message = response.choices[0].message.content
        st.session_state.history.append(
            {"role": "assistant", "content": assistant_message}
        )
        st.rerun()
with col2:
    if st.button("🗑️"):
        st.session_state.history = [{"role": "system", "content": system_message}]
        st.rerun()

for message in st.session_state.history:
    if message["role"] == "user":
        st.chat_message("user", avatar="🃏").write(message["content"])
    if message["role"] == "assistant":
        st.chat_message("assistant", avatar="✨").write(message["content"])
