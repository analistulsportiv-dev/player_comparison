import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

class RadarChartPlotter:
    @staticmethod
    def plot(stats_list, player_names, categories):
        num_vars = len(categories)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

        # Close the stats and angles for a loop
        stats_list = [list(stats) + [stats[0]] for stats in stats_list]
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

        for stats, name in zip(stats_list, player_names):
            ax.plot(angles, stats, label=name)
            ax.fill(angles, stats, alpha=0.25)

            # Add value labels slightly above each point
            for angle, stat in zip(angles, stats):
                ax.text(angle, stat + 0.05, f"{stat:.2f}", ha='center', va='center')

        ax.set_thetagrids(np.degrees(angles[:-1]), categories)
        ax.set_ylim(0, 1)  # Assuming normalized values between 0 and 1
        ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))

        # Instead of plt.show(), use Streamlit to display the figure
        st.pyplot(fig)
