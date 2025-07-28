import streamlit as st

class PlayerSelector:
    def __init__(self, players_df):
        self.players_df = players_df

    def get_player_names(self):
        return self.players_df['Player'].unique()

    def select_players(self):
        player_names = self.get_player_names()
        player1 = st.selectbox("Select Player 1", player_names)
        player2 = st.selectbox("Select Player 2", player_names, index=1 if len(player_names) > 1 else 0)

        if player1 == player2:
            st.warning("Please select two different players to compare.")
            st.stop()
        return player1, player2
