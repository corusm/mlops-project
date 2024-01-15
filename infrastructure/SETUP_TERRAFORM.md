# Setup Terraform 

## Create Bucket to save state
1. Install Terraform 
2. Create bucket for terraform 


![image](https://dlabs.ai/wp-content/uploads/2023/08/unnamed-13.png)

## Configure variables
Adjust variables (especially for `Project-Name`) in `main.tf` and `variables.tf` and `./mlflow-docker/Makefile`.

## Latest ERROR

```text
│ Error: Error creating Service: googleapi: Error 403: Cloud Run Admin API has not been used in project dtumlops-g62v2 before or it is disabled. Enable it by visiting https://console.developers.google.com/apis/api/run.googleapis.com/overview?project=dtumlops-g62v2 then retry. If you enabled this API recently, wait a few minutes for the action to propagate to our systems and retry.
│ Details:
│ [
│   {
│     "@type": "type.googleapis.com/google.rpc.Help",
│     "links": [
│       {
│         "description": "Google developers console API activation",
│         "url": "https://console.developers.google.com/apis/api/run.googleapis.com/overview?project=dtumlops-g62v2"
│       }
│     ]
│   },
│   {
│     "@type": "type.googleapis.com/google.rpc.ErrorInfo",
│     "domain": "googleapis.com",
│     "metadata": {
│       "consumer": "projects/dtumlops-g62v2",
│       "service": "run.googleapis.com"
│     },
│     "reason": "SERVICE_DISABLED"
│   }
│ ]
│ 
│   with google_cloud_run_v2_service.mlflow_on_cloudrun,
│   on cloud-run.tf line 1, in resource "google_cloud_run_v2_service" "mlflow_on_cloudrun":
│    1: resource "google_cloud_run_v2_service" "mlflow_on_cloudrun" {
│ 
╵
╷
│ Error: Error when reading or editing Resource "storage bucket \"b/dtumlops-g62v2-mlflow-prod-europe-west2\"" with IAM Policy: Error retrieving IAM policy for storage bucket "b/dtumlops-g62v2-mlflow-prod-europe-west2": googleapi: Error 403: nik.leinz@googlemail.com does not have storage.buckets.getIamPolicy access to the Google Cloud Storage bucket. Permission 'storage.buckets.getIamPolicy' denied on resource (or it may not exist)., forbidden
│ 
│   with google_storage_bucket_iam_policy.policy_bucket_object_create,
│   on iam.tf line 52, in resource "google_storage_bucket_iam_policy" "policy_bucket_object_create":
│   52: resource "google_storage_bucket_iam_policy" "policy_bucket_object_create" {
```