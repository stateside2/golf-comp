
import pandas as pd
import streamlit as st
import streamlit_antd_components as sac


win2526_file: str = "data/WINTER_GOLF_2526.xlsx"
sum25_file: str = "data/SUMMER GOLF 2025.xlsx"
win2425_file: str = "data/WINTER2425.xlsx"


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
st.image("images/golf_banner_all_time.png", use_container_width="auto")
st.divider()


menu_selection = sac.buttons(
   items=[
    	sac.ButtonsItem(label="Best Average Score", icon="trophy-fill"),
    	sac.ButtonsItem(label="Best Round Score", icon="justify-left"),
    	sac.ButtonsItem(label="Worst Round Score", icon="justify-right"),
    	sac.ButtonsItem(label="Best Total Score", icon="bar-chart-fill"),
    	sac.ButtonsItem(label="Most Rounds Played", icon="person-walking"),
    	sac.ButtonsItem(label="Full Details", icon="person-lines-fill"),
    	# sac.ButtonsItem(label="Weekly Wins", icon="pin-map"),
], label="All Time Statistics", format_func=None, align="center", size="md", radius="md", color="#598506", use_container_width=True)
# ---


df_w2425_sun = pd.read_excel(win2425_file, skiprows=[0,1,2,3,4,5,6,7,8,9,31,32,33,34,35,36,37,38], sheet_name='Sheet1', usecols=[0,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26])
df_w2425_thurs = pd.read_excel(win2425_file, skiprows=[0,1,2,19,20,21,22,23,24,25,26,27], sheet_name="THURSDAY SINGLES", usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])

df_sum25_sun = pd.read_excel(sum25_file, skiprows=[0,1,2,22,23,24], sheet_name='SUNDAY SINGLES', usecols=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25])
df_sum25_thurs = pd.read_excel(sum25_file, skiprows=[0,1,2,18,19,20], sheet_name='THURSDAY SINGLES', usecols=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25])

df_w2526_sun = pd.read_excel(win2526_file, skiprows=[0,1,2,22,23,24], sheet_name='SUNDAY SINGLES', usecols=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25])
df_w2526_thurs = pd.read_excel(win2526_file, skiprows=[0,1,2,18,19,20], sheet_name='THURSDAY SINGLES', usecols=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25])


# df_alltime = df_w2425_sun.merge(df_w2425_thurs,on='NAME',how='outer').merge(df_sum25_sun,on='NAME',how='outer').merge(df_sum25_thurs,on='NAME',how='outer')
# df_alltime = pd.merge(df_w2425_sun, df_w2425_thurs, on='NAME', how='outer').merge(df_sum25_sun, on='NAME', how='outer')

df_join_1 = df_w2425_sun.join(df_w2425_thurs.set_index("NAME"), on="NAME", how="outer", lsuffix="_24sun", rsuffix="_24thr")
df_join_2 = df_join_1.join(df_sum25_sun.set_index("NAME"), on="NAME", how="outer", lsuffix="_jn1", rsuffix="_25sun")
df_join_3 = df_join_2.join(df_sum25_thurs.set_index("NAME"), on="NAME", how="outer", lsuffix="_jn2", rsuffix="_25thr")
df_join_4 = df_join_3.join(df_w2526_sun.set_index("NAME"), on="NAME", how="outer", lsuffix="_jn3", rsuffix="_2526sun")
df_alltime = df_join_4.join(df_w2425_thurs.set_index("NAME"), on="NAME", how="outer", lsuffix="_jn4", rsuffix="_2526thr")

# HIGHEST AND LOWEST SCORE CALCULATION
df_highlow = df_alltime
df_at_high = df_highlow.max(axis=1, numeric_only=True)
df_at_low = df_highlow.min(axis=1, numeric_only=True)

# BEST AVERAGE CALCULATION
df_avgcalc = df_alltime
df_rndsplayed = df_avgcalc.count(axis=1, numeric_only=True)
df_total = df_avgcalc.sum(axis=1, numeric_only=True)
df_bestavg = df_total/df_rndsplayed


df_alltime['RNDS_PLAYED'] = df_rndsplayed
df_alltime['TOTAL'] = df_total
df_alltime['AVERAGE'] = df_bestavg

df_alltime['HIGH_SCORE'] = df_at_high
df_alltime['LOW_SCORE'] = df_at_low



table_height = 1123

