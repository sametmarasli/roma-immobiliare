with source as (
    select *
    from {{ source('staging', 'table_test_dbt_i') }}
) , renamed as (
    select 
        ingestion_date,
        realEstate.visibility,
        realEstate.properties[offset(0)].bathrooms,

    from source
)
select *
from renamed
