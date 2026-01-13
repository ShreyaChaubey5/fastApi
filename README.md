Patient Information System API
A lightweight, fully functional backend API built with FastAPI to manage patient records. This system allows for creating, viewing, and updating patient data, including automatic BMI (Body Mass Index) calculation using Pydantic's computed fields.

🚀 Features
**CRUD Operations**: Create, Read, and Update patient records.

**Data Validation**: Strict type checking and value constraints using Pydantic.

**Automatic BMI Calculation**: Uses @computed_field to calculate BMI based on weight and height in real-time.

**Local Persistence**: Data is stored in a patient.json file, acting as a lightweight database.

**Search & Sort**: Endpoints to view specific patients or sort the patient list based on physical metrics.

🛠️ Technologies Used
Python: The core programming language.

FastAPI: For building the web API.

Pydantic: For data modeling and validation.

Uvicorn: An ASGI server to run the application.

JSON: Used for local data storage.
