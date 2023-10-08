with selling_adverts as (
    select *
    from {{ source('immobiliare', 'raw_immobiliare') }}
    where (realestate.type = 'ad') and (realestate.isprojectlike = 'false')
)

select * from selling_adverts
