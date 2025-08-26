from enum import Enum
from typing import Dict, Union

class Position(Enum):
    GOALKEEPER = ["GK"]
    RIGHT_BACK = ["RB", "RWB", "RB5"]
    CENTER_BACK = ["CB", "LCB", "RCB", "LCB3", "RCB3"]
    LEFT_BACK = ["LB", "LWB", "LB5"]
    DEFENSIVE_MIDFIELDER = ["DMF", "LDMF", "RDMF"]
    CENTRAL_MIDFIELDER = ["CMF", "RCMF", "LCMF", "RCMF3", "LCMF3"]
    ATTACKING_MIDFIELDER = ["AMF"]
    LEFT_WINGER = ["LWF", "LAMF", "LW"]
    RIGHT_WINGER = ["RWF", "RAMF", "RW"]
    STRIKER = ["CF"]

    def __str__(self):
        return self.name.replace("_", " ").title()

class Stats(Enum):
    GOALKEEPER = []
    CENTER_BACK = ["Duels per 90", "Duels won per 90", "Defensive duels per 90", "Defensive duels won per 90", "Aerial duels per 90",
                   "Aerial duels won per 90", "Sliding tackles per 90", "Shots blocked per 90", "Interceptions per 90", "Successful defensive actions per 90",
                   "PAdj Sliding tackles", "PAdj Interceptions"]
    FULL_BACK = []
    DEFENSIVE_MIDFIELDER = ["Accurate passes per 90", "Progressive passes per 90", "Sliding tackles per 90", "Interceptions per 90",
                            "Aerial duels won per 90", "PAdj Sliding tackles", "PAdj Interceptions", "Duels won per 90", 
                            "Defensive duels won per 90", "Successful defensive actions per 90", "Progressive runs per 90",
                            "Accurate forward passes per 90", "Accurate vertical passes per 90", "Accurate progressive passes per 90",
                            "Assists per 90", "xA per 90",]
    CENTRAL_MIDFIELDER = ["Forward passes per 90", "Accurate forward passes per 90", "Progressive passes per 90", "Accurate progressive passes per 90", "Accurate passes per 90",
                          "Accurate passes to penalty area per 90", "Accurate vertical passes per 90", "Offensive duels per 90", "Offensive duels won per 90", "Goals per 90", "xG per 90", "Assists per 90", "xA per 90",
                          "Crosses to goalie box per 90", "Touches in box per 90"]
    ATTACKING_MIDFIELDER = ["Forward passes per 90", "Accurate forward passes per 90", "Progressive passes per 90", "Accurate progressive passes per 90", 
                          "Offensive duels per 90", "Offensive duels won per 90", "Goals per 90", "xG per 90", "Assists per 90", "xA per 90"]
    WINGER = ["Goals per 90", "Assists per 90", "Shots on target per 90", "xG per 90", "Accurate crosses, %", "Successful dribbles, %", 
              "Offensive duels won, %", "Touches in box per 90", "Progressive runs per 90", "Passes to final third per 90", 
              "Shot efficiency"]
    STRIKER = ["Goals per 90", "xG per 90", "Assists per 90", "xA per 90", "Shots per 90", "Shots on target per 90", "Touches in box per 90", "Offensive duels won per 90",
                            "Shot efficiency", "Aerial duels won per 90", "Aerial duels per 90", "Fouls suffered per 90", "Progressive runs per 90"]
    

