{% macro tame_squaremeters(column_name) %}
    CAST(CAST(
        NULLIF(
                split({{ column_name }}, ' ')[0]
            ,'n/a')
        as FLOAT64) as INT64)
{% endmacro %}


{% macro create_realestate_id(column_name) %}
    CAST( split({{ column_name }}, '/')[4] as string)
{% endmacro %}
