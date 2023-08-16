with source_1 as (
    select *
    from {{ ref('base_immobiliare__real_estate_features_i') }}
),

source_2 as (
    select *
    from {{ ref('base_immobiliare__real_estate_features_ii') }}
),

concatenated_features as (
    select * from source_1
    union all
    select * from source_2
)

select distinct *
from concatenated_features
