{% macro tame_squaremeters(column_name) %}
    CAST(
        NULLIF(
                split({{ column_name }}, ' ')[0]
            ,'n/a')
        as int)
{% endmacro %}


{% macro create_realestate_id(column_name) %}
    CAST( split({{ column_name }}, '/')[4] as string)
{% endmacro %}
