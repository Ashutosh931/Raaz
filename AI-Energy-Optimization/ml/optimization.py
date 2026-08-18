"""
Smart Energy Optimization & Recommendation Engine
Provides dynamic, physically grounded energy conservation advice and interactive simulation calculations.
"""

from typing import List, Dict, Any

def generate_smart_recommendations(
    hour: int = 14,
    temperature: float = 30.0,
    humidity: float = 60.0,
    people: int = 2,
    appliance_level: str = "medium",
    predicted_kwh: float = 4.5,
    tariff: float = 8.0,
    currency: str = "₹"
) -> List[Dict[str, Any]]:
    """
    Dynamically generates personalized energy-saving recommendations
    based on current ambient weather, time of day, occupancy, and predicted load.
    """
    recommendations = []
    
    # 1. Peak Hour Management (18:00 - 22:00 / 6 PM - 10 PM)
    if 18 <= hour <= 22:
        saved_kwh_mo = round(1.8 * 30, 1)  # ~54 kWh/month
        saved_cost_mo = round(saved_kwh_mo * tariff, 2)
        recommendations.append({
            "id": "peak_hour_shift",
            "title": "Shift Heavy Appliances Away from Peak Hours (6 PM - 10 PM)",
            "category": "Load Shifting",
            "impact": "High",
            "badge_color": "danger",
            "icon": "bi-lightning-charge-fill",
            "description": "Electricity grid demand peaks during evening hours. Defer running washing machines, dishwashers, and water pumps until after 10:00 PM or during morning off-peak hours.",
            "action": "Schedule laundry and water pumping before 5 PM or after 10 PM.",
            "kwh_saved_monthly": saved_kwh_mo,
            "money_saved_monthly": saved_cost_mo,
            "currency": currency
        })

    # 2. HVAC & Air Conditioning Optimization
    if temperature >= 28.0:
        saved_kwh_mo = round(predicted_kwh * 0.22 * 24 * 30 * 0.15, 1)
        saved_cost_mo = round(saved_kwh_mo * tariff, 2)
        recommendations.append({
            "id": "ac_thermostat",
            "title": "Set Air Conditioner Thermostat to 24°C - 26°C",
            "category": "Cooling Efficiency",
            "impact": "High",
            "badge_color": "warning",
            "icon": "bi-snow",
            "description": f"Ambient temperature is {temperature}°C. Every 1°C increase in AC temperature setting saves approximately 6% of cooling electricity. Pair with a ceiling fan for optimal comfort.",
            "action": "Raise AC temperature from 18°C/20°C to 24°C and ensure doors/windows are sealed.",
            "kwh_saved_monthly": max(35.0, saved_kwh_mo),
            "money_saved_monthly": max(280.0, saved_cost_mo),
            "currency": currency
        })
        
    if humidity >= 70.0 and temperature >= 26.0:
        recommendations.append({
            "id": "ac_dry_mode",
            "title": "Switch AC to 'Dry Mode' During High Humidity",
            "category": "Humidity Control",
            "impact": "Medium",
            "badge_color": "info",
            "icon": "bi-droplet-half",
            "description": f"High humidity ({humidity}%) makes the air feel warmer. Operating the AC in 'Dry Mode' removes excess moisture while consuming up to 25% less compressor power than continuous cooling.",
            "action": "Use Dry Mode (Dehumidification) on your air conditioner.",
            "kwh_saved_monthly": round(25.0, 1),
            "money_saved_monthly": round(25.0 * tariff, 2),
            "currency": currency
        })
    elif temperature < 16.0:
        recommendations.append({
            "id": "heating_efficiency",
            "title": "Targeted Space Heating & Insulation",
            "category": "Heating Efficiency",
            "impact": "Medium",
            "badge_color": "warning",
            "icon": "bi-fire",
            "description": f"Cold ambient temperature ({temperature}°C) increases heating load. Heat only occupied rooms and utilize thick curtains to block thermal drafts.",
            "action": "Seal window gaps and use programmable radiant heaters.",
            "kwh_saved_monthly": round(30.0, 1),
            "money_saved_monthly": round(30.0 * tariff, 2),
            "currency": currency
        })

    # 3. High Appliance Usage Optimization
    if str(appliance_level).lower() == "high":
        recommendations.append({
            "id": "stagger_loads",
            "title": "Stagger High-Wattage Appliance Operation",
            "category": "Demand Management",
            "impact": "High",
            "badge_color": "danger",
            "icon": "bi-cpu",
            "description": "High appliance intensity detected. Running microwave ovens, electric geysers, induction cooktops, and irons simultaneously causes high current draw and spikes maximum demand tariffs.",
            "action": "Operate high-wattage equipment sequentially rather than simultaneously.",
            "kwh_saved_monthly": round(40.0, 1),
            "money_saved_monthly": round(40.0 * tariff, 2),
            "currency": currency
        })

    # 4. Standby & Phantom Power Elimination
    if hour >= 23 or hour <= 6 or predicted_kwh > 5.0:
        saved_kwh_mo = round(0.4 * 24 * 30 * 0.35, 1)  # ~100 kWh/mo
        saved_cost_mo = round(saved_kwh_mo * tariff, 2)
        recommendations.append({
            "id": "vampire_draw",
            "title": "Eliminate Standby 'Vampire' Power Draw",
            "category": "Standby Power",
            "impact": "Medium",
            "badge_color": "success",
            "icon": "bi-plug-fill",
            "description": "Televisions, gaming consoles, microwave clocks, and laptop chargers continuously draw standby power even when turned off, accounting for 8–10% of residential bills.",
            "action": "Use smart power strips or switch off socket switches when appliances are idle.",
            "kwh_saved_monthly": max(20.0, saved_kwh_mo),
            "money_saved_monthly": max(160.0, saved_cost_mo),
            "currency": currency
        })

    # 5. Lighting & Occupancy Optimization
    if people >= 3 or (18 <= hour <= 23):
        recommendations.append({
            "id": "led_lighting",
            "title": "Switch to Energy Star LED Lighting & Motion Sensors",
            "category": "Lighting Efficiency",
            "impact": "Medium",
            "badge_color": "primary",
            "icon": "bi-lightbulb-fill",
            "description": "Replace older CFL or incandescent bulbs with high-efficiency 9W-12W LEDs. LEDs consume 80% less electricity and produce negligible waste heat.",
            "action": "Install LED bulbs in common areas and hallways.",
            "kwh_saved_monthly": round(18.0, 1),
            "money_saved_monthly": round(18.0 * tariff, 2),
            "currency": currency
        })

    # 6. Refrigerator & Appliance Maintenance
    recommendations.append({
        "id": "refrigerator_maintenance",
        "title": "Maintain Refrigerator Efficiency & Defrost Coils",
        "category": "Appliance Maintenance",
        "impact": "Low",
        "badge_color": "secondary",
        "icon": "bi-gear-wide-connected",
        "description": "Ensure the refrigerator door gasket has a tight seal and maintain 3°C–5°C for the fridge and -18°C for the freezer. Clean dust off rear condenser coils every 6 months.",
        "action": "Avoid placing hot food inside and leave 2 inches clearance around the fridge.",
        "kwh_saved_monthly": round(12.0, 1),
        "money_saved_monthly": round(12.0 * tariff, 2),
        "currency": currency
    })

    return recommendations

