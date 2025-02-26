from flask import Flask, render_template, request, jsonify
import folium
import json
from geopy.distance import geodesic

app = Flask(__name__)

# Predefined shop locations (10+ locations)
shops = [
    {"name": "Chandresh General Store", "coords": (25.752317, 82.946685)},
    {"name": "Moni Devi General Store", "coords": (25.752820, 82.946920)},
    {"name": "Angaan", "coords": (25.787375, 82.996254)},
    {"name": "Raman", "coords": (25.807570, 82.999268)},
    {"name": "Shashi General Store", "coords": (25.346826, 82.992287)},
    {"name": "Vishal Mega Mart", "coords": (25.761500, 82.950900)},
    {"name": "Shyam Kirana Store", "coords": (25.755421, 82.940987)},
    {"name": "Mohan Fast Food", "coords": (25.760220, 82.945612)},
    {"name": "Radha Medical Store", "coords": (25.765987, 82.949321)},
    {"name": "Sita Sweets and Bakery", "coords": (25.770112, 82.953789)}
]

# Function to check if a shop is within 5 km radius
def is_within_range(coord1, coord2, radius_km=5):
    return geodesic(coord1, coord2).km <= radius_km

@app.route("/")
def home():
    return render_template("map.html")

@app.route("/get_shops")
def get_shops():
    return jsonify(shops)

@app.route("/add_location", methods=["POST"])
def add_location():
    data = request.json
    new_shop = {"name": data["name"], "coords": (data["lat"], data["lon"])}
    shops.append(new_shop)
    return jsonify({"message": "Location added successfully!", "shop": new_shop})

@app.route("/generate_map")
def generate_map():
    user_lat = request.args.get("lat", type=float, default=25.753793)
    user_lon = request.args.get("lon", type=float, default=82.948879)
    user_coords = (user_lat, user_lon)

    # Filter shops within 5 km
    nearby_shops = [shop for shop in shops if is_within_range(user_coords, shop["coords"])]

    # Create a map centered on the user
    m = folium.Map(location=user_coords, zoom_start=14, tiles="OpenStreetMap")

    # Add user location marker
    folium.Marker(
        user_coords, popup="You are here", icon=folium.Icon(color="red", icon="user")
    ).add_to(m)

    # Add shop markers (blue for nearby, gray for others)
    for shop in shops:
        color = "blue" if shop in nearby_shops else "gray"
        folium.Marker(
            shop["coords"], popup=f"{shop['name']} ({shop['coords']})", icon=folium.Icon(color=color)
        ).add_to(m)

    # Draw 5 km radius circle
    folium.Circle(
        location=user_coords, radius=5000, color="green", fill=True, fill_opacity=0.2
    ).add_to(m)

    # Save map
    m.save("templates/generated_map.html")
    return jsonify({"message": "Map generated successfully!", "map_url": "/generated_map.html"})

if __name__ == "__main__":
    app.run(debug=True)
