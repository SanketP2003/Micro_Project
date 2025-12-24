# Student Enrollment System (JPDB Micro-Project)

## Description

This project is a dynamic **Student Enrollment Form** designed to manage student records efficiently. It features a real-time data validation system that interacts with **JsonPowerDB (JPDB)**. The form integrates seamlessly with JPDB's REST API to perform CRUD operations without requiring any backend server code.

---

## Table of Contents

- [Benefits of using JsonPowerDB](#benefits-of-using-jsonpowerdb)
- [Scope of Functionalities](#scope-of-functionalities)
- [Illustrations](#illustrations)
- [Examples of Use](#examples-of-use)
- [Release History](#release-history)
- [Project Status](#project-status)
- [Sources](#sources)
- [Other Information](#other-information)

---

## Benefits of using JsonPowerDB

- **Real-time Performance**: Built on top of a lightning-fast indexing engine, ensuring minimal latency during CRUD operations.
- **Schema-free**: As a NoSQL database, it allows for flexible data structures without complex migrations.
- **Serverless Integration**: Eliminates the need for server-side code (like PHP or Node.js) by allowing the frontend to communicate directly with the database via a REST API.
- **Low Memory Footprint**: Extremely efficient in resource management compared to traditional relational databases.
- **Easy to Use**: Simple API commands for database operations (GET, PUT, UPDATE).
- **Multi-mode Database**: Supports Document DB, Key-Value DB, and RDBMS use cases.

---

## Scope of Functionalities

- **Primary Key Validation**: Automatically checks for existing Roll-No on field blur.
- **State Management**: Controls the "Enabled/Disabled" status of form inputs and buttons based on database response.
- **Data Persistence**: Supports full CRUD (Create, Read, Update) functionality.
- **Input Sanitization**: Prevents empty records from being saved to the SCHOOL-DB.

---

## Illustrations

Below is the logical flow of the application:

```
┌─────────────────┐
│  Enter Roll-No  │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│ Check if exists in  │
│     JPDB Database   │
└────────┬────────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌───────┐  ┌────────┐
│  New  │  │ Exists │
└───┬───┘  └───┬────┘
    │          │
    ▼          ▼
┌───────┐  ┌────────┐
│ SAVE  │  │ UPDATE │
└───────┘  └────────┘
```

---

## Examples of Use

1. **Enrolling a New Student**:
   - Enter a unique Roll-No
   - The form unlocks
   - Fill in the name, class, birth date, address, and enrollment date
   - Click **Save**

2. **Updating Records**:
   - Enter an existing Roll-No (e.g., 101)
   - The system fetches the existing record from the database
   - Modify the required fields (e.g., "Address")
   - Click **Update**

3. **Clearing the Workspace**:
   - Click **Reset** at any time to lock the form and start a new search

---

## Release History

| Version | Date | Description |
|---------|------|-------------|
| **v1.0.0** | 2025-12-24 | Initial release of the Student Enrollment Form |

### v1.0.0 (Current Release)
- Initial release of the Student Enrollment Form
- Integration with `jpdb-commons.js`
- Implementation of GET, PUT, and UPDATE commands
- Basic UI with Bootstrap 3.4
- Form validation and state management

---

## Project Status

✅ **Completed**

The micro-project fulfills all requirements for the form-based database interaction using JsonPowerDB.

---

## Sources

- [JsonPowerDB Documentation](https://login2explore.com/jpdb/docs.html)
- [Bootstrap Framework](https://getbootstrap.com/)
- [jQuery Library](https://jquery.com/)

---

## Other Information

- **Developer**: SanketP2003
- **Purpose**: This project was developed as a Micro-Project to demonstrate the integration of High-Performance Web Services with frontend forms.
- **Database Used**: JsonPowerDB (JPDB)
- **Frontend Technologies**: HTML, CSS, JavaScript, jQuery, Bootstrap 3.4

---

### License

This project is open source and available for educational purposes.