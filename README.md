# Prueba técnica para desarrolladores backend de tuHabi

## Project Structure

The project is structured based on the Repository and the Dependency Injection Patterns.

```
API/
    contexts/                               // Database contexts
    controllers/                            // Endpoint definitions
    interfaces/                             // Interfaces to connect to databases
    models/                                 // Pydantic models
    repositories/                           // Repositories that uses interfaces
    services/                               // Services
    .gitignore                              // Ignore files for Git
    config.py                               // File that loads the env vars
    main.py                                 // Server manager
    README.md                               // Instructions file
    requirements.txt                        // Requirements for the application
    example.env                             // Example for project's variables
    request_example.json                    // Example of the request structure for using the endpoint
```

<div style="margin-bottom: 3%"></div>

## Requirements

For this project you need the next requirements

* Python >= 3.7
* pip >= 19.0.2
* virtualenv or pyenv

Then you have to create a virtual environment

* With virtualenv:

  ```console
  $ virtualenv -p python3 venv

  $ source venv/bin/activate

  $ pip install -r requirements.txt
  ```

* With pyenv:
  ```console
  $ pyenv virtualenv 3.8.x venv

  $ pyenv activate venv

  $ pip install -r requirements.txt
  ```
<div style="margin-bottom: 3%"></div>

## Local Environment

### DB

For the test's purposes, a tuHabi's database was used. If you want to use it, please contact them :D.

### Run the API

To run the API use the following code:

```console
$ ENV=dev uvicorn main:app --reload --port 3001

INFO:     Uvicorn running on http://127.0.0.1:3001 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

<div style="margin-bottom: 3%"></div>


## Documentation

Because the API is built using FastAPI, the documentation for the endpoints is built automatically.

### OpenAPI

Previously known as Swagger UI, to access the interactive docs open your browser at <a href="http://127.0.0.1:3001/docs" class="external-link" target="_blank">http://localhost:3001/docs</a>.

Using this platform, you can test the endpoint.

## Explanation

### Task 1: Consultation service

1. The name of the endpoint is `/PropertiesInfo`
2. You can access this endpoint with a GET request
3. This endpoint returns some information about the properties that are saved in tuHabi's database which status is `preventa` (presale), `en venta` (on sale), or  `vendido` (sold). These property's info are: property's year of construction, property's address, property's city, property'status, property's price, and property's description.
4. You can filter the data using some optional parameters.

    4.1 *year*: Integer parameter. Using this parameter you will obtain all the properties which year of construction matches with it.

    4.2 *city*: String parameter. Using this parameter you will obtain all the properties which city's text contains it. 

    4.3 *status*: Integer/parameter. Using this parameter you will obtain all the properties which status matches with it. The reason why you can send an integer or a string value relies on the idea that some filters on the front-end development uses either numeric or string ids.  `preventa` = 3, `en venta` = 4, `vendido` = 5

### Task 2: Properties can be liked by user service

1. According to the analysis of the ERD and RD (you can watch them in `images/ERD_Task2.png` and `RD_Task2.png` respectively), the solution for this task is to create another table called `properties_liked_by` due to the relationship between the tables `auth_user` and `property` is many-to-many. In this new table the id of both the user and the property is saved (datetime in which this action was done is saved as well).
2. The query for creating the table is:
```
CREATE TABLE properties_liked_by  (id_user int(11) NOT NULL, id_property int(11) NOT NULL,
  date_like datetime NULL,
  FOREIGN KEY (id_user) REFERENCES auth_user (id),
  FOREIGN KEY (id_property) REFERENCES property (id)
);
```
3. The query for inserting the user's 'like' is:
```
INSERT INTO properties_liked_by (id_user, id_property, date_like) VALUES (<id_user>, <id_property>, NOW());
```
4. The query for retrieving the liked properties (their id's) done by a user is:
```
SELECT id_property FROM properties_liked_by WHERE id_user = <id_user>
```
5. The query for retrieving which users (their id's) have liked a property is:
```
SELECT id_user FROM properties_liked_by WHERE id_property = <id_property>
```
6. The query for deleting a user's like is:
```
DELETE FROM properties_liked_by WHERE id_user = <id_user>
```

### Task 3 (Optional): New DB's design
I realized that the number of queries performed to join `property` and `status_history` in order to know the current property's status can be optimized if you add a new field in `property` table called `status`. This new status field would be updated every single time the property changes of status. The `status_history` table keeps tracking the statuses' changes (if necessary).

With this change the query to retrieve the property's information changes from
```
SELECT p.*, st.status FROM property AS p, (SELECT sh.property_id, st.name AS status FROM status_history sh INNER JOIN `status` st ON st.id = sh.status_id WHERE sh.property_id = <id_property> ORDER BY sh.update_date DESC LIMIT 1) AS st WHERE st.property_id = p.id
```
to 
```
SELECT p.*, st.status FROM property AS p INNER JOIN status AS st ON st.id = p.status WHERE p.id = <id_property>
```
The relationship diagram can be seen in `images/RD_Task3.png`