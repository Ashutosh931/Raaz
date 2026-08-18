# Database Design

## 1. Relational Entity-Relationship (ER) Model
The application uses SQLite as its embedded relational database engine, managed via SQLAlchemy ORM.

```
+------------------+         1 : N         +----------------------+
|      users       |--------------------->|     predictions      |
|------------------|                      |----------------------|
| PK id (INT)      |                      | PK id (INT)          |
|    name (VARCHAR)|                      | FK user_id (INT)     |
|    email (VARCHAR|                      |    date (VARCHAR)    |
|    password_hash |                      |    time (VARCHAR)    |
|    currency (STR)|                      |    hour (INT)        |
|    tariff (FLOAT)|                      |    temperature(FLOAT)|
|    created_at(DT)|                      |    humidity (FLOAT)  |
+------------------+                      |    people (INT)      |
      |        |                          |    predicted_kwh     |
1 : N |        | 1 : N                    |    estimated_cost    |
      |        |                          |    category (VARCHAR)|
      v        v                          +----------------------+
+----------------------+   +----------------------+
|    energy_records    |   |        alerts        |
|----------------------|   |----------------------|
| PK id (INT)          |   | PK id (INT)          |
| FK user_id (INT)     |   | FK user_id (INT)     |
|    date (VARCHAR)    |   |    alert_type (STR)  |
|    time (VARCHAR)    |   |    title (VARCHAR)   |
|    hour (INT)        |   |    message (TEXT)    |
|    consumption(FLOAT)|   |    is_read (BOOLEAN) |
|    cost (FLOAT)      |   |    created_at (DT)   |
|    source (VARCHAR)  |   +----------------------+
|    created_at (DT)   |
+----------------------+
```

## 2. Table Specifications

### 1. `users` Table
Stores authenticated user accounts.
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique user identifier |
| `name` | VARCHAR(100) | NOT NULL | User's full name |
| `email` | VARCHAR(120) | UNIQUE, NOT NULL, INDEX | User login email |
| `password_hash` | VARCHAR(256) | NOT NULL | Hashed password |
| `currency` | VARCHAR(10) | DEFAULT '₹' | Preferred currency symbol |
| `default_tariff`| FLOAT | DEFAULT 8.0 | Default electricity rate per kWh |
| `created_at` | DATETIME | DEFAULT UTC_NOW | Timestamp of account registration |

### 2. `predictions` Table
Stores all historical predictions executed by the ML inference engine.
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique prediction ID |
| `user_id` | INTEGER | FOREIGN KEY (`users.id`) | Reference to user |
| `date` | VARCHAR(20) | NOT NULL | Date of prediction |
| `time` | VARCHAR(10) | NOT NULL | Time of prediction |
| `hour` | INTEGER | DEFAULT 12 | Hour of day (0–23) |
| `temperature` | FLOAT | NOT NULL | Ambient temperature (°C) |
| `humidity` | FLOAT | NOT NULL | Relative humidity (%) |
| `people` | INTEGER | DEFAULT 1 | Occupancy count |
| `appliance_usage`| VARCHAR(20) | DEFAULT 'Medium' | Categorical appliance level |
| `previous_consumption` | FLOAT | NOT NULL | Previous hour lag consumption |
| `predicted_consumption`| FLOAT | NOT NULL | Random Forest output in kWh |
| `estimated_cost` | FLOAT | NOT NULL | Billed amount in user currency |
| `category` | VARCHAR(20) | DEFAULT 'Normal' | Low, Normal, or High |
| `recommendations_json` | TEXT | NULLABLE | JSON list of recommendations |
| `created_at` | DATETIME | DEFAULT UTC_NOW | Timestamp created |

### 3. `energy_records` Table
Stores time-series consumption records (both synthetic seed data and uploaded CSV records).
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique record ID |
| `user_id` | INTEGER | FOREIGN KEY (`users.id`) | Reference to user |
| `date` | VARCHAR(20) | NOT NULL, INDEX | Date of record (YYYY-MM-DD) |
| `time` | VARCHAR(10) | DEFAULT '00:00' | Time string |
| `hour` | INTEGER | DEFAULT 0 | 24-hour integer |
| `consumption` | FLOAT | NOT NULL | Energy consumed in kWh |
| `temperature` | FLOAT | NULLABLE | Temperature (°C) |
| `humidity` | FLOAT | NULLABLE | Humidity (%) |
| `people` | INTEGER | DEFAULT 1 | Occupant count |
| `appliance` | VARCHAR(50) | DEFAULT 'All' | Appliance label |
| `cost` | FLOAT | DEFAULT 0.0 | Calculated monetary cost |
| `source` | VARCHAR(30) | DEFAULT 'manual' | Source tag (`seed`, `upload`, `manual`) |
| `created_at` | DATETIME | DEFAULT UTC_NOW | Logged timestamp |

### 4. `alerts` Table
Stores system notifications and high consumption warnings.
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique alert ID |
| `user_id` | INTEGER | FOREIGN KEY (`users.id`) | Reference to user |
| `alert_type` | VARCHAR(20) | DEFAULT 'info' | `info`, `warning`, `critical`, `success` |
| `title` | VARCHAR(120) | NOT NULL | Short title |
| `message` | TEXT | NOT NULL | Full alert explanation |
| `is_read` | BOOLEAN | DEFAULT FALSE | Read state flag |
| `created_at` | DATETIME | DEFAULT UTC_NOW | Timestamp raised |
