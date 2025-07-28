import streamlit as st
import pandas as pd
from data_loader import DatasetLoader, load_player_data
from stats_processor import StatsProcessor
from chart_plotter import RadarChartPlotter


class PlayerComparisonApp:
    def __init__(self):
        self.dataset_loader = DatasetLoader()

    def get_color(self, percent):
        if percent >= 70:
            return "green"
        elif percent >= 40:
            return "yellow"
        elif percent >= 20:
            return "orange"
        else:
            return "red"

    def run(self):
        st.title("Player Comparison App")

        st.sidebar.header("Filter Options")

        # Load dataset metadata
        dataset_metadata = self.dataset_loader.get_metadata()
        available_years = self.dataset_loader.get_years()

        # Player 1 filters
        st.sidebar.subheader("Player 1 Filters")
        year1 = st.sidebar.selectbox("Select year (Player 1):", available_years, key="year1")
        leagues1 = dataset_metadata[dataset_metadata['YEAR'] == year1]['LEAGUE'].unique()
        league1 = st.sidebar.selectbox("Select league (Player 1):", leagues1, key="league1")
        dataset_path1 = self.dataset_loader.get_dataset_path(league1, year1)
        players_df1 = load_player_data(dataset_path1)
        player_names1 = players_df1['Player'].unique()
        player1_name = st.sidebar.selectbox("Select player 1:", player_names1, key="player1")

        st.sidebar.markdown("---")

        # Toggle comparison
        compare_two_players = st.sidebar.checkbox("Compare with a second player", value=True)

        if compare_two_players:
            st.sidebar.subheader("Player 2 Filters")
            year2 = st.sidebar.selectbox("Select year (Player 2):", available_years, key="year2")
            leagues2 = dataset_metadata[dataset_metadata['YEAR'] == year2]['LEAGUE'].unique()
            league2 = st.sidebar.selectbox("Select league (Player 2):", leagues2, key="league2")
            dataset_path2 = self.dataset_loader.get_dataset_path(league2, year2)
            players_df2 = load_player_data(dataset_path2)
            player_names2 = players_df2['Player'].unique()
            player2_name = st.sidebar.selectbox("Select player 2:", player_names2, key="player2")

        st.sidebar.markdown("---")

        # Stats multiselect
        stats_processor1 = StatsProcessor(players_df1)
        numeric_cols = stats_processor1.get_numeric_stats_columns()
        default_stats = ["Goals", "Assists", "xG"]
        selected_stats = st.sidebar.multiselect(
            "Select stats to compare:",
            options=numeric_cols,
            default=[stat for stat in default_stats if stat in numeric_cols]
        )

        # Output
        if not selected_stats:
            st.info("Please select at least one stat to proceed.")
            return

        player1_data = players_df1[players_df1['Player'] == player1_name].iloc[0]
        stats_processor1 = StatsProcessor(players_df1)
        player1_stats_norm = stats_processor1.get_normalized_stats(player1_data, selected_stats)

        if compare_two_players:
            # Tag both datasets with year and league info
            players_df1["Year"] = year1
            players_df1["League"] = league1
            players_df2["Year"] = year2
            players_df2["League"] = league2

            # Add name_year helper column
            players_df1["name_year"] = players_df1["Player"] + f" ({year1})"
            players_df2["name_year"] = players_df2["Player"] + f" ({year2})"

            player1_name_year = f"{player1_name} ({year1})"
            player2_name_year = f"{player2_name} ({year2})"

            if year1 == year2 and league1 == league1:
                # Same dataset → use original dfs
                stats_processor = StatsProcessor(players_df1)
                player1_data = players_df1[players_df1["name_year"] == player1_name_year].iloc[0]
                player2_data = players_df2[players_df2["name_year"] == player2_name_year].iloc[0]

            else:
                # Merge and normalize from common distribution
                combined_df = pd.concat([players_df1, players_df2], ignore_index=True)
                stats_processor = StatsProcessor(combined_df)
                player1_data = combined_df[combined_df["name_year"] == player1_name_year].iloc[0]
                player2_data = combined_df[combined_df["name_year"] == player2_name_year].iloc[0]

            # Normalize from the appropriate processor
            player1_stats_norm = stats_processor.get_normalized_stats(player1_data, selected_stats)
            player2_stats_norm = stats_processor.get_normalized_stats(player2_data, selected_stats)

            # Plot radar
            RadarChartPlotter.plot(
                [player1_stats_norm, player2_stats_norm],
                [player1_name_year, player2_name_year],
                selected_stats
            )
        else:
           st.header(f"🔎 {player1_name} – Attribute Overview")

           for stat in selected_stats:
                raw_value = player1_data[stat]
                norm_value = player1_stats_norm[stat] * 100
                color = self.get_color(norm_value)

                st.markdown(f"**{stat}**: {raw_value} ({norm_value:.0f}%)")

                st.markdown(f"""
                    <div style="background-color: #e0e0e0; border-radius: 8px; overflow: hidden; height: 20px; width: 100%; margin-bottom: 10px;">
                        <div style="width: {norm_value}%; background-color: {color}; height: 100%; text-align: center;">
                            <span style="color: black; font-size: 14px;">{norm_value:.0f}%</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)


if __name__ == "__main__":
    app = PlayerComparisonApp()
    app.run()