{{ config( materialized='table') }}

with

source as (
    select *
    from {{ ref(...) }}
),

renamed as (
    select
        -- ids
        -- strings 
        -- numerics 
        -- booleans 
        -- some adverts are projects links which include more than one advert
        -- dates 
        --timestamps
        
    from source
)

select * from renamed
