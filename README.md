# sqlalchemy-challenge
Glantz Adam Bootcamp RUT-VIRT-DATA-PT-04-2023-U-LOLC-MWTH - Module 10 SQLAlchemy Challenge

## TABLE OF CONTENTS

1. Project Description
   - Analyze and Explore Climate Data
   - Design Climate App
2. Installation
3. Contributing
4. Acknowledgements
5. Licenses

### 1. PROJECT DESCRIPTION

In this project, the author was tasked with making use of weather and weather station data from Hawaii. First, the author was instructed to **analyze and explore climate data** pulled from a sqlite file using the SQLAlchemy of Python, including running summary statistics and creating visualizations via Python's other libraries. Having become familiar with the data, the author was instructed to **design a climate app** using Flask, so that users can access APIs that retrieve weather and weather station data in the form of JSON lists. 

- [**Analyze and Explore Climate Data**](https://courses.bootcampspot.com/courses/3337/assignments/54000?module_item_id=961336)

The most current data was isolated by finding the last entry (8/23/2017) and working back by 365 days to get a year interval's worth of data. See **Figure 1** below for the resulting plot of precipitation data, which shows considerable volatility in volume over time.

![Precipitation_One_Year_Interval](https://github.com/aglantzrbc/sqlalchemy-challenge/assets/127694342/75d38e23-0307-4104-9c5e-34cf3510294e)

**Figure 1** | *Plot of precipitation in inches in Hawaii USA from weather station observations between 8/23/2016 through 8/23/2017, with null values dropped*

Further insight was provided by summary statistics, which can be found in **Table 1** below.

**_Please note that the author's findings use a slightly lower volume than the table in the starter code (2015 vs. 2021, respectively) because he eliminated NA values before tabulating._**

![image](https://github.com/aglantzrbc/sqlalchemy-challenge/assets/127694342/78cde0e3-5219-47ab-bc96-54eb704e481d)

**Table 1** | *Summary statistics of the volume of weather station precipitation observations in Hawaii USA between 8/23/2016 through 8/23/2017, with null values dropped*

The most active weather station out of the nine by volume of observations was identified: *WAIHEE 837.5, HI US Station ID USC00519281*, with 2772 observations. **Figure 2** is a 12-bin histogram showing temperature observations (tobs) for this weather station over a year. The plot is unipolar with temperatures most frequenly in the mid-70s (Fahrenheit).

![Tobs](https://github.com/aglantzrbc/sqlalchemy-challenge/assets/127694342/5c11f138-43c1-4c81-9fa0-b64a2a687561)

**Figure 2** | *Histogram of temperature observations (tobs) from weather station USC0051928 between 8/23/2016 through 8/23/2017**

- [**Design Climate App**](https://courses.bootcampspot.com/courses/3337/assignments/54000?module_item_id=961336)

The flask library was employed to create an application object, which was then decorated to make [API routes](http://localhost:5000/).

**_Though establishing the "Measurement" and "Station" variable names in all lower case (i.e., "measurement" and "station") is ideal, the author didn't do this for the following reasons:_**

1. Keeping the "Station" variable upper-lower case prevents confusion with the function "station" and the attribute "Station.station", which occur toward the end of the Python code.
2. Keeping the "Measurement" variable upper-lower maintains consistency with the concurrent "Station" variable, described above.
3. It should be noted that the "Base" variable assigned with "automap_base()" was also kept in upper-lower case, because this is what the SQLAlchemy automap function expects.

The following **static API** routes were created besides the [welcome ("/") route](http://localhost:5000/).

**_All the links assume the user runs the app.py code and employs port 5000 for Flask output._**

- [Precipitation route](http://localhost:5000/api/v1.0/precipitation)

*This provides a JSON list of the last 12 months worth of precipitation data, using the date and precipitation volume keys.*

- [Stations route](http://localhost:5000/api/v1.0/stations)

*This provides a JSON list of the nine weather stations with sequence ID and station ID keys.*

- [Tobs route](http://localhost:5000/api/v1.0/tobs)

*This provides a JSON list of the last 12 months worth of temperature observation (tobs) data from the most active station, using the tobs value and date keys.*

A **dynamic API** route was also set up.

- Start-End route

*This is set up with the decoration "/api/v1.0/**[start]**/**[end]**", where [start] and [end] are to be replaced with start and end dates using the format: YYYY-mm-dd/YYYY-mm-dd.* Example: http://localhost:5000/api/v1.0/2016-08-23/2017-08-23. Date ranges outside the scope of actual dates occurring in the dataset will default to the earliest and latest dates in the data.
If only one date is provided, the output will calculate from that date through the latest record in the dataset.

### 2. INSTALLATION

- The [GitHub repository]([https://github.com/aglantzrbc/sqlalchemy-challen](https://github.com/aglantzrbc/sqlalchemy-challen) containing all project files is publicly accessible.
- The assignment details and starter code are proprietary and located on the [Rutgers University](https://www.rutgers.edu/) ([edX](https://www.edx.org/)) Bootcamp Spot [Module 9 SQL Challenge](https://courses.bootcampspot.com/courses/3337/assignments/54030?module_item_id=961277) page.
- All code source files were coded in [postgreSQL](https://www.postgresql.org/) version 11 through the [pgAdmin](https://www.pgadmin.org/) 4 version 7 application.
- This project's **table schemata source file** is available in the repository under the name: [EmployeeSQL_code_schemata.sql](https://github.com/aglantzrbc/sql-challenge/blob/main/EmployeeSQL_code_schemata.sql).
- This project's **queries source file** is available in the repository under the name: [EmployeeSQL_code_queries.sql](https://github.com/aglantzrbc/sql-challenge/blob/main/EmployeeSQL_code_queries.sql).
- The **data modeling diagram file** is [EmployeeSQL_diagram_erd.pgerd](https://github.com/aglantzrbc/sql-challenge/blob/main/EmployeeSQL_diagram_erd.pgerd) and can be accessed using the [*QuickDBD*](http://www.quickdatabasediagrams.com/) functionality.
- A **scan of the data modeling diagram file** is available with a .png extension here: [EmployeeSQL_diagram_scan.png](https://github.com/aglantzrbc/sql-challenge/blob/main/EmployeeSQL_diagram_scan.png).

### 3. CONTRIBUTING

- [Glantz, Adam](https://www.linkedin.com/in/adam-glantz/): Annapolis, Maryland, USA, June 2023, email: adamglantz@yahoo.com

### 4. ACKNOWLEDGEMENTS

In addition to using the GitHub, Rutgers University (edX), Jupyter Notebook, VSCode resources listed above, the author acquired query responses in OpenAI's [ChatGPT](https://chat.openai.com/) platform.

The author also consulted code and results from similar projects publicly accessible in [GitHub](https://github.com/) repositories and recoverable through [Google](https://www.google.com/) and comparable search engines:

- [Mehta, Pragati](https://www.linkedin.com/in/pragati-mehta-%E2%99%95-3b10823/): Pennington, New Jersey, USA, September 2018. [Hawaii-Climate-Analysis-using-SQLALCHEMY](https://github.com/PragatisGitHub/Hawaii-Climate-Analysis-using-SQLALCHEMY)
- [Thorpe, Margaret](https://www.linkedin.com/in/margaret-thorpe-datapm/): Trinidad, California, USA, May 2021. [sqlalchemy-challenge](https://github.com/MThorpester/sqlalchemy-challenge)
- [Yousuf, Bennet](https://www.linkedin.com/in/bennetyousuf/): Dallas, Texas, USA, June 2021. [sqlalchemy-challenge](https://github.com/bennetyousuf/sqlalchemy-challenge)

### 5. LICENSES

**N/A**

