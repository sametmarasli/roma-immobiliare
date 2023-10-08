# Monitoring Rome House Prices with Cloud Technologies
This project aims to create a data pipeline to monitor house prices in Rome by using data from immobiliare.it. 
We use Google cloud tools (Bigquery, GCS, GCE, Cloud Run ..),Prefect for orchestration, dbt for data transformations, Terraform for infrastructure, Dash for reporting, Docker and Python. 
The data scraped from immobiliare.it.

todo:
- [x] reorganize the repo for a valid structure for Prefect
- [x] setup datamodels for handling api calls and pagination
- [x] add unit tests 
- [x] setup dbt to transform data by using Bigquery
- [ ] setup Prefect 
- [ ] set github as code storage for Prefect
- [ ] setup CI/CD
- [ ] setup Dash for dashboard
- [ ] move all the infra code to terraform

![Alt text](./images/data%20pipeline.jpg?raw=true "Data Pipeline and Technologies")
