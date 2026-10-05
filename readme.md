Fact? - it convey truth about something.

Data?
it is a collection of facts used for analysis

Information?
it is a processed meaningful data

Knowledge?
it uses the information to perform something
utilizing the information to complete a task

Wisdom?
the ability to take right decisions

Database:-
a database is referred to a well organized data.

    a media/place where the data is stored

    database can be:
        - paper with some data like list of students, records,etc
        - spreadsheet
        - Databases maintained by the DBMSs.(these databases are used by the software apps)

Database vs DBMS

DBMS (DataBase Management System): - it is a software application which creates,alters, drop and manipulates the databases.

Ex: MySQL, Postgres, MongoDB, etc.

Data Models:-
the data models represents the structure of the data to be stored in the database

    There are multiple data models

    1. Relational data model
        - this data model stores the data in the tables
        - tables are called relation
        - due to normalization the data will be stored into multiple tables and these
        tables will be in relationships using primary key, foreign keys,etc.

    2. document data model
        - this data model stores the data in the documents(json like objects)
        - this data model is more flexible, scalable and suitable or storing the unstructured data.

DBMS:- - the DBMS which follows to Relational data model are called Relational DBMS / RDBMS.
Ex: MySQL, PostgreSQL, MSSQL,etc.

    - the DBMS which follows to non relational data model are called NoSQL DBMS
    Ex. Mongodb

SQL - Structured Query Language - it is used to compose the commands to be given to RDBMS. - SQL is also called SEQueL(Structured English Query Language)

SQL vs NoSQL

SQL - query langauge for RDBMS
NoSQL - Not only SQL. all the DBMS except relational are called NoSQL DBMS.

SQL vs MySQL - SQL is query langauge to pass commands to MySQL - MySQL is RDBMS.

MySQL v Postgres

MySQL - Open source - preferred for content based apps like web apps, blogging, ecommerce, etc. - it is not suitable for JSON data - it is suitable for structured data - it requires predefined structure

Postgres - Open source - enterpries apps - it can easily store JSON data. - it is suitable for structured data - it requires predefined structure

MongoDB - it is NoSQL DBMS - it does not require predefined structured - it is suitable for structured and unstructured data - it supports vertical and horizontal scaling through 'sharding'

scaling:-
app -> database on a server(32 GB, 2TB SSD)

    1 million users -> 100 millions

vertical scaling - increases the resources(RAM, Processor, SSD) of same server machine

horizontal scaling - attach multiple server machines

SQL - Structured Query Language - it is a query langauge used to compose commands to be passed to RDBMS.

There are four categories of the SQL commands

1.  DDL - Data Definition Language

    - it is used to create the structure of the databases,tables,index,etc.
      Commands: Create, alter, drop

2.  DML - Data Manipulation Language
    it is used to manipulate(insert, update, delete) the data

        Commands: insert, update, delete

3.  DQL - Data Query Language
    it is used to read the data from database
    Commands: select

4.  DCL - Data Control Language - this is used to control the permissions
    Commands: revoke, set the permissions

Datatype:-

1. Numerical Types

- SMALLINT -> 2 bytes -> -32,768 to +32,767
- INTEGER/INT -> 4 bytes ->
- BIGINT -> 8 bytes large range integer (ids)
- DECIMAL/NUMERIC -> variable -> financial data amount
- REAL / DOUBLE -> 4/8 bytes -> scientific meansurements

- SERIAL (SMALLSERIAL - 2 bytes,SERIAL - 4 bytes,BIGSERIAL - 8 bytes)
  it is postgres specific used as autoincremented value

2. Text and Characters types

- VARCHAR(N) - variable length with a hard limit of 'N' characters
  it is preferred to store small text values like name, email,etc

- CHAR(N)
  fixed length. adds trailing spaces if shorter than 'N'.
  it is rarely used.
  use cases like storing 2 char country codes

- TEXT
  it is used to store unlimited variable length text.
  large texts like articles,etc.

3. Date and Time types

- DATE
  calendar date (year, month,date)

- TIME
  time of day without date

- TIMESTAMP
  Date+time without time zone context

- TIMESTAMPTZ
  timestamp with time zone.

4. Boolean and Enum Types

