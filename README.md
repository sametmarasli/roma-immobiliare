# Monitoring Rome House Prices with Cloud Technologies
This project aims to create a data pipeline to monitor house prices in Rome by using data from immobiliare.it. 
We use Google cloud tools (Bigquery, GCS, GCE, Cloud Run, Data(looker) studio ...), ,Prefect for orchestration, dbt for data transformations, Terraform for infrastructure, Docker and Python. 
We scrape the data from from immobiliare.it.
The project is still under development (18-Jun-2023).

todo:
- [ ] set github as code storage for prefect
- [ ] reorganize the repo for a valid structure for Prefect
- [ ] move all the infra code to terraform
- [ ] setup CI/CD
- [ ] setup piperider for profiling
- [ ] add tests
- [ ] setup dbt to transform data by using Bigquery
- [ ] use Looker studio for dashboard