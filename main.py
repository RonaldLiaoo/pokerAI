import streamlit as st
import config as c

pg = st.navigation(c.PAGES)
pg.run()