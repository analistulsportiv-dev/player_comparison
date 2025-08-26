import streamlit as st
import pandas as pd
from data_loader import DatasetLoader, load_player_data
from stats_processor import StatsProcessor
from chart_plotter import RadarChartPlotter
from enums import Position, Stats

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
        
        # Initialize StatsProcessor for player 1 data and create new columns
        stats_processor1 = StatsProcessor(players_df1)
        stats_processor1.create_columns()
        
        # Select player names from the processed DataFrame to include new columns
        player_names1 = stats_processor1.players_df['Full name'].unique()
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
            
            stats_processor2 = StatsProcessor(players_df2)
            stats_processor2.create_columns()
            
            player_names2 = stats_processor2.players_df['Full name'].unique()
            player2_name = st.sidebar.selectbox("Select player 2:", player_names2, key="player2")

        st.sidebar.markdown("---")

        # === Configuration Selector ===
        config_options = [config.name.replace("_", " ").title() for config in Stats]
        config_options.append("Custom")

        selected_config = st.sidebar.selectbox("Select role configuration:", config_options)

        # === Stat Selection ===
        numeric_cols = stats_processor1.get_numeric_stats_columns()

        if selected_config == "Custom":
            selected_stats = st.sidebar.multiselect(
                "Select stats to compare:",
                options=numeric_cols,
                default=[]
            )
        else:
            config_key = selected_config.upper().replace(" ", "_")
            stats_enum = Stats[config_key]
            default_stats = [s for s in stats_enum.value if s in numeric_cols]
            selected_stats = default_stats

            st.sidebar.markdown(f"**Using predefined stats for:** {selected_config}")
            st.sidebar.write(f"{', '.join(default_stats)}")

        # Validation
        if not selected_stats:
            st.info("Please select at least one stat to proceed.")
            return

        # Select player1_data from stats_processor1's processed DataFrame
        player1_data = stats_processor1.players_df[stats_processor1.players_df['Full name'] == player1_name].iloc[0]
        player1_stats_norm = stats_processor1.get_normalized_stats(player1_data, selected_stats)

        if compare_two_players:
            # Prepare both datasets
            stats_processor1.players_df["Year"] = year1
            stats_processor1.players_df["League"] = league1
            stats_processor2.players_df["Year"] = year2
            stats_processor2.players_df["League"] = league2

            stats_processor1.players_df["name_year"] = stats_processor1.players_df["Full name"] + f" ({year1})"
            stats_processor2.players_df["name_year"] = stats_processor2.players_df["Full name"] + f" ({year2})"

            player1_name_year = f"{player1_name} ({year1})"
            player2_name_year = f"{player2_name} ({year2})"

            if year1 == year2 and league1 == league2:
                # Use one DataFrame and processor for both players
                stats_processor = StatsProcessor(stats_processor1.players_df)
                stats_processor.create_columns()

                player1_data = stats_processor.players_df[stats_processor.players_df["name_year"] == player1_name_year].iloc[0]
                player2_data = stats_processor.players_df[stats_processor.players_df["name_year"] == player2_name_year].iloc[0]

            else:
                # Combine processed DataFrames from both processors
                combined_df = pd.concat([stats_processor1.players_df, stats_processor2.players_df], ignore_index=True)
                stats_processor = StatsProcessor(combined_df)
                stats_processor.create_columns()

                player1_data = stats_processor.players_df[stats_processor.players_df["name_year"] == player1_name_year].iloc[0]
                player2_data = stats_processor.players_df[stats_processor.players_df["name_year"] == player2_name_year].iloc[0]

            player1_stats_norm = stats_processor.get_normalized_stats(player1_data, selected_stats)
            player2_stats_norm = stats_processor.get_normalized_stats(player2_data, selected_stats)

            player1_stats_real = player1_data[selected_stats]
            player2_stats_real = player2_data[selected_stats]

            RadarChartPlotter.plot(
                [player1_stats_norm, player2_stats_norm],
                [player1_stats_real, player2_stats_real],
                [player1_name_year, player2_name_year],
                selected_stats
            )

        else:
            st.header(f"🔎 {player1_name} – Attribute Overview")

            player1_position = player1_data["Primary position"]

            # Toggle: normalize relative to same-position players or all players
            normalize_by_position = st.toggle(f"Normalize relative to average {player1_position}", value=True)

            if normalize_by_position:
                # Filter players with same position (including player1)
                base_players = stats_processor1.players_df[
                    stats_processor1.players_df["Primary position"] == player1_position
                ]
            else:
                # Use all players
                base_players = stats_processor1.players_df

            # Create a temp processor with the chosen base players for normalization
            temp_stats_processor = StatsProcessor(base_players)
            temp_stats_processor.create_columns()

            # Normalize player1 stats based on chosen base group
            player1_stats_norm = temp_stats_processor.get_normalized_stats(player1_data, selected_stats)

            # Divide selected stats into two columns
            half = (len(selected_stats) + 1) // 2
            col1_stats = selected_stats[:half]
            col2_stats = selected_stats[half:]
            col1, col2 = st.columns(2)

            # Display in col1
            with col1:
                for stat in col1_stats:
                    raw_value = player1_data[stat]
                    norm_value = player1_stats_norm[stat] * 100
                    color = self.get_color(norm_value)

                    st.markdown(f"**{stat}**: {raw_value:.3f} ({norm_value:.0f}%)")
                    st.markdown(f"""
                        <div style="background-color: #e0e0e0; border-radius: 8px; overflow: hidden; height: 20px; width: 100%; margin-bottom: 10px;">
                            <div style="width: {norm_value}%; background-color: {color}; height: 100%; text-align: center;">
                                <span style="color: black; font-size: 14px;">{norm_value:.0f}%</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

            # Display in col2
            with col2:
                for stat in col2_stats:
                    raw_value = player1_data[stat]
                    norm_value = player1_stats_norm[stat] * 100
                    color = self.get_color(norm_value)

                    st.markdown(f"**{stat}**: {raw_value:.3f} ({norm_value:.0f}%)")
                    st.markdown(f"""
                        <div style="background-color: #e0e0e0; border-radius: 8px; overflow: hidden; height: 20px; width: 100%; margin-bottom: 10px;">
                            <div style="width: {norm_value}%; background-color: {color}; height: 100%; text-align: center;">
                                <span style="color: black; font-size: 14px;">{norm_value:.0f}%</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)


