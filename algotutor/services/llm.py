"""LLM service for CB Algorithm Tutor."""

import json
from typing import Dict, List, Optional, Any
from algotutor.core.config import settings

# Make OpenAI optional so the app can start without the package
try:
    from openai import OpenAI  # type: ignore
except Exception:  # ImportError or other environment issues
    OpenAI = None  # type: ignore


class LLMService:
    """Service for LLM interactions using OpenAI."""
    
    def __init__(self):
        # Lazily initialize client; tolerate missing SDK in non-LLM paths
        self.client = None
        self.model = settings.model_name
        if OpenAI is not None and settings.openai_api_key:
            try:
                self.client = OpenAI(api_key=settings.openai_api_key)
            except Exception:
                # If initialization fails (e.g., bad key), keep client as None
                self.client = None
        
    def generate_socratic_question(self, code: str, problem: str, context: str) -> str:
        """Generate a Socratic question to guide learning."""
        if self.client is None:
            return "What invariant or data structure could simplify your approach?"
        system_prompt = """You are a Socratic algorithm tutor. Your role is to guide students 
        through understanding algorithms by asking probing questions rather than giving direct answers.
        
        When analyzing student code, ask questions that help them:
        1. Identify the problem they're trying to solve
        2. Understand the approach they're taking
        3. Recognize patterns and inefficiencies
        4. Think through edge cases
        5. Consider alternative approaches
        
        Keep questions focused, specific, and encouraging."""
        
        user_prompt = f"""
        Problem: {problem}
        Student's current code:
        ```python
        {code}
        ```
        Context: {context}
        
        Generate a Socratic question to help guide this student's learning.
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=settings.max_tokens,
            temperature=settings.temperature
        )
        
        return response.choices[0].message.content.strip()
    
    def analyze_code_patterns(self, code: str) -> List[str]:
        """Analyze code to identify algorithm patterns."""
        if self.client is None:
            return []
        system_prompt = """You are an expert algorithm pattern analyzer. 
        Identify the algorithmic patterns, data structures, and techniques used in the given code.
        
        Return only a JSON array of pattern names, such as:
        ["two_pointer", "sliding_window", "dynamic_programming", "binary_search", "recursion", "backtracking"]
        
        Common patterns include:
        - two_pointer, sliding_window, prefix_sum
        - binary_search, binary_tree_traversal
        - dynamic_programming, memoization
        - recursion, backtracking, divide_and_conquer
        - graph_traversal, topological_sort
        - greedy, sorting
        """
        
        user_prompt = f"""
        Analyze this code and identify algorithmic patterns:
        ```python
        {code}
        ```
        
        Return only a JSON array of pattern names.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=200,
                temperature=0.2
            )
            
            patterns_json = response.choices[0].message.content.strip()
            patterns = json.loads(patterns_json)
            return patterns if isinstance(patterns, list) else []
        except (json.JSONDecodeError, Exception):
            return []
    
    def provide_line_by_line_feedback(self, code: str, problem: str) -> Dict[str, Any]:
        """Provide detailed line-by-line feedback on code."""
        if self.client is None:
            return {
                "overall_feedback": "LLM not configured; basic checks only.",
                "line_feedback": {},
                "suggestions": [],
                "patterns_used": [],
                "time_complexity": "Unknown",
                "space_complexity": "Unknown",
            }
        system_prompt = """You are an expert algorithm tutor providing line-by-line code feedback.
        Analyze the code and provide constructive feedback focusing on:
        
        1. Correctness and logic issues
        2. Efficiency and optimization opportunities  
        3. Code style and readability
        4. Algorithm pattern recognition
        5. Edge case handling
        
        Return feedback as JSON with this structure:
        {
            "overall_feedback": "General assessment and suggestions",
            "line_feedback": {
                "1": "Feedback for line 1",
                "3": "Feedback for line 3"
            },
            "suggestions": ["Suggestion 1", "Suggestion 2"],
            "patterns_used": ["pattern1", "pattern2"],
            "time_complexity": "O(n)",
            "space_complexity": "O(1)"
        }
        """
        
        user_prompt = f"""
        Problem: {problem}
        
        Code to analyze:
        ```python
        {code}
        ```
        
        Provide detailed line-by-line feedback in JSON format.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=settings.max_tokens,
                temperature=0.3
            )
            
            feedback_json = response.choices[0].message.content.strip()
            return json.loads(feedback_json)
        except (json.JSONDecodeError, Exception):
            return {
                "overall_feedback": "Unable to analyze code at this time",
                "line_feedback": {},
                "suggestions": [],
                "patterns_used": [],
                "time_complexity": "Unknown",
                "space_complexity": "Unknown"
            }
    
    def generate_hint(self, problem: str, current_code: str, hint_level: int = 1) -> str:
        """Generate progressive hints based on problem and current code."""
        if self.client is None:
            return "Consider the core pattern likely involved (e.g., hash map, two pointers)."
        hint_prompts = {
            1: "Provide a subtle hint about the approach without giving away the solution.",
            2: "Give a more direct hint about the algorithm or data structure to use.",
            3: "Provide a clearer direction including key insights needed to solve the problem."
        }
        
        system_prompt = f"""You are a helpful algorithm tutor. {hint_prompts.get(hint_level, hint_prompts[1])}
        
        Focus on guiding the student's thinking rather than providing complete solutions.
        Be encouraging and educational in your response."""
        
        user_prompt = f"""
        Problem: {problem}
        Student's current attempt:
        ```python
        {current_code}
        ```
        
        Provide a hint at level {hint_level}.
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()


# Global LLM service instance
llm_service = LLMService()
