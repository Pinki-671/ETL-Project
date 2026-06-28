# Databricks notebook source
# MAGIC %md
# MAGIC ## How to Read The data From CSV and Store it into a table format 
# MAGIC - first i created a unity catlog or catlog inside the catlog we have to create a schema inside that we have to create the volume insid ethe volume we are uploaded the csv files 
# MAGIC - after that i created a workspace and inside that i created a note book 
# MAGIC - now i create a temporary view table from the csv files
# MAGIC - after that the view table converted to the actual table means created a real table (delat table)
# MAGIC - now i am abke to read the table properly  
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW bank_branch_data
# MAGIC USING CSV 
# MAGIC OPTIONS(
# MAGIC   path '/Volumes/my_catlog/my_schema/my_volume/raw/Bank_Branch_Data.csv',
# MAGIC   header 'true',
# MAGIC   inferSchema 'true'
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM bank_branch_data
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE my_catlog.my_schema.bank_branch_data AS
# MAGIC SELECT * FROM bank_branch_data;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM my_catlog.my_schema.bank_branch_data

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW bank_customer_data
# MAGIC USING CSV 
# MAGIC OPTIONS(
# MAGIC   path '/Volumes/my_catlog/my_schema/my_volume/raw/Bank_Customer_Data.csv',
# MAGIC   header 'true',
# MAGIC   inferSchema 'true');

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE my_catlog.my_schema.bank_customer_data AS
# MAGIC SELECT * FROM bank_customer_data ;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM my_catlog.my_schema.bank_customer_data

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW bank_loan_data
# MAGIC USING CSV 
# MAGIC OPTIONS(
# MAGIC   path '/Volumes/my_catlog/my_schema/my_volume/raw/Bank_Loan_Data.csv',
# MAGIC   header 'true',
# MAGIC   inferSchema 'true');

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE my_catlog.my_schema.bank_loan_data AS
# MAGIC SELECT * FROM bank_loan_data;

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from my_catlog.my_schema.bank_loan_data
# MAGIC