- BOOLEAN / BOOL
  TRUE, FALSE, NULL,
  it can accept string values like 'yes', 'no', '1', '0', 't', 'f'.

- ENUM
  it is postgres specific
  it allows to define custom static, strongly typed.

Ex: CREATE TYPE typename as ENUM ('value1', 'value2')

CREATE TYPE user_role as ENUM ('superadmin','admin','viewer')

5. Semi structured data: JSON and Arrays
   Normally SQL stores single values in a column But Postgres allows to store multiple values using json and arrays.

Ex:
CREATE TABLE post (
id SERIAL PRIMARY KEY,
tags TEXT[]
)

JSON and JSONB

JSON
it store raw json
write operation is faster but read operation is slower because every time it need to parse the raw json

JSONB
binary json deconstruct json into a decomposed binary form. slower to insert but faster to query.

    object->prop

DDL

list the databases

\l
\list

create database

> CREATE DATABSE mydb;

rename database name

> ALTER DATABASE mydb RENAME TO estore;

delete a database

> DROP DATABASE mydb;

Schema:-
schema is a virtual container within the database

    schema helps to group the tables

    two schemas can have tables of same name

- create a schema

  > CREATE SCHEMA schema_name;
  > CREATE SCHEMA sales;

- create a schema if not available

  > CREATE SCHEMA IF NOT EXISTS marketing;

- rename a schema

  > ALTER SCHEMA marketing RENAME TO branding;

- drop a schema

  > DROP SCHEMA branding;

- drop a schema if exists

  > DROP SCHEMA IF EXISTS branding;

- delete a schema along with all tables,views,etc.
  > DROP SCHEMA branding CASCADE;

Table:-

table -> columns(name and datatype, constraints)

> CREATE TABLE table_name(colname datatype,)

> CREATE TABLE sales.orders(order_id BIGINT GENERATED
> ALWAYS AS IDENTITY PRIMARY KEY, amount NUMERIC(12,2),

    status VARCHAR(20),
    cust_id INT

);

- create a new table by cloning table structure of existing table

> CREATE TABLE archive_orders( LIKE sales.orders
> INCLUDING DEFAULTS
> INCLUDING CONSTRAINTS
> INCLUDING INDEXES
> )

CREATE TABLE emps (emp_id SERIAL PRIMARY KEY,
name VARCHAR(50),
mobile VARCHAR(13) UNIQUE,
email VARCHAR(50) UNIQUE,
salary NUMERIC(10,2),
dept VARCHAR(50),
gender VARCHAR(20),
city VARCHAR(50)

)

modify the table structure
ALTER

- add new column

  > ALTER TABLE sales.emps

      ADD COLUMN designation VARCHAR(50);

- remove a column from table

  > ALTER TABLE sales.emps

      DROP COLUMN email;

- rename a column

  > ALTER TABLE sales.emps

      RENAME COLUMN mobile TO phone;

- change(set/drop) constraints

  > ALTER TABLE sales.emps
  > ALTER COLUMN phone SET NOT NULL;

- set default value to existing column

  > ALTER TABLE sales.emps

      ALTER COLUMN city SET DEFAULT "Pune";

- drop default value of city

  > ALTER TABLE sales.emps

      ALTER COLUMN city DROP DEFAULT;

- rename the table

  > ALTER TABLE sales.emps RENAME TO employees;

- TRUNCATE

  - removes all data from table but structure will be maintained.

- truncate a table

  > TRUNCATE TABLE employees;

- truncate a table and all table referencing it via foreign key

  > TRUNCATE TABLE employees CASCADE;

- reset identity/serial counters back to 1
  > TRUNCATE TABLE employees RESTART IDENTITY;

> ALTER TABLE employees ALTER COLUMN city TYPE INT;

Drop the table

> DROP TABLE sales.orders;
> DROP TABLE IF EXISTS orders;
> DROP TABLE orders CASCADE;

Constraints
constraints sets rules for the columns

PRIMARY KEY = to uniquely identify each row in a table

defining primary key

1. simply set primary key on a column

CREATE TABLE employees (
empId INT PRIMARY KEY,
name VARCHAR(50),
salary NUMERIC(10,2)
)

