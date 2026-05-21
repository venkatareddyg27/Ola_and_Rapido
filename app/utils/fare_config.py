from app.core.enums import VehicleCategory


VEHICLE_PRICING = {

    VehicleCategory.BIKE: {
        "base_fare": 30,
        "per_km_rate": 8,
        "minimum_fare": 40
    },

    VehicleCategory.AUTO: {
        "base_fare": 50,
        "per_km_rate": 12,
        "minimum_fare": 70
    },

    VehicleCategory.HATCHBACK: {
        "base_fare": 80,
        "per_km_rate": 15,
        "minimum_fare": 120
    },

    VehicleCategory.SEDAN: {
        "base_fare": 100,
        "per_km_rate": 18,
        "minimum_fare": 150
    },

    VehicleCategory.SUV: {
        "base_fare": 150,
        "per_km_rate": 22,
        "minimum_fare": 220
    },

    VehicleCategory.LUXURY: {
        "base_fare": 300,
        "per_km_rate": 40,
        "minimum_fare": 500
    }
}