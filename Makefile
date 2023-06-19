include .env

create_gcs_bucket:
	gcloud storage buckets create gs://${BUCKET_NAME} --location=europe-west8

create_service_account_for_prefect:
	gcloud iam service-accounts create prefect \
  --description="Authorisation to use with Prefect Cloud and Prefect Agent"

create_service_account_key_for_prefect_cloud:
	gcloud iam service-accounts keys create service_account.json \
  --iam-account=prefect@${PROJECT_ID}.iam.gserviceaccount.com

grant_service_account_access_to_bucket:
	gcloud storage buckets add-iam-policy-binding gs://${BUCKET_NAME} \
	--member=serviceAccount:prefect@${PROJECT_ID}.iam.gserviceaccount.com \
	--role=roles/storage.objectAdmin

grant_service_account_access_for_cloud_runs:
	gcloud projects add-iam-policy-binding ${PROJECT_ID} \
	--member=serviceAccount:prefect@${PROJECT_ID}.iam.gserviceaccount.com \
	--role=roles/run.admin

	gcloud projects add-iam-policy-binding ${PROJECT_ID} \
	--member=serviceAccount:prefect@${PROJECT_ID}.iam.gserviceaccount.com \
	--role=roles/iam.serviceAccountUser

create_vm_as_prefect_agent:
	gcloud compute instances create prefect-agent \
		--image=ubuntu-2004-focal-v20230605 \
		--image-project=ubuntu-os-cloud \
		--machine-type=e2-micro \
		--zone=${ZONE} \
		--service-account=prefect@${PROJECT_ID}.iam.gserviceaccount.com


create_docker_repo_on_gcp:
	gcloud artifacts repositories create prefect-flows-docker \
	--repository-format=docker \
	--location=${REGION} \
	--description="Docker repository for Prefect Flows"


setup_instructions_for_artifact_registery:
	gcloud auth configure-docker \
    europe-west8-docker.pkg.dev

build_and_push_docker_image_to_artifact_registery:
	docker image build -t ${ARTIFACT_REGISTRY_PATH}/prefect:roma .
	docker image push ${ARTIFACT_REGISTRY_PATH}/prefect:roma

clean:
	rm data/*

setup_prefect_blocks:
	sh ./setup_prefect_blocks.sh