2.  set primary key on a column with sequence/auto_increment

CREATE TABLE employees (
empId INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
name VARCHAR(50),
salary NUMERIC(10,2)
)

3.  set primary key on a column with sequence/auto_increment

CREATE TABLE students (
roll_no INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
name VARCHAR(50),
std VARCHAR(20),
gender VARCHAR(15),
city VARCHAR(50)

);

CREATE TABLE users (
user_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
name VARCHAR(50),
mobile VARCHAR(20) UNIQUE NOT NULL,
gender VARCHAR(15),
city VARCHAR(50)

);

CREATE TABLE orders (
order_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
amount NUMERIC(10,2)
);

ALTER TABLE sales.orders
ADD COLUMN cust_id INT NOT NULL,
ADD CONSTRAINT suraj_key FOREIGN KEY (cust_id) REFERENCES users(user_id);

SERIAL = this is old, non standard postgres specific sequence
IDENTITY = this is the standard sequence in SQL, which supported in Postgres v10+

FOREIGN KEY
UNIQUE
NOT NULL
IDENTITY
SERIAL
DEFAULT
GENERATED ALWAYS
GENERATED BY DEFAULT
CHECK

INSERT INTO sales.users(name,mobile,gender,city)
VALUES ('aaa','1111111','male','Pune'),('bbb','222222222','female','Pune'),('cccc','33333333','male','Mumbai');

INSERT INTO sales.orders(amount) VALUES(1000)
INSERT INTO sales.orders(amount,cust_id) VALUES(1000,100);

UNIQUE
it force a column to insert only unique values
it can accept null values but whatever the values you are providing
those must be unique.

it can be used for a single column or a group of columns.

CREATE TABLE users (
user_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
name VARCHAR(50),
mobile VARCHAR(20) UNIQUE NOT NULL,
gender VARCHAR(15),
city VARCHAR(50)
);

CREATE TABLE admission (
id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
stud_id INT,
course_id INT,
UNIQUE(stud_id, course_id)
);

PRIMARY KEY vs UNIQUE

PK is used to uniquely identify each row in a table
UNIQUE is used to force to insert unique values for a columns

PK does not allows null values
UNIQUE allows null values

PK creates indexes

NOT NULL constraints

- it forces to provide a value for each rows. it makes a column as required

DEFAULT constraints

it is used to use a default value for a column if not provided.

CHECK constaint
it executes a condition for insert and update the rows, if condition
becomes true then only it allows insert and update operations otherwise
throws an error.

CREATE TABLE customers (
user_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
name VARCHAR(50) NOT NULL,
mobile VARCHAR(20) UNIQUE NOT NULL,
email TEXT UNIQUE,
age INT,
gender VARCHAR(15),
city VARCHAR(50) DEFAULT 'Pune',
status VARCHAR(50) DEFAULT 'active',
UNIQUE(name, city),
CONSTRAINT age_check CHECK(age >=18)
);

Constraints to existing table

ALTER TABLE employees
ADD CONSTRAINT ck_salary CHECK (salary > 0 )

INSERT INTO employees(name, phone, salary,dept) VALUES('aaa','9999999999', 1000, 'dev');

Indexing:-  
 An index is a database object that improves the speed of data retrival operations(SELECT).

Without index, it read every record to find a specific row.

With index, it jump directly to the relevant record.

1000000

SELECT \* FROM users WHERE email = 'topperskills@gmail.com'
1 row email ?
2 row email ?
3 row email ?
4 row email ?
99999
100000 row email ?

B tree

Sorting

tree structure

Create an index on a column

CREATE INDEX idx_name ON tablename(columnname);
CREATE INDEX idx_email ON users(email);

NOTE- indexes are default for PRIMARY KEY and UNIQUE constraints

INSERT command:-
it is used to insert the records in the table.

- insert a record. If you know the sequence of columns and wants to insert values of all columns.

  > INSERT INTO tablename VALUES(value1, value2);
  > INSERT INTO customers VALUES(1,'abcd','8787878787','abc@gmail.com',10);

- insert a record by specifying column names

  > INSERT INTO tablename (colname, colname) VALUES(value1, value2);
  > INSERT INTO customers(city,name,mobile,email,age) VALUES('Pune','abcd','8787878787','abc@gmail.com',20);

