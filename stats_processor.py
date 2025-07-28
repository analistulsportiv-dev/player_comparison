import pandas as pd

class StatsProcessor:
    def __init__(self, players_df: pd.DataFrame):
        self.players_df = players_df.copy()
        self.players_df.columns = [col.strip() for col in self.players_df.columns]

    def get_numeric_stats_columns(self) -> list[str]:
        return self.players_df.select_dtypes(include='number').columns.tolist()

    def normalize(self, column_name: str, values):
        if column_name not in self.players_df.columns:
            raise KeyError(f"Column '{column_name}' not found in DataFrame columns")

        min_val = self.players_df[column_name].min()
        max_val = self.players_df[column_name].max()
        if max_val == min_val:
            return 0  # avoid division by zero if value is scalar
        return (values - min_val) / (max_val - min_val)

    def get_normalized_stats(self, player_row: pd.Series, columns: list[str]) -> pd.Series:
        normalized_stats = {}
        for col in columns:
            normalized_stats[col] = self.normalize(col, player_row[col])
        return pd.Series(normalized_stats)