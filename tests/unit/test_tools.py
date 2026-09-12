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

from app.tools import (
    calculate_budget_breakdown,
    generate_itinerary,
    get_flight_suggestions,
    get_hotel_recommendations,
)


def test_get_flight_suggestions():
    result = get_flight_suggestions(
        origin="NYC",
        destination="SFO",
        departure_date="2026-10-15",
        return_date="2026-10-18",
        seat_class="Economy",
    )
    assert result["status"] == "success"
    assert len(result["flight_options"]) >= 2
    assert result["flight_options"][0]["estimated_price_usd"] > 0


def test_get_hotel_recommendations():
    result = get_hotel_recommendations(
        location="San Francisco Downtown",
        check_in_date="2026-10-15",
        check_out_date="2026-10-18",
        max_nightly_rate=300.0,
        preferences="high-speed wifi",
    )
    assert result["status"] == "success"
    assert len(result["hotel_recommendations"]) >= 2


def test_generate_itinerary():
    result = generate_itinerary(
        city="San Francisco",
        duration_days=3,
        travel_purpose="Tech Conference",
    )
    assert result["status"] == "success"
    assert len(result["itinerary"]) == 3


def test_calculate_budget_breakdown():
    result = calculate_budget_breakdown(
        flight_cost=450.0,
        hotel_nightly_rate=200.0,
        num_nights=3,
        daily_per_diem=75.0,
        total_budget=2000.0,
    )
    assert result["status"] == "success"
    assert result["is_within_budget"] is True
    assert result["total_estimated_cost_usd"] == 1350.0