- insert multiple records

> INSERT INTO customers (city,name,mobile,email,age,gender)
> VALUES
> ('Pune','aaadd','8787878543','dadd@gmail.com',21,'male'),
> ('Mumbai','dddd','2323444444','ddd@gmail.com',22,'female'),
> ('Pune','ffff','434512343234','fff@gmail.com',23,'male'),
> ('Mumbai','gggg','5453212345','ggg@gmail.com',24,'female'),
> ('Pune','hhhh','9898987898','hhh@gmail.com',25,'male');

- insert records of customers table into users table

INSERT INTO users (name,mobile,gender,city)
SELECT name, mobile,gender,city FROM customers;

- insert a specific record from customers into users;

INSERT INTO users (name,mobile,gender,city)
SELECT name, mobile,gender,city FROM customers
WHERE name = 'ffff';

- insert a transformed records from customers into users;

INSERT INTO users (name,mobile,gender,city)
SELECT UPPER(name), mobile,LOWER(gender),city FROM customers
WHERE name = 'ffff';

- to insert a record with default values only
  this is useful only if every column has default value.

INSERT INTO tablename
DEFAULT VALUES;

- insert and return

  > INSERT INTO customers(city,name,mobile,email,age)
  > VALUES('Satara','ppp','9856542354','ppp@gmail.com',25)
  > RETURNING name,mobile;

- ignore the MOBILE conflicts

INSERT INTO customers(city,name,mobile,email,age)
VALUES('Satara','ppp','9856542354','ppp@gmail.com',25)
ON CONFLICT (mobile)
DO NOTHING;

- ignore the conflicts on any unique constraints

INSERT INTO customers(city,name,mobile,email,age)
VALUES('Satara','ppp','9856542354','ppp@gmail.com',25)
ON CONFLICT DO NOTHING;

Updation

> UPDATE tablename
> SET columnname = value
> WHERE column = value;

- set gender to male and city to Nashik of customer with user_id = 11

> UPDATE customers
> SET gender = 'male', city='Nashik'
> WHERE user_id=11;

- update all the records

ALTER TABLE customers
ADD COLUMN country TEXT;

UPDATE customers
SET country = 'Bharat';

- increase age by 1 of all the customers
  UPDATE customers
  SET age = age+1;

- transform all names to uppercase
  > UPDATE customers
  > SET name = UPPER(name);

INSERT INTO employees(name,phone,salary,dept,gender,city,designation)
VALUES
('aaaa','111111111',10000,'IT','male','Pune','developer'),
('bbbb','2222222222',11000,'HR','female','Pune','developer'),
('cccc','3333333333',12000,'IT','male','Mumbai','developer'),
('dddd','4444444444',13000,'HR','female','Mumbai','developer'),
('eeee','5555555555',14000,'IT','male','Pune','designer'),
('ffff','6666666666',15000,'HR','female','Pune','designer'),
('gggg','7777777777',16000,'IT','male','Mumbai','developer'),
('hhhh','8888888888',17000,'HR','female','Mumbai','developer'),
('iiiii','999999999',18000,'IT','male','Pune','designer'),
('jjjj','1010101010',19000,'IT','female','Pune','designer');

UPDATE employees
SET salary = 10000;

- increment salary of IT by 10% and HR by 5%;

UPDATE employees
SET salary = CASE
WHEN dept='IT' THEN salary*1.10
WHEN dept='HR' THEN salary*1.05
ELSE salary
END;

- set gender to others if not available;
  UPDATE customers SET gender='other'
  WHERE gender IS NULL;

- update customer by employees data

UPDATE customers c
SET
name = e.name,
city = e.city
FROM employees e
WHERE c.user_id = e.emp_id;

- update records based on another table.
- set avg salary in hr department

UPDATE employees
SET salary = (SELECT AVG(salary) FROM employees) WHERE dept='HR';

DROP
to delete table, databases, views,etc

TRUNCATE
to delete all rows data by preserving the structure
cannot use WHERE clause
faster
cannot delete table

DELETE
to delete the row data
can use WHERE clause to delete rows with a condition
cannot delete table