class ExistentFieldPlayerColumn(Enum):
    HEIGHT = "Height"
    MATCHES_PLAYED = "Matches played"
    MINUTES_PLAYED = "Minutes played"
    GOALS = "Goals"
    XG = "xG"
    ASSISTS = "Assists"
    XA = "xA"
    DUELS_PER_90 = "Duels per 90"
    DUELS_WON_PERCENTAGE = "Duels won, %"
    SUCCESFUL_DEFENSIVE_ACTIONS_PER_90 = "Successful defensive actions per 90"
    DEFENSIVE_DUELS_PER_90 = "Defensive duels per 90"
    DEFENSIVE_DUELS_WON_PERCENTAGE = "Defensive duels won, %"
    AERIAL_DUELS_PER_90 = "Aerial duels per 90"
    AERIAL_DUELS_WON_PERCENTAGE = "Aerial duels won, %"
    SLIDING_TACKLES_PER_90 = "Sliding tackles per 90"
    POSSESION_ADJUSTED_SLIDING_TACKLES_PER_90 = "PAdj Sliding tackles"
    SHOTS_BLOCKED_PER_90 = "Shots blocked per 90"
    INTERCEPTIONS_PER_90 = "Interceptions per 90"
    POSSESION_ADJUSTED_INTERCEPTIONS_PER_90 = "PAdj Interceptions"
    FOULS_PER_90 = "Fouls per 90"
    YELLOW_CARDS = "Yellow cards"
    YELLOW_CARDS_PER_90 = "Yellow cards per 90"
    RED_CARDS = "Red cards"
    RED_CARDS_PER_90 = "Red cards per 90"
    SUCCESFUL_ATTACKING_ACTIONS_PER_90 = "Successful attacking actions per 90"
    GOALS_PER_90 = "Goals per 90"
    NON_PENALTY_GOALS = "Non-penalty goals"
    NON_PENALTY_GOALS_PER_90 = "Non-penalty goals per 90"
    XG_PER_90 = "xG per 90"
    HEAD_GOALS = "Head goals"
    HEAD_GOALS_PER_90 = "Head goals per 90"
    SHOTS = "Shots"
    SHOTS_PER_90 = "Shots per 90"
    SHOTS_ON_TARGET_PERCENTAGE = "Shots on target, %"
    GOAL_CONVERSION_PERCENTAGE = "Goal conversion, %"
    ASSISTS_PER_90 = "Assists per 90"
    CROSSES_PER_90 = "Crosses per 90"
    ACCURATE_CROSSES_PERCENTAGE = "Accurate crosses, %"
    CROSSES_FROM_LEFT_FLANK_PER_90 = "Crosses from left flank per 90"
    ACCURATE_CROSSES_FROM_LEFT_FLANK_PERCENTAGE = "Accurate crosses from left flank, %"
    CROSSES_FROM_RIGHT_FLANK_PER_90 = "Crosses from right flank per 90"
    ACCURATE_CROSSES_FROM_RIGHT_FLANK_PERCENTAGE = "Accurate crosses from right flank, %"
    CROSSES_TO_BOX_PER_90 = "Crosses to goalie box per 90"
    DRIBBLES_PER_90 = "Dribbles per 90"
    SUCCESFUL_DRIBBLES_PERCENTAGE = "Successful dribbles, %"
    OFFENSIVE_DUELS_PER_90 = "Offensive duels per 90"
    OFFENSIVE_DUELS_WON_PERCENTAGE = "Offensive duels won, %"
    TOUCHES_IN_BOX_PER_90 = "Touches in box per 90"
    PROGRESSIVE_RUNS_PER_90 = "Progressive runs per 90"
    ACCELERATIONS_PER_90 = "Accelerations per 90"
    RECEIVED_PASSES_PER_90 = "Received passes per 90"
    RECEIVED_LONG_PASSES_PER_90 = "Received long passes per 90"
    FOULS_SUFFERED_PER_90 = "Fouls suffered per 90"
    PASSES_PER_90 = "Passes per 90"
    ACCURATE_PASSES_PERCENTAGE = "Accurate passes, %"
    FORWARD_PASSES_PER_90 = "Forward passes per 90"
    ACCURATE_FORWARD_PASSES_PERCENTAGE = "Accurate forward passes, %"
    BACK_PASSES_PER_90 = "Back passes per 90"
    ACCURATE_BACK_PASSES_PERCENTAGE = "Accurate back passes, %"
    SHORT_MEDIUM_PASSES_PER_90 = "Short / medium passes per 90"
    ACCURATE_SHORT_MEDIUM_PASSES_PERCENTAGE = "Accurate short / medium passes, %"
    LONG_PASSES_PER_90 = "Long passes per 90"
    ACCURATE_LONG_PASSES_PERCENTAGE = "Accurate long passes, %"
    AVERAGE_PASS_LENGTH = "Average pass length, m"
    AVERAGE_LONG_PASS_LENGTH = "Average long pass length, m"
    XA_PER_90 = "xA per 90"
    SHOT_ASSISTS_PER_90 = "Shot assists per 90"
    SECOND_ASSISTS_PER_90 = "Second assists per 90"
    THIRD_ASSISTS_PER_90 = "Third assists per 90"
    SMART_PASSES_PER_90 = "Smart passes per 90"
    ACCURATE_SMART_PASSES_PERCENTAGE = "Accurate smart passes, %"
    KEY_PASSES_PER_90 = "Key passes per 90"
    PASSES_TO_FINAL_THIRD_PER_90 = "Passes to final third per 90"
    ACCURATE_PASSES_TO_FINAL_THIRD_PERCENTAGE = "Accurate passes to final third, %"
    PASSES_TO_PENALTY_AREA_PER_90 = "Passes to penalty area per 90"
    ACCURATE_PASSES_TO_PENALTY_AREA_PER_90 = "Accurate passes to penalty area per 90"
    ACCURATE_PASSES_TO_PENALTY_AREA_PERCENTAGE = "Accurate passes to penalty area, %"
    THROUGH_PASSES_PER_90 = "Through passes per 90"
    ACCURATE_THROUGH_PASSES_PERCENTAGE = "Accurate through passes, %"
    DEEP_COMPLETIONS_PER_90 = "Deep completions per 90"
    DEEP_COMPLETED_CROSSES_PER_90 = "Deep completed crosses per 90"
    PROGRESSIVE_PASSES_PER_90 = "Progressive passes per 90"
    ACCURATE_PROGRESSIVE_PASSES_PERCENTAGE = "Accurate progressive passes, %"
    VERTICAL_PASSES_PER_90 = "Vertical passes per 90"
    ACCURATE_VERTICAL_PASSES_PERCENTAGE = "Accurate vertical passes, %"
    FREE_KICKS_PER_90 = "Free kicks per 90"
    DIRECT_FREE_KICKS_PER_90 = "Direct free kicks per 90"
    DIRECT_FREE_KICKS_ON_TARGET_PERCENTAGE = "Direct free kicks on target, %"
    CORNERS_PER_90 = "Corners per 90"
    PENALTIES = "Penalties taken"
    PENALTIES_CONVERTED_PERCENTAGE = "Penalty conversion, %"

    def __str__(self):
        return self.name.replace("_", " ").title()
    
    @classmethod
    def all_values(cls):
        excluded_values = {"Matches played", "Minutes played"}
        return [item.value for item in cls if item.value not in excluded_values]

    @classmethod
    def values_for_similarity(cls):
        excluded_values = {
            "Yellow cards per 90", 
            "Red cards per 90", 
            "Corners per 90", 
            "Direct free kicks per 90", 
            "Free kicks per 90",
            "xG per 90",
            "Goals per 90",
            "Assists per 90",
            "xA per 90",
            "Head goals per 90",
            "Shot assists per 90",
            "Second assists per 90",
            "Third assists per 90"
            "Shot efficiency"
        }
        
        return [item.value for item in cls if (item.value.endswith("per 90") or item.value == "Height") and item.value not in excluded_values]
 

