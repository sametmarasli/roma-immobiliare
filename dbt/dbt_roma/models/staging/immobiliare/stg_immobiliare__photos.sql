with
source as (
    select *
    from {{ ref('base_immobiliare__selling_adverts') }}
),

renamed as (
    select
        advert_id,
        photos_unnested.id as fotos_id,
        photos_unnested.urls.small as photos_url,
        photos_unnested.caption as photos_caption
    from source
    cross join
        unnest(realestate.properties[safe_offset(0)].multimedia.photos)
            as photos_unnested
)

select * from renamed
