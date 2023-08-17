with selling_adverts as (
    select *
    from {{ source('immobiliare', 'table_test_dbt') }}
    where (realestate.type = 'ad') and (realestate.isprojectlike = "false" )
)

select * from selling_adverts
