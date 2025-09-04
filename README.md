# Vehicle Assignment Django Project

This project is a Django REST API for managing orders, vehicles, and drivers in Slovakia.  
It automatically assigns the most suitable vehicle and driver to an order using a weighted scoring system based on multiple criteria, currently distance to pickup (priority 70 %) and estimated travel cost (priority 30 %).
---

## Table of Contents

- [Features](#features)  
- [Project Structure](#project-structure)  
- [Installation](#installation)  
- [Sample Data](#sample-data)  
- [API Endpoints](#api-endpoints)  
- [Assignment Algorithm](#assignment-algorithm)  
- [Dependencies](#dependencies)  

---

## Features

- Create, list, and manage Orders, Vehicles, and Drivers.  
- Automatically assign the best vehicle and driver for each order.  
- Distance calculation using Haversine formula (accurate for geographic coordinates).  
- Cost estimation for each vehicle based on distance. 

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/DeeHornacek/assign_vehicles_drivers.git
cd assign_vehicles_drivers
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Apply migrations to create the database schema:
```bash
python manage.py migrate
```
5. Run the development server
```bash
python manage.py runserver
```
## Sample Data

This project ships with prepared fixtures for initial data loading.  
You can use them to quickly populate the database with realistic test data for vehicles, drivers, and orders.

- **vehicles.json** → 30 vehicles (varied types, capacities, costs, and availability across Slovak district towns).  
- **drivers.json** → 20 drivers (Slovak names, phone numbers, licenses, with 15 available and 5 unavailable).  
- **orders.json** → 20 orders (random weights, pickup and delivery in Slovak district towns, status mix).  

### Loading the fixtures

Run the following commands from the project root:

```bash
python manage.py loaddata vehicles.json
python manage.py loaddata drivers.json
python manage.py loaddata orders.json
```
## Example request
- POST /api/orders/1/assign-optimal-vehicle/

## Example response

```json
{
    "assigned_vehicle": "AB101AB",
    "assigned_driver": "Patrik Varga",
    "estimated_cost": 549.56,
    "distance_km": 219.82,
    "reasoning": "Selected AB101AB: adequate capacity, distance: 41.29, cost: 549.56, weighted criteria applied."
}
```

## Assignment Algorithm
- Driver Filtering: Select available drivers
- Vehicle Filtering: Select available vehicles that can carry the order weight.
- Distance Calculation: Compute distance from vehicle to pickup and total route distance using Haversine formula.
- Cost Estimation: Calculate estimated cost per vehicle based on distance and cost per km.
- Vehicle Selection:
Weighted Multi-Criteria Assignment:
Each available vehicle is scored based on multiple criteria:
Distance to pickup – weight 0.7
Estimated total cost – weight 0.3
Values are normalized to 0–1 and combined into a single score.
Vehicle with the lowest score is selected.
Driver is randomly selected among available drivers.

## Dependencies
- Python 3.11+
- Django==5.2.6
- djangorestframework==3.16.1
- environs==14.3.0
