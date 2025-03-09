
import pandas as pd
import streamlit as st
import streamlit_antd_components as sac
import sys
from variables import *


# --- SETTING THE PYTHON PATH SO THAT VARIABLES CAN BE IMPORTED FROM variables.py
sys.path.insert(0, "../")


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
st.image("images/golf_banner_thurs.png", use_container_width="auto")
st.divider()


menu_selection = sac.buttons(
   items=[
    	sac.ButtonsItem(label="Individual Leaderboard", icon="person-arms-up"),
    	sac.ButtonsItem(label="Weekly Winners", icon="person-circle"),
    	sac.ButtonsItem(label="Handicaps", icon="activity"),
    	sac.ButtonsItem(label="Full Table", icon="table"),
], label="Week " + str(week_thurs) + "/24 - Thursday Singles", format_func=None, align="center", size="md", radius="md", color="#598506", use_container_width=True)
# ---


# --- PANDAS DATA FRAME CREATION ---
df_golf_tab = pd.read_excel(excel_file, skiprows=[0,1,2,19,20,21,22,23,24,25,26,27], sheet_name="THURSDAY SINGLES", usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25])
df_golf_tab = df_golf_tab.fillna(0)





# --- FUNCTION TO CREATE A LIST OF WEEKS: ['WK 1', 'WK 2', 'WK 3', etc...]
# --- THIS IS USED IN CALCULATION FOR THE BEST 8 SCORES
def week_list_func(final_week):
	week_list = []
	week_thurs = 1
	while week_thurs <= final_week:
		week_list.append("WK "+str(week_thurs))
		week_thurs = week_thurs + 1
	return week_list
week_list = week_list_func(24)


# -------------------

def week_winners_thurs_func(no_of_weeks):
	week_win_list_thurs = []
	week_score_list_thurs = []
	round_week = 1
	while round_week <= no_of_weeks:
		if round_week <= week_thurs:  # --- IF THE WEEK HAS BEEN PLAYED (AND THEREFORE HAS AN ACTUAL WINNER)
			if round_week == 15:
				week_winner_thurs = None
				week_winner_score_thurs = None
			else:
				if round_week == 9:
					week_winner_thurs = "TONY SLATER"
					week_winner_score_thurs = 36
				else:
					if round_week == 12:
						week_winner_thurs = "STEW TAYLOR"
						week_winner_score_thurs = 38
					else:
						# --- BOTH THESE week_winner_thurs STATEMENTS DO THE SAME THING. item() IS NEEDED TO EXTRACT JUST THE NAME FROM THE OUTPUT
						# week_winner_thurs = df_golf_tab["NAME"][df_golf_tab["WK "+str(round_week)]==df_golf_tab["WK "+str(round_week)].max()].item()
						week_winner_thurs = df_golf_tab.loc[df_golf_tab["WK "+str(round_week)]==df_golf_tab["WK "+str(round_week)].max(), "NAME"].item()
						week_winner_score_thurs = df_golf_tab.loc[df_golf_tab["WK "+str(round_week)]==df_golf_tab["WK "+str(round_week)].max(), "WK "+str(round_week)].item()
		else:
			week_winner_thurs = None # --- THIS IS USED FOR THE WEEKS NOT YET PLAYED
			week_winner_score_thurs = None
		week_win_list_thurs.append(week_winner_thurs)
		week_score_list_thurs.append(week_winner_score_thurs)
		round_week = round_week + 1
	return week_win_list_thurs, week_score_list_thurs
week_win_list_thurs, week_score_list_thurs = week_winners_thurs_func(24)



week_win_thurs_data = {"WEEK": week_list, "WINNER": week_win_list_thurs, "SCORE": week_score_list_thurs}
df_weekly_thurs_tab = pd.DataFrame(week_win_thurs_data)

# df_weekly_tab = pd.DataFrame(columns = ["WEEK", "WINNER"])
# df_weekly_tab["WEEK"] = week_list
# df_weekly_tab["WINNER"] = week_win_list_thurs






def best_8_func(no_of_players):
	best_8_list = []
	player_no = 1
	while player_no <= no_of_players:
		df_lead_list = df_golf_tab.loc[(player_no - 1), week_list].values.tolist()
		df_lead_list = list(filter(None,df_lead_list))  #--- REMOVES THE NULL VALUES IN THE LIST (SO ONLY INTEGERS ARE REMAIN)
		best_8 = pd.Series(df_lead_list).nlargest(8).sum()
		best_8_list.append(best_8)
		player_no = player_no + 1
	return best_8_list
