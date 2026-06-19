import os
import json
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from disease import identify_crop_disease
from gemini import (
    generate_treatment_advice,
    generate_planner_advice,
    generate_grow_calendar,
    generate_companion_suggestions,
    generate_plant_guide,
    generate_plant_doctor_response,
    generate_composting_guide,
)

load_dotenv()

app = Flask(__name__)
# Allow the user-supplied API key headers through CORS preflight.
CORS(app, resources={r"/api/*": {"origins": "*"}},
     allow_headers=["Content-Type", "X-Gemini-Key", "X-HF-Key"])


def _gemini_key():
    """The Gemini key for this request: user-supplied header, else owner's .env key."""
    header_key = (request.headers.get("X-Gemini-Key") or "").strip()
    return header_key or os.getenv("GEMINI_API_KEY", "").strip()


def _hf_key():
    """The HuggingFace key for this request: user-supplied header, else owner's .env key."""
    header_key = (request.headers.get("X-HF-Key") or "").strip()
    return header_key or os.getenv("HUGGINGFACE_API_KEY", "").strip()


def _require_gemini_key():
    """Returns an error response tuple if no usable Gemini key is present, else None."""
    key = _gemini_key()
    if not key or "placeholder" in key.lower():
        return jsonify({
            "error": "A Gemini API key is required. Add your own key in Settings to use this tool.",
            "code": "NO_API_KEY",
        }), 401
    return None


@app.route("/", methods=["GET"])
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "online",
        "app": "UrbanSprout Backend API",
        "version": "2.0.0",
        "modules": [
            "disease_detection",
            "space_planner",
            "grow_calendar",
            "companion_planting",
            "plant_guide",
            "plant_doctor",
            "composting_guide",
        ]
    }), 200


# ---------------------------------------------------------------------------
# Module 4: Plant Disease Detector (kept from v1, updated)
# ---------------------------------------------------------------------------
@app.route("/api/detect", methods=["POST"])
def detect_disease():
    key_error = _require_gemini_key()
    if key_error:
        return key_error

    if "image" not in request.files:
        return jsonify({"error": "No image file uploaded"}), 400

    image_file = request.files["image"]
    if image_file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    try:
        image_bytes = image_file.read()
        mime_type = image_file.content_type or "image/jpeg"
        base64_encoded = base64.b64encode(image_bytes).decode("utf-8")
        image_base64 = f"data:{mime_type};base64,{base64_encoded}"

        analysis_result = identify_crop_disease(image_bytes, filename=image_file.filename, api_key=_hf_key())
        disease_name = analysis_result["disease"]
        confidence = analysis_result["confidence"]
        is_healthy = analysis_result["is_healthy"]
        method = analysis_result["method"]

        treatment_text = generate_treatment_advice(disease_name, api_key=_gemini_key())

        return jsonify({
            "disease": disease_name,
            "confidence": confidence,
            "is_healthy": is_healthy,
            "treatment": treatment_text,
            "image_base64": image_base64,
            "ai_source": method
        }), 200

    except Exception as e:
        print(f"[API ERROR] Disease detection failed: {e}")
        return jsonify({"error": f"AI model inference failed: {str(e)}"}), 500


# ---------------------------------------------------------------------------
# Module 1: Space Planner — What Can I Grow?
# ---------------------------------------------------------------------------
@app.route("/api/planner", methods=["POST"])
def space_planner():
    key_error = _require_gemini_key()
    if key_error:
        return key_error

    data = request.get_json(silent=True) or {}
    city = data.get("city", "").strip() or "Bangalore"
    sqft = data.get("sqft", 10)
    sunlight_hours = data.get("sunlight_hours", 4)
    space_type = data.get("space_type", "balcony").strip()

    try:
        raw = generate_planner_advice(city, sqft, sunlight_hours, space_type, api_key=_gemini_key())
        parsed = json.loads(raw)
        return jsonify(parsed), 200
    except json.JSONDecodeError:
        # Gemini returned non-JSON; wrap it
        return jsonify({"plants": [], "tips": [raw], "parse_error": True}), 200
    except Exception as e:
        print(f"[API ERROR] Planner failed: {e}")
        return jsonify({"error": str(e)}), 500


