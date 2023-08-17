with source as (
    select *
    from {{ ref('base_immobiliare__selling_adverts') }}

),

renamed as (
    select
        -- ids
        advert_id,

        -- strings 
    
        case
            when realestate.properties[safe_offset(0)].condition = "Buono / Abitabile" then 'fine'
            when realestate.properties[safe_offset(0)].condition = "Ottimo / Ristrutturato" then 'good'
            when realestate.properties[safe_offset(0)].condition = "Nuovo / In costruzione" then 'new'
            when realestate.properties[safe_offset(0)].condition = "Da ristrutturare" then 'poor'
            else 'unknown'
        end as realestate_condition,

    
    
        -- realestate.properties[safe_offset(0)].ga4condition as realestate_condition_ii, -- not necessary
        realestate.properties[safe_offset(0)].typologyga4translation as realestate_type_i,
        realestate.typology.name as realestate_type_ii,
        realestate.properties[safe_offset(0)].category.name as realestate_category,
        realestate.properties[safe_offset(0)].location.microzone as realestate_microzone,
        realestate.properties[safe_offset(0)].location.macrozone as realestate_macrozone,
        realestate.properties[safe_offset(0)].location.city as realestate_city,
        realestate.properties[safe_offset(0)].location.province as realestate_province,
        realestate.properties[safe_offset(0)].location.region as realestate_region,
        seo.url as advert_url,
        -- numerics 
        realestate.properties[safe_offset(0)].bathrooms as realestate_number_of_bathrooms,
        realestate.properties[safe_offset(0)].bedroomsnumber as realestate_number_of_bedrooms,
        realestate.properties[safe_offset(0)].rooms as realestate_number_of_rooms,
        realestate.properties[safe_offset(0)].floors as realestate_floor,
        realestate.properties[safe_offset(0)].surfacevalue as realestate_surface_squaremeter,
        realestate.properties[safe_offset(0)].location.latitude as realestate_latitude,
        realestate.properties[safe_offset(0)].location.longitude as realestate_longitude

        -- booleans 
        -- dates 
        --timestamps

    from source
)

select *
from renamed
