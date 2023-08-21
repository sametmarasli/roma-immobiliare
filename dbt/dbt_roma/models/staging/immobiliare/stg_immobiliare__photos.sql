with
source as (
    select *
    from {{ ref('base_immobiliare__selling_adverts') }}
),

renamed as (
    select
        -- ids
        concat(advert_id, '_', photos_unnested.id) as photo_id,
        {{ create_realestate_id('seo.url') }} as realestate_id,
        advert_id,
        photos_unnested.id as photos_immobiliare_id,

        -- strings 
        photos_unnested.urls.small as photos_url,
        nullif(photos_unnested.caption, '') as photos_caption

        -- numerics 
        -- booleans 
        -- dates 
        --timestamps

    from source
    cross join
        unnest(realestate.properties[safe_offset(0)].multimedia.photos)
            as photos_unnested
)

select * from renamed