DELETE COMMAND:-

DELETE FROM table_name
WHERE condition;

- delete all rows
  TRUNCATE TABLE table_name;
  DELETE FROM table_name;

- to delete specific row, delete a customer with id 2
  DELETE FROM customers
  WHERE user_id = 2;

- multiple condition
  > DELETE FROM employees
  > WHERE dept='HR'
  > AND salary > 10000;

-IN clause

- delete employees by ids
  DELETE FROM employees
  WHERE emp_id IN (1,2,3);

-delete employees having salary between 20000 and 40000

DELETE FROM employees
WHERE salary BETWEEN 20000 AND 40000;

DQL - Data Query Langauge

SELECT command

- it is used to read/fetch the data from database

- to select all the columns;

SELECT _ FROM tablename;
SELECT _ FROM customers;

- to select specific columns;

SELECT name,mobile,gender FROM customers;

- read columns and use aliases
  SELECT name,mobile AS phone,gender FROM customers;

- fetch unique column values

SELECT DISTINCT dept FROM employees;

- to limit the result
  SELECT \* FROM customers LIMIT 4;

WHERE CLAUSE

it is used to provide a condition in the query

WHERE id = 1
WHERE city = 'pune' AND gender ='male'
WHERE id IN (1,2,3,4)
WHERE salary > 10000;

- read customers having id 2
  SELECT \* FROM customers WHERE user_id = 2;

-read employees having salary greater than 10000
SELECT \* FROM employees WHERE salary > 10000;

- read male customers from pune city
  SELECT \* FROM customers
  WHERE city = 'pune' AND gender ='male';

LIKE AND ILIKE clauses

LIKE - case sensitive
ILIKE - case insensitive

- read male customers from pune city - Case sensitive
  SELECT \* FROM customers
  WHERE city LIKE 'pune' AND gender LIKE 'male';

SELECT \* FROM customers
WHERE LOWER(city) LIKE LOWER('pune') AND gender LIKE 'male';

- read male customers from pune city - Case insensitive
  SELECT \* FROM customers
  WHERE city ILIKE 'pune' AND gender ILIKE 'male';

- search the customer by name,mobile,email;

%value = value must ends with
value% = value must starts with
%value% = value must contains anywhere

- read customers by name,mobile,city
  SELECT \* FROM customers
  WHERE name ILIKE '%ee%';

SELECT \* FROM customers
WHERE email ILIKE '%ddd%';

ORDER BY clause:-
It sorts the result records fetch by the query
it does not sort the actual data stord in the tables.

There are two sorting orders

1. Ascending order (ASC) - default
2. Descending order(DESC)

Syntax:

SELECT col1, col2, colN
FROM tablename
ORDER BY column_name ASC/DESC;

- fetch employees by emp_id in ascending order.

SELECT _ FROM employees ORDER BY emp_id;
SELECT _ FROM employees ORDER BY emp_id ASC;
SELECT \* FROM employees ORDER BY emp_id DESC;

- order by multiple columns

SELECT _ FROM employees ORDER BY dept ASC, name DESC;;
SELECT _ FROM employees ORDER BY dept ASC, name ASC;

- handle null values
- if a column having null values is used for sorting then
  ASC order puts NULL values at last ad DESC order puts NUll values at first

SELECT _ FROM employees ORDER BY gender ASC;
SELECT _ FROM employees ORDER BY gender DESC;

If you want control the position of NULL values in the order by then use;
NULLS FIRST
NULLS LAST

- sort by gender and put NULL values to start
  SELECT _ FROM employees ORDER BY gender ASC NULLS FIRST;
  SELECT _ FROM employees ORDER BY gender DESC NULLS LAST;

A = 65

a = 97
d = 100

- sort by dept case insensitively
  SELECT \* FROM employees ORDER BY LOWER(dept) ASC;

- sort the records by length of city
  SELECT \* FROM employees ORDER BY LENGTH(city) ASC;

- sort by salary + 500 in ascending

SELECT \* FROM employees ORDER BY (salary+500) ASC;

- Alias is used to use a temporary name for the columns.

existing_column AS new_name
existing_column new_name,

