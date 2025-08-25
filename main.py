import streamlit as st

st.title("POKER AI")

st.markdown(
    """
歡迎使用 **Poker AI GTO**！  
這是一個基於 OpenAI API 的德州撲克 GTO 輔助工具，  
能夠根據你的手牌、位置、籌碼與行動線，給出 GTO 行動比例建議。  

---

### 📖 使用教學

1. 進入左側選單，選擇遊玩模式 
2. 輸入你的 **手牌**（Rank + Suit）  
3. 選擇你的 **位置**(Position) 與 **籌碼量**(Stack)
4. 新增其他玩家的 **位置** 與 **籌碼**  
5. 根據牌局進行(Community Cards)，設定 **公共牌 (Flop / Turn / River)**  
6. 新增每個玩家的 **行動線** (Check, Bet...)  
7. 點擊 **打法建議**，系統將給出對應的 **GTO 建議比例**

---

### ⚙️ 注意事項
- 請先在 `.streamlit/secrets.toml` 中設定你的 OpenAI API Key  
- 本工具僅提供 **輔助學習**，實際牌局請自行判斷
- **本工具不提倡任何形式的賭博行為**，請勿將此程式用於真實金錢下注

---

### 📸 位置示意圖

"""
)

st.image("images/Positions.png", caption="六人位置圖", use_container_width=True)