if menu_selection == "Best Average Score":
	df_alltime = df_alltime.sort_values(by=["AVERAGE", "NAME"], ascending=[False, True])
	df_alltime.insert(0, "POSITION", range(1, 1 + len(df_alltime)))
	df_alltime = df_alltime.style.format({"AVERAGE": "{:.2f}"})
	st.dataframe(df_alltime, width=None, height=table_height, use_container_width=True, hide_index=True, column_order=("POSITION","NAME","RNDS_PLAYED","AVERAGE"), column_config={"POSITION": " ", "RNDS_PLAYED": "ROUNDS", "AVERAGE": "AVERAGE", "HIGH_SCORE": "BEST SCORE", "LOW_SCORE": "WORST SCORE"})

if menu_selection == "Best Round Score":
	df_alltime = df_alltime.sort_values(by=["HIGH_SCORE", "NAME"], ascending=[False, True])
	df_alltime.insert(0, "POSITION", range(1, 1 + len(df_alltime)))
	st.dataframe(df_alltime, width=None, height=table_height, use_container_width=True, hide_index=True, column_order=("POSITION","NAME","RNDS_PLAYED","HIGH_SCORE"), column_config={"POSITION": " ", "RNDS_PLAYED": "ROUNDS", "HIGH_SCORE": "BEST SCORE"})

if menu_selection == "Worst Round Score":
	df_alltime = df_alltime.sort_values(by=["LOW_SCORE", "NAME"], ascending=[True, True])
	df_alltime.insert(0, "POSITION", range(1, 1 + len(df_alltime)))
	st.dataframe(df_alltime, width=None, height=table_height, use_container_width=True, hide_index=True, column_order=("POSITION","NAME","RNDS_PLAYED","LOW_SCORE"), column_config={"POSITION": " ", "RNDS_PLAYED": "ROUNDS", "LOW_SCORE": "WORST SCORE"})

if menu_selection == "Best Total Score":
	df_alltime = df_alltime.sort_values(by=["TOTAL", "NAME"], ascending=[False, True])
	df_alltime.insert(0, "POSITION", range(1, 1 + len(df_alltime)))
	st.dataframe(df_alltime, width=None,height=table_height, use_container_width=True, hide_index=True, column_order=("POSITION","NAME","RNDS_PLAYED","TOTAL"), column_config={"POSITION": " ", "RNDS_PLAYED": "ROUNDS", "TOTAL": "TOTAL SCORE"})

if menu_selection == "Most Rounds Played":
	df_alltime = df_alltime.sort_values(by=["RNDS_PLAYED", "NAME"], ascending=[False, True])
	df_alltime.insert(0, "POSITION", range(1, 1 + len(df_alltime)))
	st.dataframe(df_alltime, width=None, height=table_height, use_container_width=True, hide_index=True, column_order=("POSITION","NAME","RNDS_PLAYED"), column_config={"POSITION": " ", "RNDS_PLAYED": "ROUNDS"})

if menu_selection == "Full Details":
	df_alltime = df_alltime.sort_values(by=["NAME"], ascending=[True])
	df_alltime = df_alltime.style.format({"AVERAGE": "{:.2f}", "TOTAL": "{:.0f}", "HIGH_SCORE": "{:.0f}", "LOW_SCORE": "{:.0f}"})
	st.dataframe(df_alltime, width=None, height=table_height, use_container_width=True, hide_index=True, column_order=("NAME","RNDS_PLAYED","TOTAL","AVERAGE","HIGH_SCORE","LOW_SCORE"), column_config={"RNDS_PLAYED": "ROUNDS", "TOTAL": "TOTAL SCORE", "AVERAGE": "AVERAGE", "HIGH_SCORE": "BEST SCORE", "LOW_SCORE": "WORST SCORE"})



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
		<a href="https://www.initrode.uk" target="_blank"><small>initrode - 3.1</a></small>
	</div>
		"""
	)

st.echo(call_sign)




# # --- FUTURE ADDITIONS
# # st.markdown("##")
# # st.snow() # --- WINTER / XMAS UPDATE --- DOES IT WORK ON CELLPHONE?
# # st.balloons() # --- END OF SEASON CELEBRATION --- DOES IT WORK ON CELLPHONE?
# # st.toast("xxxxxxx is the winner", icon="🔥") # --- WINNER ANNOUNCEMENT --- DOES IT WORK ON CELLPHONE?
# # time.sleep(1) --- ALSO HAVE TO import time
# # POSSIBLE ICONS = [🔥, 🚨, 💩, 💥, 🔆, 😎, 😖, 😟, 🥇, 🏅, ☠️, ⚠️, ⚽, ⭐, 💯, ✅, ❗, 🏆, ⛳️, 🏌️]

# # st.title("Title Marlow Dukes") --- st.header("This is a header") --- st.subheader("Sub Header") --- st.markdown("data correct as of ...")

