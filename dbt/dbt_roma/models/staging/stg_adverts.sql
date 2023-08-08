{{
  config(
    materialized='table'
)
}}

select *
from `roma-immobiliare-395210.dwh_test_1881.table_test_i` 
limit 1000