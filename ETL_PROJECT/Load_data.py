# Databricks notebook source
# MAGIC %md
# MAGIC ### now i want to store the data of transfomed data in gold layer or gold table 

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE my_catlog.my_schema.gold_branch_summary AS
# MAGIC SELECT
# MAGIC     branch_id,
# MAGIC     branch_name,
# MAGIC     branch_state,
# MAGIC     COUNT(loan_id) AS total_loans,
# MAGIC     SUM(loan_amount) AS total_loan_amount
# MAGIC FROM my_catlog.my_schema.customer_loan_branch_data
# MAGIC GROUP BY
# MAGIC     branch_id,
# MAGIC     branch_name,
# MAGIC     branch_state;
# MAGIC
# MAGIC     

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from my_catlog.my_schema.gold_branch_summary 

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE my_catlog.my_schema.gold_customer_summary AS
# MAGIC SELECT
# MAGIC     customer_id,
# MAGIC     customer_name,
# MAGIC     COUNT(loan_id) AS total_loans,
# MAGIC     SUM(loan_amount) AS total_loan_amount
# MAGIC FROM my_catlog.my_schema.customer_loan_branch_data
# MAGIC GROUP BY
# MAGIC     customer_id,
# MAGIC     customer_name;
# MAGIC select * from my_catlog.my_schema.gold_customer_summary

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE my_catlog.my_schema.gold_customer_loan_data AS
# MAGIC SELECT *
# MAGIC FROM my_catlog.my_schema.customer_loan_branch_data;
# MAGIC
# MAGIC select * from my_catlog.my_schema.gold_customer_loan_data

# COMMAND ----------

