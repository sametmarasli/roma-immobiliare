with source as (
    select *
    from {{ source('immobiliare', 'table_test_dbt') }}
),
renamed as (
    select 
        -- ids
        advert_id,
        
        -- strings 
        realEstate.properties[SAFE_OFFSET(0)].condition as realestate_condition_i,
        realEstate.properties[SAFE_OFFSET(0)].ga4Condition as realestate_condition_ii,
        realEstate.properties[SAFE_OFFSET(0)].typologyGA4Translation as realestate_type_i,
        realEstate.typology.name as realestate_type_ii,
        realEstate.properties[SAFE_OFFSET(0)].category.name as realestate_category,
        realEstate.properties[SAFE_OFFSET(0)].location.microzone as realestate_microzone,
        realEstate.properties[SAFE_OFFSET(0)].location.macrozone as realestate_macrozone,
        realEstate.properties[SAFE_OFFSET(0)].location.city as realestate_city,
        realEstate.properties[SAFE_OFFSET(0)].location.province as realestate_province,
        realEstate.properties[SAFE_OFFSET(0)].location.region as realestate_region,
        
        -- numerics 
        realEstate.properties[SAFE_OFFSET(0)].bathrooms as realestate_number_of_bathrooms,
        realEstate.properties[SAFE_OFFSET(0)].bedRoomsNumber as realestate_number_of_bedrooms,
        realEstate.properties[SAFE_OFFSET(0)].rooms as realestate_number_of_rooms,
        realEstate.properties[SAFE_OFFSET(0)].floors as realestate_floor,
        realEstate.properties[SAFE_OFFSET(0)].surfaceValue as realestate_surface_squaremeter,
        realEstate.properties[SAFE_OFFSET(0)].location.latitude as realestate_latitude,
        realEstate.properties[SAFE_OFFSET(0)].location.longitude as realestate_longitude,
        
        -- booleans 
        -- dates 
        --timestamps

    from source
)
select *
from renamed