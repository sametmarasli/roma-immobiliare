SELECT
  advert_id,
  a.urls.small as deneme,
  a.caption,
  a.id as fotoid

FROM `roma-immobiliare-395210.dwh_test_dbt.table_test_dbt` 
   CROSS JOIN UNNEST(realEstate.properties[SAFE_OFFSET(0)].multimedia.photos) AS a

