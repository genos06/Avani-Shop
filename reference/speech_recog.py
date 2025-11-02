import os
import json
import tempfile
from flask import Flask, request, jsonify, render_template, url_for
from testing_model import transcribe_audio
from google import genai
from parser import parse_json_from_text
from flask_bootstrap import Bootstrap4

app = Flask(__name__)
app.secret_key = "Hello World"

bootstrap = Bootstrap4(app)

# Configure upload folder
UPLOAD_FOLDER = 'temp_uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Initialize GenAI client
client = genai.Client(api_key="YOUR_GEMINI_API_KEY_HERE")


def get_fertilizer_recommendation(user_input: str):
    """
    Get fertilizer recommendation from AI based on farmer's input
    
    Args:
        user_input (str): Farmer's description of land, soil, and crops
    
    Returns:
        dict: Contains product_name, amount, and why
    """
    # Validate input transcription
    if not user_input or not user_input.strip():
        return {
            "success": False,
            "error": "Empty transcription received",
            "user_message": "कृपया फिर से बोलें। आपकी आवाज़ स्पष्ट नहीं थी। / Please speak again. Your voice was not clear."
        }
    
    # Check if transcription is too short (likely noise or error)
    if len(user_input.strip()) < 10:
        return {
            "success": False,
            "error": "Transcription too short",
            "user_message": "कृपया अधिक जानकारी दें। अपनी ज़मीन, मिट्टी और फसल के बारे में बताएं। / Please provide more information about your land, soil and crops."
        }
    
    prompt = f"""
You are an expert agronomist AI. A farmer will provide information about their land, soil, and crops in English or Hinglish.

**Task:**  
- Extract only:  
    1. `nutrients` → list of nutrients required (subset of ["Nitrogen", "Phosphorus", "Potassium"])  
    2. `land_acres` → size of land in acres (convert local units like bigah to acres if needed)  
    3. `why` → simple explanation for the recommendation in farmer's language  

**Important:**  
- Respond **ONLY** in a Python dict format.  
- Do NOT include anything else.  

farmer input : 

{user_input}
"""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        llm_text = response.text.strip()
        print(f"AI Response: {llm_text}")
        
        try:
            llm_dict = parse_json_from_text(llm_text)
        except Exception as parse_error:
            print(f"Parse error: {parse_error}")
            return {
                "success": False,
                "error": f"Failed to parse AI response: {str(parse_error)}",
                "raw_response": llm_text
            }

        if not llm_dict:
            return {
                "success": False,
                "error": "Failed to parse AI response",
                "raw_response": llm_text,
                "user_message": "कुछ गड़बड़ हुई। कृपया फिर से कोशिश करें। / Something went wrong. Please try again."
            }

        nutrients_list = llm_dict.get("nutrients", [])
        land_acres = llm_dict.get("land_acres") or 0  # Handle null/None values
        why_text = llm_dict.get("why", "")
        
        print(f"Parsed - Nutrients: {nutrients_list}, Land: {land_acres} acres")
        
        # Validate LLM output - check for weird/empty values
        if not isinstance(nutrients_list, list):
            return {
                "success": False,
                "error": "Invalid nutrients format from AI",
                "user_message": "कुछ गड़बड़ हुई। कृपया फिर से कोशिश करें और अपनी फसल के बारे में स्पष्ट रूप से बताएं। / Something went wrong. Please try again and clearly describe your crops."
            }
        
        # Check if nutrients list is empty or contains invalid values
        if not nutrients_list or len(nutrients_list) == 0:
            return {
                "success": False,
                "error": "No nutrients identified from input",
                "user_message": "हम आपकी फसल की ज़रूरतों को समझ नहीं पाए। कृपया अपनी मिट्टी और फसल के बारे में अधिक जानकारी दें। / We couldn't understand your crop needs. Please provide more details about your soil and crops."
            }
        
        # Validate land_acres is a reasonable number
        if land_acres is not None and (not isinstance(land_acres, (int, float)) or land_acres < 0):
            return {
                "success": False,
                "error": "Invalid land size from AI",
                "user_message": "ज़मीन का आकार समझ में नहीं आया। कृपया फिर से बताएं कि आपके पास कितनी ज़मीन है। / Land size not understood. Please tell us again how much land you have."
            }
        
        # Check if land_acres is unreasonably large (likely an error)
        if land_acres and land_acres > 10000:  # More than 10,000 acres is suspicious
            return {
                "success": False,
                "error": "Unrealistic land size detected",
                "user_message": "ज़मीन का आकार बहुत बड़ा लग रहा है। कृपया एकड़ या बीघा में सही आकार बताएं। / Land size seems too large. Please provide correct size in acres or bigha."
            }
        
        # Validate why_text is not empty
        if not why_text or not why_text.strip():
            why_text = "आपकी फसल के लिए अनुशंसित खाद। / Recommended fertilizer for your crops."

        # Generate product name
        if nutrients_list:
            product_name = f"Avanii {' '.join(nutrients_list)} Mix"
        else:
            product_name = "Avanii General Purpose Fertilizer"
        
        # Calculate amount only if we have land size
        if land_acres and land_acres > 0:
            amount = len(nutrients_list) * land_acres * 12  # kg per nutrient per acre
            amount_str = f"{amount} kg"
        else:
            amount_str = "Contact for consultation (land size not provided)"
        
        result = {
            "success": True,
            "product_name": product_name,
            "amount": amount_str,
            "why": why_text,
            "nutrients": nutrients_list,
            "land_acres": land_acres if land_acres else "Not specified"
        }
        
        print(f"Recommendation result: {result}")
        return result
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "user_message": "कुछ तकनीकी समस्या हुई। कृपया फिर से कोशिश करें। / A technical issue occurred. Please try again."
        }


