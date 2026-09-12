# ✈️ Business Travel Planning Agent (Google ADK)

A professional AI-powered **Business Travel Planning Agent** built using the **Google Agent Development Kit (ADK)** and **Gemini 3.7 Flash**.

The agent is designed to help business travelers plan efficient, realistic, and budget-aware trips by gathering requirements, querying specialized travel tools, and generating an executive-ready 4-part travel package.

---

## 🌟 Key Features

The agent extracts and processes **6 Core Travel Parameters**:
1. **Origin City / Airport**
2. **Destination City / Airport**
3. **Trip Duration** (in days)
4. **Total Budget** (in USD)
5. **Purpose of Travel** (Conference, Client Meetings, Team Workshop, etc.)
6. **Traveler Preferences** (Cabin class, Wi-Fi, proximity to business district, etc.)

And delivers a structured **4-Part Travel Plan**:
- ✈️ **Flight Suggestions & Schedules:** Airline options, non-stop routes, departure/arrival timings, and estimated fares.
- 🏨 **Hotel Recommendations:** Accommodations selected for business amenities (fiber Wi-Fi, work desks, meeting facilities) within the nightly budget.
- 📅 **Day-by-Day Business Itinerary:** Balanced schedule with meeting slots, commute buffer times, and dinner recommendations.
- 💵 **Audited Budget Breakdown:** Itemized expense summary (Airfare + Lodging + Per Diem) with budget compliance validation.

---

## 🛡️ Built-in Safety & Guardrails

- **Estimates Only:** All pricing, airfare, and lodging rates are explicitly labeled as estimates.
- **No Booking Falsehoods:** The agent clearly discloses that it does not make direct reservations or confirmed bookings.
- **Budget Awareness:** Strictly checks that the total estimated trip expenses stay within the user's allocated budget, alerting if exceeded.

---

## 📁 Project Architecture

```
travel-planning-agent/
├── app/
│   ├── __init__.py            # App package entry point
│   ├── agent.py               # Main agent definition & instructions
│   ├── tools.py               # Modular tools (flights, hotels, itinerary, budget)
│   ├── fast_api_app.py        # FastAPI server backend with SSE streaming
│   └── app_utils/             # A2A protocol and telemetry helpers
├── tests/
│   └── unit/
│       └── test_tools.py      # Automated unit tests for all tools
├── .env                       # Local environment variables & API keys
├── .agents-cli-spec.md        # Agent specification & requirements
├── agents-cli-manifest.yaml   # Manifest for agents-cli tooling
├── pyproject.toml             # Python dependencies (managed via uv)
└── README.md                  # Project documentation
```

---

## 🧰 Modular Tool Functions (`app/tools.py`)

| Tool Function | Description |
| :--- | :--- |
| `get_flight_suggestions` | Searches available flight options, airlines, non-stop schedules, and estimated pricing. |
| `get_hotel_recommendations` | Finds business-ready lodging with work desks, high-speed Wi-Fi, and location advantages. |
| `generate_itinerary` | Builds a structured daily business agenda with arrival logistics, meetings, and dinners. |
| `calculate_budget_breakdown` | Computes itemized costs against total budget and checks financial compliance. |

---

## 🚀 Getting Started

### **Prerequisites**
- **Python 3.10+**
- **`uv`** (Fast Python package manager):
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **`agents-cli`** (Google Agents CLI):
  ```bash
  uv tool install google-agents-cli
  ```

---

### **1. Clone & Setup Environment**

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/travel-planning-agent.git
cd travel-planning-agent

# Install dependencies into virtual environment
uv sync
```

---

### **2. Configure API Key**

Create or edit your `.env` file in the project root:

```ini
# Get your free API key at: https://aistudio.google.com/apikey
GEMINI_API_KEY=AIzaSy...your-actual-api-key-here
```

*(Optional: If running via Google Cloud Vertex AI instead, uncomment the Vertex AI lines in `.env` and authenticate via `gcloud auth application-default login`)*.

---

## 💻 Running the Agent

### **Option 1: Interactive Web Playground (Recommended)**
Launch the local web-based playground with interactive chat and live tool inspection:

```bash
agents-cli playground
```
Open the URL printed in the terminal (e.g., `http://localhost:8000`) in your browser.

---

### **Option 2: Terminal CLI Execution**
Run single-turn prompts directly from your shell:

```bash
agents-cli run "Plan a 3-day business trip from NYC to San Francisco for a tech conference next month with a $2,500 budget."
```

---

### **Option 3: Run Automated Tests**
Run the unit test suite to verify all tools and calculations:

```bash
uv run pytest
```

---

## 💬 Example Prompt & Output

### **User Input:**
```text
1. Origin City: New York (JFK)
2. Destination City: San Francisco (SFO)
3. Duration of the Trip: 3 days
4. Total Budget: $2,500
5. Purpose of Travel: Google Cloud Conference & Partner Meetings
6. Preferences: Morning non-stop flights, downtown hotel with fast Wi-Fi and work desk
```

### **Agent Output Preview:**
```markdown
✈️ Flight Options & Schedule (Estimates)
- Airline: United Airlines (UA 240) | Route: JFK -> SFO | 08:30 AM -> 11:45 AM | Non-stop | $450.00
- Airline: Delta Air Lines (DL 482) | Route: JFK -> SFO | 01:15 PM -> 04:35 PM | Non-stop | $490.00

🏨 Hotel Recommendations (Estimates)
- Grand Hyatt San Francisco Downtown | $280/night | Dedicated Work Desk, Fiber Wi-Fi, Breakfast Included
- Marriott Marquis San Francisco | $220/night | Executive Lounge, High-Speed Wi-Fi, Fitness Center

📅 3-Day Business Itinerary
- Day 1: Flight arrival at 11:45 AM, check-in, afternoon conference badge pickup, welcome dinner.
- Day 2: 08:30 AM breakfast, 09:30 AM - 05:00 PM keynotes & partner meetings, 07:00 PM business dinner.
- Day 3: Morning wrap-up sessions, 01:00 PM hotel checkout, transit to SFO for evening return.

💵 Budget Breakdown (USD)
- Airfare: $450.00
- Lodging (2 nights @ $280/night): $560.00
- Per Diem / Meals / Transit (3 days @ $75/day): $225.00
- Total Estimated Cost: $1,235.00
- Status: ✅ Within Budget (Remaining Margin: $1,265.00)

*Disclaimer: All pricing and availability are estimates only. Bookings are not confirmed.*
```

---

## 📜 License
Apache-2.0 License - see the [LICENSE](LICENSE) file for details.
