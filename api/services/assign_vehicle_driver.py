import json
import os
import math
import random

from ..models import Orders, Drivers,Vehicles


class AssignVehicleDriver:
    """
        Handles assignment of a vehicle and driver to a specific order.
        Uses pre-stored coordinates of Slovak district towns to calculate distances
        and chooses the most suitable vehicle based on weighted distance and estimated cost.
    """

    # Coordinates of Slovak district towns are stored in a JSON config file.
    # This avoids timeouts from using geopy and simplifies data handling.
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    conf_path = os.path.abspath(os.path.join(curr_dir, '..', 'config', 'location_coordinates.json'))
    with open(conf_path, 'r') as f:
        locations_coordinates = json.load(f)

    def __init__(self, id_order, **kwargs):
        """
        Initializes the assignment class by loading the order, available drivers,
        and available vehicles that can carry the order's weight.
        Prepares a template for storing the assignment result.

        Args:
            id_order (int): The ID of the order to assign.
            **kwargs: Optional additional arguments.

        Attributes:
            order (Orders): The order object.
            drivers (QuerySet): Available drivers.
            vehicles (QuerySet): Available vehicles that can carry the order weight.
            result (dict): Template for assignment result.
        """

        # Load order data
        self.order = Orders.objects.get(order_id=id_order)

        # Filter available drivers
        # (according to assignment we assume all available drivers ARE ABLE to drive all types of vehicles
        # and ARE AVAILABLE to any location necessary => distances of drivers to available vehicles and
        # costs of these travels are NOT included in the final reasonings)
        self.drivers = Drivers.objects.filter(availability_status_driver=True)

        # Filter all vehicles that are available AND can carry the order weight
        self.vehicles = Vehicles.objects.filter(
            availability_status_vehicle=True,
            max_capacity__gte=self.order.total_weight
        )

        # Template for assignment result - due to smaller size of the response
        self.result = {
            "assigned_vehicle": "",
            "assigned_driver": "",
            "estimated_cost": 0.0,
            "distance_km": 0.0,
            "reasoning": ""
        }

    def get_assigned_vehicle_driver(self):
        """
        Assigns a driver and a vehicle to the order.

        Returns:
            dict: Assignment result containing:
                - assigned_vehicle (str)
                - assigned_driver (str)
                - estimated_cost (float)
                - distance_km (float)
                - reasoning (str)
        """

        # If the order has already been processed, return default response
        if self.order.status:
            self.result['reasoning'] = "Order already processed."
            return self.result
        elif not self.vehicles.exists():
            self.result['reasoning'] = "No available vehicles for this order."
            return self.result
        elif not self.drivers.exists():
            self.result['reasoning'] = "No available drivers for this order."
            return self.result
        else:
            # Get coordinates of pickup and delivery addresses and calculate path of order
            order_pickup_coords = self.locations_coordinates[self.order.pickup_addr]
            order_delivery_coords = self.locations_coordinates[self.order.delivery_addr]
            path_order = self.calculate_haversine_distance_km(order_pickup_coords, order_delivery_coords)

            vehicles_data = []
            for v in self.vehicles:
                distance_to_pickup = self.calculate_haversine_distance_km(
                    self.locations_coordinates[v.current_position],
                    order_pickup_coords
                )
                estimated_cost = self.calculate_cost(distance_to_pickup + path_order, v.cost_per_km)
                vehicles_data.append({
                    **v.__dict__,
                    "distance_to_pickup": distance_to_pickup,
                    "estimated_cost": estimated_cost
                })

            # Normalize distance and cost to 0-1 scale
            max_distance = max(v['distance_to_pickup'] for v in vehicles_data)
            min_distance = min(v['distance_to_pickup'] for v in vehicles_data)
            max_cost = max(v['estimated_cost'] for v in vehicles_data)
            min_cost = min(v['estimated_cost'] for v in vehicles_data)

            weight_distance = 0.7  # priority weight for distance
            weight_cost = 0.3  # priority weight for cost

            for v in vehicles_data:
                norm_distance = (v['distance_to_pickup'] - min_distance) / (
                            max_distance - min_distance) if max_distance != min_distance else 0
                norm_cost = (v['estimated_cost'] - min_cost) / (max_cost - min_cost) if max_cost != min_cost else 0
                v['score'] = weight_distance * norm_distance + weight_cost * norm_cost

            # Select vehicle with lowest weighted score
            selected_vehicle = min(vehicles_data, key=lambda x: x['score'])

            # Randomly pick available driver
            self.assigned_driver = random.choice(list(self.drivers))

            # Fill result
            self.result['assigned_driver'] = self.assigned_driver
            self.result["assigned_vehicle"] = selected_vehicle['license_plate']
            self.result['distance_km'] = round(selected_vehicle['distance_to_pickup'] + path_order, 2)
            self.result['estimated_cost'] = round(selected_vehicle['estimated_cost'], 2)
            self.result['reasoning'] = (
                f"Selected {selected_vehicle['license_plate']}: "
                f"adequate capacity, distance: {round(selected_vehicle['distance_to_pickup'], 2)} km, "
                f"cost: {round(selected_vehicle['estimated_cost'], 2)}€, weighted criteria applied."
            )

            return self.result

    @staticmethod
    def calculate_haversine_distance_km(coords_start: tuple[float, float], coords_finish: tuple[float, float]) -> float:
        """
            Calculates the distance between two geographic coordinates (latitude, longitude) in kilometers.
            Uses the Haversine formula, which converts differences in degrees into distance along the Earth's surface.
            This approach was chosen to provide a more accurate measurement than a Euclidean distance.

            Args:
                coords_start (tuple[float, float]): Pickup coordinates (latitude, longitude).
                coords_finish (tuple[float, float]): Delivery coordinates (latitude, longitude).

            Returns:
                float: Distance between the two points in kms
        """
        lat1, lon1 = coords_start
        lat2, lon2 = coords_finish

        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        # 6371 mean radius of earth
        return 6371 * c


    @staticmethod
    def calculate_cost(distance: float, cost_per_km: float) -> float:
        """
            Calculates travel cost given distance and cost per kilometer.

            Args:
                distance (float): Travel distance in kilometers.
                cost_per_km (float): Cost per kilometer.

            Returns:
                float: Total travel cost.
        """
        return distance * cost_per_km



    @classmethod
    def get_location_coordinates(cls, location: str) -> tuple[float, float]:
        """
            Returns the coordinates (latitude, longitude) of a location.

            Args:
                location (str): Name of the location.

            Returns:
                tuple[float, float]: (latitude, longitude) of the location.
        """
        return (cls.locations_coordinates[location][0],cls.locations_coordinates[location][1])