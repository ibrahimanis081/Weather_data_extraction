<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->


<!-- PROJECT LOGO -->
<br />
<div align="center">
  
   <h3 align="center">Weather Forecast Data Pipeline</h3>
 
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Building a Weather forecast dashboard using data extracted from Stomglass Global API.
Stormglass provides future and historical data from the world’s most trusted meteorological institutions in one single API https://stormglass.io/. Data are provided base on a given coordinate.
<br/>
You will be extracting the tempreture, humidity and precicipitation data for the next seven days, transform, load and visualize the data using the steps illustrated in the diagram below.

[![weather-pipeline-Page-1-drawio-2.png](https://i.postimg.cc/hjgX7PNY/weather-pipeline-Page-1-drawio-2.png)](https://postimg.cc/VSGfx1f9)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With
<br/>

* ![Python](https://img.shields.io/badge/python-233161.svg?style=for-the-badge&logo=python&logoColor=yellow)

* ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

* ![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-233161?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)

* ![Grafana](https://img.shields.io/badge/grafana-017CEE?style=for-the-badge&logo=grafana&logoColor=fdd54)


<!-- GETTING STARTED -->
## Getting Started
### Install python
Python is used to pull data, transform and load the data into a database.
download python here
[Python](https://www.python.org/downloads/)

### Set up postgres
You will need a database to store the data pulled from the API. Follow these [steps](https://www.postgresql.org/download/linux/ubuntu/) to download and install postgres on ubuntu.
* After the instalation, run the following commands from PSQL CLI;

```sql
--Create a database
CREATE DATABASE weather_db;
```

```sql
--Connect to the database
\c weather_db;
```

```sql
--Create a table
CREATE TABLE weather_table(timestamp TIMESTAMP PRIMARY KEY NOT NULL, temperature FLOAT, humidity FLOAT, precipitation FLOAT
);
```

```sql
--Create a user
CREATE USER weather_user WITH PASSWORD 'weather_pass';
```

```sql
--Grant selected privileges to the user
GRANT SELECT, INSERT, UPDATE, DELETE ON weather_table TO weather_user;
```
#### Optional
Apache Airflow ships with a SQLite database as its default metadata database which does not allow for running parallel tasks with the default SequentialExecutor.

You can instead set up postgres as the metadata database and change the executor to LocalExecutor which allows for paralellism. To do that, you have to first create a database specifically for airflow.
* run the following commands from PSQL CLI

```sql
--Create database
CREATE DATABASE airflow_db;
```

```sql
--Create a user
CREATE USER airflow_user WITH PASSWORD 'airflow_pass';
```

```sql
--Grant all privileges to the user
GRANT ALL PRIVILEGES ON DATABASE airflow_db TO airflow_user;
```
### Apache Airflow: 
A workflow orchestrator use to define how and in what order to run your pipeline.
<br/>
Since it requires a lot of specific dependencies, it is adviced to run airflow in a virtual environment. Navigate to your project folder from the CLI and the run the following commands;

```py
# create a python virtual environment called venv
python -m venv venv
```

```py
# activate the virtual environment
source venv/bin/activate
```

```py
# install the 'requirements.txt' file, contains airflow and all its dependencies
pip install -r requirements.txt
```

* To verify that airflow is installed, from the virtual environment run
```
airflow info
```

* If it doesn't throw an error, airflow is installed correctly.
* Move to the `airflow` folder which is created by default in your `home` directory.
* Create a directory called `'dags'`.
* Inside the `'dags'` directory create another directory `'python_scripts'` to house our python script and allow easier import into our airflow dag file.

#### Configuring airflow metadata database
* If you previously set up postgres as the airflow metadata database, then you need to change the airflow configuration file to relect this, otherwise skip this step.
* Move to `airflow` folder in your `home` diretory.
* Open the `airflow.cfg` file.
* Change the executor to `LocalExecutor`.
* Also change the sql_alchemy_conn to `postgresql+psycopg2://airflow_user:airflow_pass@localhost/airflow_db`.
* Save and close the file.

## Further Settings
* Move the `weather_dag.py` file to the `dags` directory.
* Open the file `weather_dag.py`, change the `start_date` to tomorrow’s
* Also move the `weather_data.py` to the `python_scripts` directory.
* Get a free API Authorization Key  [here](https://stormglass.io/)
* Enter your API in `weather_data.py`
   ```py
   'Authorization': 'ENTER YOUR API'
   ```
#### Running Airflow

* From your virtual environment, run this command to start the airflow webserver and scheduler

```
airflow standalone
```

* open your browser and go to `localhost:8080,` the default port for airflow.
* from the list of dags, trigger `weather_pipeline`.

[![weather-pipeline.jpg](https://i.postimg.cc/1RN9L6Cy/weather-pipeline.jpg)](https://postimg.cc/MXq2BcJL)

[![graph-view.jpg](https://i.postimg.cc/NF1vL6ST/graph-view.jpg)](https://postimg.cc/1V5jjq95)


[![trigger-dag.jpg](https://i.postimg.cc/CxpVyQZN/trigger-dag.jpg)](https://postimg.cc/rKjHxgN0)

* after it runs successfully, open PSQL CLI.
* connect with your weather_database.
```sql
\c weather_db;
```

* run this command to verify that the data was inserted into the database
```sql
SELECT * FROM weather_table;
```
### Visualization
You can then use any graphical software to visualize your data.


<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_


<!-- CONTACT -->
## Contact

[@ابراهيم انيس](https://twitter.com/ibrahim__Anees)


<p align="right">(<a href="#readme-top">back to top</a>)</p>


