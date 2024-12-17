# Fleet-Service

Fleet-Service is a Flask-based microservice that handles vehicle management for a fleet. It includes endpoints for adding new vehicles, retrieving vehicle details, updating vehicle data, deleting vehicles, and listing all vehicles. The service uses SQLite for database management and provides API documentation via Swagger.

## Features
	•	Create Vehicles: Add new vehicles to the fleet with details like brand, model, and monthly price.
	•	Retrieve Vehicle Details: Fetch vehicle details by their unique ID.
	•	Update Vehicle Data: Modify details for an existing vehicle.
	•	Delete Vehicles: Remove vehicles from the fleet.
	•	List Vehicles: List all vehicles currently in the fleet.

## Requirements

### Python Packages
	•	Python 3.7 or higher
	•	Flask
	•	Flasgger
	•	Python-Dotenv
	•	SQLite (built into Python)

### Python Dependencies

Install the required dependencies using:
```Pip install -r requirements.txt```

### Environment Variables

Create a .env file in the root directory and specify the following:
```FLASK_DEBUG=1```
```DATABASE=fleet-database.db```

## Getting Started

1. Initialize the Database

The service uses SQLite to store vehicle data. The database is automatically initialized when the service starts.
If reinitialization is needed, you can modify the init_db() function in fleet.app.py.

2. Start the Service

Run the Flask application:
```python fleet.app.py```
The service will be available at: http://127.0.0.1:5003

## API Endpoints

1. GET /

Provides a list of available endpoints in the service.

#### Response Example:
```
{
  "service": "Fleet-Service",
  "available_endpoints": [
    {"path": "/create_vehicle", "method": "POST", "description": "Opret ny bil i flåden"},
    {"path": "/get_vehicle/<int:bil_id>", "method": "GET", "description": "Hent bil detaljer baseret på bil ID"},
    {"path": "/update_vehicle/<int:bil_id>", "method": "PUT", "description": "Opdater en bils detaljer"},
    {"path": "/delete_vehicle/<int:bil_id>", "method": "DELETE", "description": "Slet en bil fra flåden"},
    {"path": "/list_vehicles", "method": "GET", "description": "Liste over alle køretøjer i flåden"}
  ]
}
```

2. POST /create_vehicle

Creates a new vehicle in the fleet.

#### Request Body:
```
{
  "stelnummer": "ABC12345DEF67890",
  "abonnement_id": 123,
  "mærke": "Tesla",
  "model": "Model S",
  "månedlig_pris": 8999.99,
  "kilometer_grænse": 1500,
  "kilometerafstand": 0,
  "registreringsnummer": "AB12345",
  "status": "Tilgængelig",
  "admin_id": 456
}
```

#### Response Example:
```
{
  "message": "Køretøj oprettet"
}
```

3. GET /get_vehicle/<int:bil_id>

Fetches details for a specific vehicle by ID.

#### Response Example:
```
{
  "bil_id": 1,
  "stelnummer": "ABC12345DEF67890",
  "abonnement_id": 123,
  "mærke": "Tesla",
  "model": "Model S",
  "månedlig_pris": 8999.99,
  "kilometer_grænse": 1500,
  "kilometerafstand": 0,
  "registreringsnummer": "AB12345",
  "status": "Tilgængelig",
  "admin_id": 456
}
```

4.  PUT /update_vehicle/<int:bil_id>

Updates an existing vehicle's details.

#### Request Body:
```
{
  "kilometerafstand": 1200,
  "status": "Udlejet"
}
```

#### Response Example:
```
{
  "message": "Køretøj opdateret"
}
```

5. DELETE /delete_vehicle/<int:bil_id>

Deletes a vehicle from the fleet.

#### Response Example:
```
{
  "message": "Køretøj slettet"
}
```
### GET /list_vehicles

Fetches a list of all vehicles in the fleet.
```
[
  {
    "bil_id": 1,
    "stelnummer": "ABC12345DEF67890",
    "mærke": "Tesla",
    "model": "Model S",
    "status": "Tilgængelig"
  },
  {
    "bil_id": 2,
    "stelnummer": "XYZ67890GHI12345",
    "mærke": "Audi",
    "model": "A4",
    "status": "Udlejet"
  }
]


```

## Project Structure
```
.
├── fleet.app.py            # Main Flask application
├── data/
│   └── fleet-database.db   # SQLite database (created automatically)
├── swagger/                # YAML files for Swagger documentation
│   ├── home.yaml
│   ├── create_vehicle.yaml
│   ├── get_vehicle.yaml
│   ├── update_vehicle.yaml
│   ├── delete_vehicle.yaml
│   └── list_vehicles.yaml
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
└── README.md               # Project documentation
```

## Development Notes

### Swagger Documentation
	•	Swagger is available at /apidocs.
	•	API specifications are written in YAML and stored in the swagger/ folder.

### Database Management
####	•	Initialization: Automatically initializes the database on start.
####	•	Schema:
	•	bil_id: Unique ID for the vehicle (Primary Key).
	•	stelnummer: Chassis number of the vehicle.
	•	abonnement_id: Associated subscription ID.
	•	mærke: Brand of the vehicle.
	•	model: Vehicle model.
	•	månedlig_pris: Monthly rental price.
	•	kilometer_grænse: Monthly mileage limit.
	•	kilometerafstand: Current mileage.
  • registreringsnummer: Vehicle registration number.
  • status: Status of the vehicle (e.g., "Tilgængelig", "Udlejet").
  • admin_id: Admin ID responsible for managing the vehicle.

## Contributions

Feel free to fork the repository and submit pull requests. For major changes, open an issue to discuss what you would like to change.

## License

This project is licensed under the MIT License. See LICENSE for more information.
