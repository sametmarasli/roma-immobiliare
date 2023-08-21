with source as (
    select *
    from {{ ref('base_immobiliare__selling_adverts') }}

),

renamed as (
    select
        -- ids
        {{ create_realestate_id('seo.url') }} as realestate_id,
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
        -- realestate.typology.name as realestate_type_ii, -- extra granuler type

        case
            when realestate.properties[safe_offset(0)].typologyga4translation = "Appartamento" then "flat"
            when realestate.properties[safe_offset(0)].typologyga4translation = "Villa" then "villa"
            when realestate.properties[safe_offset(0)].typologyga4translation = "Villetta a schiera" then "villa"
            when realestate.properties[safe_offset(0)].typologyga4translation = "Attico - Mansarda" then  "attic"
            when realestate.properties[safe_offset(0)].typologyga4translation = "Casa indipendente" then   "townhouse"
            when realestate.properties[safe_offset(0)].typologyga4translation = "Palazzo - Edificio" then  "other"
            when realestate.properties[safe_offset(0)].typologyga4translation = "Rustico - Casale" then "townhouse"
            when realestate.properties[safe_offset(0)].typologyga4translation = "Loft" then "other"
            else "other"
        end as realestate_type,


        realestate.properties[safe_offset(0)].location.macrozone as realestate_macrozone,
        realestate.properties[safe_offset(0)].location.microzone as realestate_microzone,
        realestate.properties[safe_offset(0)].location.city as realestate_city,
        realestate.properties[safe_offset(0)].location.province as realestate_province,
        realestate.properties[safe_offset(0)].location.region as realestate_region,
        seo.url as advert_url,

        -- numerics 
        case   
            when realestate.properties[safe_offset(0)].bathrooms = '1' then 1
            when realestate.properties[safe_offset(0)].bathrooms = '2' then 2
            when realestate.properties[safe_offset(0)].bathrooms = '0' then null
            when realestate.properties[safe_offset(0)].bathrooms = 'n/a' then null
            else 3
        end as realestate_number_of_bathrooms,
        
        case   
            when realestate.properties[safe_offset(0)].bedroomsnumber = '1' then 1
            when realestate.properties[safe_offset(0)].bedroomsnumber = '2' then 2
            when realestate.properties[safe_offset(0)].bedroomsnumber = '3' then 3
            when realestate.properties[safe_offset(0)].bedroomsnumber = '4' then 4
            when realestate.properties[safe_offset(0)].bedroomsnumber = '0' then null
            when realestate.properties[safe_offset(0)].bedroomsnumber = 'n/a' then null
            else 5
        end as realestate_number_of_bedrooms,

        case   
            when realestate.properties[safe_offset(0)].rooms = '1' then 1
            when realestate.properties[safe_offset(0)].rooms = '2' then 2
            when realestate.properties[safe_offset(0)].rooms = '3' then 3
            when realestate.properties[safe_offset(0)].rooms = '4' then 4
            when realestate.properties[safe_offset(0)].rooms = '0' then null
            when realestate.properties[safe_offset(0)].rooms = 'n/a' then null
            else 5
        end as realestate_number_of_rooms,
        

        case   
            when realestate.properties[safe_offset(0)].floors = '1 piano' then 1
            when realestate.properties[safe_offset(0)].floors = '2 piani' then 2
            when realestate.properties[safe_offset(0)].floors = '3 piani' then 3
            when realestate.properties[safe_offset(0)].floors = '4 piani' then 4
            when realestate.properties[safe_offset(0)].floors = '5 piani' then 5
            when realestate.properties[safe_offset(0)].floors = '0' then null
            when realestate.properties[safe_offset(0)].floors = 'n/a' then null
            else 6
        end as realestate_floor,

        {{ tame_squaremeters('realestate.properties[safe_offset(0)].surfacevalue') }} as realestate_surface_squaremeter,

        realestate.properties[safe_offset(0)].location.latitude as realestate_latitude,
        realestate.properties[safe_offset(0)].location.longitude as realestate_longitude

        -- booleans 
        -- dates 
        --timestamps

    from source
)

select *
from renamed
