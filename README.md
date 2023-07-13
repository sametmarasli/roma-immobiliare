# Monitoring Rome House Prices with Cloud Technologies
This project aims to create a data pipeline to monitor house prices in Rome by using data from immobiliare.it. 
We use Google cloud tools (Bigquery, GCS, GCE, Cloud Run, Data(looker) studio ...), ,Prefect for orchestration, dbt for data transformations, Terraform for infrastructure, Docker and Python. 
We scrape the data from from immobiliare.it.
The project is still under development (18-Jun-2023).

todo:
- [x] reorganize the repo for a valid structure for Prefect
- [x] setup datamodels for handling api calls and pagination
- [x] add unit tests 
- [ ] setup Prefect 
- [ ] set github as code storage for prefect
- [ ] setup CI/CD
- [ ] setup piperider (or another tool) for profiling
- [ ] setup dbt to transform data by using Bigquery
- [ ] setup Data Studio studio for dashboard
- [ ] move all the infra code to terraform