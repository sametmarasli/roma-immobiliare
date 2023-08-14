with source_1 as (
    select * from {{ ref('base_immobiliare__real_estate_features_i') }}
),
source_2 as (
    select * from {{ ref('base_immobiliare__real_estate_features_ii') }}
),
concatenated_features as (
    SELECT * FROM source_1
    UNION ALL
    SELECT * FROM source_2
)
select DISTINCT *
from concatenated_features