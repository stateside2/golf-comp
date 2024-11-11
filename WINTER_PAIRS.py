
import pandas as pd
import streamlit as st
import streamlit_antd_components as sac


excel_file: str = "data/WINTER.xlsx"
week = 5 #--- USED IN "Week 1/24" LABEL AND AVG. POINTS CALCULATION



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
    	# sac.ButtonsItem(label="Weekly Winners", icon="person-circle"),
    	sac.ButtonsItem(label="Handicaps", icon="activity"),
    	sac.ButtonsItem(label="Full Table", icon="table"),
], label="Week " + str(week) + "/24 - Winter Pairs", format_func=None, align="center", size="md", radius="md", color="#598506", use_container_width=True)
# ---



# --- PANDAS DATA FRAME CREATION ---
df_golf_tab = pd.read_excel(excel_file, skiprows=[0,1,3,2,4,5,6,7,8,9,31,32,33,34,35,36,37,38], sheet_name='Sheet1', usecols=[0,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28])
df_golf_tab = df_golf_tab.fillna(value="")


df_handi_tab = pd.read_excel(excel_file, sheet_name="HANDICAPS", usecols=[0,1])
df_handi_tab = df_handi_tab.sort_values(by=["HANDICAP", "NAME"], ascending=[True, True])
df_handi_tab.insert(0, "POSITION", range(1, 1 + len(df_handi_tab)))


# --- FUNCTION TO CREATE A LIST OF WEEKS: ['WK 1', 'WK 2', 'WK 3', etc...]
# --- THIS IS USED IN CALCULATION FOR THE BEST 8 SCORES
def week_list_func(final_week):
	week_list = []
	week = 1
	while week <= final_week:
		week_list.append("WK "+str(week))
		week = week + 1
	return week_list
week_list = week_list_func(24)



week_win_list = df_golf_tab["WK 1"].tolist()


# def weekly_win_func():
# 	week_win_list = []
# 	for i in range(23):
# 		week_win_list = df_golf_tab.loc[(WK1), week_list].values.tolist()


# df_weekly_tab = week_list


def best_8_func(no_of_players):
	# global df_lead_list
	best_8_list = []
	player_no = 1
	while player_no <= no_of_players:
		df_lead_list = df_golf_tab.loc[(player_no - 1), week_list].values.tolist()
		df_lead_list = list(filter(None,df_lead_list))  #--- REMOVES THE NULL VALUES IN THE LIST (SO ONLY INTEGERS ARE REMAIN)
		best_8 = pd.Series(df_lead_list).nlargest(8).sum()
		best_8_list.append(best_8)
		player_no = player_no + 1
	return best_8_list

best_8_list = best_8_func(20)
# print(len(df_lead_list))



df_indv_tab = pd.read_excel(excel_file, skiprows=[0,1,3,2,4,5,6,7,8,9,31,32,33,34,35,36,37,38], sheet_name='Sheet1', usecols=[0,30])
df_indv_tab["BEST 8 TOTAL"] = best_8_list
# INCLUDE A COLUMN (FROM A LIST) HERE WITH THE COUNT OF NOT NULL VALUES. FILTER for None, THEN LEN() THE LIST
# USE IT WHEN CALCULATING THE AVERAGE. 
df_indv_tab["AVG"] = df_indv_tab["BEST 8 TOTAL"]/df_indv_tab["RNDS PLAYED"]
df_indv_tab = df_indv_tab.sort_values(by=["BEST 8 TOTAL", "NAME"], ascending=[False, True])
df_indv_tab.insert(0, "POSITION", range(1, 1 + len(df_indv_tab)))
df_indv_tab["DELTA"] = df_indv_tab["BEST 8 TOTAL"] - max(df_indv_tab["BEST 8 TOTAL"])
df_indv_tab.loc[df_indv_tab["DELTA"] == 0, "DELTA"] = None
df_indv_tab = df_indv_tab.style.format({"AVG": "{:.2f}", "BEST 8 TOTAL": "{:.0f}", "DELTA": "{:.0f}"})



def team_best_8_func(no_of_players):
	team_best_8 = []
	player_no = 1
	while player_no <= no_of_players:
		team_best_8.append(best_8_list[player_no - 1] + best_8_list[player_no])
		player_no = player_no + 2
	return team_best_8

team_best_8 = team_best_8_func(20)



df_team_tab = pd.read_excel(excel_file, skiprows=None, sheet_name='xxDO NOT EDITxx', usecols=[0,1])
df_team_tab["BEST 16 TOTAL"] = team_best_8
df_team_tab["AVG"] = df_team_tab["BEST 16 TOTAL"]/df_team_tab["PLAYED"]
df_team_tab = df_team_tab.sort_values(by=["BEST 16 TOTAL", "TEAM"], ascending=[False, True])
df_team_tab.insert(0, "POSITION", range(1, 1 + len(df_team_tab)))
df_team_tab["DELTA"] = df_team_tab["BEST 16 TOTAL"] - max(df_team_tab["BEST 16 TOTAL"])
df_team_tab.loc[df_team_tab["DELTA"] == 0, "DELTA"] = None
df_team_tab = df_team_tab.style.format({"AVG": "{:.2f}", "BEST 16 TOTAL": "{:.0f}", "DELTA": "{:.0f}"})



# df_lead_list = df_golf_tab.loc[0, week_list].values.tolist()
# df_lead_list = list(filter(None,df_lead_list))  #--- REMOVES THE NULL VALUES IN THE LIST (SO ONLY INTEGERS ARE REMAIN)
# best_8 = pd.Series(df_lead_list).nlargest(8).sum()

# print(df_lead_list)
# print(best_8)


# -----------

if menu_selection == "Team Leaderboard":
	st.dataframe(df_team_tab, width=None, height=388, use_container_width=True, hide_index=True, column_order=("POSITION","TEAM","PLAYED","AVG","BEST 16 TOTAL","DELTA"), column_config={"POSITION": " ", "PLAYED": "RNDS PLAYED", "DELTA": " "})

if menu_selection == "Individual Leaderboard":
	st.dataframe(df_indv_tab, width=None, height=738, use_container_width=True, hide_index=True, column_order=("POSITION","NAME","RNDS PLAYED","AVG","BEST 8 TOTAL","DELTA"), column_config={"POSITION": " ", "DELTA": " "})

# if menu_selection == "Weekly Winners":
# 	st.dataframe(df_weekly_tab, width=None, height=738, use_container_width=True, hide_index=True)

if menu_selection == "Handicaps":
	st.dataframe(df_handi_tab, width=None, height=738, use_container_width=True, hide_index=True, column_config={"POSITION": " "})

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

