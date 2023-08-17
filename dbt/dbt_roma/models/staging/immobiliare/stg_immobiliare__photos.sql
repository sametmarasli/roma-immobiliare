with
source as (
    select *
    from {{ ref('base_immobiliare__selling_adverts') }}
),

renamed as (
    select
        -- ids
        CONCAT(advert_id, '_', photos_unnested.id) AS photo_id,
        advert_id,
        photos_unnested.id as photos_immobiliare_id,
        -- strings 
        photos_unnested.urls.small as photos_url,
        NULLIF(photos_unnested.caption,'') as photos_caption
        -- numerics 
        -- booleans 
        -- some adverts are projects links which include more than one advert
        -- dates 
        --timestamps

    from source
    cross join
        unnest(realestate.properties[safe_offset(0)].multimedia.photos)
            as photos_unnested
)

select * from renamed
