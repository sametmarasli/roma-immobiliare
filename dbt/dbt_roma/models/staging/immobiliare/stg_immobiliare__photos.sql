with 
source as (
    select * from {{ source('immobiliare', 'table_test_dbt') }}
), 
renamed as (
    SELECT 
        advert_id,
        photos_unnested.id as fotos_id,
        photos_unnested.urls.small as photos_url,
        photos_unnested.caption as photos_caption,
    FROM source 
    CROSS JOIN UNNEST(realEstate.properties [SAFE_OFFSET(0)].multimedia.photos) AS photos_unnested
)
select * from renamed