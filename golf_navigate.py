import streamlit as st

# st.set_page_config(page_title="Marlow Dukes", page_icon="images/marlowdukesicon.png", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.set_page_config(page_title="Stoneleigh Golf Tournaments", page_icon="images/golf.png", layout="centered", initial_sidebar_state="auto", menu_items=None)


sunday_singles = st.Page("SUNDAY_SUMMER_SINGLES.py", title="SUNDAY SINGLES", icon=":material/sports_golf:")
thursday_singles = st.Page("THURSDAY_SUMMER_SINGLES.py", title="THURSDAY SINGLES", icon=":material/sports_golf:")

winter2425_pairs = st.Page("WINTER_PAIRS.py", title="WINTER 24/25 - PAIRS", icon=":material/trophy:")
winter2425_singles = st.Page("THURSDAY_SINGLES.py", title="WINTER 24/25 - SINGLES", icon=":material/trophy:")


with st.sidebar:
	st.subheader("Current Tournament")
	st.page_link(sunday_singles, label=sunday_singles.title, icon=sunday_singles.icon)
	st.page_link(thursday_singles, label=thursday_singles.title, icon=thursday_singles.icon)

	st.write("---")

	st.subheader("Past Tournaments")
	st.page_link(winter2425_pairs, label=winter2425_pairs.title, icon=winter2425_pairs.icon)
	st.page_link(winter2425_singles, label=winter2425_singles.title, icon=winter2425_singles.icon)

	st.subheader("Other")
	st.page_link(page="https://www.stoneleighdeerparkgolfclub.com/", label="CLUB WEBSITE", icon=":material/globe:")
	st.page_link(page="https://www.stoneleighdeerparkgolfclub.com/members-login", label="CLUB MEMBERS LOGIN", icon=":material/login:")

	st.write("---")

pg = st.navigation([sunday_singles, thursday_singles, winter2425_pairs, winter2425_singles], position="hidden")
pg.run()


# --- ICONS ... 📕, 📚, 📖, 📘, 📈, 📊, 📋, 🗄️, 🛒, 🏪,🏅, 🚩, 💼, 
