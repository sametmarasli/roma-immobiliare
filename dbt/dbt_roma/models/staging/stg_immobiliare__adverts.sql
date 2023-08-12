with source as (
    select *
    from { { source('staging', 'table_test_dbt') } }
),
renamed as (
    select -- ids
        advert_id as advert_id,
        realEstate.id as immobiliare_advert_id,
        -- strings 
        realEstate.properties [SAFE_OFFSET(0)].description as advert_description,
        realEstate.properties [SAFE_OFFSET(0)].caption as advert_caption,
        realEstate.visibility as advert_visibility,
        realEstate.type as advert_type,
        realEstate.contract as advert_contract,
        realEstate.title as advert_title,
        seo.url as advert_url,
        seo.metaTitle as advert_seo_meta_title,
        -- numerics 
        realEstate.price.value as advert_price,
        -- booleans 
        realEstate.isProjectLike as flag_project, # some adverts are projects links which include more than one advert

        -- dates 
        ingestion_date as ingestion_date,
        --timestamps
    from source
)
select *
from renamed