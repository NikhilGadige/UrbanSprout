import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# ---------------------------------------------------------------------------
# Disease Treatment Fallbacks
# ---------------------------------------------------------------------------
FALLBACK_TREATMENTS = {
    "Tomato Late Blight": """
### Disease Overview
**Tomato Late Blight** is caused by *Phytophthora infestans*. It thrives in cool, wet weather and can destroy plants within days, turning leaves, stems, and fruits dark brown.

### Recommended Treatments
* **Fungicides**: Apply **Mancozeb**, **Chlorothalonil**, or **Copper hydroxide** immediately.
* **Systemic Options**: For active infections, use **Metalaxyl** or **Mefenoxam**.
* **Organic**: Weekly **Bacillus subtilis** or Copper octanoate sprays.

### Prevention
* Space plants 24+ inches apart and prune lower branches for air circulation.
* Water at the base — never overhead.
* Rotate away from tomatoes/potatoes for 3+ years.
""",
    "Tomato Leaf Mold": """
### Disease Overview
**Tomato Leaf Mold** (*Passalora fulva*) creates olive-green fuzzy patches on leaf undersides, causing yellowing and defoliation. Common in humid, enclosed spaces like balcony gardens.

### Recommended Treatments
* **Fungicides**: **Chlorothalonil**, **Mancozeb**, or **Difenoconazole** at first sign.
* **Bio-fungicides**: **Bacillus amyloliquefaciens** weekly.
* **Organic**: Wettable sulfur to reduce spore density.

### Prevention
* Keep humidity below 85% — use fans on your balcony/terrace.
* Plant certified leaf-mold-resistant varieties.
* Remove and dispose of all infected plant debris.
""",
    "Powdery Mildew": """
### Disease Overview
**Powdery Mildew** is a fungal disease producing white, powdery spots on leaves and stems. Extremely common in container gardens due to poor air circulation. Affects cucumbers, squash, beans, roses, and many herbs.

### Recommended Treatments
* **Organic Spray**: Mix 1 tsp baking soda + 1 tsp neem oil + 1L water. Spray weekly.
* **Milk Spray**: 40% milk, 60% water. Spray on affected leaves — proven effective.
* **Potassium Bicarbonate**: Commercial organic fungicide, very effective.

### Prevention
* Space containers to allow airflow between plants.
* Avoid wetting foliage when watering.
* Remove infected leaves immediately to stop spread.
""",
    "Aphid Infestation": """
### Disease Overview
**Aphids** are tiny soft-bodied insects that cluster on new growth, sucking plant sap. They cause curled, yellowed leaves and secrete sticky honeydew that attracts sooty mold. Common on terrace-grown roses, chillies, and tomatoes.

### Recommended Treatments
* **Neem Oil Spray**: 5ml cold-pressed neem + 1ml dish soap per liter water. Spray every 5 days.
* **Water Jet**: Blast aphids off with strong water spray — works well on sturdy plants.
* **Insecticidal Soap**: Diluted dish soap spray suffocates aphids on contact.

### Prevention
* Introduce companion plants: marigold, basil, and nasturtium repel aphids naturally.
* Inspect new growth weekly — catch early before colonies establish.
* Avoid over-fertilizing with nitrogen, which produces soft growth aphids love.
""",
    "Root Rot": """
### Disease Overview
**Root Rot** is caused by overwatering and poor drainage, leading to fungal pathogens (*Pythium*, *Phytophthora*) destroying root tissue. Leaves yellow, wilt, and drop. A very common problem in container gardening.

### Recommended Treatments
* **Immediate Action**: Remove plant from pot, trim all black/mushy roots with sterilized scissors.
* **Hydrogen Peroxide**: Water with diluted H2O2 (1 part 3% H2O2 to 3 parts water) to oxygenate soil.
* **Repot**: Use fresh, well-draining mix with added perlite (30%).

### Prevention
* Always use pots with drainage holes — no exceptions.
* Water only when top inch of soil is dry.
* Add 20-30% perlite to potting mix for aeration.
""",
    "Default Healthy": """
### Plant Health Status: Excellent
Your plant looks healthy with no visible signs of infection or pest damage.

### Suggested Care
* **Nutrition**: Apply balanced liquid fertilizer every 2-3 weeks during growing season.
* **Watering**: Water deeply but infrequently — let soil breathe between waterings.
* **Pruning**: Remove dry or yellowing lower leaves to keep airflow good.

### Proactive Prevention
* Apply diluted neem oil spray once every 3 weeks as a natural pest repellent.
* Check leaf undersides weekly for early signs of mites, aphids, or fungal spots.
"""
}

