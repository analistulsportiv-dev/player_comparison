import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

class RadarChartPlotter:
    @staticmethod
    def plot(normalized_stats_list, real_stats_list, player_names, categories):
        num_vars = len(categories)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1]

        normalized_stats_list = [list(stats) + [stats[0]] for stats in normalized_stats_list]
        real_stats_list = [list(stats) + [stats[0]] for stats in real_stats_list]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

        for norm_stats, real_stats, name in zip(normalized_stats_list, real_stats_list, player_names):
            line = ax.plot(angles, norm_stats, label=name)
            ax.fill(angles, norm_stats, alpha=0.25)

            color = line[0].get_color()

            for angle, norm_val, real_val in zip(angles, norm_stats, real_stats):
                ax.text(angle, norm_val + 0.02, f"{real_val:.2f}", ha='center', va='center', fontsize=8, color=color)


        ax.set_thetagrids(np.degrees(angles[:-1]), categories, fontsize=8)
        ax.set_ylim(0, 1)
        ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))
        st.pyplot(fig)