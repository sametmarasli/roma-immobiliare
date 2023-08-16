with selling_adverts as (
    select *
    from {{ source('immobiliare', 'table_test_dbt') }}
    where realestate.type = 'ad'
)

select * from selling_adverts