SELECT emp_id, phone, salary, city, designation FROM employees;
SELECT emp_id ID, phone AS Mobile, salary, city Address, designation AS Role FROM employees;

SELECT name, salary\*12 AS annual_salary
FROM employees
ORDER BY annual_salary DESC;

Positional numbers to refers the columns by their positions
starting from 1.

SELECT emp_id, phone, salary, city, designation
FROM employees
ORDER BY 1 ASC, 3 ASC;

LIMIT clause;
it restricts the number of rows returned by a query.

Syntax:
SELECT column1,column2
FROM table_name
LIMIT number_of_rows;

SELECT emp_id, phone, salary, city, designation
FROM employees
ORDER BY 1 ASC, 3 ASC
LIMIT 3;

it first sorts the all records and then set the limit;

OFFSET clause
it skips the records.

SELECT \* FROM employees
LIMIT 3 OFFSET 2;

- fetch highest paid employees
  SELECT \* FROM employees ORDER BY salary DESC LIMIT 1;

- fetch second highest paid employees
  SELECT DISTINCT ON (salary) \* FROM employees ORDER BY salary DESC LIMIT 1 OFFSET 1;

- fetch third highest paid employees
  SELECT DISTINCT ON (salary) \* FROM employees ORDER BY salary DESC LIMIT 1 OFFSET 2;

Aggregate Functions

COUNT(column)

- it is used to count number of rows

- count total number of employees

SELECT COUNT(_) FROM employees;
SELECT COUNT(_) AS total_emps FROM employees;

- count total female employees
  SELECT COUNT(\*) AS total_emps FROM employees WHERE gender = 'female';

- count total female employees in Pune
  SELECT COUNT(\*) AS total_emps FROM employees WHERE gender = 'female' AND city ILIKE 'Pune';

- count total employees having salary greater than 10900
  SELECT COUNT(\*) AS total_emps FROM employees WHERE salary > 10900;

AVG(column)
it is for numeric values

SELECT AVG(salary) FROM employees;

find average age
SELECT AVG(age) FROM customers;

SUM(column)
calculate sum

SELECT SUM(salary) AS total_salary FROM employees;

find total salary of Pune employees
SELECT SUM(salary) AS total_salary FROM employees WHERE city ILIKE 'pune';

MIN(column)
fetched lowest value of a column

SELECT MIN(salary) AS lowest_salary FROM employees;

find yougest customer
SELECT MIN(age) FROM customers;

MAX(column)
returns biggest value of a column

find oldest customer
SELECT MAX(age) FROM customers;

STRING_AGG(column,separator)

- it is used to concat multiple values into one

get names of customers as single string value

SELECT STRING_AGG(name,', ') AS names FROM customers;

get unique cities list
SELECT STRING_AGG(DISTINCT city,',') AS cities FROM customers;

ARRAY_AGG(column)
it collects all values of a column into an array

SELECT ARRAY_AGG(name) as names FROM customers;

BOOL_AND()
returns true of all values are true

SELECT BOOL_AGG(is_deleted) FROM customers;

BOOL_OR(column)  
 returns true if one of values of a column is true
SELECT BOOL_OR(is_deleted) FROM customers;

GROUP BY clause

it is used to group the rows that have the same values in one or more columns
it is commonly used with aggregate functions.

Syntax:

SELECT column1, aggregate_function(column)
FROM table_name
GROUP BY column1;

group the employees by dept
find minimum, maximum and average salary by dept

SELECT dept,city,
MIN(salary) AS min_salary,
MAX(salary) AS max_salary,
ROUND(AVG(salary),2) AS avg_salary
FROM employees
GROUP BY dept,city;

- Find total salary paid for each city employees

SELECT city,
SUM(salary) AS total_salary
FROM employees
GROUP BY city;

WHERE vs HAVING

WHERE

- executes before GROUP BY
- cannot use aggregate function
- filters individual rows

HAVING

- executes after GROUP BY
- can use aggregate functions
- filters the groups

- count the total number of employees per dept and return result of dept having atleast 2 employees

SELECT dept, COUNT(_) as total_emps
FROM employees
WHERE salary >= 10000
GROUP BY dept
HAVING COUNT(_) >=2;

