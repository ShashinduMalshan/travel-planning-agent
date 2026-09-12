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

"""Tools for Business Travel Planning Agent."""

from typing import Any, Dict, List


def get_flight_suggestions(
    origin: str,
    destination: str,
    departure_date: str,
    return_date: str,
    seat_class: str,
) -> Dict[str, Any]:
    """Get flight options and price estimates for a business trip.

    Args:
        origin: Origin airport code or city (e.g., 'NYC', 'JFK', 'London').
        destination: Destination airport code or city (e.g., 'SFO', 'Tokyo').
        departure_date: Date of departure in YYYY-MM-DD format.
        return_date: Date of return in YYYY-MM-DD format.
        seat_class: Cabin class preference (e.g., 'Economy', 'Premium Economy', 'Business').

    Returns:
        Dictionary with flight suggestions, airlines, departure times, and estimated costs.
    """
    multiplier = {
        "economy": 1.0,
        "premium economy": 1.5,
        "business": 2.8,
        "first": 4.5,
    }.get(seat_class.lower().strip(), 1.0)
    
    base_fare = 450.0

    options = [
        {
            "airline": "United Airlines",
            "flight_number": "UA 240",
            "route": f"{origin} -> {destination}",
            "departure": f"{departure_date} 08:30 AM",
            "arrival": f"{departure_date} 11:45 AM",
            "flight_type": "Non-stop",
            "cabin_class": seat_class.title(),
            "estimated_price_usd": round(base_fare * multiplier, 2),
            "amenities": ["High-Speed Wi-Fi", "In-seat Power", "Complimentary Refreshments"],
        },
        {
            "airline": "Delta Air Lines",
            "flight_number": "DL 482",
            "route": f"{origin} -> {destination}",
            "departure": f"{departure_date} 01:15 PM",
            "arrival": f"{departure_date} 04:35 PM",
            "flight_type": "Non-stop",
            "cabin_class": seat_class.title(),
            "estimated_price_usd": round((base_fare + 40) * multiplier, 2),
            "amenities": ["Fast Free Wi-Fi", "Live TV", "Power at every seat"],
        },
    ]

    return {
        "status": "success",
        "origin": origin,
        "destination": destination,
        "flight_options": options,
        "note": "Prices and availability are estimates only.",
    }


def get_hotel_recommendations(
    location: str,
    check_in_date: str,
    check_out_date: str,
    max_nightly_rate: float,
    preferences: str,
) -> Dict[str, Any]:
    """Get hotel accommodation recommendations tailored for business travelers.

    Args:
        location: City or business district (e.g., 'San Francisco Downtown', 'Chicago Loop').
        check_in_date: Check-in date in YYYY-MM-DD format.
        check_out_date: Check-out date in YYYY-MM-DD format.
        max_nightly_rate: Maximum nightly budget in USD.
        preferences: Business preferences such as 'high-speed wifi', 'meeting rooms', 'quiet room'.

    Returns:
        Dictionary with hotel recommendations, business amenities, and estimated nightly rates.
    """
    hotels = [
        {
            "name": f"Grand Hyatt {location.title()} Center",
            "star_rating": 4.5,
            "estimated_nightly_rate_usd": min(280.0, max_nightly_rate),
            "distance_to_center": "0.3 miles",
            "business_amenities": [
                "Dedicated Work Desk",
                "High-Speed Fiber Wi-Fi",
                "24/7 Business Center",
                "Meeting Rooms",
            ],
            "breakfast_included": True,
        },
        {
            "name": f"Marriott Marquis {location.title()}",
            "star_rating": 4.0,
            "estimated_nightly_rate_usd": min(220.0, max_nightly_rate),
            "distance_to_center": "0.6 miles",
            "business_amenities": [
                "Executive Lounge Access",
                "Ergonomic Workspace",
                "High-Speed Wi-Fi",
                "Fitness Center",
            ],
            "breakfast_included": False,
        },
    ]

    return {
        "status": "success",
        "location": location,
        "check_in": check_in_date,
        "check_out": check_out_date,
        "hotel_recommendations": hotels,
        "note": "Prices and availability are estimates only.",
    }


def generate_itinerary(
    city: str,
    duration_days: int,
    travel_purpose: str,
) -> Dict[str, Any]:
    """Generate a structured day-by-day business itinerary.

    Args:
        city: Destination city name.
        duration_days: Number of days for the trip.
        travel_purpose: Purpose of the business trip (e.g., 'Tech Conference', 'Client Meetings').

    Returns:
        Dictionary with day-by-day business schedule, transit times, and dining recommendations.
    """
    daily_schedule = []
    for day in range(1, duration_days + 1):
        if day == 1:
            schedule = {
                "day": day,
                "title": "Arrival & Initial Meetings / Prep",
                "activities": [
                    "Morning: Flight arrival, transfer to hotel, check-in",
                    f"Afternoon: Registration / initial meetings for {travel_purpose}",
                    "Evening: Welcome reception or team dinner downtown",
                ],
            }
        elif day == duration_days:
            schedule = {
                "day": day,
                "title": "Wrap-up & Departure",
                "activities": [
                    "Morning: Final business sessions / debrief meetings",
                    "Afternoon: Hotel check-out, transit to airport",
                    "Evening: Return flight departure",
                ],
            }
        else:
            schedule = {
                "day": day,
                "title": f"Full Business Day {day} - {travel_purpose}",
                "activities": [
                    "08:30 AM: Breakfast & schedule review",
                    f"09:30 AM - 05:00 PM: Primary sessions & meetings for {travel_purpose}",
                    "07:00 PM: Business dinner / networking",
                ],
            }
        daily_schedule.append(schedule)

    return {
        "status": "success",
        "city": city.title(),
        "duration_days": duration_days,
        "purpose": travel_purpose,
        "itinerary": daily_schedule,
    }


def calculate_budget_breakdown(
    flight_cost: float,
    hotel_nightly_rate: float,
    num_nights: int,
    daily_per_diem: float,
    total_budget: float,
) -> Dict[str, Any]:
    """Calculate and audit the business trip budget breakdown.

    Args:
        flight_cost: Estimated flight cost in USD.
        hotel_nightly_rate: Estimated hotel nightly rate in USD.
        num_nights: Total number of hotel nights.
        daily_per_diem: Estimated daily food & local transit allowance in USD.
        total_budget: Total budget allocated by the user in USD.

    Returns:
        Dictionary containing itemized costs, total estimate, and budget compliance status.
    """
    total_hotel_cost = round(hotel_nightly_rate * num_nights, 2)
    total_per_diem = round(daily_per_diem * (num_nights + 1), 2)
    total_estimated = round(flight_cost + total_hotel_cost + total_per_diem, 2)
    margin = round(total_budget - total_estimated, 2)
    is_within = total_estimated <= total_budget

    return {
        "status": "success",
        "total_budget_usd": total_budget,
        "total_estimated_cost_usd": total_estimated,
        "remaining_margin_usd": margin,
        "is_within_budget": is_within,
        "breakdown": {
            "flight_cost_usd": round(flight_cost, 2),
            "hotel_cost_usd": total_hotel_cost,
            "hotel_nights": num_nights,
            "per_diem_usd": total_per_diem,
        },
        "disclaimer": "All figures are estimated and subject to change.",
    }
