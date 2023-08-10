include config/.env.test


export_environment_variables:
	export $(cat config/.env.test|xargs)

service_account_create:
	gcloud iam service-accounts create ${SERVICE_ACCOUNT_NAME} \
	--description "Service account for project Roma" 

	gcloud iam service-accounts keys create ${SERVICE_ACCOUNT_NAME}_service_account.json \
	--iam-account=${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com

service_account_give_roles:
	gcloud projects add-iam-policy-binding ${PROJECT_ID} \
	--member=serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com  \
	--role roles/viewer
	
	gcloud projects add-iam-policy-binding ${PROJECT_ID} \
	--member=serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com  \
	--role roles/storage.admin
	
	gcloud projects add-iam-policy-binding ${PROJECT_ID} \
	--member=serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com  \
	--role roles/editor

create_gcs_bucket:
	# gcloud storage buckets create gs://${GCS_BUCKET_NAME} --location=${REGION}
	gsutil mb -p ${PROJECT_ID} -c regional -l ${REGION} gs://${GCS_BUCKET_NAME}

create_bq_dataset:	
	bq --project_id=${PROJECT_ID} mk --location=${REGION} --dataset ${BQ_DATASET_ID}


create_service_account_key:
	gcloud iam service-accounts keys create ${SERVICE_ACCOUNT_NAME}_service_account.json \
	--iam-account=${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com

test:
	echo "y" | bq rm ${BQ_DATASET_ID}.${BQ_TABLE_ID}
	python main.py

dbt_debug:
	dbt init --project-dir ${DBT_PROJECT_DIR} --profiles-dir ${DBT_PROFILES_DIR}

set_env_variables:
	export $(cat ./config/.env.development | xargs)