class ExistentGoalkeeperColumn(Enum):
    CONCEDED_GOALS = "Conceded goals"
    CONCEDED_GOALS_PER_90 = "Conceded goals per 90"
    SHOTS_AGAINST = "Shots against"
    SHOTS_AGAINST_PER_90 = "Shots against per 90"
    CLEAN_SHEETS = "Clean sheets"
    SAVE_RATE_PERCENTAGE = "Save rate, %"
    XG_AGAINST = "xG against"
    XG_AGAINST_PER_90 = "xG against per 90"
    PREVENTED_GOALS = "Prevented goals"
    PREVENTED_GOALS_PER_90 = "Prevented goals per 90"
    BACK_PASSES_RECEIVED_AS_GK_PER_90 = "Back passes received as GK per 90"
    EXITS_PER_90 = "Exits per 90"
    AERIAL_DUELS_PER_90 = "Aerial duels per 90"

    def __str__(self):
        return self.name.replace("_", " ").title()
    
    @classmethod
    def all_values(cls):
        return [item.value for item in cls]
    
class ToCreateColumns(Enum):
    SHOT_EFFICIENCY = "Shot efficiency"
    DUELS_WON_PER_90 = "Duels won per 90"
    DEFENSIVE_DUELS_WON_PER_90 = "Defensive duels won per 90"
    AERIAL_DUELS_WON_PER_90 = "Aerial duels won per 90"
    SHOTS_ON_TARGET_PER_90 = "Shots on target per 90"
    ACCURATE_CROSSES_PER_90 = "Accurate crosses per 90"
    ACCURATE_CROSSES_FROM_LEFT_FLANK_PER_90 = "Accurate crosses from left flank per 90"
    ACCURATE_CROSSES_FROM_RIGHT_FLANK_PER_90 = "Accurate crosses from right flank per 90"
    SUCCESFUL_DRIBBLES_PER_90 = "Succesful dribbles per 90"
    OFFENSIVE_DUELS_WON_PER_90 = "Offensive duels won per 90"
    ACCURATE_PASSES_PER_90 = "Accurate passes per 90"
    ACCURATE_FORWARD_PASSES_PER_90 = "Accurate forward passes per 90"
    ACCURATE_BACK_PASSES_PER_90 = "Accurate back passes per 90"
    ACCURATE_SHORT_MEDIUM_PASSES_PER_90 = "Accurate short medium passes per 90"
    ACCURATE_LONG_PASSES_PER_90 = "Accurate long passes per 90"
    ACCURATE_SMART_PASSES_PER_90 = "Accurate smart passes per 90"
    ACCURATE_PASSES_TO_FINAL_THIRD_PER_90 = "Accurate passes to final third per 90"
    ACCURATE_PASSES_TO_PENALTY_AREA_PER_90 = "Accurate passes to penalty area per 90"
    ACCURATE_THROUGH_PASSES_PER_90 = "Accurate through passes per 90"
    ACCURATE_PROGRESSIVE_PASSES_PER_90 = "Accurate progressive passes per 90"
    ACCURATE_VERTICAL_PASSES_PER_90 = "Accurate vertical passes per 90"
    DIRECT_FREE_KICKS_ON_TARGET_PER_90 = "Direct free kicks on target per 90"

    def __str__(self):
            return self.name.replace("_", " ").title()

