from crewai import Agent, Task

# ✅ USE WORKING GROQ MODEL (CURRENT)
llm = "groq/llama-3.1-8b-instant" # groq open ai LLM model

# -----------------------------
# AGENTS
# -----------------------------
analysis_agent = Agent(
    role="Medical Analyzer",
    goal="Analyze blood report",
    backstory="Expert doctor",
    llm=llm,
    verbose=True
)

diet_agent = Agent(
    role="Diet Planner",
    goal="Suggest diet plan",
    backstory="Nutrition expert",
    llm=llm,
    verbose=True
)

exercise_agent = Agent(
    role="Exercise Planner",
    goal="Suggest exercise plan",
    backstory="Fitness trainer",
    llm=llm,
    verbose=True
)

# -----------------------------
# TASKS
# -----------------------------
def build_tasks(data):

    analysis_task = Task(
        description=f"""
Analyze this medical report:

{data}

Return STRICT JSON:
{{
  "analysis": {{
    "t3": {{"value": number, "status": "low/normal/high"}},
    "t4": {{"value": number, "status": "low/normal/high"}},
    "tsh": {{"value": number, "status": "low/normal/high"}},
    "vitamin_b12": {{"value": number, "status": "low/normal/high"}}
  }}
}}
""",
        agent=analysis_agent,
        expected_output="JSON analysis"
    )

    diet_task = Task(
        description=f"""
Based on this report:

{data}

Return JSON:
{{
  "diet": ["...", "..."]
}}
""",
        agent=diet_agent,
        expected_output="JSON diet"
    )

    exercise_task = Task(
        description=f"""
Based on this report:

{data}

Return JSON:
{{
  "exercise": ["...", "..."]
}}
""",
        agent=exercise_agent,
        expected_output="JSON exercise"
    )

    return [analysis_task, diet_task, exercise_task]