# ---------------------------------------------------------------------------
# Planner Fallbacks
# ---------------------------------------------------------------------------
FALLBACK_PLANNER_PLANTS = [
    {"name": "Cherry Tomatoes", "emoji": "🍅", "difficulty": "Easy", "days_to_harvest": 60, "why_it_fits": "Thrives in containers with 6+ hours sun. Very rewarding for beginners."},
    {"name": "Basil", "emoji": "🌿", "difficulty": "Easy", "days_to_harvest": 25, "why_it_fits": "Grows anywhere with 4+ hours sun. Ready to harvest in weeks."},
    {"name": "Spinach", "emoji": "🥬", "difficulty": "Easy", "days_to_harvest": 30, "why_it_fits": "Perfect for partial shade. Fast-growing and nutritious."},
    {"name": "Chilli Peppers", "emoji": "🌶️", "difficulty": "Medium", "days_to_harvest": 75, "why_it_fits": "Loves heat and full sun. Produces abundantly in containers."},
    {"name": "Mint", "emoji": "🌱", "difficulty": "Easy", "days_to_harvest": 30, "why_it_fits": "Extremely low maintenance. Spreads quickly — keep in its own pot."},
    {"name": "Coriander", "emoji": "🌿", "difficulty": "Easy", "days_to_harvest": 21, "why_it_fits": "Grows fast in any container. Harvest leaves continuously."},
    {"name": "Spring Onions", "emoji": "🧅", "difficulty": "Easy", "days_to_harvest": 35, "why_it_fits": "Minimal space needed. Can regrow from kitchen scraps."},
    {"name": "Lettuce", "emoji": "🥗", "difficulty": "Easy", "days_to_harvest": 45, "why_it_fits": "Prefers partial shade. Great for window boxes and small containers."},
]
FALLBACK_PLANNER_TIPS = [
    "Start with herbs (basil, coriander, mint) — they're forgiving and give you quick wins.",
    "Use light-colored pots in hot climates to prevent root overheating.",
    "Group plants by water needs so you can water efficiently."
]

# ---------------------------------------------------------------------------
# Companion Planting Fallbacks
# ---------------------------------------------------------------------------
FALLBACK_COMPANIONS = {
    "tomato": {
        "companions": [
            {"plant": "Basil", "reason": "Repels aphids, whiteflies, and tomato hornworms. Also said to improve tomato flavor."},
            {"plant": "Marigold", "reason": "Deters nematodes in soil and repels many common pests."},
            {"plant": "Parsley", "reason": "Attracts predatory insects that eat tomato pests."},
            {"plant": "Carrot", "reason": "Loosens soil around tomato roots, improving drainage."},
        ],
        "avoid": [
            {"plant": "Fennel", "reason": "Inhibits tomato growth through allelopathic chemicals."},
            {"plant": "Cabbage", "reason": "Competes aggressively for nutrients and stunts both plants."},
            {"plant": "Corn", "reason": "Attracts the tomato fruit worm, which also attacks corn."},
        ]
    },
    "default": {
        "companions": [
            {"plant": "Marigold", "reason": "A universal companion — deters pests and attracts pollinators for almost any plant."},
            {"plant": "Basil", "reason": "Natural pest repellent, benefits most vegetables and herbs."},
            {"plant": "Nasturtium", "reason": "Acts as a trap crop, luring aphids away from your main plants."},
        ],
        "avoid": [
            {"plant": "Fennel", "reason": "Fennel is allelopathic — it inhibits the growth of most plants around it."},
            {"plant": "Wormwood", "reason": "Releases chemicals that can stunt nearby plants."},
        ]
    }
}


def _get_model(api_key=None):
    """Returns a configured Gemini model, or None if no valid API key.

    A per-request `api_key` (supplied by the end user) takes priority over the
    owner's optional .env key so that public usage runs on the user's own quota.
    """
    key = (api_key or GEMINI_API_KEY or "").strip()
    is_demo_key = not key or "placeholder" in key.lower()
    if is_demo_key:
        return None
    try:
        genai.configure(api_key=key)
        return genai.GenerativeModel("gemini-1.5-flash")
    except Exception as e:
        print(f"[GEMINI] Model init failed: {e}")
        return None


def _call_gemini(prompt, fallback_fn, api_key=None):
    """Calls Gemini with a prompt, falling back to fallback_fn() on any failure."""
    model = _get_model(api_key)
    if model:
        try:
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text
        except Exception as e:
            print(f"[GEMINI] Call failed: {e}")
    return fallback_fn()


