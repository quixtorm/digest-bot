"""Pydantic schemas for structured LLM output (used with client.messages.parse)."""
from pydantic import BaseModel


class Solution(BaseModel):
    description: str
    stack_and_apis: str
    first_step_tonight: str


class Problem(BaseModel):
    title: str
    explanation: str  # simple, school-student-level language
    solution_obvious: Solution
    solution_creative: Solution


class FieldAnalysis(BaseModel):
    problems: list[Problem]


class ImprovementItem(BaseModel):
    title: str
    description: str


class ImprovementsOutput(BaseModel):
    items: list[ImprovementItem]
