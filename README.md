# Graphhopper Enhanced Directions App
**Project Activity 3 – Social Coding | Cisco Networking Academy**
**Option 1: Feature Enhancements of Lab 4.9.2**

---

## Team Information
| Field | Details |
|-------|---------|
| Team Name | [YOUR TEAM NAME HERE] |
| Member 1 | Christian Louis Suico — Lead Developer / API Integration |
| Member 2 | Jay Talingting — Feature Developer / Transport Modes |
| Member 3 | Jan Earl Tampus — Feature Developer / Estimator Functions |
| Member 4 | Wilfred Cholo Penales — Tester / Documentation |
| Course | DevNet Associate – Cisco Networking Academy |

---

## About This Project
This is an enhanced version of the **Graphhopper Directions App** from Lab 4.9.2.
It uses the Graphhopper Geocoding and Routing REST APIs to provide turn-by-turn
directions between two locations, with added features for real-world usefulness.

---

## New Features Added

### 1. Additional Transport Modes
Two new vehicle profiles added on top of the original `car`, `bike`, `foot`:
- **`scooter`** — routes via car road network (Graphhopper `car` profile)
- **`wheelchair`** — routes via walkable paths (Graphhopper `foot` profile)

### 2. Fuel Cost Estimator (car / scooter)
- Estimated **liters of fuel** consumed (~12 km/L efficiency)
- Estimated **PHP cost** (~PHP 63/liter)

### 3. Calorie Burn Estimator (bike / foot / wheelchair)
- Estimated **kcal burned** using MET values and route distance
- Assumes 65 kg body weight

---

## Files in This Repository
| File | Description |
|------|-------------|
| `graphhopper_enhanced.py` | Main enhanced Python application |
| `requirements.txt` | Python package dependencies |
| `README.md` | Project documentation |

---

## How to Run

```
pip install requests
python3 graphhopper_enhanced.py
```

Get a free API key at https://www.graphhopper.com/ and replace `YOUR_API_KEY_HERE` in the script.

---

## Future Enhancements (Backlog)
- Save trip history to a log file
- Real-time fuel prices via external API
- User-input body weight for calorie calculations
- Simple GUI using tkinter
- Multi-stop routing support

---

*© 2020 - 2024 Cisco and/or its affiliates. All rights reserved. Cisco Public*