# ---------------------------------------------------------------------------
# Module 2: Grow Calendar
# ---------------------------------------------------------------------------
@app.route("/api/calendar", methods=["GET"])
def grow_calendar():
    key_error = _require_gemini_key()
    if key_error:
        return key_error

    city = request.args.get("city", "Bangalore").strip()
    month = request.args.get("month", "").strip()

    if not month:
        from datetime import datetime
        month = datetime.now().strftime("%B")

    try:
        guide = generate_grow_calendar(city, month, api_key=_gemini_key())
        return jsonify({"city": city, "month": month, "guide": guide}), 200
    except Exception as e:
        print(f"[API ERROR] Calendar failed: {e}")
        return jsonify({"error": str(e)}), 500


# ---------------------------------------------------------------------------
# Module 5: Companion Planting
# ---------------------------------------------------------------------------
@app.route("/api/companion", methods=["POST"])
def companion_planting():
    key_error = _require_gemini_key()
    if key_error:
        return key_error

    data = request.get_json(silent=True) or {}
    plant_name = data.get("plant_name", "").strip()

    if not plant_name:
        return jsonify({"error": "plant_name is required"}), 400

    try:
        raw = generate_companion_suggestions(plant_name, api_key=_gemini_key())
        parsed = json.loads(raw)
        return jsonify(parsed), 200
    except json.JSONDecodeError:
        return jsonify({"companions": [], "avoid": [], "tips": [raw], "parse_error": True}), 200
    except Exception as e:
        print(f"[API ERROR] Companion failed: {e}")
        return jsonify({"error": str(e)}), 500


# ---------------------------------------------------------------------------
# Module 6: Container / Plant Guide
# ---------------------------------------------------------------------------
@app.route("/api/guide", methods=["POST"])
def plant_guide():
    key_error = _require_gemini_key()
    if key_error:
        return key_error

    data = request.get_json(silent=True) or {}
    plant_name = data.get("plant_name", "").strip()

    if not plant_name:
        return jsonify({"error": "plant_name is required"}), 400

    try:
        guide = generate_plant_guide(plant_name, api_key=_gemini_key())
        return jsonify({"plant": plant_name, "guide": guide}), 200
    except Exception as e:
        print(f"[API ERROR] Guide failed: {e}")
        return jsonify({"error": str(e)}), 500


# ---------------------------------------------------------------------------
# Module 7: AI Plant Doctor Chat
# ---------------------------------------------------------------------------
@app.route("/api/chat", methods=["POST"])
def plant_doctor():
    key_error = _require_gemini_key()
    if key_error:
        return key_error

    data = request.get_json(silent=True) or {}
    symptoms = data.get("symptoms", "").strip()
    plant_type = data.get("plant_type", "").strip()

    if not symptoms:
        return jsonify({"error": "symptoms description is required"}), 400

    try:
        response = generate_plant_doctor_response(symptoms, plant_type, api_key=_gemini_key())
        return jsonify({"response": response}), 200
    except Exception as e:
        print(f"[API ERROR] Plant doctor failed: {e}")
        return jsonify({"error": str(e)}), 500


# ---------------------------------------------------------------------------
# Module 8: Composting Guide
# ---------------------------------------------------------------------------
@app.route("/api/composting", methods=["GET"])
def composting_guide():
    key_error = _require_gemini_key()
    if key_error:
        return key_error

    scale = request.args.get("scale", "balcony").strip()
    valid_scales = ["balcony", "terrace", "indoor"]
    if scale not in valid_scales:
        scale = "balcony"

    try:
        guide = generate_composting_guide(scale, api_key=_gemini_key())
        return jsonify({"scale": scale, "guide": guide}), 200
    except Exception as e:
        print(f"[API ERROR] Composting failed: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