INSERT INTO employees (name,phone,salary,dept,gender,city,designation)
VALUES ('kkk','6655778898',20000,'dev','male','Pune','PM'),
('lll','6655778822',20000,'dev','female','Pune','PM'),
('mmm','6655778833',25000,'HR','male','Pune','designer'),
('nnn','6655778844',28000,'IT','female','Pune','PM'),
('ooo','6655778855',30000,'dev','male','Pune','designer');

CREATE TABLE department(dept_id INT PRIMARY KEY,
name VARCHAR(50)
);

INSERT INTO department VALUES
(1,'IT'),
(2,'HR'),
(3,'dev'),
(4,'Sales'),
(5,'Admin');

Sub query:-
writing a query inside another query is called sub query
sub query provides the data for where condition
Syntax:

    SELECT col1, col2,
    FROM table_name
    WHERE condition (SELECT col FROM table_name)

find the employees having salary greater than average salary.

SELECT \* FROM employees WHERE salary > (SELECT AVG(salary) FROM employees);

Scalar subquery

- it provides single value
- if subquery is a scalar then in the where condition =,<,>,etc can be used.

fetch employees of IT and HR dept

SELECT \* FROM employees
WHERE dept IN('IT','HR');

SELECT \* FROM employees
WHERE emp_id IN(SELECT emp_id FROM employees WHERE gender LIKE 'female' );

select employees of dept id 2

SELECT \* FROM employees WHERE dept = (SELECT name FROM department WHERE DEPT_ID =2);

INSERT INTO orders (amount,cust_id)
VALUES
(120, 6),
(220, 6),
(320, 7),
(420, 6),
(520, 8),
(350, 8),
(980, 9),
(410, 9),
(789, 1),
(190, 1),
(160, 1),
(230, 2),
(630, 3),
(660, 4);

find the user who placed highest order.

SELECT \* FROM users WHERE user_id = (
SELECT cust_id FROM orders WHERE amount = (
SELECT MAX(amount) FROM orders
)
);

SELECT \* FROM users WHERE user_id = (
SELECT cust_id FROM orders ORDER BY amount DESC LIMIT 1
);

find the customers who placed order greater than 500;

SELECT \* FROM users WHERE user_id IN (
SELECT cust_id FROM orders WHERE amount >500
);

fetch all users except user 1 and 2
SELECT \* FROM users WHERE user_id NOT IN(1,2);

<!-- EXISTS
NOT EXISTS -->

-find the users who have placed the orders

SELECT \* FROM users u
WHERE EXISTS
(
SELECT 1 FROM orders o WHERE o.cust_id = u.user_id
);

-find the users who have not placed the orders

SELECT \* FROM users u
WHERE NOT EXISTS
(
SELECT 1 FROM orders o WHERE o.cust_id = u.user_id
);

ANY, ALL

ANY - greater than lowest salary of HR
find the employees having salary greater than the salary of ANY employees of HR dept

SELECT \* FROM employees
WHERE salary > ANY
(
SELECT salary
FROM employees
WHERE dept = 'HR'
);

ALL - Greater than highest salary of HR
SELECT \* FROM employees
WHERE salary > ALL
(
SELECT salary
FROM employees
WHERE dept = 'HR'
);

JOIN Query
it is used to fetch the data from multiple table
a row in the result can contains columns of different tables

Types of JOIN

1. Inner Join

   - joins only rows having common data

2. Left Join

   - it returns all record from left table and only matched records from right table

3. Right Join

   - it returns all records from right table and only matched records from left table

4. Full outer join

   - it joins all the records from both tables

5. Cross join

   - it joins each record of left table with every records of right table

CREATE TABLE users (
user_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
name VARCHAR(50),
mobile VARCHAR(20) UNIQUE NOT NULL,
gender VARCHAR(15),
city VARCHAR(50),
age INT
);

CREATE TABLE orders (
order_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
user_id INT NOT NULL,
order_date DATE DEFAULT CURRENT_DATE,
amount DECIMAL(10, 2),
status VARCHAR(20),

    CONSTRAINT fk_orders_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)

);

fetch only users having orders

SELECT u.user_id, u.name, u.mobile, o.amount, o.status
FROM users u
INNER JOIN orders o ON u.user_id = o.user_id;

