{{ config( materialized='table') }}

with

source as (
    select *
    from {{ ref('base_immobiliare__selling_adverts') }}
),

renamed as (
    select
        -- ids
        advert_id as advert_id,
        cast(realestate.id as string) as advert_immobiliare_id,

        -- strings 
        realestate.title as advert_title,
        seo.metatitle as advert_seo_meta_title,
        realestate.properties[safe_offset(0)].description as advert_description,
        realestate.properties[safe_offset(0)].caption as advert_caption,
        realestate.visibility as advert_visibility,
        seo.url as advert_url,
        realestate.advertiser.agency.displayname as advert_agency_name,

        case
            when realestate.advertiser.agency.label = 'Impresa Edile' then 'construction_company'
            when realestate.advertiser.agency.label = 'agenzia' then 'realestate_agency'
            else 'n/a'
        end as advert_agency_type,

        -- numerics 
        realestate.price.value as advert_price,

        -- booleans 
        -- some adverts are projects links which include more than one advert
        realestate.isprojectlike as advert_is_project,

        -- dates 
        ingestion_date as advert_ingestion_date

        --timestamps

    from source
)

select * from renamed
