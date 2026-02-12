from __future__ import annotations

from dataclasses import dataclass

from ....native import NativeTaikoDifficultyAttributes
from .base import DifficultyAttributes


@dataclass
class TaikoDifficultyAttributes(DifficultyAttributes):
    """Difficulty attributes for osu!taiko mode.

    Attributes:
        mechanical_difficulty: The difficulty corresponding to the mechanical
            skills in osu!taiko. This includes colour and stamina combined.
        rhythm_difficulty: The difficulty corresponding to the rhythm skill.
        reading_difficulty: The difficulty corresponding to the reading skill.
        colour_difficulty: The difficulty corresponding to the colour skill.
        stamina_difficulty: The difficulty corresponding to the stamina skill.
        mono_stamina_factor: The ratio of stamina difficulty from mono-color
            (single colour) streams to total stamina difficulty.
        consistency_factor: The factor corresponding to the consistency of a map.
        stamina_top_strains: The top stamina strains.
    """

    mechanical_difficulty: float
    rhythm_difficulty: float
    reading_difficulty: float
    colour_difficulty: float
    stamina_difficulty: float
    mono_stamina_factor: float
    consistency_factor: float
    stamina_top_strains: float

    @classmethod
    def from_native(cls, native: NativeTaikoDifficultyAttributes) -> TaikoDifficultyAttributes:
        return cls(
            star_rating=native.starRating,
            max_combo=native.maxCombo,
            mechanical_difficulty=native.mechanicalDifficulty,
            rhythm_difficulty=native.rhythmDifficulty,
            reading_difficulty=native.readingDifficulty,
            colour_difficulty=native.colourDifficulty,
            stamina_difficulty=native.staminaDifficulty,
            mono_stamina_factor=native.monoStaminaFactor,
            consistency_factor=native.consistencyFactor,
            stamina_top_strains=native.staminaTopStrains,
        )
