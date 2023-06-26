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

- The following **static API** routes were created besides the [welcome ("/") route](http://localhost:5000/).

**_All the links assume the user runs the app.py code and employs port 5000 for Flask output._**

- [Precipitation route](http://localhost:5000/api/v1.0/precipitation)

*This provides a JSON list of the last 12 months worth of precipitation data, using the date and precipitation volume keys.*

- [Stations route](http://localhost:5000/api/v1.0/stations)

*This provides a JSON list of the nine weather stations with sequence ID and station ID keys.*

- [Tobs route](http://localhost:5000/api/v1.0/tobs)

*This provides a JSON list of the last 12 months worth of temperature observation (tobs) data from the most active station, using the tobs value and date keys.*

The *dept_name* attribute was made unique, since this is the "source of truth" for department names on all other lists. **See Figure 2 and Code Block 1, both below.**

![departments_table](https://github.com/aglantzrbc/sql-challenge/assets/127694342/d8dcbf85-f100-40f7-aad9-7cd3c24b0d61)

**Figure 2** | *departments list table and postgreSQL code*

```
-- Create departments table
CREATE TABLE departments (
    dept_no VARCHAR(4) NOT NULL,
    dept_name VARCHAR(40) NOT NULL,
    PRIMARY KEY (dept_no),
    UNIQUE (dept_name) -- source of truth for rest of tables
);

SELECT * FROM departments;
```
**Code Block 1** | *departments list table postgreSQL code block*

*dept_emp list:*

As aforementioned, this list didn't have a unique attribute, so both *emp_no* and *dept_no* (Department Number) were used as a [composite key](https://en.wikipedia.org/wiki/Composite_key), as commented in the code. **See Figure 3 and Code Block 2, both below.**

![dept_emp_table](https://github.com/aglantzrbc/sql-challenge/assets/127694342/5a43c9c9-3db2-486a-94f0-81b219ec7f11)

**Figure 3** | *dept_emp list table and postgreSQL code*

```
-- Create dept_emp table
CREATE TABLE dept_emp (
    emp_no INT NOT NULL,
    dept_no VARCHAR(4) NOT NULL,
    FOREIGN KEY (emp_no) REFERENCES employees (emp_no),
    FOREIGN KEY (dept_no) REFERENCES departments (dept_no),
    PRIMARY KEY (emp_no, dept_no) -- composite key
);

SELECT * FROM dept_emp;
```
**Code Block 2** | *dept_emp list table postgreSQL code block*

*dept_manager list:*

 **See Figure 4 and Code Block 3, both below.**

![dept_manager_table](https://github.com/aglantzrbc/sql-challenge/assets/127694342/94255ac3-ee4f-45c0-9f8e-342fb1deab47)

**Figure 4** | *dept_manager list table and postgreSQL code*

```
-- Create dept_manager table
CREATE TABLE dept_manager (
    dept_no VARCHAR(4) NOT NULL,
    emp_no INT NOT NULL,
    FOREIGN KEY (dept_no) REFERENCES departments (dept_no),
    FOREIGN KEY (emp_no) REFERENCES employees (emp_no),
    PRIMARY KEY (emp_no)
);

SELECT * FROM dept_manager;
```
**Code Block 3** | *dept_manager list table postgreSQL code block*

*employees list:*

 **See Figure 5 and Code Block 4, both below.**

![employees_table](https://github.com/aglantzrbc/sql-challenge/assets/127694342/c147f448-812b-49f2-81bd-13d06f90d243)

**Figure 5** | *employees list table and postgreSQL code*

```
-- Create employees table
CREATE TABLE employees (
    emp_no INT NOT NULL,
    emp_title_id VARCHAR(5) NOT NULL,
    birth_date DATE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    sex VARCHAR(1) NOT NULL,
    hire_date DATE NOT NULL, 
    FOREIGN KEY (emp_title_id) REFERENCES titles (title_id),
    PRIMARY KEY (emp_no)
);

SELECT * FROM employees;
```
**Code Block 4** | *employees list table postgreSQL code block*

*salaries list:*

 **See Figure 6 and Code Block 5, both below.**

![salaries_table](https://github.com/aglantzrbc/sql-challenge/assets/127694342/fb9f7058-c93e-4a05-9200-dc2b7801e0b5)

**Figure 6** | *salaries list table and postgreSQL code*

```
-- Create salaries table
CREATE TABLE salaries (
    emp_no INT NOT NULL,
    salary INT NOT NULL,
    FOREIGN KEY (emp_no) REFERENCES employees (emp_no),
    PRIMARY KEY (emp_no)
);

SELECT * FROM salaries;
```
**Code Block 5** | *salaries list table postgreSQL code block*

*titles list:*

The *title* attribute was made unique, since this is the "source of truth" for titles on all other lists. **See Figure 7 and Code Block 6, both below.**

![titles_table](https://github.com/aglantzrbc/sql-challenge/assets/127694342/c3bcb885-b4b4-4b3b-b81d-1bcaaa83918c)

**Figure 7** | *titles list table and postgreSQL code*

```
-- Create titles table
CREATE TABLE titles (
    title_id VARCHAR(5) NOT NULL,
    title VARCHAR(40) NOT NULL,
    PRIMARY KEY (title_id),
    UNIQUE (title) -- source of truth for rest of tables
);

SELECT * FROM titles;
```
**Code Block 6** | *titles list table postgreSQL code block*

*Scan of code to display tables:*

The order of tables, above, is alphabetical, but the tables were coded and run in a sequence to allow foreign keys to refer back to where they originate in previous blocks of code. See **Figure 8** for the actual run sequence.

![display_tables](https://github.com/aglantzrbc/sql-challenge/assets/127694342/38b52fad-29c8-42e9-9b7e-260153578403)

**Figure 8** | *Scan of postgreSQL code showing the coding block sequence for the tables*

- [**Data Analysis**](https://github.com/aglantzrbc/sql-challenge/blob/main/EmployeeSQL_code_queries.sql)

1. **_TASK:_** List the employee number, last name, first name, sex, and salary of each employee. **See Figure 9 and Code Block 7, both below.**

![task1_employees_general](https://github.com/aglantzrbc/sql-challenge/assets/127694342/7dbdfe8e-53ba-4cb6-a64f-f8f86e52f8f8)

**Figure 9** | *List of the employee number, last name, first name, sex, and salary of each employee*

```
/* List the employee number, last name, first name, sex, and salary 
of each employee. */

SELECT
    e.emp_no AS "Employee Number",
    e.last_name AS "Last Name",
    e.first_name AS "First Name",
    e.sex AS "Sex",
    CONCAT('$', TO_CHAR(s.salary, '999,999')) AS "Salary"
FROM
    employees e
    INNER JOIN salaries s ON e.emp_no = s.emp_no;
```

**Code Block 7** | *Code block for the list of the employee number, last name, first name, sex, and salary of each employee*

2. **_TASK:_** List the first name, last name, and hire date for the employees who were hired in 1986. **See Figure 10 and Code Block 8, both below.**

![task2_employees_1986](https://github.com/aglantzrbc/sql-challenge/assets/127694342/3cc1fe99-4760-4805-ae8f-a647966d15af)

**Figure 10** | *List of employees who were hired in 1986 by their first name, last name, and hire date*

```
/* List the first name, last name, and hire date for the 
employees who were hired in 1986. */

SELECT
    first_name AS "First Name",
    last_name AS "Last Name",
    hire_date AS "Hire Date"
FROM
    employees e
WHERE
    hire_date >= DATE '1986-01-01'
    AND hire_date < DATE '1987-01-01'
ORDER BY
    hire_date ASC;
```

**Code Block 8** | *Code block for the List of the employee number, last name, first name, sex, and salary of each employee*

3. **_TASK:_** List the manager of each department along with their department number, department name, employee number, last name, and first name. **See Figure 11 and Code Block 9, both below.**

![task3_managers_details](https://github.com/aglantzrbc/sql-challenge/assets/127694342/19002efa-dcf7-464c-9b8a-ed671460231a)

**Figure 11** | *List of the managers of each department along with their department number, department name, employee number, last name, and first name*

```
/* List the manager of each department along with their department 
number, department name, employee number, last name, and first name */

SELECT
    m.dept_no AS "Department Number",
    d.dept_name AS "Department Name",
    m.emp_no AS "Employee Number",
    e.last_name AS "Last Name",
    e.first_name AS "First Name"
FROM
    dept_manager m
INNER JOIN
    employees e ON e.emp_no = m.emp_no
INNER JOIN
    departments d ON d.dept_no = m.dept_no;
```

**Code Block 9** | *Code block for the list of the managers of each department along with their department number, department name, employee number, last name, and first name*

4. **_TASK:_** List the department number for each employee along with that employee’s employee number, last name, first name, and department name. **See Figure 12 and Code Block 10, both below.**

![task4_department_employee](https://github.com/aglantzrbc/sql-challenge/assets/127694342/c28655f4-787c-4b0b-8360-85c69545e66e)

**Figure 12** | *List of the department number for each employee along with that employee’s employee number, last name, first name, and department name*

```
/* List the department number for each employee along with that 
employee’s employee number, last name, first name, and department 
name */

SELECT
    b.dept_no AS "Department Number",
    e.emp_no AS "Employee Number",
    e.last_name AS "Last Name",
    e.first_name AS "First Name",
	d.dept_name AS "Department Name"
FROM
    employees e
INNER JOIN
    dept_emp b ON b.emp_no = e.emp_no
INNER JOIN
    departments d ON d.dept_no = b.dept_no;
```

**Code Block 10** | *Code block for the list of the department number for each employee along with that employee’s employee number, last name, first name, and department name*

5. **_TASK:_** List first name, last name, and sex of each employee whose first name is Hercules and whose last name begins with the letter B. **See Figure 13 and Code Block 11, both below.**

![task5_hercules_nameb](https://github.com/aglantzrbc/sql-challenge/assets/127694342/456ca428-4fb6-4c55-a07e-dcfce0f84bf5)

**Figure 13** | *List of the first name, last name, and sex of each employee whose first name is Hercules and whose last name begins with the letter B*

```
/* List first name, last name, and sex of each employee whose first
name is Hercules and whose last name begins with the letter B */

SELECT
    first_name AS "First Name",
    last_name AS "Last Name",
    sex AS "Sex"
FROM
    employees e
WHERE
    first_name = 'Hercules'
    AND last_name LIKE 'B%';
```

**Code Block 11** | *Code block for the list of the first name, last name, and sex of each employee whose first name is Hercules and whose last name begins with the letter B*

6. **_TASK:_** List each employee in the Sales department, including their employee number, last name, and first name. **See Figure 14 and Code Block 12, both below.**

![task6_employee_sales](https://github.com/aglantzrbc/sql-challenge/assets/127694342/1ab073b9-9405-479e-8fe2-7d16341376d3)

**Figure 14** | *List of each employee in the Sales department, including their employee number, last name, and first name*

```
/* List each employee in the Sales department, including their 
employee number, last name, and first name */

SELECT
    e.emp_no AS "Employee Number",
    e.last_name AS "Last Name",
    e.first_name AS "First Name"
FROM
    departments d
    INNER JOIN dept_emp b ON d.dept_no = b.dept_no
    INNER JOIN employees e ON b.emp_no = e.emp_no
WHERE
    d.dept_name = 'Sales';
```
![arrow up](https://github.com/aglantzrbc/sql-challenge/assets/127694342/020f42c9-7068-40f2-8c7b-7cd22da9cd12) 

**Code Block 12** | *Code block for the list of each employee in the Sales department, including their employee number, last name, and first name* **(Sales department filter indicated by a red arrow)**

7. **_TASK:_** List each employee in the Sales and Development departments, including their employee number, last name, first name, and department name. **See Figure 15 and Code Block 13, both below.**

![task7_sales_development](https://github.com/aglantzrbc/sql-challenge/assets/127694342/d258720c-e88c-49c5-b912-4f1adcc439ea)

**Figure 15** | *List of each employee in the Sales and Development departments, including their employee number, last name, first name, and department name*

```
/* List each employee in the Sales and Development departments, 
including their employee number, last name, first name, and department 
name */

SELECT
    e.emp_no AS "Employee Number",
    e.last_name AS "Last Name",
    e.first_name AS "First Name",
    d.dept_name AS "Department Name"
FROM
    employees e
    INNER JOIN dept_emp b ON e.emp_no = b.emp_no
    INNER JOIN departments d ON b.dept_no = d.dept_no
WHERE
    d.dept_name IN ('Sales', 'Development');
```

**Code Block 13** | *Code block for the list of each employee in the Sales and Development departments, including their employee number, last name, first name, and department name*

8. **_TASK:_** List the frequency counts, in descending order, of all the employee last names (that is, how many employees share each last name). **See Figure 16 and Code Block 14, both below.**

![task8_frequency_lastname](https://github.com/aglantzrbc/sql-challenge/assets/127694342/2f3b4bfe-7058-42e5-b258-547da48b9766)

**Figure 16** | *List of the frequency counts, in descending order, of all the employee last names*

```
/* List the frequency counts, in descending order, of all the 
employee last names (that is, how many employees share each 
last name) */

SELECT
	COUNT(*) AS "Frequency",
	last_name AS "Last Name"
FROM
    employees e
GROUP BY
    last_name
ORDER BY
    "Frequency" DESC;
```

**Code Block 14** | *Code block for the list of the frequency counts, in descending order, of all the employee last names*

### 2. INSTALLATION

- The [GitHub repository](https://github.com/aglantzrbc/sql-challenge) containing all project files is publicly accessible.
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

