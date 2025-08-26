"""
Comprehensive structured output schemas for MTG LLM testing.
This module defines Pydantic models for various MTG-specific structured outputs.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Union
from enum import Enum

# === Generic Answer Types ===

class SimpleAnswer(BaseModel):
    """Simple yes/no or short answer"""
    answer: str = Field(..., description="Simple answer")

class NumericAnswer(BaseModel):
    """Numeric answer"""
    value: int = Field(..., description="Numeric value")

class BooleanAnswer(BaseModel):
    """Boolean yes/no answer"""
    answer: Literal["yes", "no"] = Field(..., description="Boolean answer (yes/no)")

class ExplanationAnswer(BaseModel):
    """Detailed explanation"""
    explanation: str = Field(..., description="Detailed explanation")

# === MTG-Specific Answer Types ===

class CardName(str, Enum):
    """Common MTG card names for validation"""
    # This will be dynamically populated based on scenarios
    pass

class CardSelectionAnswer(BaseModel):
    """Answer for card selection from a specific list"""
    selected_card: str = Field(..., description="Selected card name from the provided options")
    
    @classmethod
    def with_options(cls, options: List[str]):
        """Create a dynamic model with specific card options validation"""
        class DynamicCardSelectionAnswer(BaseModel):
            selected_card: str = Field(..., description="Selected card name", enum=options)
        return DynamicCardSelectionAnswer

class MultipleCardSelectionAnswer(BaseModel):
    """Answer for selecting multiple cards from a list"""
    selected_cards: List[str] = Field(..., description="List of selected card names", min_items=1)

class CombatAssignmentAnswer(BaseModel):
    """Answer for combat damage assignment"""
    damage_assignment: int = Field(..., description="Damage assigned to opponent", ge=0)
    blockers: List[str] = Field(..., description="List of blocking creatures")

class ManaCostAnswer(BaseModel):
    """Answer for mana cost calculations"""
    mana_cost: str = Field(..., description="Mana cost in standard MTG format (e.g., '2WW', '3B')")

class PhaseAnswer(BaseModel):
    """Answer for phase identification"""
    phase: Literal[
        "untap", "upkeep", "draw", "main1", "combat", 
        "beginning_of_combat", "declare_attackers", "declare_blockers", 
        "combat_damage", "end_of_combat", "main2", "end", "cleanup"
    ] = Field(..., description="Game phase")

class TurnStepAnswer(BaseModel):
    """Answer for turn step identification"""
    step: Literal["beginning", "main", "combat", "ending"] = Field(..., description="Turn step")

class CardTypeAnswer(BaseModel):
    """Answer for card type identification"""
    card_type: Literal[
        "creature", "instant", "sorcery", "enchantment", 
        "artifact", "land", "planeswalker", "tribal"
    ] = Field(..., description="Card type")

class ZoneAnswer(BaseModel):
    """Answer for zone identification"""
    zone: Literal[
        "hand", "battlefield", "graveyard", "exile", 
        "library", "stack", "command"
    ] = Field(..., description="Game zone")

class PriorityAnswer(BaseModel):
    """Answer for priority/pass decisions"""
    action: Literal["pass", "cast", "activate", "trigger"] = Field(..., description="Priority action")

class DraftPickAnswer(BaseModel):
    """Answer for draft pick decisions"""
    pick: str = Field(..., description="Card to pick in draft")
    reason: Optional[str] = Field(None, description="Reason for the pick")

# === Dynamic Schema Factory ===

class SchemaFactory:
    """Factory for creating dynamic schemas based on scenario requirements"""
    
    @staticmethod
    def create_card_selection_schema(options: List[str]) -> type:
        """Create a schema that constrains selection to specific card options"""
        class DynamicCardSelection(BaseModel):
            selected_card: str = Field(
                ..., 
                description="Selected card from the provided options",
                enum=options
            )
        return DynamicCardSelection
    
    @staticmethod
    def create_multiple_choice_schema(choices: List[str]) -> type:
        """Create a schema for multiple choice questions"""
        class DynamicMultipleChoice(BaseModel):
            answer: str = Field(
                ..., 
                description="Selected answer from the provided choices",
                enum=choices
            )
        return DynamicMultipleChoice
    
    @staticmethod
    def create_boolean_schema() -> type:
        """Create a schema for boolean yes/no questions"""
        class DynamicBoolean(BaseModel):
            answer: Literal["yes", "no"] = Field(
                ..., 
                description="Boolean answer (yes/no)"
            )
        return DynamicBoolean
    
    @staticmethod
    def create_numeric_range_schema(min_val: int = 0, max_val: int = 100) -> type:
        """Create a schema for numeric answers within a range"""
        class DynamicNumericRange(BaseModel):
            value: int = Field(
                ..., 
                description="Numeric value within specified range",
                ge=min_val,
                le=max_val
            )
        return DynamicNumericRange

# === Schema Registry ===

SCHEMA_REGISTRY = {
    "simple": SimpleAnswer,
    "numeric": NumericAnswer,
    "boolean": BooleanAnswer,
    "explanation": ExplanationAnswer,
    "card_selection": CardSelectionAnswer,
    "multiple_card_selection": MultipleCardSelectionAnswer,
    "combat_assignment": CombatAssignmentAnswer,
    "mana_cost": ManaCostAnswer,
    "phase": PhaseAnswer,
    "turn_step": TurnStepAnswer,
    "card_type": CardTypeAnswer,
    "zone": ZoneAnswer,
    "priority": PriorityAnswer,
    "draft_pick": DraftPickAnswer,
}