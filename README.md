Student Enrollment System (JPDB Micro-Project)
Description
This project is a dynamic Student Enrollment Form designed to manage student records efficiently. It features a real-time data validation system that interacts with JsonPowerDB (JPDB). The form intelligently detects whether a student (via Roll-No) already exists in the database. If the record exists, it retrieves and displays the data for updating; if not, it allows for a new entry.

Table of Contents
Benefits of using JsonPowerDB

Scope of Functionalities

Illustrations

Examples of Use

Release History

Project Status

Benefits of using JsonPowerDB
Real-time Performance: Built on top of a lightning-fast indexing engine, ensuring minimal latency during CRUD operations.

Schema-free: As a NoSQL database, it allows for flexible data structures without complex migrations.

Serverless Integration: Eliminates the need for server-side code (like PHP or Node.js) by allowing the frontend to communicate directly with the database via a REST API.

Low Memory Footprint: Extremely efficient in resource management compared to traditional relational databases.

Scope of Functionalities
Primary Key Validation: Automatically checks for existing Roll-No on field blur.

State Management: Controls the "Enabled/Disabled" status of form inputs and buttons based on database response.

Data Persistence: Supports full CRUD (Create, Read, Update) functionality.

Input Sanitization: Prevents empty records from being saved to the SCHOOL-DB.

Illustrations
Below is the logical flow of the application:

Examples of Use
Enrolling a New Student: Enter a unique Roll-No. The form unlocks. Fill in the name, class, and dates. Click Save.

Updating Records: Enter an existing Roll-No (e.g., 101). The system fetches "Arjun Sharma" from the database. Modify the "Address" and click Update.

Clearing the Workspace: Click Reset at any time to lock the form and start a new search.

Release History
v1.0.0 (Current): * Initial release of the Student Enrollment Form.

Integration with jpdb-commons.js.

Implementation of GET, PUT, and UPDATE commands.

Basic UI with Bootstrap 3.4.

Project Status
Completed. The micro-project fulfills all requirements for the form-based database interaction using JsonPowerDB.

Sources
JsonPowerDB Documentation

Bootstrap Framework

jQuery Library

Other Information
This project was developed as a Micro-Project to demonstrate the integration of High-Performance Web Services with frontend forms.