# ---------------------------------------------------------------------------
# 1. Disease Treatment (original, updated branding)
# ---------------------------------------------------------------------------
def generate_treatment_advice(disease_name, api_key=None):
    def fallback():
        for key, content in FALLBACK_TREATMENTS.items():
            if key.lower() in disease_name.lower():
                return content
        if "healthy" in disease_name.lower():
            return FALLBACK_TREATMENTS["Default Healthy"]
        return f"""
### Disease Overview
Your plant shows signs of **{disease_name}**. This condition disrupts the plant's cellular systems, often triggered by excess humidity, poor airflow, or contaminated soil.

### Recommended Treatments
* **Broad-Spectrum Fungicide**: Apply **Copper oxychloride** or **Mancozeb** (2g per liter) on all foliage.
* **Organic Option**: Cold-pressed **Neem Oil** (5ml/L with dish soap) to coat all leaf surfaces.
* **Systemic Backup**: If symptoms persist after 5 days, use **Carbendazim** or **Hexaconazole**.

### Prevention
* Remove all infected leaves immediately and dispose of them away from the garden.
* Water at the base only — never wet the foliage.
* Improve airflow by spacing containers further apart.
"""

    prompt = f"""
You are UrbanSprout AI, an expert plant pathologist and urban gardening advisor.
Provide a detailed, practical treatment guide for the plant condition: "{disease_name}".

Format using Markdown with exactly these sections:

### Disease Overview
(Explain what this condition is, what causes it, and visual symptoms — 2-3 sentences)

### Recommended Treatments
(3-4 specific bullet points with exact product names like Neem Oil, Mancozeb, Bacillus subtilis, baking soda spray, etc. Mention application rates where known)

### Prevention
(3-4 actionable bullet points focused on container/urban gardening: airflow, watering habits, soil, spacing)

Keep the tone helpful and accessible to home gardeners.
"""
    return _call_gemini(prompt, fallback, api_key)


# ---------------------------------------------------------------------------
# 2. Space Planner
# ---------------------------------------------------------------------------
def generate_planner_advice(city, sqft, sunlight_hours, space_type, api_key=None):
    def fallback():
        return json.dumps({
            "plants": FALLBACK_PLANNER_PLANTS[:6],
            "tips": FALLBACK_PLANNER_TIPS
        })

    prompt = f"""
You are UrbanSprout AI, an expert in urban and terrace gardening.

The user has the following setup:
- City: {city}
- Available space: {sqft} sq ft
- Direct sunlight: {sunlight_hours} hours/day
- Space type: {space_type} (balcony / terrace / window sill / indoor)

Return a JSON object (no markdown, just raw JSON) with this exact structure:
{{
  "plants": [
    {{
      "name": "Plant Name",
      "emoji": "🌱",
      "difficulty": "Easy|Medium|Hard",
      "days_to_harvest": 45,
      "why_it_fits": "One sentence explaining why this plant suits their specific setup"
    }}
  ],
  "tips": ["Tip 1 tailored to their setup", "Tip 2", "Tip 3"]
}}

Return 8-10 plants ranked from easiest to most rewarding. Consider the city's climate, sunlight hours, and space constraints. Use relevant emojis. Return ONLY valid JSON, no extra text.
"""
    raw = _call_gemini(prompt, fallback, api_key)
    # Try to parse JSON, fall back to default if malformed
    try:
        # Strip markdown code fences if Gemini wraps in ```json
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("```")[1]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:]
        return cleaned.strip()
    except Exception:
        return fallback()


# ---------------------------------------------------------------------------
# 3. Grow Calendar
# ---------------------------------------------------------------------------
def generate_grow_calendar(city, month, api_key=None):
    def fallback():
        return f"""
### Sow Now in {city}
- **Spinach** — Fast grower, ready in 30 days
- **Coriander** — Sow densely, harvest in 3 weeks
- **Methi (Fenugreek)** — Extremely easy, harvest leaves in 2-3 weeks
- **Spring Onions** — Can regrow from kitchen scraps in a glass of water

### Currently Growing — Care Tips
- **Tomatoes**: Check for early signs of leaf curl or yellowing. Feed with liquid fertilizer weekly.
- **Chillies**: Side-dress with compost. Ensure 6+ hours direct sunlight.
- **Herbs**: Pinch flower buds to keep basil and mint producing leaves longer.

### Ready to Harvest This Month
- Any leafy greens planted 3-4 weeks ago should be harvest-ready.
- Check your chilli plants — ripe chillies are firm and fully colored.
- Harvest herbs by cutting stems (not pulling), leaving the crown intact.

### Seasonal Tip
Use this month to plan your next rotation — what goes in when current plants finish.
"""

    prompt = f"""
You are UrbanSprout AI, an expert in urban gardening for Indian cities.

Create a practical monthly grow guide for a home/terrace gardener in {city} for the month of {month}.

Format using Markdown with exactly these sections:

### Sow Now in {city}
(List 4-6 plants perfect to start this month. For each: plant name in bold + one-line tip on sowing or growing)

### Currently Growing — Care Tips
(3-4 care reminders for plants that should currently be in mid-growth. Specific, actionable tips)

### Ready to Harvest This Month
(2-4 items that should be harvestable now, with harvest tips)

### Seasonal Tip
(One key insight about this time of year for urban gardening in this climate)

Be specific to {city}'s climate and the month {month}.
"""
    return _call_gemini(prompt, fallback, api_key)


