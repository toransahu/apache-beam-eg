# Run local source code using DirectRunner

```bash
/github.com/toransahu/apache-beam-eg
$ python python/examples/using_classic_template/etl.py \
--runner DirectRunner
```

# Run local source code using Dataflow

```bash
/github.com/toransahu/apache-beam-eg
$ python python/examples/using_classic_template/etl.py \
--runner DataflowRunner \
--region us-central1 \
--project apache-beam-eg \
--temp_location gs://apache-beam-eg/tmp
```

# Stage the local source code into cloud as Dataflow Classic Template

## Using service account auth

```bash
/github.com/toransahu/apache-beam-eg
$ python python/examples/using_classic_template/etl.py \
--project=apache-beam-eg \
--job_name=etl-`date +%Y%m%d-%H%M%S` \
--template_location=gs://apache-beam-eg/templates/etl \
--temp_location=gs://apache-beam-eg/tmp \
--region=us-central1 \
--runner=DataflowRunner \
--staging_location=gs://apache-beam-eg/staging
```

## Using user account auth

# Run the Classic Template

## Using Web Console

Create job from template

```
Job name = etl-template
Regional endpoint = us-central1 (Iowa)
Dataflow template = Custom template
Template path = gs://apache-beam-eg/templates/etl
Temporary location = gs://apache-beam-eg/tmp

# Encryption
Google-managed encryption key

# Additional parameters
input: gs://dataflow-samples/shakespeare/kinglear.txt
output: gs://apache-beam-eg/results/python/examples/using_classic_template/output
```

Run the template

## Using `gcloud` CLI

```bash
$ gcloud config configurations activate <config_name>

$ gcloud dataflow jobs run etl-template \
--project apache-beam-eg \
--region us-central1 \
--gcs-location gs://apache-beam-eg/templates/etl \
--parameters input=gs://dataflow-samples/shakespeare/kinglear.txt,output=gs://apache-beam-eg/results/python/examples/using_classic_template/output
```

## Using REST API

```bash
$ curl \
--url "https://dataflow.googleapis.com/v1b3/projects/apache-beam-eg/locations/us-central1/templates:launch?gcsPath=gs://apache-beam-eg/templates/etl" \
--request POST \
--header "Authorization: Bearer "$(gcloud auth print-access-token) \
--header 'Accept: application/json' \
--header 'Content-Type: application/json' \
--data '{
    "jobName": "etl-job-'$(date +%Y%m%d-%H%M%S)'",
    "environment": {
        "bypassTempDirValidation": false,
        "tempLocation": "gs://apache-beam-eg/tmp/",
        "ipConfiguration": "WORKER_IP_UNSPECIFIED",
        "additionalExperiments": []
    },
    "parameters": {
        "input": "gs://dataflow-samples/shakespeare/kinglear.txt",
        "output": "gs://apache-beam-eg/results/python/examples/using_classic_template/output"
    }
}'
```


## Using Python Client

```bash
$ pip install google-api-python-client

/github.com/toransahu/apache-beam-eg
$ python python/examples/using_classic_template/run_template.py \
```

