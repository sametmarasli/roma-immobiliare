{{ config(materialized='table') }}

SELECT 
  realEstate.isNew as isNew,
  realEstate.id as id,
from {{ source('staging','table_development_i') }}
limit 100 

