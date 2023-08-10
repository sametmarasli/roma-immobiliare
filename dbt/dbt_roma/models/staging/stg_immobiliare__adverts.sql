with 
source as (
    select * from {{ source('staging', 'table_test_dbt_i') }}
) , 
renamed as (
    select 
        -- ids
        -- id as payment_id,
        ingestion_date,

        -- strins, numerics, booleans, dates, timestamps...
        -- case
        --     when payment_method in ('stripe', 'paypal', 'credit_card', 'gift_card') then 'credit'
        --     else 'cash'
        -- end as payment_type,
        realEstate.properties[SAFE_OFFSET(0)].description as advert_description,
        realEstate.price.value as advert_price,
        realEstate.visibility as advert_visibility,
        realEstate.type as advert_type,
        realEstate.contract as advert_contract,
        realEstate.id as advert_immobiliare_id,
        realEstate.title as advert_title,
        seo.url as advert_url,
        seo.metaTitle as advert_seo_meta_title


    from source
)
select *
from renamed
