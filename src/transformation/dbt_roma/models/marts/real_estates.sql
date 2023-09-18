with

realestate_properties as (
    select *
    from {{ ref('stg_immobiliare__real_estate_properties') }}

),

adverts as (
    select *
    from {{ ref('stg_immobiliare__adverts') }}

),

photos_by_realestate as (
    select
        realestate_id,
        count(photo_id) as number_of_photos
    from {{ ref('stg_immobiliare__photos') }}
    group by 1
),

features_by_realestate as (
    select
        realestate_id,
        count(realestate_features) as number_of_features
    from {{ ref('stg_immobiliare__real_estate_features') }}
    group by 1
),
mapped_cities as (
    select
        *
    from {{ ref('int_cities_mapped') }}
),
realestate_properties_and_adverts_joined as (

    select
        -- ids
        realestate_properties.realestate_id,

        -- strings 
        realestate_properties.realestate_condition,
        realestate_properties.realestate_type,
        realestate_properties.realestate_city,
        mapped_cities.mapped_realestate_city,
        adverts.advert_agency_type,
        adverts.advert_visibility,

        -- numerics 
        realestate_properties.realestate_number_of_bathrooms,
        realestate_properties.realestate_number_of_bedrooms,
        realestate_properties.realestate_number_of_rooms,
        realestate_properties.realestate_floor,
        realestate_properties.realestate_surface_squaremeter,
        realestate_properties.realestate_latitude,
        realestate_properties.realestate_longitude,
        photos_by_realestate.number_of_photos,
        features_by_realestate.number_of_features,
        adverts.advert_price,

        -- booleans 
        -- dates
        adverts.advert_date
        --timestamps

    from realestate_properties

    left join adverts on realestate_properties.realestate_id = adverts.realestate_id
    left join photos_by_realestate on realestate_properties.realestate_id = photos_by_realestate.realestate_id
    left join features_by_realestate on realestate_properties.realestate_id = features_by_realestate.realestate_id
    left join mapped_cities on realestate_properties.realestate_id = mapped_cities.realestate_id
)

select *
from realestate_properties_and_adverts_joined