#Ibrahim Diabate #Yannick Agnero #Alexandr Thongla-lad #Romaric Yapi #Nail Omerovic

def run_squad_overview():
    st.title("📊 Squad Overview")

    left_col, center_col, right_col = st.columns([1, 2, 1], gap="large")

    df = pd.read_excel("fcsb.xlsx")
    df["BirthDate"] = pd.to_datetime(df["BirthDate"], dayfirst=True, errors="coerce")
    df["StartDate"] = pd.to_datetime(df["StartDate"], dayfirst=True, errors="coerce")
    df["EndDate"] = pd.to_datetime(df["EndDate"], dayfirst=True, errors="coerce")
    today = pd.to_datetime(dt.datetime.today().date())
    df["Age"] = (today - df["BirthDate"]).dt.days / 365.25
    df["AgeStart"] = (df["StartDate"] - df["BirthDate"]).dt.days / 365.25
    df["AgeEnd"] = (df["EndDate"] - df["BirthDate"]).dt.days / 365.25
    df["YearsAtClub"] = (today - df["StartDate"]).dt.days / 365.25

    def map_color(series):
        min_val, max_val = series.min(), series.max()
        def inner(val):
            norm = (val - min_val) / (max_val - min_val + 1e-6)
            return mcolors.to_hex(plt.cm.RdYlGn(norm))
        return inner

    # ---- Goals per position (left col) ----
    with left_col:
        zone_goals = df.groupby("Position")["Goals"].sum()
        color_func = map_color(zone_goals)

        pitch = Pitch(pitch_type='custom', pitch_length=100, pitch_width=100, line_color='black')
        fig_goals, ax_goals = plt.subplots(figsize=(6, 10))
        pitch.draw(ax=ax_goals)
        ax_goals.set_title("Goals per Position", fontsize=14)

        zones = {
            "LB": (0, 15, 30, 18),
            "CB": (35, 10, 30, 18),
            "RB": (70, 15, 30, 18),
            "CDM": (35, 35, 30, 20),
            "LM": (0, 55, 30, 18),
            "RM": (70, 55, 30, 18),
            "CAM": (35, 60, 30, 18),
            "ST": (35, 82, 30, 18), 
        }

        for pos, (x0, y0, w, h) in zones.items():
            total = zone_goals.get(pos, 0)
            rect = plt.Rectangle((y0, x0), h, w, color=color_func(total), alpha=0.5)
            ax_goals.add_patch(rect)

            players = df[df["Position"] == pos].sort_values(by="Goals", ascending=False)
            text = "\n".join([f"{row['Name']} ({row['Goals']})" for _, row in players.iterrows()])
            ax_goals.text(y0 + h/2, x0 + w/2, f"{pos}\n{total}\n{text}", ha="center", va="center", fontsize=9)

        ax_goals.invert_yaxis()
        ax_goals.set_aspect('equal')
        st.pyplot(fig_goals)

        st.subheader("Top Scorers")
        top5 = df.sort_values(by="Goals", ascending=False).head(6)
        nr = 1
        for i, row in top5.iterrows():
            st.write(f"{nr}. {row['Name']} ({row['Goals']} goals)")
            nr+=1

    # ---- Age profile (center col) ----
    with center_col:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.axvspan(24, 30, color="gray", alpha=0.3)
        ax.axvspan(19, 21, color="red", alpha=0.3)
        for m in [200, 400, 600, 800, 1000]:
            ax.axhline(y=m, color="lightgray", linestyle="--", linewidth=0.8)

        xmin, xmax = int(df["Age"].min()) - 2, int(df["Age"].max()) + 2
        for age in range(xmin, xmax + 1, 2):
            ax.axvline(x=age, color="lightgray", linestyle="--", linewidth=0.8)

        for _, row in df.iterrows():
            ax.hlines(y=row["Minutes played"], xmin=row["AgeStart"], xmax=row["AgeEnd"], color="black", alpha=0.6)
            if row["YearsAtClub"] > 1:
                ax.scatter(row["Age"], row["Minutes played"], color="purple", s=70, zorder=3)
            else:
                ax.scatter(row["Age"], row["Minutes played"], color="red", marker="x", s=80, zorder=3)
            ax.text(row["Age"], row["Minutes played"] + 30, row["Name"], fontsize=8)

        avg_age = df["Age"].mean()
        ax.axvline(x=avg_age, color="blue", linestyle="--", linewidth=2, label=f"Average Age: {avg_age:.1f}")
        y_max = df["Minutes played"].max()
        ax.text(avg_age + 0.2, y_max * 0.8, f"Avg Age: {avg_age:.1f}", color="blue", rotation=90, 
            verticalalignment='top', fontsize=10)

        ax.set_xlabel("Age")
        ax.set_ylabel("Minutes Played")
        ax.set_title("Squad Age Profile")
        ax.set_xlim(xmin, xmax)

        purple_dot = mpatches.Patch(color='purple', label='Years > 1')
        red_x = mpatches.Patch(color='red', label='Years ≤ 1')
        gray_patch = mpatches.Patch(color='gray', alpha=0.3, label='Peak Years (24–30)')
        red_patch = mpatches.Patch(color='red', alpha= 0.3, label = '19-21')
        ax.legend(handles=[purple_dot, red_x, gray_patch, red_patch], loc="upper left")
        st.pyplot(fig)

        # Age groups bar chart
        bins = [15, 19, 25, 31, 40]
        labels = ["<19", "20-24", "25-30", "30+"]
        df["AgeGroup"] = pd.cut(df["Age"], bins=bins, labels=labels, right=False)
        age_counts = df["AgeGroup"].value_counts().sort_index()
        feb2024_counts = pd.Series([1, 5, 9, 9], index=labels)

        fig2, ax2 = plt.subplots(figsize=(10, 2.8))
        width = 0.35
        age_counts.plot(kind="bar", ax=ax2, width=width, color="steelblue", edgecolor="black", position=0, label="Current")
        feb2024_counts.plot(kind="bar", ax=ax2, width=width, color="orange", edgecolor="black", position=1, label="Jan 2024")
        ax2.set_xlim(-0.5, len(labels)-0.5)
        ax2.set_xlabel("Age Group")
        ax2.set_ylabel("Number of Players")
        ax2.set_title("Players per Age Group (Current vs Jan 2024)")
        ax2.legend()
        st.pyplot(fig2)

    # ---- Salaries and values (right col) ----
    with right_col:
        if "Salariu" in df.columns:
            zone_salary = df.groupby("Position")["Salariu"].mean()
            color_func_salary = map_color(zone_salary)

            pitch = Pitch(pitch_type='custom', pitch_length=100, pitch_width=100, line_color='black')
            fig_salary, ax_salary = plt.subplots(figsize=(6, 9))
            pitch.draw(ax=ax_salary)
            ax_salary.set_title("Average Salary per Position", fontsize=14)

            zones = {
                "GK": (30, 0, 40, 16),
                "LB": (0, 18, 30, 18),
                "CB": (35, 18, 30, 18),
                "RB": (70, 18, 30, 18),
                "CDM": (35, 40, 30, 20),
                "LM": (0, 55, 30, 18),
                "RM": (70, 55, 30, 18),
                "CAM": (35, 62, 30, 18),
                "ST": (35, 82, 30, 18), 
            }

            for pos, (x0, y0, w, h) in zones.items():
                avg_salary = zone_salary.get(pos, 0)
                rect = plt.Rectangle((y0, x0), h, w, color=color_func_salary(avg_salary), alpha=0.5)
                ax_salary.add_patch(rect)

                players = df[df["Position"] == pos].sort_values(by="Salariu", ascending=False)
                text = "\n".join([f"{row['Name']} ({row['Salariu']})" for _, row in players.iterrows()])
                ax_salary.text(y0 + h/2, x0 + w/2, f"{pos}\n{avg_salary:.1f}\n{text}", ha="center", va="center", fontsize=8)

            ax_salary.invert_yaxis()
            ax_salary.set_aspect('equal')
            st.pyplot(fig_salary)

            total_salary = df["Salariu"].sum()
            st.markdown(f"**Total Salary: {total_salary:.1f}k**")

            if "Valoare" in df.columns:
                zone_value = df.groupby("Position")["Valoare"].sum()
                color_func_value = map_color(zone_value)

                fig_value, ax_value = plt.subplots(figsize=(6, 9))
                pitch.draw(ax=ax_value)
                ax_value.set_title("Player Values per Position", fontsize=14)

                for pos, (x0, y0, w, h) in zones.items():
                    avg_val = zone_value.get(pos, 0)
                    rect = plt.Rectangle((y0, x0), h, w, color=color_func_value(avg_val), alpha=0.5)
                    ax_value.add_patch(rect)

                    players = df[df["Position"] == pos].sort_values(by="Valoare", ascending=False).head(10)
                    text = "\n".join([f"{row['Name']} ({row['Valoare']})" for _, row in players.iterrows()])
                    ax_value.text(y0 + h/2, x0 + w/2, f"{pos}\n{avg_val:.1f}\n{text}", ha="center", va="center", fontsize=8 )

                ax_value.invert_yaxis()
                ax_value.set_aspect('equal')
                st.pyplot(fig_value)
            else:
                st.warning("Value column not found in the dataset.")

        else:
            st.warning("Salary column not found in the dataset.")


# ---------------------------
# MAIN APP ENTRYPOINT
# ---------------------------
if __name__ == "__main__":
    st.set_page_config(layout="wide")

    st.title("Football Analytics Dashboard")

    # 🔥 Horizontal toolbar with tabs
    tab1, tab2 = st.tabs(["⚽ Player Comparison", "📊 Squad Overview"])

    with tab1:
        app = PlayerComparisonApp()
        app.run()

    with tab2:
        run_squad_overview()

