-- models/load_data.sql
{{ adapter.dispatch('load', table='table_prova_1881', file_format='json', location='gs://bucket-prova-1881/20230704/100000_100100.json') }}