# Transliteration function (Devanagari to Latin script)
def transliterate_to_english(text):
    """
    Transliterate Devanagari (Hindi) text to clean English Latin script
    
    Args:
        text (str): Text in Devanagari script or mixed script
    
    Returns:
        str: Transliterated text in clean English Latin script
    """
    try:
        from indic_transliteration import sanscript
        from indic_transliteration.sanscript import transliterate
        
        transliterated = transliterate(text, sanscript.DEVANAGARI, sanscript.ISO)
        
        # Clean up the output - make it completely English (no diacritical marks)
        transliterated = transliterated.replace('ā', 'a')
        transliterated = transliterated.replace('ī', 'i')
        transliterated = transliterated.replace('ū', 'u')
        transliterated = transliterated.replace('ṛ', 'ri')
        transliterated = transliterated.replace('ṝ', 'ri')
        transliterated = transliterated.replace('ḷ', 'l')
        transliterated = transliterated.replace('ḹ', 'l')
        transliterated = transliterated.replace('ē', 'e')
        transliterated = transliterated.replace('ō', 'o')
        transliterated = transliterated.replace('ṃ', 'n')
        transliterated = transliterated.replace('ṁ', 'n')  # Anusvara
        transliterated = transliterated.replace('ḥ', 'h')
        transliterated = transliterated.replace('ṅ', 'ng')
        transliterated = transliterated.replace('ñ', 'ny')
        transliterated = transliterated.replace('ṭ', 't')
        transliterated = transliterated.replace('ḍ', 'd')
        transliterated = transliterated.replace('ṇ', 'n')
        transliterated = transliterated.replace('ś', 'sh')
        transliterated = transliterated.replace('ṣ', 'sh')
        transliterated = transliterated.replace('c', 'ch')  # च is actually 'ch' sound
        transliterated = transliterated.replace('ñ', 'n')
        
        return transliterated
    except ImportError:
        return f"[Transliteration library not installed. Original: {text}]"
    except Exception as e:
        return text






@app.route("/")
def home():
    return render_template("index.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/shop")
def shop():
    return render_template("shop.html")


@app.route("/ai", methods=["GET"])
def ai():
    """Home page with audio recording interface"""
    return render_template("ai.html")


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Audio Transcription API"
    })


