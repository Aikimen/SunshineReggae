# SunshineReggae.py
"""
SunshineReggae — A simple visualization of how a house can orient itself towards the sun based on hemisphere and season.
The house rotates to face the sun in winter (or away from it in summer), and a compass + sun path are drawn for context.
"""

import tkinter as tk
from geopy.geocoders import Nominatim
import math

# Geolocation

def get_coordinates(address):
    """
    Translates a given user address into (latitude, longitude) using geopy.
    """
    geolocator = Nominatim(user_agent="sunshine_reggae")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

def get_coordinates_from_input(user_input):
    """
    Parses input string: either coordinates (lat, lon) or a location name.
    """
    if "," in user_input:
        try:
            lat_str, lon_str = user_input.split(",")
            return float(lat_str.strip()), float(lon_str.strip())
        except ValueError:
            print("Invalid coordinate format. Use: 37.42, -122.08")
            return None, None
    else:
        return get_coordinates(user_input)

# Sun direction logic

def get_sun_direction(lat, season="winter"):
    """
    Returns the approximate direction (angle in degrees) where the sun is located
    depending on the hemisphere and the season.
    Physically:
    - 180° = Sun is to the South (typical winter position in the Northern Hemisphere)
    - 0° = Sun is to the North (typical winter position in the Southern Hemisphere)
    - 135° = Southeast (summer approximation, Northern Hemisphere)
    - 45° = Northeast (summer approximation, Southern Hemisphere)
    """
    if lat >= 0:
        return 180 if season == "winter" else 135
    else:
        return 0 if season == "winter" else 45

def is_northern_hemisphere(lat):
    """
    Determines if the given latitude is in the Northern Hemisphere.
    """
    return lat >= 0

def rotate_points(points, angle_deg, origin):
    """
    Rotates a list of 2D points around a given origin by a specified angle in degrees.
    Used to turn the house and its parts toward the sun.
    """
    angle_rad = math.radians(angle_deg)
    ox, oy = origin
    rotated = []
    for x, y in points:
        qx = ox + math.cos(angle_rad) * (x - ox) - math.sin(angle_rad) * (y - oy)
        qy = oy + math.sin(angle_rad) * (x - ox) + math.cos(angle_rad) * (y - oy)
        rotated.append((qx, qy))
    return rotated

# Drawing

def draw_house(canvas, cx, cy, angle_deg):
    """
    Draws a stylized house with a roof and one window, rotated by angle_deg.
    Physically:
    - Window is on the 'sun-facing' side of the house.
    - Angle 180° = window faces south.

    standard rotation formulas:
    x' = ox + cos(θ) * (x - ox) - sin(θ) * (y - oy)
    y' = oy + sin(θ) * (x - ox) + cos(θ) * (y - oy)
    """
    body = [
        (cx - 40, cy + 30), (cx + 40, cy + 30),
        (cx + 40, cy), (cx - 40, cy)
    ]
    roof = [
        (cx - 40, cy), (cx, cy - 40), (cx + 40, cy)
    ]
    window = [
        (cx + 10, cy + 10), (cx + 30, cy + 10),
        (cx + 30, cy + 25), (cx + 10, cy + 25)
    ]
    rotated_body = rotate_points(body, angle_deg, (cx, cy))
    rotated_roof = rotate_points(roof, angle_deg, (cx, cy))
    rotated_window = rotate_points(window, angle_deg, (cx, cy))
    canvas.create_polygon(rotated_body, fill="#D2691E", outline="black")
    canvas.create_polygon(rotated_roof, fill="#8B0000", outline="black")
    canvas.create_polygon(rotated_window, fill="#ADD8E6", outline="black")

def draw_compass(canvas, w, h):
    """
    Draws N, S, W, E compass labels on the canvas.
    """
    canvas.create_text(w/2, 30, text="N", font=("Helvetica", 14), fill="black")
    canvas.create_text(w/2, h - 30, text="S", font=("Helvetica", 14), fill="black")
    canvas.create_text(30, h/2, text="W", font=("Helvetica", 14), fill="black")
    canvas.create_text(w - 30, h/2, text="E", font=("Helvetica", 14), fill="black")

def draw_sun_path(canvas, cx, cy, radius, is_north=True):
    """
    Draws an arc representing the sun's path in the sky and a sun symbol.
    Arc direction depends on hemisphere:
    - Northern Hemisphere: arc goes from east to west, above the house (south)
    - Southern Hemisphere: arc goes from east to west, below the house (north)
    """
    offset = -90 if is_north else 90
    canvas.create_arc(cx - radius, cy - radius, cx + radius, cy + radius,
                      start=offset, extent=180, style=tk.ARC, outline="orange", width=2)
    sx = cx + radius * math.cos(math.radians(offset + 90))
    sy = cy + radius * math.sin(math.radians(offset + 90))
    canvas.create_oval(sx - 15, sy - 15, sx + 15, sy + 15, fill="yellow", outline="gold")

def draw_scene(lat, lon):
    """
    Sets up the main canvas window and draws the entire scene:
    compass, sun path, and rotated house.
    """
    root = tk.Tk()
    root.title("Sunshine Reggae")
    w, h = 600, 400
    canvas = tk.Canvas(root, width=w, height=h, bg="lightgreen")
    canvas.pack()

    draw_compass(canvas, w, h)
    cx, cy = w//2, h//2
    angle = get_sun_direction(lat, season="winter")
    draw_house(canvas, cx, cy, angle)
    draw_sun_path(canvas, cx, cy, 120, is_north=is_northern_hemisphere(lat))
    root.mainloop()



def main():
    """
    Entry point program: asks for user input, gets coordinates and draws scene
    """
    print("Enter an address (e.g. 'Stanford') or coordinates (e.g. '37.42, 122.16')")
    user_input = input("Address or coordinates: ")
    lat, lon = get_coordinates_from_input(user_input)
    if lat is None:
        print("Could not retrieve coordinates.")
        return
    draw_scene(lat, lon)

if __name__ == "__main__":
    main()