class EnergySavingSimulator:
    """
    Interactive Energy Saving Simulator model that computes monthly
    kWh and monetary savings based on user conservation selections.
    """
    
    @staticmethod
    def calculate_simulation(
        baseline_monthly_kwh: float = 240.0,
        tariff_per_kwh: float = 8.0,
        reduce_ac_pct: float = 0.0,
        reduce_lighting_pct: float = 0.0,
        reduce_appliances_pct: float = 0.0,
        shift_peak_pct: float = 0.0,
        eliminate_standby: bool = False
    ) -> Dict[str, Any]:
        """
        Calculates projected savings based on energy component proportions.
        
        Typical Residential Component Weightages:
        - HVAC / Cooling: 42%
        - Major Appliances & Laundry: 24%
        - Lighting: 14%
        - Peak Load Grid Strain: 12%
        - Standby Phantom Load: 8%
        """
        baseline_kwh = max(10.0, float(baseline_monthly_kwh))
        tariff = max(0.5, float(tariff_per_kwh))
        
        # Component baselines
        ac_base = baseline_kwh * 0.42
        appliance_base = baseline_kwh * 0.24
        lighting_base = baseline_kwh * 0.14
        peak_base = baseline_kwh * 0.12
        standby_base = baseline_kwh * 0.08
        
        # Savings
        saved_ac = ac_base * (min(50.0, max(0.0, float(reduce_ac_pct))) / 100.0)
        saved_appliances = appliance_base * (min(50.0, max(0.0, float(reduce_appliances_pct))) / 100.0)
        saved_lighting = lighting_base * (min(50.0, max(0.0, float(reduce_lighting_pct))) / 100.0)
        saved_peak = peak_base * (min(50.0, max(0.0, float(shift_peak_pct))) / 100.0)
        saved_standby = standby_base * 0.85 if eliminate_standby else 0.0
        
        total_kwh_saved = saved_ac + saved_appliances + saved_lighting + saved_peak + saved_standby
        total_kwh_saved = min(baseline_kwh * 0.65, total_kwh_saved)  # Realistic upper bound cap at 65%
        
        projected_kwh = baseline_kwh - total_kwh_saved
        baseline_cost = baseline_kwh * tariff
        projected_cost = projected_kwh * tariff
        money_saved = total_kwh_saved * tariff
        percentage_saved = (total_kwh_saved / baseline_kwh) * 100.0
        
        return {
            "baseline_monthly_kwh": round(baseline_kwh, 1),
            "baseline_monthly_cost": round(baseline_cost, 2),
            "projected_monthly_kwh": round(projected_kwh, 1),
            "projected_monthly_cost": round(projected_cost, 2),
            "total_kwh_saved": round(total_kwh_saved, 1),
            "money_saved_monthly": round(money_saved, 2),
            "money_saved_yearly": round(money_saved * 12, 2),
            "percentage_saved": round(percentage_saved, 1),
            "breakdown": {
                "cooling_saved_kwh": round(saved_ac, 1),
                "appliances_saved_kwh": round(saved_appliances, 1),
                "lighting_saved_kwh": round(saved_lighting, 1),
                "peak_shift_saved_kwh": round(saved_peak, 1),
                "standby_saved_kwh": round(saved_standby, 1)
            }
        }