@app.route("/transcribe", methods=["POST"])
def transcribe_endpoint():
    """
    Flask endpoint to transcribe audio in Hindi, English, or Hinglish
    
    Form Parameters:
        - file: Audio file (required)
        - language: Language code - 'hi' (Hindi), 'en' (English). Defaults to 'hi' to prevent Urdu transcription
    
    Returns:
        JSON with transcription and fertilizer recommendation
        
    Note:
        - Only supports Hindi, English, and Hinglish transcription
        - Urdu transcription is explicitly prevented by defaulting to Hindi
    """
    try:
        # Get audio file from request
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        audio_file = request.files["file"]
        
        # Check if file is empty
        if audio_file.filename == '':
            return jsonify({"error": "Empty filename"}), 400
        
        # Get parameters - default to Hindi to prevent Urdu transcription
        language = request.form.get("language", "hi")  # Default to Hindi

        # Save audio temporarily with original extension
        file_ext = os.path.splitext(audio_file.filename)[1] or '.wav'
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp:
            audio_file.save(temp.name)
            temp_path = temp.name

        try:
            # Use the transcribe_audio function from testing_model
            # Language will be 'hi' by default to prevent Urdu transcription
            print(f"Transcribing audio: {audio_file.filename}, Language: {language}")
            transcription = transcribe_audio(temp_path, language=language)
            
            # Validate transcription output
            if not transcription or not transcription.strip():
                return jsonify({
                    "success": False,
                    "error": "Empty transcription",
                    "user_message": "कोई आवाज़ नहीं सुनाई दी। कृपया फिर से रिकॉर्ड करें। / No voice detected. Please record again."
                }), 400
            
            # Check for weird transcription (too short, only special characters, etc.)
            if len(transcription.strip()) < 5:
                return jsonify({
                    "success": False,
                    "error": "Transcription too short",
                    "user_message": "आवाज़ स्पष्ट नहीं थी। कृपया ज़ोर से और साफ़ बोलें। / Voice was not clear. Please speak louder and clearer."
                }), 400
            
            # Check if transcription contains mostly non-alphanumeric characters (likely noise)
            import re
            alphanumeric_count = len(re.findall(r'[a-zA-Z0-9\u0900-\u097F]', transcription))
            if alphanumeric_count < 3:
                return jsonify({
                    "success": False,
                    "error": "Invalid transcription - mostly noise",
                    "user_message": "केवल शोर सुनाई दिया। कृपया शांत जगह में रिकॉर्ड करें। / Only noise detected. Please record in a quiet place."
                }), 400
            
            print(f"Transcription successful: {transcription}")
            
            # Get fertilizer recommendation from AI
            print("Getting fertilizer recommendation...")
            recommendation = get_fertilizer_recommendation(transcription)
            print(f"Recommendation returned: {recommendation}")
            
            # Check if recommendation failed
            if not recommendation.get("success", False):
                error_message = recommendation.get("user_message", 
                                                   "कुछ गड़बड़ हुई। कृपया फिर से कोशिश करें। / Something went wrong. Please try again.")
                return jsonify({
                    "success": False,
                    "error": recommendation.get("error", "Recommendation failed"),
                    "user_message": error_message,
                    "transcription": transcription
                }), 400
            
            # Prepare response
            response_data = {
                "success": True,
                "filename": audio_file.filename,
                "language": language or "auto-detected",
                "transcription": transcription,
                "recommendation": recommendation
            }
            
            print(f"Final response: {json.dumps(response_data, indent=2)}")
            return jsonify(response_data)
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
                print(f"Cleaned up temporary file: {temp_path}")
    
    except FileNotFoundError as e:
        return jsonify({
            "success": False,
            "error": "File not found",
            "details": str(e),
            "user_message": "फ़ाइल नहीं मिली। कृपया फिर से रिकॉर्ड करें। / File not found. Please record again."
        }), 404
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Transcription failed",
            "details": str(e),
            "user_message": "कुछ तकनीकी समस्या हुई। कृपया फिर से कोशिश करें। / A technical issue occurred. Please try again."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