best_8_list = best_8_func(15)



df_handi_thurs_tab = pd.read_excel(excel_file, sheet_name="HANDICAPS", usecols=[0,2])
df_handi_thurs_tab = df_handi_thurs_tab.sort_values(by=["HANDICAP THURS", "NAME"], ascending=[True, True])
df_handi_thurs_tab = df_handi_thurs_tab.head(len(best_8_list))
df_handi_thurs_tab.insert(0, "POSITION", range(1, 1 + len(df_handi_thurs_tab)))



def rnds_played_func(no_of_players):
	rnds_played_list = []
	player_no = 1
	while player_no <= no_of_players:
		df_lead_list = df_golf_tab.loc[(player_no - 1), week_list].values.tolist()
		df_lead_list = list(filter(None,df_lead_list))  #--- REMOVES THE NULL VALUES IN THE LIST (SO ONLY INTEGERS ARE REMAIN)
		rnds_played_list.append(len(df_lead_list))
		player_no = player_no + 1
	return rnds_played_list
rnds_played_list = rnds_played_func(15)


df_inv_thurs_tab = pd.read_excel(excel_file, skiprows=[0,1,2,19,20,21,22,23,24,25,26,27], sheet_name="THURSDAY SINGLES", usecols=[0,25])
df_inv_thurs_tab["BEST 8 TOTAL"] = best_8_list
df_inv_thurs_tab["RNDS PLAYED"] = rnds_played_list
df_inv_thurs_tab["AVG"] = df_inv_thurs_tab["TOTAL SCORE"]/df_inv_thurs_tab["RNDS PLAYED"]
df_inv_thurs_tab = df_inv_thurs_tab.sort_values(by=["BEST 8 TOTAL", "NAME"], ascending=[False, True])
df_inv_thurs_tab.insert(0, "POSITION", range(1, 1 + len(df_inv_thurs_tab)))
df_inv_thurs_tab["DELTA"] = df_inv_thurs_tab["BEST 8 TOTAL"] - max(df_inv_thurs_tab["BEST 8 TOTAL"])
df_inv_thurs_tab.loc[df_inv_thurs_tab["DELTA"] == 0, "DELTA"] = None
df_inv_thurs_tab = df_inv_thurs_tab.style.format({"AVG": "{:.2f}", "BEST 8 TOTAL": "{:.0f}", "DELTA": "{:.0f}"})


# -----------
if menu_selection == "Individual Leaderboard":
	st.dataframe(df_inv_thurs_tab, width=None, height=592, use_container_width=True, hide_index=True, column_order=("POSITION","NAME","RNDS PLAYED","AVG","BEST 8 TOTAL","DELTA"), column_config={"POSITION": " ", "DELTA": " "})

if menu_selection == "Weekly Winners":
	st.dataframe(df_weekly_thurs_tab, width=None, height=912, use_container_width=True, hide_index=True)

if menu_selection == "Handicaps":
	st.dataframe(df_handi_thurs_tab, width=None, height=592, use_container_width=True, hide_index=True, column_config={"POSITION": " ", "HANDICAP THURS": "HANDICAP"})

if menu_selection == "Full Table":
	st.dataframe(df_golf_tab, width=None, height=592, use_container_width=True, hide_index=True, column_config={"NAME": st.column_config.Column(pinned=True),"Unnamed: 25": "TOTAL"})

st.divider()

call_sign = st.html(
	"""
	<style>
		a {
			text-decoration: none;
			color: grey;
			}
	</style>

	<div style="text-align:right">
		<a href="https://www.initrode.uk" target="_blank"><small>initrode - v2.0.8</a></small>
	</div>
		"""
	)

st.echo(call_sign)


# --- FUTURE ADDITIONS
# st.markdown("##")
# st.snow() # --- WINTER / XMAS UPDATE --- DOES IT WORK ON CELLPHONE?
# st.balloons() # --- END OF SEASON CELEBRATION --- DOES IT WORK ON CELLPHONE?
# st.toast("xxxxxxx is the winner", icon="🔥") # --- WINNER ANNOUNCEMENT --- DOES IT WORK ON CELLPHONE?
# time.sleep(1) --- ALSO HAVE TO import time
# POSSIBLE ICONS = [🔥, 🚨, 💩, 💥, 🔆, 😎, 😖, 😟, 🥇, 🏅, ☠️, ⚠️, ⚽, ⭐, 💯, ✅, ❗, 🏆]

# st.title("Title Marlow Dukes") --- st.header("This is a header") --- st.subheader("Sub Header") --- st.markdown("data correct as of ...")

