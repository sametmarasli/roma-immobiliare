with
source as (
    select *
    from {{ ref('real_estates') }}
),

cityhousecounts as (
    select
        realestate_city,
        count(*) as realestate_city_count
    from
        source
    group by
        realestate_city
),

citymapping as (
    select
        realestate_city,
        case
            when realestate_city_count >= 5 then realestate_city
            else 'Other'
        end as mapped_realestate_city
    from
        cityhousecounts
),

meanpricebycity as (
    select
        source.*,
        citymapping.mapped_realestate_city
    from
        source
    inner join
        citymapping on source.realestate_city = citymapping.realestate_city

)

select *
from
    meanpricebycity
