# Databricks notebook source
# MAGIC %sql
# MAGIC DESCRIBE my_catlog.my_schema.bank_branch_data;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE my_catlog.my_schema.bank_customer_data;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE my_catlog.my_schema.bank_loan_data;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Rename The column name 

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE my_catlog.my_schema.bank_branch_data AS
# MAGIC SELECT
# MAGIC     BRANCH_ID AS branch_id,
# MAGIC     BRANCH_NAME AS branch_name,
# MAGIC     BRANCH_STATE AS branch_state
# MAGIC FROM my_catlog.my_schema.bank_branch_data;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE my_catlog.my_schema.bank_customer_data AS
# MAGIC SELECT
# MAGIC     CUSTOMER_ID AS customer_id,
# MAGIC     First_Name AS first_name,
# MAGIC     Last_Name AS last_name,
# MAGIC     City AS city,
# MAGIC     Phone_Number AS phone_number,
# MAGIC     Occupation AS occupation,
# MAGIC     DOB AS dob
# MAGIC FROM my_catlog.my_schema.bank_customer_data;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE my_catlog.my_schema.bank_loan_data AS
# MAGIC SELECT
# MAGIC     LOAN_ID AS loan_id,
# MAGIC     CUSTOMER_ID AS customer_id,
# MAGIC     BRANCH_ID AS branch_id,
# MAGIC     LOAN_AMOUNT AS loan_amount
# MAGIC FROM my_catlog.my_schema.bank_loan_data;

# COMMAND ----------

# MAGIC %md
# MAGIC REMOVE DUPLICATES AND STORE INTO A SILVER TABLE 

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE my_catlog.my_schema.silver_bank_branch_data AS
# MAGIC SELECT DISTINCT *
# MAGIC FROM my_catlog.my_schema.bank_branch_data;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE my_catlog.my_schema.silver_bank_customer_data AS
# MAGIC SELECT DISTINCT *
# MAGIC FROM my_catlog.my_schema.bank_customer_data;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE my_catlog.my_schema.silver_bank_loan_data AS
# MAGIC SELECT DISTINCT *
# MAGIC FROM my_catlog.my_schema.bank_loan_data;
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Check null values in each table

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM my_catlog.my_schema.silver_bank_branch_data
# MAGIC WHERE branch_id IS NULL
# MAGIC    OR branch_name IS NULL
# MAGIC    OR branch_state IS NULL;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM my_catlog.my_schema.silver_bank_customer_data
# MAGIC WHERE customer_id IS NULL
# MAGIC    OR first_name IS NULL
# MAGIC    OR last_name IS NULL
# MAGIC    OR city IS NULL
# MAGIC    OR phone_number IS NULL
# MAGIC    OR occupation IS NULL
# MAGIC    OR dob IS NULL;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM my_catlog.my_schema.silver_bank_loan_data
# MAGIC WHERE loan_id IS NULL
# MAGIC    OR customer_id IS NULL
# MAGIC    OR branch_id IS NULL
# MAGIC    OR loan_amount IS NULL;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Case 1: Primary keys should never be null

# COMMAND ----------

# MAGIC %sql
# MAGIC DELETE FROM my_catlog.my_schema.silver_bank_branch_data
# MAGIC WHERE branch_id IS NULL;

# COMMAND ----------

# MAGIC %sql
# MAGIC DELETE FROM my_catlog.my_schema.silver_bank_customer_data
# MAGIC WHERE customer_id IS NULL;

# COMMAND ----------

# MAGIC %sql
# MAGIC DELETE FROM my_catlog.my_schema.silver_bank_loan_data
# MAGIC WHERE loan_id IS NULL;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Case 2: Replace null values with defaults

# COMMAND ----------

# MAGIC %sql
# MAGIC -- for city
# MAGIC UPDATE my_catlog.my_schema.silver_bank_customer_data
# MAGIC SET city = 'Unknown'
# MAGIC WHERE city IS NULL;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Occupation
# MAGIC UPDATE my_catlog.my_schema.silver_bank_customer_data
# MAGIC SET occupation = 'Not Available'
# MAGIC WHERE occupation IS NULL;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Loan Amount
# MAGIC UPDATE my_catlog.my_schema.silver_bank_loan_data
# MAGIC SET loan_amount = 0
# MAGIC WHERE loan_amount IS NULL;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Branch State
# MAGIC UPDATE my_catlog.my_schema.silver_bank_branch_data
# MAGIC SET branch_state = 'Unknown'
# MAGIC WHERE branch_state IS NULL;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Create Derived Columns

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE my_catlog.my_schema.silver_bank_customer_data AS
# MAGIC SELECT
# MAGIC     customer_id,
# MAGIC     first_name,
# MAGIC     last_name,
# MAGIC     CONCAT(first_name, ' ', last_name) AS customer_name,
# MAGIC     city,
# MAGIC     phone_number,
# MAGIC     occupation,
# MAGIC     dob,
# MAGIC     FLOOR(months_between(current_date(), dob)/12) AS age
# MAGIC FROM my_catlog.my_schema.silver_bank_customer_data;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Join Customer and Loan tables

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE my_catlog.my_schema.customer_loan_data AS
# MAGIC SELECT
# MAGIC     c.customer_id,
# MAGIC     c.customer_name,
# MAGIC     c.age,
# MAGIC     c.city,
# MAGIC     c.occupation,
# MAGIC     l.loan_id,
# MAGIC     l.branch_id,
# MAGIC     l.loan_amount
# MAGIC FROM my_catlog.my_schema.silver_bank_customer_data c
# MAGIC LEFT JOIN my_catlog.my_schema.silver_bank_loan_data l
# MAGIC ON c.customer_id = l.customer_id;
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### customer_loan_data join with the branch table

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE my_catlog.my_schema.customer_loan_branch_data AS
# MAGIC SELECT
# MAGIC     cl.*,
# MAGIC     b.branch_name,
# MAGIC     b.branch_state
# MAGIC FROM my_catlog.my_schema.customer_loan_data cl
# MAGIC LEFT JOIN my_catlog.my_schema.silver_bank_branch_data b
# MAGIC ON cl.branch_id = b.branch_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM my_catlog.my_schema.customer_loan_branch_data;