# ---------------------------------------------------------------------------
# 4. Companion Planting
# ---------------------------------------------------------------------------
def generate_companion_suggestions(plant_name, api_key=None):
    def fallback():
        key = plant_name.lower()
        data = FALLBACK_COMPANIONS.get(key, FALLBACK_COMPANIONS["default"])
        return json.dumps(data)

    prompt = f"""
You are UrbanSprout AI, an expert in companion planting for container and terrace gardens.

For the plant "{plant_name}", provide companion planting advice.

Return a JSON object (raw JSON only, no markdown) with this structure:
{{
  "companions": [
    {{"plant": "Plant Name", "reason": "Why they grow well together and specific benefit"}}
  ],
  "avoid": [
    {{"plant": "Plant Name", "reason": "Why they should NOT be planted together"}}
  ],
  "tips": ["Practical tip 1 about growing {plant_name} in containers", "Tip 2", "Tip 3"]
}}

Provide 4-6 good companions and 3 plants to avoid. Tips should be specific to container/urban gardening. Return ONLY valid JSON.
"""
    raw = _call_gemini(prompt, fallback, api_key)
    try:
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("```")[1]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:]
        return cleaned.strip()
    except Exception:
        return fallback()


# ---------------------------------------------------------------------------
# 5. Plant Container Guide
# ---------------------------------------------------------------------------
def generate_plant_guide(plant_name, api_key=None):
    def fallback():
        return f"""
### Growing {plant_name} in Containers

#### Pot Size
Use a container at least 20-30 cm deep and 25 cm wide. Larger is always better for root development.

#### Soil Mix
Combine: 40% good potting soil + 30% compost + 20% cocopeat + 10% perlite. This gives nutrients, moisture retention, and drainage.

#### Watering
Water when the top 1 inch of soil feels dry. In hot weather, this may be daily. In cool weather, every 2-3 days. Always water until it drains from the bottom.

#### Fertilizing
Feed with a balanced liquid fertilizer (NPK 10-10-10) every 2 weeks during active growth. Switch to a high-potassium feed once flowering starts.

#### Sunlight
Most vegetables and herbs need 5-8 hours of direct sunlight. Place on your sunniest balcony or terrace spot.

#### Common Problems
- **Yellowing leaves**: Usually nitrogen deficiency or overwatering. Check drainage first.
- **Wilting despite watering**: Check roots — possible root rot. Improve drainage immediately.
- **Slow growth**: Move to sunnier spot or increase feeding frequency.

#### Harvest Tips
Harvest regularly to encourage continuous production. Never let fruits fully over-ripen on the plant.
"""

    prompt = f"""
You are UrbanSprout AI, an expert in container gardening.

Write a complete container growing guide for "{plant_name}" targeting urban/terrace gardeners in India.

Format using Markdown with these sections:

### Growing {plant_name} in Containers

#### Pot Size
(Minimum size recommendation, material preference)

#### Soil Mix
(Specific recipe: percentages of potting soil, compost, cocopeat, perlite, etc.)

#### Watering
(Frequency, how to check moisture, signs of over/under watering)

#### Fertilizing
(What type, how often, when to switch from growth to fruiting feed)

#### Sunlight
(Hours required, placement tips for Indian balconies/terraces)

#### Common Problems
(3-4 bullet points with problem and quick fix)

#### Harvest Tips
(How and when to harvest for continuous production)

Be specific, practical, and written for beginner-to-intermediate urban gardeners.
"""
    return _call_gemini(prompt, fallback, api_key)


