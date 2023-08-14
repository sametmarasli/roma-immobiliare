with source as (
    select *
    from {{ source('immobiliare', 'table_test_dbt') }}
),
renamed as (
    SELECT 
        advert_id,
        re_features,
    FROM source
    CROSS JOIN UNNEST(realEstate.properties [SAFE_OFFSET(0)].ga4features) AS re_features
)
select *
from renamed