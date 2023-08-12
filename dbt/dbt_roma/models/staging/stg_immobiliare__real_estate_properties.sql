with source as (
    select *
    from { { source('staging', 'table_test_dbt') } }
),
renamed as (
    select -- ids
        advert_id as advert_id,
        -- strings 
        -- numerics 
        realEstate.properties[SAFE_OFFSET(0)].floors as realestate_floor_number,
        realEstate.properties[SAFE_OFFSET(0)].bathrooms as realestate_number_of_bathrooms,
        -- booleans 
        -- dates 
        --timestamps
    from source
)
select *
from renamed