# LNG Intelligence Dashboard — Configuration
# All project constants 



# ----------------------------------------------------------------
# EIA API
# ----------------------------------------------------------------

import os
from dotenv import load_dotenv

# Load keys from .env file —
load_dotenv()


EIA_API_KEY = os.getenv("EIA_API_KEY")  



# ----------------------------------------------------------------
# CARGO & VESSEL BASICS
# ----------------------------------------------------------------

# Standard TFDE cargo — 160,000 m³ liquid = ~3.4mn MMBtu regasified
CARGO_SIZE_MMBTU = 3_400_000

# Boil-off — LNG evaporates in transit, gas goes to engines as fuel
# Excess beyond engine needs goes to reliquefaction or GCU
BOILOFF_RATE_STANDARD = 0.001    # 0.10%/day — typical TFDE
BOILOFF_RATE_MODERN   = 0.00085  # 0.085%/day — newer high-spec vessels
BOILOFF_RATE_OLD      = 0.0015   # 0.15%/day — older steam turbine ships

# Vessel speeds
# Design max: 19.5 kts — used when cargo is urgent or hire rates high
# Economical: 16.6 kts — minimises fuel per nm, but adds hire days
# We use 16.5 kts as operational average — reflects real practice
# where vessels rarely push maximum on routine voyages
VESSEL_SPEED_KNOTS = 16.5


# ----------------------------------------------------------------
# UNIT CONVERSION
# ----------------------------------------------------------------

# TTF trades in EUR/MWh — convert to $/MMBtu to compare with JKM/HH
# 1 MWh = 3.412 MMBtu (fixed physical constant, never changes)
# EUR/USD rate loaded separately from live feed
MWH_TO_MMBTU = 3.412


# ----------------------------------------------------------------
# TRADE ROUTES
# ----------------------------------------------------------------
# Freight costs estimated at $90,000/day hire, 16.5 kts, TFDE vessel
# Real freight quoted per cargo by broker — these are planning estimates
#
# How freight $/MMBtu is derived:
#   voyage days = distance nm / (speed kts x 24)
#   hire cost   = voyage days x daily hire rate
#   freight/MMBtu = hire cost / cargo size MMBtu
#   + canal tolls + port fees where applicable

ROUTES = {

    "Sabine Pass → Japan": {
        "freight_mmbtu": 2.50,
        "distance_nm": 11000,
        "origin": "Sabine Pass LNG, Louisiana — Cheniere Energy",
        "destination": "Japan — Sodegaura / Futtsu terminals",
        # Gulf of Mexico out, Panama Canal transit, then Pacific north to Japan
        # Panama toll adds ~$0.10/MMBtu on top of hire cost
        # Longest routine trade route in the market
        "path": "Gulf of Mexico → Panama Canal → Pacific Ocean → Japan",
    },

    "Sabine Pass → NW Europe": {
        "freight_mmbtu": 1.80,
        "distance_nm": 5000,
        "origin": "Sabine Pass LNG, Louisiana — Cheniere Energy",
        "destination": "NW Europe — Rotterdam / Zeebrugge / Isle of Grain",
        # Straight Atlantic crossing — no canal needed
        # This route went from niche to dominant after Russia/Ukraine 2022
        # US became Europe's largest LNG supplier almost overnight
        "path": "Gulf of Mexico → North Atlantic → English Channel",
    },

    "Qatar → Japan": {
        "freight_mmbtu": 0.90,
        "distance_nm": 6500,
        "origin": "Ras Laffan LNG, Qatar — QatarEnergy",
        "destination": "Japan — Sodegaura / Futtsu terminals",
        # Qatar supplies Japan since 1990s — dedicated fleet, optimised ops
        # Strait of Hormuz is the choke point — any Gulf tension affects this
        # Cheapest $/MMBtu despite longer distance because of volume efficiency
        "path": "Persian Gulf → Strait of Hormuz → Indian Ocean → Strait of Malacca → Japan",
    },

    "Australia → Japan": {
        "freight_mmbtu": 0.70,
        "distance_nm": 3800,
        "origin": "NW Australia — Gorgon / Wheatstone / NWS (Woodside, Chevron, Shell)",
        "destination": "Japan — Sodegaura / Futtsu terminals",
        # Shortest major trade lane — supply relationship since 1980s
        # Australia overtook Qatar as world's largest LNG exporter recently
        # Low freight gives Australian LNG strong netback into Japan vs US
        "path": "Indian Ocean → Indonesian waters → Pacific Ocean → Japan",
    },

    "Trinidad → Europe": {
        "freight_mmbtu": 1.60,
        "distance_nm": 4000,
        "origin": "Atlantic LNG, Point Fortin, Trinidad and Tobago",
        "destination": "Southern Europe — Barcelona / Sines / Huelva",
        # Atlantic LNG is one of oldest export facilities in the Americas
        # Trinidad gas reserves maturing — volumes declining year on year
        # Targets Spain and Portugal mainly — shorter haul than US to Europe
        "path": "Caribbean Sea → North Atlantic → Southern Europe",
    },

}