# ---------------------------------------------------------------------------
# 6. AI Plant Doctor Chat
# ---------------------------------------------------------------------------
def generate_plant_doctor_response(symptoms, plant_type="", api_key=None):
    plant_context = f" (plant: {plant_type})" if plant_type else ""

    def fallback():
        return f"""
### Diagnosis
Based on the symptoms described{plant_context}: **{symptoms[:80]}...**

The symptoms suggest possible issues with either **watering habits**, **nutrient deficiency**, or **pest activity**. These are the three most common causes of plant problems in container gardens.

### Severity
**Medium** — Act within 2-3 days to prevent further spread.

### Immediate Actions
1. **Check the soil**: Is it waterlogged or bone dry? Both extremes cause similar symptoms.
2. **Inspect leaf undersides**: Look for tiny moving dots (spider mites), clusters of small insects (aphids), or powdery residue.
3. **Check drainage**: Lift the pot — is water draining freely from the bottom?

### Treatment Plan
- If **overwatering**: Stop watering for 5-7 days, improve drainage, consider repotting.
- If **pests found**: Apply neem oil spray (5ml neem + 1ml dish soap per liter) every 3 days for 2 weeks.
- If **nutrient deficiency** (uniform yellowing): Apply balanced liquid fertilizer at half strength.

### Prevention
- Water only when the top inch of soil is dry.
- Inspect your plants weekly, especially leaf undersides.
- Maintain good airflow between containers.
"""

    prompt = f"""
You are UrbanSprout AI Plant Doctor, an expert in diagnosing home and terrace garden plant problems.

The user describes their problem: "{symptoms}"{plant_context}

Provide a helpful diagnosis in Markdown with exactly these sections:

### Diagnosis
(Most likely cause(s) based on the symptoms described. Be specific — name the condition/pest/deficiency)

### Severity
(One of: Low / Medium / High — and one sentence explaining why)

### Immediate Actions
(3-4 numbered steps the user should do RIGHT NOW)

### Treatment Plan
(Detailed treatment with organic options prioritized. Include product names, dilution rates where relevant)

### Prevention
(3 bullet points to prevent this from recurring)

Write as a knowledgeable but friendly advisor. The user is likely a beginner or intermediate home gardener.
"""
    return _call_gemini(prompt, fallback, api_key)


# ---------------------------------------------------------------------------
# 7. Composting Guide
# ---------------------------------------------------------------------------
def generate_composting_guide(scale="balcony", api_key=None):
    def fallback():
        return f"""
### Urban Composting for Your {scale.title()} Setup

#### What You Need
- A plastic bin or clay pot (10-20L for balcony, 50L+ for terrace)
- Kitchen scraps, dry leaves, and a little patience
- Optional: a handful of worms (vermicomposting) for faster results

#### What to Add (Greens + Browns)
**Greens** (nitrogen-rich): Vegetable peels, fruit scraps, tea leaves, coffee grounds, fresh herb trimmings
**Browns** (carbon-rich): Dry leaves, shredded newspaper, cardboard, eggshells, dry soil

**Golden ratio**: 2 parts brown : 1 part green

#### What to Avoid
- Cooked food, meat, fish, dairy — attracts pests and creates odor
- Oily or fatty food waste
- Diseased plant material
- Onion skins and citrus peels in large quantities (slows decomposition)

#### The Process
1. Layer browns and greens alternately in your bin
2. Keep it moist but not wet — like a wrung-out sponge
3. Turn or stir once a week with a stick
4. In 4-8 weeks: dark, crumbly, earthy-smelling compost is ready

#### Using Your Compost
Add 20-30% compost to any potting mix. Apply as top dressing every 4-6 weeks during growing season. Your plants will visibly respond within 2 weeks.

#### Troubleshooting
- **Smells bad**: Too wet or too many greens. Add dry leaves and turn.
- **Nothing happening**: Too dry. Sprinkle water and turn.
- **Fruit flies**: Cover food scraps with a layer of dry soil or brown material.
"""

    prompt = f"""
You are UrbanSprout AI, an expert in urban composting for Indian homes.

Write a practical composting guide for someone with a {scale} setup (balcony/terrace/indoor).

Format using Markdown with these sections:

### Urban Composting for Your {scale.title()} Setup

#### What You Need
(List of materials and containers appropriate for the scale — no large equipment)

#### What to Add (Greens + Browns)
(Clear list of what goes in with the 2:1 brown:green ratio explained)

#### What to Avoid
(Common mistakes in urban composting)

#### The Process
(Step-by-step numbered instructions)

#### Using Your Compost
(When it's ready, how to use it in containers)

#### Troubleshooting
(3-4 common problems with quick solutions)

Write for a city dweller with no prior composting experience.
"""
    return _call_gemini(prompt, fallback, api_key)
