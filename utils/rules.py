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