fetch all users and their orders if available, if there is no order then NULL will be placed in orders.

LEFT Join

SELECT u.user_id, u.name, u.mobile, o.amount, o.status
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id;

RIGHT JOIN:-

SELECT u.user_id, u.name, u.mobile, o.amount, o.status
FROM users u
RIGHT JOIN orders o ON u.user_id = o.user_id;

FULL JOIN:-

SELECT u.user_id, u.name, u.mobile, o.amount, o.status
FROM users u
FULL JOIN orders o ON u.user_id = o.user_id;

CROSS JOIN:-

SELECT u.user_id, u.name, u.mobile, o.amount, o.status
FROM users u
CROSS JOIN orders o;

JOINs with condition

-get users and orders of completed orders only

SELECT u.user_id, u.name, u.mobile, o.amount, o.status
FROM users u
JOIN orders o ON u.user_id = o.user_id
AND o.status = 'Completed';

SELECT u.user_id, u.name, u.mobile, o.amount, o.status
FROM users u
JOIN orders o ON u.user_id = o.user_id
WHERE o.status = 'Completed'
ORDER BY u.name ASC;

ACID Property

Transaction:-
you can execute multiple related commands to be successfully executed all or none.

Syntax:

BEGIN TRANSACTION;

command 1
command 2
command 3
command N

COMMIT;

ROLLBACK;

deduct 5000 from user A account and add 5000 to user B account

BEGIN TRANSACTION;

UPDATE accounts
SET balance = balance - 5000
WHERE account_no = 2;

UPDATE accounts
SET balance = balancee + 5000
WHERE account_no = 3;

COMMIT;

//storing permanently

CREATE TABLE accounts(
account_no INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
balance NUMERIC(10,2),
name TEXT,
mobile VARCHAR(15),
gender VARCHAR(15),
type VARCHAR(15)
);

<!--
insert an account

update an account

delete account
 -->

BEGIN TRANSACTION;

INSERT INTO accounts(name,balance,type)
VALUES('ABC', 10000,'saving');

SAVEPOINT sp1;

UPDATE accounts
SET balance = 80000, type='current'
WHERE account_no = 1;

DELETE FROM account
WHERE account_no = 2;

ROLLBACK TO SAVEPOINT sp1;

COMMIT;

CTE - Common Table Expression

- it temporaly makes data available to be used in another single sql query.

find top customers

WITH top_cust AS (
SELECT user_id, SUM(amount) AS total
FROM orders
GROUP BY user_id
HAVING SUM(amount) > 5000
)

SELECT u.name, tc.total
FROM top_cust tc
JOIN users u ON u.user_id = tc.user_id;

VIEWS

The views are the queries stored to read the data.
views works like virtual tables.

create a view to read user order summery

CREATE VIEW user_order_summary AS
SELECT u.user_id, u.name AS user_name,
u.city, u.age,
COUNT(o.order_id) AS total_orders,
COALESCE(SUM(o.amount),0.00) AS total_spent,
COALESCE(AVG(o.amount),0.00) AS avg_value
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
GROUP BY u.user_id, u.name;

SELECT \* FROM user_order_summary
WHERE total_spent > 2000;

CREATE VIEW completed_orders AS
SELECT
order_id,
user_id,
amount
FROM orders
WHERE status = 'completed';

CREATE VIEW pending_orders AS
SELECT
order_id,
user_id,
amount
FROM orders
WHERE status ILIKE 'Pending';

python3 -m venv .venv
source .venv/bin/activate

pip install fastapi uvicorn sqlalchemy greenlet "psycopg[binary]"

python -m pip show sqlalchemy

ORM - Object Relational Mapping

user = {
id:1,
name:"aa",
address:{
city:"pune",
pincode:121212
}
}# fast-api-examples

client -> post formdata(username & password) -> server (auth/login)-> check in DB -> if available then generate JWT token -> send response to the client

Bcrypt -> to encrypt the password.

Ex

abcd123 -> encryption/hashing -> store in DB

Tokens
Access TOken - Bearer
access token - expires in 30 minutes

    Refresh TOken - expires in 24 hours
