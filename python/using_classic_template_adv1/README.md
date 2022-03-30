# If the source code is spawned across multiple python files

# Run local source code using DirectRunner

```bash
/github.com/toransahu/apache-beam-eg/python/using_classic_template_adv1
$ python -m example.etl \
--runner DirectRunner
```

# Run local source code using Dataflow

```bash
/github.com/toransahu/apache-beam-eg/python/using_classic_template_adv1
$ python -m example.etl \
--runner DataflowRunner \
--region us-central1 \
--project apache-beam-eg \
--temp_location gs://apache-beam-eg/tmp \
--setup_file ./setup.py
```

# Stage the local source code into cloud as Dataflow Classic Template

## Using service account auth

```bash
$ export GOOGLE_APPLICATION_CREDENTIALS=~/Downloads/apache-beam-eg-7c9aae5fbeb3.json

/github.com/toransahu/apache-beam-eg/python/using_classic_template_adv1
$ python -m example.etl \
--project=apache-beam-eg \
--job_name=etl-`date +%Y%m%d-%H%M%S` \
--template_location=gs://apache-beam-eg/templates/etl \
--temp_location=gs://apache-beam-eg/tmp \
--region=us-central1 \
--runner=DataflowRunner \
--staging_location=gs://apache-beam-eg/staging \
--setup_file ./setup.py
```

# Run the Classic Template

## Using `gcloud` CLI

```bash
$ gcloud config configurations activate <config_name>

$ gcloud dataflow jobs run etl-template \
--project apache-beam-eg \
--region us-central1 \
--gcs-location gs://apache-beam-eg/templates/etl \
--parameters input=gs://dataflow-samples/shakespeare/kinglear.txt,output=gs://apache-beam-eg/results/python/examples/using_classic_template_adv1/output
```
