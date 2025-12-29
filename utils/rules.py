def soil_rules(soil_type, rainfall):
    if soil_type == "Clay" and rainfall > 150:
        return "Waterlogging Risk", "Clay soil retains water. Improve drainage with compost or sand."

    if soil_type == "Sandy" and rainfall < 50:
        return "Underwatered", "Sandy soil drains quickly. Increase watering frequency."

    return None, None

def pest_disease_rules(temperature, humidity):
    if humidity > 85 and temperature > 30:
        return "Pest Risk", "High heat and humidity favor pests. Inspect leaves and apply organic pesticides."

    return None, None

def nutrient_rules(n, p, k):
    if n < -0.5 or p < -0.5 or k < -0.5:
        return "Nutrient Deficiency", "Soil nutrients are low. Apply balanced organic fertilizer."

    if n > 1.5:
        return "Excess Nitrogen", "Too much nitrogen can harm plants. Reduce fertilizer application."

    return None, None

def vegetable_rules(crop):
    if crop in ["lettuce", "spinach", "pechay"]:
        return "High Water Demand", "Leafy vegetables need consistent moisture. Water regularly."

    if crop in ["tomato", "eggplant", "pepper"]:
        return "Pest Sensitive", "Check underside of leaves for pests like aphids."

    return None, None

def climate_rules(climate, soil_type):
    if climate == "Tropical Wet" and soil_type == "Clay":
        return "Flood Risk", "Frequent rain may cause root rot. Elevate beds or improve drainage."

    if climate == "Urban Heat Zone":
        return "Heat Stress", "Provide shade and water early morning or late afternoon."

    return None, None

def apply_rules(inputs):

    # 1. Climate + Soil (highest priority)
    if inputs["climate"] == "Tropical Wet" and inputs["soil_type"] == "Clay":
        return (
            "Flood / Waterlogging Risk",
            "High rainfall combined with clay soil causes poor drainage.",
            "Improve drainage using compost or sand and reduce watering."
        )

    # 2. Overwatering
    if inputs["rainfall"] > 200:
        return (
            "Overwatered",
            "Excessive rainfall increases soil moisture beyond safe levels.",
            "Reduce watering and ensure proper drainage."
        )

    # 3. Underwatering
    if inputs["rainfall"] < 40:
        return (
            "Underwatered",
            "Low rainfall indicates insufficient water supply.",
            "Increase watering frequency and apply mulch."
        )

    # 4. Pest risk
    if inputs["humidity"] > 85 and inputs["temperature"] > 30:
        return (
            "Pest Risk",
            "Warm and humid conditions favor pests and plant diseases.",
            "Inspect leaves regularly and use organic pest control."
        )

    # 5. Nutrient deficiency
    if inputs["n"] < -0.5 or inputs["p"] < -0.5 or inputs["k"] < -0.5:
        return (
            "Nutrient Deficiency",
            "Soil nutrient levels are below the recommended range.",
            "Apply balanced organic fertilizer."
        )

    return (
        "Healthy",
        "Environmental conditions are within acceptable ranges.",
        "Maintain current care and monitor regularly."
    )


def generate_growing_tips(inputs: dict, crop: str | None = None) -> list[str]:
    """Generate user-friendly growing tips based on inputs and optional crop.
    Always returns at least a few actionable tips so the UI never looks empty.
    """
    tips: list[str] = []

    soil = inputs.get("soil_type", "").strip()
    climate = inputs.get("climate", "").strip()
    ph = float(inputs.get("ph", 0))
    humidity = float(inputs.get("humidity", 0))
    temp = float(inputs.get("temperature", 0))
    rainfall = float(inputs.get("rainfall", 0))

    # pH guidance
    if ph < 6.0:
        tips.append(f"Your soil is acidic (pH {ph:g}). Consider adding agricultural lime to raise pH and improve nutrient uptake.")
    elif ph > 7.5:
        tips.append(f"Your soil is alkaline (pH {ph:g}). Add organic compost or elemental sulfur to gently lower pH over time.")
    else:
        tips.append(f"pH {ph:g} is within a healthy range for most crops. Maintain with regular organic matter additions (compost/mulch).")

    # Humidity guidance
    if humidity < 50:
        tips.append(f"Low humidity ({int(humidity)}%). Mulch and water deeply to reduce evaporation and maintain soil moisture.")
    elif humidity > 80:
        tips.append(f"High humidity ({int(humidity)}%). Improve air circulation and avoid overhead watering to reduce fungal risk.")
    else:
        tips.append("Humidity looks good. Water in the early morning so foliage dries quickly, limiting disease pressure.")

    # Temperature guidance
    if temp > 30:
        tips.append(f"Hot conditions ({temp:g}°C). Provide afternoon shade, increase mulching, and monitor for heat stress.")
    elif temp < 20:
        tips.append(f"Cool conditions ({temp:g}°C). Use row covers or cloches and choose cold-tolerant varieties.")
    else:
        tips.append("Temperature is optimal. Keep soil evenly moist and avoid drastic swings with consistent irrigation.")

    # Rainfall + soil type interplay
    if soil == "Clay" and rainfall > 150:
        tips.append("Clay soil with heavy rain can waterlog roots. Improve drainage with raised beds and coarse amendments.")
    elif soil == "Sandy" and rainfall < 100:
        tips.append("Sandy soil drains fast. Use frequent, smaller waterings and add compost to improve water retention.")
    elif soil == "Loam":
        tips.append("Loam is ideal. Maintain structure by avoiding compaction and topping up organic matter each season.")

    # Climate specifics
    if climate == "Tropical Wet":
        tips.append("In tropical wet climates, space plants generously and prune to airflow; consider disease-resistant cultivars.")
    elif climate == "Tropical Dry":
        tips.append("In tropical dry climates, prioritize drought-tolerant crops and schedule irrigation to match crop stages.")
    elif climate == "Urban Heat Zone":
        tips.append("Urban heat zones run warmer; add shade cloth and monitor containers which heat/dry faster.")

    # Crop-specific general guidance (basic heuristics)
    crop_key = (crop or "").strip().lower()
    if crop_key:
        if crop_key in {"rice"}:
            tips.append("Rice prefers consistent moisture; avoid nutrient spikes, keep pH near neutral, and manage standing water carefully.")
        elif crop_key in {"tomato", "eggplant", "pepper", "chili"}:
            tips.append("Solanaceae tip: stake early, remove lower leaves, and water at soil level to limit leaf diseases.")
        elif crop_key in {"lettuce", "spinach", "pechay", "bok choy"}:
            tips.append("Leafy greens benefit from steady moisture and partial shade in hot weather to prevent bolting.")
        elif crop_key in {"maize", "corn"}:
            tips.append("Corn needs nitrogen and consistent water during tasseling/silking; plant blocks (not rows) for better pollination.")

    # Ensure a minimum number of tips and unique messages
    # Remove duplicates while preserving order
    seen = set()
    unique_tips = []
    for t in tips:
        if t not in seen:
            unique_tips.append(t)
            seen.add(t)

    # Guarantee at least three tips
    if len(unique_tips) < 3:
        unique_tips.append("General: Keep a 2–3 cm mulch layer, water deeply but less often, and inspect plants weekly for early issue detection.")
    if len(unique_tips) < 4:
        unique_tips.append("Fertilization: Use balanced, slow-release or organic fertilizers and avoid overfeeding to prevent imbalances.")

    return unique_tips
