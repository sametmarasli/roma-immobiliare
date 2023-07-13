from prefect.deployments import run_deployment


def main():
    response = run_deployment(name="trigger-ingest-data/deployment-trigger_ingest_data")
    print(response)


if __name__ == "__main__":
   main()