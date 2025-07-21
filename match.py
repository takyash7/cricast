import streamlit as st
import requests
from datetime import datetime

def app():
    st.markdown("<h1 style='color:	#DC143C;'>🏏 UpComing Matches</h1>", unsafe_allow_html=True)

    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/upcoming"
    headers = {
        "X-RapidAPI-Key": "e899045387msh88494ef0ff792a0p137073jsnb76291cf3160",  # Replace with your valid API key
        "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        match_list = data.get("typeMatches", [])
        total_matches = 0

        for match_type in match_list:
            series_matches = match_type.get("seriesMatches", [])
            for series in series_matches:
                series_name = series.get("seriesAdWrapper", {}).get("seriesName", "🔖 Unknown Series")
                matches = series.get("seriesAdWrapper", {}).get("matches", [])

                series_displayed = False

                for match in matches:
                    match_info = match.get("matchInfo", {})
                    match_dt = match_info.get("startDate")
                    if match_dt:
                        dt = datetime.fromtimestamp(int(match_dt) / 1000)
                        delta = (dt - datetime.utcnow()).days
                        if 0 <= delta <= 15:
                            if not series_displayed:
                                st.markdown(f"<h3 style='color:#1E90FF; font-size:26px;'>🏆 {series_name}</h3>", unsafe_allow_html=True)
                                series_displayed = True

                            team1 = match_info.get("team1", {}).get("teamName", "TBD")
                            team2 = match_info.get("team2", {}).get("teamName", "TBD")
                            teams = f"{team1} vs {team2}"

                            st.markdown(f"### {teams}")
                            st.write(f"🏟️ Venue: {match_info.get('venueInfo', {}).get('ground', 'N/A')}")
                            st.write(f"📅 Date & Time (UTC): {dt.strftime('%Y-%m-%d %H:%M')}")
                            st.write(f"🔁 Match Type: {match_info.get('matchFormat', 'N/A')}")
                            st.markdown("---")
                            total_matches += 1

        if total_matches == 0:
            st.info("🚧 No matches scheduled in the next 15 days.")

    except Exception as e:
        st.error(f"❌ Failed to fetch match data: {e}")
