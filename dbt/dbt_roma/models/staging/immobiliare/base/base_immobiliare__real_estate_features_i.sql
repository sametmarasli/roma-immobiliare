with source as (
    select *
    from {{ ref('base_immobiliare__selling_adverts') }}
),

renamed as (
    select
        advert_id,
        re_features
    from source
    cross join unnest(realestate.properties[safe_offset(0)].ga4features) as re_features
)

select *
from renamed
