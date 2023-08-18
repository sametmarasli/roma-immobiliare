{% macro tame_squaremeters(column_name) %}
    CAST(
        NULLIF(
                split({{ column_name }}, ' ')[0]
            ,'n/a')
        as int)
{% endmacro %}
