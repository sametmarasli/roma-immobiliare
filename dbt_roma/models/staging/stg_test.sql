{{ config(materialized='table') }}

select realEstate
from {{ source('staging','table_development_i') }}
limit 100 

