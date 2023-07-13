    {{ config( materialized='table')}}

SELECT 
    COUNT(*) AS num_rows
FROM 
    {{source('staging','table_prova_1881')}}