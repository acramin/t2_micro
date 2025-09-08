"""
Utility functions for D&D calculations
"""

import random

def calculate_modifier(score):
    """Calculate ability modifier from score: (score - 10) // 2"""
    return (score - 10) // 2

def calculate_proficiency_bonus(level):
    """Calculate proficiency bonus based on level (D&D 5e standards)"""
    if level < 5:
        return 2
    elif level < 9:
        return 3
    elif level < 13:
        return 4
    elif level < 17:
        return 5
    else:
        return 6

def validate_ability_score(score):
    """Validate ability score is between 1 and 30"""
    return max(1, min(30, score))

# utils/calculations.py (add this function)
def roll_dice(dice_type, count=1):
    """Roll dice of the specified type"""
    if dice_type == 100:  # Special case for d100 (percentile)
        return random.randint(1, 100)
    else:
        return sum(random.randint(1, dice_type) for _ in range(count))