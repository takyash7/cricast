import streamlit as st
import requests

def app():
    st.markdown("<h1 style='color:	#DC143C;'>🏏 Live Scores</h1>", unsafe_allow_html=True)


    url = "your url"
    headers = {
        "X-RapidAPI-Key": " ",  # Replace with your API key
        "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        match_list = data.get("typeMatches", [])
        total = 0

        for match_type in match_list:
            series_matches = match_type.get("seriesMatches", [])
            for series in series_matches:
                series_name = series.get("seriesAdWrapper", {}).get("seriesName", "🏆 Unknown Series")
               
                matches = series.get("seriesAdWrapper", {}).get("matches", [])
                series_displayed = False

                for match in matches:
                    match_info = match.get("matchInfo", {})
                    score_info = match.get("matchScore", {})

                    team1 = match_info.get("team1", {}).get("teamName", "TBD")
                    team2 = match_info.get("team2", {}).get("teamName", "TBD")
                    match_status = match_info.get("status", "N/A")
                    match_format = match_info.get("matchFormat", "N/A")
                    venue = match_info.get("venueInfo", {}).get("ground", "N/A")

                    score_summary = ""
                    innings_score_list = score_info.get("inningsScoreList", [])
                    for inn in innings_score_list:
                        score_summary += f"**{inn.get('battingTeamShort', 'Team')}**: {inn.get('score', '0')}/{inn.get('wickets', '0')} in {inn.get('overs', '0')} overs\n\n"

                    if not series_displayed:
                        st.markdown(f"<h3 style='color:#1E90FF; font-size:26px;'>🏆 {series_name}</h3>", unsafe_allow_html=True)

                        series_displayed = True

                    st.markdown(f"### {team1} vs {team2}")
                    st.write(f"🏟️ Venue: {venue}")
                    st.write(f"🔁 Format: {match_format}")
                    st.write(f"📣 Status: {match_status}")
                    st.markdown(score_summary)
                    st.markdown("---")
                    total += 1

        if total == 0:
            st.info("🚧 No live matches currently in progress.")

    except Exception as e:
        st.error(f"❌ Failed to fetch live match data: {e}")
