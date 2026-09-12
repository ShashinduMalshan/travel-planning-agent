# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import google.auth
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from .tools import (
    get_flight_suggestions,
    get_hotel_recommendations,
    generate_itinerary,
    calculate_budget_breakdown,
)

try:
    _, project_id = google.auth.default()
    if project_id:
        os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
        os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
except Exception:
    pass

MODEL = "gemini-3.7-flash"

instruction = """You are a professional Business Travel Planning Agent.
Your goal is to help users plan efficient and budget-aware business trips.

For every request, you must:
1. Extract or ask for: Origin, Destination, Duration (in days), Total Budget, Travel Purpose, Preferences.
2. Provide Flight Suggestions with estimated prices.
3. Provide Hotel Recommendations within the budget, highlighting business amenities.
4. Generate a structured daily Itinerary based on the purpose.
5. Provide a Budget Breakdown showing how the funds are allocated across flight, hotel, and per diem.

Safety and Clarity Rules:
- All prices and availability MUST be explicitly marked as estimates.
- Do NOT claim bookings or reservations are confirmed.
- Keep recommendations practical, realistic, and strictly within the user's allocated budget.
"""

root_agent = Agent(
    name="travel_planning_agent",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=instruction,
    tools=[
        get_flight_suggestions,
        get_hotel_recommendations,
        generate_itinerary,
        calculate_budget_breakdown,
    ],
)

app = App(
    root_agent=root_agent,
    name="app",
)
