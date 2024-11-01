from flask import Flask, request, jsonify, make_response, render_template
from langchain_community.llms import OpenAI  # Updated import based on deprecation warning
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

# Get API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize Langchain with OpenAI
llm = OpenAI(api_key=openai_api_key)

# Car recommendations based on manufacturer and style
car_recommendations = {
    "chery": {
        "sporty": "Chery Omoda E5 - The perfect sporty EV that’s stylish and versatile for any urban adventure. It’s a bold choice for anyone with a vibrant personality!",
        "luxury": "Chery iCar 03 - Elegant yet compact, perfect for those who value sophistication and a refined sense of style."
    },
    "tesla": {
        "sporty": "Tesla Model 3 Performance - A high-tech and futuristic ride, ideal for someone in a fast-paced job who loves speed and innovation!",
        "luxury": "Tesla Model S - A luxurious experience with cutting-edge technology, perfect for making a statement in any industry."
    },
    "bmw": {
        "sporty": "BMW i4 M50 - Sporty and sleek, it’s the perfect choice for the professional who demands both style and performance.",
        "luxury": "BMW iX - A luxurious EV SUV that’s as powerful as it is comfortable, perfect for those who want both prestige and practicality."
    },
    "wuling": {
        "economic": "Wuling Air EV - An eco-friendly choice that’s practical, efficient, and designed for those who appreciate simplicity and value.",
        "sporty": "Wuling Bingo - A compact and fun EV that’s easy to drive, ideal for the urban professional who loves a little flair on the go!"
    }
}

# Default recommendations for "All Manufacturers" based on style preference
all_manufacturers_recommendations = {
    "sporty": "Tesla Model 3 Performance - Known for its speed and futuristic design, perfect for a professional who enjoys a high-tech, thrilling ride!",
    "luxury": "BMW iX - A luxurious EV SUV that brings both prestige and comfort, ideal for a stylish professional.",
    "economic": "Wuling Air EV - Compact, affordable, and eco-friendly, it’s the perfect choice for those who value practicality and sustainability."
}

# Template for generating conversational recommendations
prompt_template = PromptTemplate(
    input_variables=["umur", "gaya", "pekerjaan", "manufacturer"],
    template=(
        "Berdasarkan umur {umur}, gaya {gaya}, pekerjaan {pekerjaan}, dan produsen mobil {manufacturer}, "
        "berikan rekomendasi mobil listrik yang cocok untuk pengguna berdasarkan gaya hidup mereka. Tambahkan sentuhan tema yang menyenangkan!"
    )
)

def add_cors_headers(response):
    """
    Manually add CORS headers to allow requests from any origin.
    """
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/rekomendasi-mobil', methods=['POST', 'OPTIONS'])
def rekomendasi_mobil():
    if request.method == 'OPTIONS':
        # Handle preflight CORS request
        response = make_response()
        return add_cors_headers(response)

    try:
        # Get input from JSON request
        data = request.get_json()

        # Extract user input
        umur = data.get("umur")
        gaya = data.get("gaya").lower()
        pekerjaan = data.get("pekerjaan").capitalize()
        manufacturer = data.get("manufacturer").lower()

        if not umur or not gaya or not pekerjaan or not manufacturer:
            response = make_response(
                jsonify({"error": "Semua field (umur, gaya, pekerjaan, produsen) harus diisi"}), 400)
            return add_cors_headers(response)

        # Check for specific car recommendation based on manufacturer and style
        rekomendasi = None
        if manufacturer != "all":
            rekomendasi = car_recommendations.get(manufacturer, {}).get(gaya)

            # If no specific car is found for the preferred manufacturer
            if not rekomendasi:
                rekomendasi = (
                    f"Sorry, we couldn’t find a {gaya} style EV from {manufacturer.capitalize()} that matches your preferences. "
                    "Please explore more options within the brand or try another style or manufacturer."
                )
        else:
            # If "All Manufacturers" is selected, recommend a car based on style without fallback message
            rekomendasi = all_manufacturers_recommendations.get(gaya)

        # Format and send the response
        rekomendasi = rekomendasi.format(
            umur=umur,
            gaya=gaya,
            pekerjaan=pekerjaan,
            manufacturer=manufacturer.capitalize())

        response = make_response(jsonify({"rekomendasi": rekomendasi}), 200)
        return add_cors_headers(response)

    except Exception as e:
        response = make_response(jsonify({"error": str(e)}), 500)
        return add_cors_headers(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Ensures public access in Replit
