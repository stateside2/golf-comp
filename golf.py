
import pandas as pd
import streamlit as st
import streamlit_antd_components as sac


excel_file: str = "data/WINTER.xlsx"
week = 3 #--- USED IN "Week 1/24" LABEL AND AVG. POINTS CALCULATION


st.set_page_config(page_title="Winter Best Pairs", page_icon="images/golf.png", layout="centered", initial_sidebar_state="auto", menu_items=None)

# --- HIDE 1) STREAMLIT HEADER/FOOTER MENUS, 2) POP-UP DOWNLOAD, SEARCH, EXPAND DATAFRAME ELEMENTS, 3) EXPAND IMAGE  ---
hide_st_style = """ 
	<style>MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;} 
	[data-testid="stElementToolbar"] {display: none;} 
	button[title="View fullscreen"] {visibility: hidden;} 
	</style>
	"""
st.markdown(hide_st_style, unsafe_allow_html=True)
# ----


# --- BANNER IMAGE
st.image("images/golf_banner.png", use_column_width="auto")
st.divider()


menu_selection = sac.buttons(
   items=[
    	sac.ButtonsItem(label="Team Leaderboard", icon="trophy-fill"),
    	sac.ButtonsItem(label="Individual Leaderboard", icon="person-arms-up"),
    	sac.ButtonsItem(label="Full Table", icon="table"),
], label="Week " + str(week) + "/24", format_func=None, align="center", size="md", radius="md", color="#598506", use_container_width=True)
# ---


# --- PANDAS DATA FRAME CREATION ---
df_lead_tab = pd.read_excel(excel_file, skiprows=None, sheet_name='xxDO NOT EDITxx', usecols=[0,1])
df_lead_tab["AVERAGE"] = df_lead_tab["TEAM TOTAL"]/week
df_lead_tab = df_lead_tab.sort_values(by=["TEAM TOTAL", "TEAM"], ascending=[False, True])
df_lead_tab.insert(0, "POSITION", range(1, 1 + len(df_lead_tab)))
df_lead_tab = df_lead_tab.style.format({"AVERAGE": "{:.1f}"})


df_indv_tab = pd.read_excel(excel_file, skiprows=[0,1,3,2,4,5,6,7,8,9,31,32,33,34,35,36,37,38], sheet_name='Sheet1', usecols=[0,27])
df_indv_tab["AVERAGE"] = df_indv_tab["SCORE"]/week
df_indv_tab = df_indv_tab.sort_values(by=["SCORE", "NAME"], ascending=[False, True])
df_indv_tab.insert(0, "POSITION", range(1, 1 + len(df_indv_tab)))
df_indv_tab = df_indv_tab.style.format({"AVERAGE": "{:.1f}"})


df_golf_tab = pd.read_excel(excel_file, skiprows=[0,1,3,2,4,5,6,7,8,9,31,32,33,34,35,36,37,38], sheet_name='Sheet1', usecols=[0,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28])
df_golf_tab = df_golf_tab.fillna(value="")


# -----------

if menu_selection == "Team Leaderboard":
	st.dataframe(df_lead_tab, width=None, height=388, use_container_width=True, hide_index=True, column_order=("POSITION","TEAM","TEAM TOTAL"), column_config={"POSITION": " ","AVERAGE": "BEST 8 AVG", "TEAM TOTAL": "BEST 8 TOTAL"})

if menu_selection == "Individual Leaderboard":
	st.dataframe(df_indv_tab, width=None, height=738, use_container_width=True, hide_index=True, column_order=("POSITION","NAME","SCORE"), column_config={"POSITION": " ","AVERAGE": "BEST 8 AVG", "SCORE": "BEST 8 TOTAL"})

if menu_selection == "Full Table":
	st.dataframe(df_golf_tab, width=None, height=738, use_container_width=True, hide_index=True, column_config={"NAME": " ","Unnamed: 28": "TEAM SCORE"})

st.divider()

# --- FUTURE ADDITIONS
# st.markdown("##")
# st.snow() # --- WINTER / XMAS UPDATE --- DOES IT WORK ON CELLPHONE?
# st.balloons() # --- END OF SEASON CELEBRATION --- DOES IT WORK ON CELLPHONE?
# st.toast("xxxxxxx is the winner", icon="🔥") # --- WINNER ANNOUNCEMENT --- DOES IT WORK ON CELLPHONE?
# time.sleep(1) --- ALSO HAVE TO import time
# POSSIBLE ICONS = [🔥, 🚨, 💩, 💥, 🔆, 😎, 😖, 😟, 🥇, 🏅, ☠️, ⚠️, ⚽, ⭐, 💯, ✅, ❗, 🏆]

# st.title("Title Marlow Dukes") --- st.header("This is a header") --- st.subheader("Sub Header") --- st.markdown("data correct as of ...")

