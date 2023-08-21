with source as (
    select *
    from {{ ref('base_immobiliare__selling_adverts') }}
),

renamed as (
    select
        {{ create_realestate_id('seo.url') }} as realestate_id,
        advert_id,
        lower(realestate_features) as realestate_features
    from source
    cross join unnest(realestate.properties[safe_offset(0)].features) as realestate_features
)

select *
from renamed
