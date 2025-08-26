import pandas as pd
from enums import ToCreateColumns, ExistentFieldPlayerColumn, ColumnMapping, Position

class StatsProcessor:
    def __init__(self, players_df: pd.DataFrame):
        self.players_df = players_df.copy()
        self.players_df.columns = [col.strip() for col in self.players_df.columns]

    def create_columns(self):
        # Calculate Shot Efficiency
        self.players_df[ToCreateColumns.SHOT_EFFICIENCY.value] = self.players_df.apply(
            lambda row: row[ExistentFieldPlayerColumn.GOALS_PER_90.value] / row[ExistentFieldPlayerColumn.XG_PER_90.value]
            if row[ExistentFieldPlayerColumn.XG_PER_90.value] != 0 else 0,
            axis=1
        )

        # Compute derived stats using percentage mappings
        for new_col, (base_col, pct_col) in ColumnMapping.COLUMN_MAPPING.items():
            if base_col in self.players_df.columns and pct_col in self.players_df.columns:
                self.players_df[new_col] = (
                    self.players_df[base_col] *
                    (self.players_df[pct_col].fillna(0) / 100)
                )

    def get_numeric_stats_columns(self) -> list[str]:
        return self.players_df.select_dtypes(include='number').columns.tolist()

    def normalize(self, column_name: str, values):
        if column_name not in self.players_df.columns:
            raise KeyError(f"Column '{column_name}' not found in DataFrame columns")

        min_val = self.players_df[column_name].min()
        max_val = self.players_df[column_name].max()
        if max_val == min_val:
            return 0
        return (values - min_val) / (max_val - min_val)

    def get_normalized_stats(self, player_row: pd.Series, columns: list[str]) -> pd.Series:
        normalized = {}
        for col in columns:
            if col in player_row:
                normalized[col] = self.normalize(col, player_row[col])
            else:
                # Handle missing column; could set to NaN or 0 or skip
                normalized[col] = float('nan')  # or 0
        return pd.Series(normalized)