class ColumnMapping:
    COLUMN_MAPPING = {
        ToCreateColumns.DUELS_WON_PER_90.value: (
            ExistentFieldPlayerColumn.DUELS_PER_90.value,
            ExistentFieldPlayerColumn.DUELS_WON_PERCENTAGE.value
        ),
        ToCreateColumns.DEFENSIVE_DUELS_WON_PER_90.value: (
            ExistentFieldPlayerColumn.DEFENSIVE_DUELS_PER_90.value,
            ExistentFieldPlayerColumn.DEFENSIVE_DUELS_WON_PERCENTAGE.value
        ),
        ToCreateColumns.AERIAL_DUELS_WON_PER_90.value: (
            ExistentFieldPlayerColumn.AERIAL_DUELS_PER_90.value,
            ExistentFieldPlayerColumn.AERIAL_DUELS_WON_PERCENTAGE.value
        ),
        ToCreateColumns.SHOTS_ON_TARGET_PER_90.value: (
            ExistentFieldPlayerColumn.SHOTS_PER_90.value,
            ExistentFieldPlayerColumn.SHOTS_ON_TARGET_PERCENTAGE.value
        ),
        ToCreateColumns.ACCURATE_CROSSES_PER_90.value: (
            ExistentFieldPlayerColumn.CROSSES_PER_90.value,
            ExistentFieldPlayerColumn.ACCURATE_CROSSES_PERCENTAGE.value
        ),
        ToCreateColumns.ACCURATE_CROSSES_FROM_LEFT_FLANK_PER_90.value: (
            ExistentFieldPlayerColumn.CROSSES_FROM_LEFT_FLANK_PER_90.value,
            ExistentFieldPlayerColumn.ACCURATE_CROSSES_FROM_LEFT_FLANK_PERCENTAGE.value
        ),
        ToCreateColumns.ACCURATE_CROSSES_FROM_RIGHT_FLANK_PER_90.value: (
            ExistentFieldPlayerColumn.CROSSES_FROM_RIGHT_FLANK_PER_90.value,
            ExistentFieldPlayerColumn.ACCURATE_CROSSES_FROM_RIGHT_FLANK_PERCENTAGE.value
        ),
        ToCreateColumns.SUCCESFUL_DRIBBLES_PER_90.value: (
            ExistentFieldPlayerColumn.DRIBBLES_PER_90.value,
            ExistentFieldPlayerColumn.SUCCESFUL_DRIBBLES_PERCENTAGE.value
        ),
        ToCreateColumns.OFFENSIVE_DUELS_WON_PER_90.value: (
            ExistentFieldPlayerColumn.OFFENSIVE_DUELS_PER_90.value,
            ExistentFieldPlayerColumn.OFFENSIVE_DUELS_WON_PERCENTAGE.value
        ),
        ToCreateColumns.ACCURATE_PASSES_PER_90.value: (
            ExistentFieldPlayerColumn.PASSES_PER_90.value,
            ExistentFieldPlayerColumn.ACCURATE_PASSES_PERCENTAGE.value
        ),
        ToCreateColumns.ACCURATE_FORWARD_PASSES_PER_90.value: (
            ExistentFieldPlayerColumn.FORWARD_PASSES_PER_90.value,
            ExistentFieldPlayerColumn.ACCURATE_FORWARD_PASSES_PERCENTAGE.value
        ),
        ToCreateColumns.ACCURATE_BACK_PASSES_PER_90.value: (
            ExistentFieldPlayerColumn.BACK_PASSES_PER_90.value,
            ExistentFieldPlayerColumn.ACCURATE_BACK_PASSES_PERCENTAGE.value
        ),
        ToCreateColumns.ACCURATE_SHORT_MEDIUM_PASSES_PER_90.value: (
            ExistentFieldPlayerColumn.SHORT_MEDIUM_PASSES_PER_90.value,
            ExistentFieldPlayerColumn.ACCURATE_SHORT_MEDIUM_PASSES_PERCENTAGE.value
        ),
        ToCreateColumns.ACCURATE_LONG_PASSES_PER_90.value: (
            ExistentFieldPlayerColumn.LONG_PASSES_PER_90.value,
            ExistentFieldPlayerColumn.ACCURATE_LONG_PASSES_PERCENTAGE.value
        ),
        ToCreateColumns.ACCURATE_SMART_PASSES_PER_90.value: (
            ExistentFieldPlayerColumn.SMART_PASSES_PER_90.value,
            ExistentFieldPlayerColumn.ACCURATE_SMART_PASSES_PERCENTAGE.value
        ),
        ToCreateColumns.ACCURATE_PASSES_TO_FINAL_THIRD_PER_90.value: (
            ExistentFieldPlayerColumn.PASSES_TO_FINAL_THIRD_PER_90.value,
            ExistentFieldPlayerColumn.ACCURATE_PASSES_TO_FINAL_THIRD_PERCENTAGE.value
        ),
        ToCreateColumns.ACCURATE_PASSES_TO_PENALTY_AREA_PER_90.value: (
            ExistentFieldPlayerColumn.PASSES_TO_PENALTY_AREA_PER_90.value,
            ExistentFieldPlayerColumn.ACCURATE_PASSES_TO_PENALTY_AREA_PERCENTAGE.value
        ),
        ToCreateColumns.ACCURATE_THROUGH_PASSES_PER_90.value: (
            ExistentFieldPlayerColumn.THROUGH_PASSES_PER_90.value,
            ExistentFieldPlayerColumn.ACCURATE_THROUGH_PASSES_PERCENTAGE.value
        ),
        ToCreateColumns.ACCURATE_PROGRESSIVE_PASSES_PER_90.value: (
            ExistentFieldPlayerColumn.PROGRESSIVE_PASSES_PER_90.value,
            ExistentFieldPlayerColumn.ACCURATE_PROGRESSIVE_PASSES_PERCENTAGE.value
        ),
        ToCreateColumns.ACCURATE_VERTICAL_PASSES_PER_90.value: (
            ExistentFieldPlayerColumn.VERTICAL_PASSES_PER_90.value,
            ExistentFieldPlayerColumn.ACCURATE_VERTICAL_PASSES_PERCENTAGE.value
        ),
        ToCreateColumns.DIRECT_FREE_KICKS_ON_TARGET_PER_90.value: (
            ExistentFieldPlayerColumn.DIRECT_FREE_KICKS_PER_90.value,
            ExistentFieldPlayerColumn.DIRECT_FREE_KICKS_ON_TARGET_PERCENTAGE.value
        ),
    }


