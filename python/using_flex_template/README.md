# Run local source code using DirectRunner

```bash
/github.com/toransahu/apache-beam-eg/python/using_flex_template
$ python example/etl.py \
--runner DirectRunner
```

# Run local source code using Dataflow

```bash
/github.com/toransahu/apache-beam-eg/python/using_flex_template
$ python example/etl.py \
--runner DataflowRunner \
--region us-central1 \
--project apache-beam-eg \
--temp_location gs://apache-beam-eg/tmp
```

# Build Dataflow Flex Template

## Create launcher Dockerfile

Refer to the [Dockerfile.dataflowLauncher](https://github.com/toransahu/apache-beam-eg/blob/master/python/using_flex_template/Dockerfile.dataflowLauncher)

## Build image out of Dockerfile

```bash
$ gcloud config configurations activate <config name>
$ export GOOGLE_APPLICATION_CREDENTIALS=~/Downloads/apache-beam-eg-7c9aae5fbeb3.json  # Using Service Account auth
$ gcloud auth configure-docker

/github.com/toransahu/apache-beam-eg/python/using_flex_template
$ export TEMPLATE_IMAGE="gcr.io/apache-beam-eg/dataflow/python/using_flex_template/flex_template_launcher:v0.0.1" && \
export TEMPLATE_PATH="gs://apache-beam-eg/dataflow/python/using_flex_template/flex_template_launcher.json"
$ docker image build -t $TEMPLATE_IMAGE -f Dockerfile.dataflowLauncher .
```

## Push the image to the registry 

```bash
$ docker push $TEMPLATE_IMAGE
```

## Build Dataflow Flex template

### Using `gcloud` CLI

```bash
$ gcloud dataflow flex-template build $TEMPLATE_PATH \
--image "$TEMPLATE_IMAGE" \
--sdk-language "PYTHON"
```

# Run the Flex Template

## Using `gcloud` CLI

```bash
$ gcloud dataflow flex-template run "etl-flex-`date +%Y%m%d-%H%M%S`" \
--template-file-gcs-location "$TEMPLATE_PATH" \
--region "us-central1" \
--additional-experiments=use_runner_v2 \
--parameters=input=gs://dataflow-samples/shakespeare/kinglear.txt \
--parameters=output=gs://apache-beam-eg/results/python/examples/using_flex_template/output
```
