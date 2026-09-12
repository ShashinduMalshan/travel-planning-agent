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
from functools import cached_property

from google.adk.agents import LlmAgent
from google.adk.apps import App
from google.adk.models import Gemini
from google.adk.tools import agent_tool
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.adk.tools import url_context
from google.genai import Client


class GlobalGemini(Gemini):
    """Pins the Vertex AI client to the `global` location or uses local API key."""

    @cached_property
    def api_client(self) -> Client:
        if os.environ.get("GEMINI_API_KEY"):
            return Client(api_key=os.environ.get("GEMINI_API_KEY"))
        return Client(vertexai=True, location="global")


flight_research_agent_url_context_agent = LlmAgent(
    name="Flight_Research_Agent_url_context_agent",
    model=GlobalGemini(model="gemini-3.5-flash"),
    description="Agent specialized in fetching content from URLs.",
    sub_agents=[],
    instruction="Use the UrlContextTool to retrieve content from provided URLs.",
    tools=[url_context],
)

flight_research_agent_google_search_agent = LlmAgent(
    name="Flight_Research_Agent_google_search_agent",
    model=GlobalGemini(model="gemini-3.5-flash"),
    description="Agent specialized in performing Google searches.",
    sub_agents=[],
    instruction="Use the GoogleSearchTool to find information on the web.",
    tools=[GoogleSearchTool()],
)

flight_research_agent = LlmAgent(
    name="flight_research_agent",
    model=GlobalGemini(model="gemini-3.5-flash"),
    description=(
        "Finds and summarizes suitable flight options based on destination, travel dates, budget, and user preferences."
    ),
    sub_agents=[],
    instruction=(
        "You are a Flight Research Agent.\n"
        "Your job is only to research and summarize flight options.\n"
        "Return flight findings to the Travel Planning Coordinator Agent.\n"
        "Negative Constraints:\n"
        "- You must not produce the final travel plan.\n"
        "- You must not say the trip planning is complete.\n"
        "- You must not include hotel or itinerary recommendations.\n"
        "Your output should include:\n"
        "- 2 to 3 flight options\n"
        "- airline\n"
        "- estimated price\n"
        "- duration\n"
        "- direct or one-stop\n"
        "- pros and cons\n"
        "- recommended flight option\n"
        "- note that prices are estimates"
    ),
    tools=[
        agent_tool.AgentTool(agent=flight_research_agent_url_context_agent),
        agent_tool.AgentTool(agent=flight_research_agent_google_search_agent),
    ],
)

hotel_and_itinerary_agent_google_search_agent = LlmAgent(
    name="Hotel_And_Itinerary_Agent_google_search_agent",
    model=GlobalGemini(model="gemini-3.5-flash"),
    description="Agent specialized in performing Google searches.",
    sub_agents=[],
    instruction="Use the GoogleSearchTool to find information on the web.",
    tools=[GoogleSearchTool()],
)

hotel_and_itinerary_agent_url_context_agent = LlmAgent(
    name="Hotel_And_Itinerary_Agent_url_context_agent",
    model=GlobalGemini(model="gemini-3.5-flash"),
    description="Agent specialized in fetching content from URLs.",
    sub_agents=[],
    instruction="Use the UrlContextTool to retrieve content from provided URLs.",
    tools=[url_context],
)

hotel_and_itinerary_agent = LlmAgent(
    name="hotel_and_itinerary_agent",
    model=GlobalGemini(model="gemini-3.5-flash"),
    description=(
        "Researches hotel areas, accommodation options, and creates a simple day-by-day itinerary for business trips."
    ),
    sub_agents=[],
    instruction=(
        "You are a Hotel and Itinerary Agent.\n\n"
        "Your job is only to suggest accommodation areas, hotel options, and a simple day-by-day itinerary.\n\n"
        "Return your findings to the Travel Planning Coordinator Agent.\n\n"
        "You must not produce the final travel plan.\n"
        "You must not research flights.\n\n"
        "Your output should include:\n"
        "- recommended area to stay\n"
        "- 2 to 3 hotel or accommodation suggestions\n"
        "- estimated nightly cost\n"
        "- why the area is suitable for business travel\n"
        "- 3-day itinerary\n"
        "- estimated local transport and food costs"
    ),
    tools=[
        agent_tool.AgentTool(agent=hotel_and_itinerary_agent_google_search_agent),
        agent_tool.AgentTool(agent=hotel_and_itinerary_agent_url_context_agent),
    ],
)

root_agent = LlmAgent(
    name="Travel_Planning_Coordinator_Agent",
    model=GlobalGemini(model="gemini-3.5-flash"),
    description=(
        "coordinator travel  Coordinates travel planning by understanding the user's trip requirements, "
        "asking missing questions, delegating flight and hotel/itinerary research, and producing a final travel plan."
    ),
    sub_agents=[flight_research_agent, hotel_and_itinerary_agent],
    instruction=(
        "You are the Travel Planning Coordinator Agent.\n\n"
        "Your job is to create complete, practical travel plans for users by coordinating specialist agents.\n\n"
        "The user does not know about your internal specialist agents. Do not ask the user to mention agents, tools, transfers, or internal workflow steps.\n\n"
        "Core responsibility:\n"
        "When the user asks for a complete trip plan, business trip plan, vacation plan, travel plan, or itinerary, you must gather both:\n"
        "1. Flight information\n"
        "2. Hotel/accommodation and itinerary information\n\n"
        "Specialist agents:\n"
        "- Use the Flight Research Agent for flight options.\n"
        "- Use the Hotel and Itinerary Agent for accommodation, stay-area recommendations, and day-by-day itinerary suggestions.\n\n"
        "Internal orchestration rule:\n"
        "For every complete travel planning request, you must use both specialist agents before giving the final response.\n\n"
        "Workflow:\n"
        "1. Read the user's travel request.\n"
        "2. Identify origin, destination, trip duration, travel period, number of travelers, budget, and preferences.\n"
        "3. If essential information is missing, ask a short follow-up question.\n"
        "4. Transfer to the Flight Research Agent to collect flight options.\n"
        "5. After receiving flight information, transfer to the Hotel and Itinerary Agent to collect hotel/stay suggestions and a day-by-day itinerary.\n"
        "6. After both specialist agents have provided their findings, combine the results into one complete final travel plan.\n"
        "7. Check the plan against the user's budget and preferences.\n"
        "8. Provide the final answer to the user.\n\n"
        "Before giving the final answer, confirm that you have:\n"
        "- Flight options\n"
        "- Recommended flight choice\n"
        "- Hotel or stay-area recommendation\n"
        "- 3-day itinerary or itinerary matching the requested duration\n"
        "- Estimated budget breakdown\n"
        "- Final recommendation\n"
        "- Important notes about price estimates and availability\n\n"
        "If any of these are missing, call the relevant specialist agent before answering.\n\n"
        "Rules:\n"
        "- Do not answer with only flight information.\n"
        "- Do not answer with only hotel or itinerary information.\n"
        "- Do not let one specialist agent's response become the final answer.\n"
        "- Do not mention internal agent names in the final user-facing answer.\n"
        "- Do not claim that bookings are confirmed.\n"
        "- Do not invent exact live prices if the tools do not provide them.\n"
        "- Clearly mark prices as estimates when necessary.\n"
        "- If the budget is unrealistic, explain the trade-offs clearly.\n"
        "- Prefer practical, realistic recommendations over overly broad lists.\n"
        "- Keep the final answer organized and easy to read."
    ),
    tools=[],
)

app = App(
    root_agent=root_agent,
    name="app",
)
