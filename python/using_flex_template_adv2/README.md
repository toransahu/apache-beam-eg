# If the source code is spawned across multiple python files + If the source code is dependent on multiple python remote libs + If the source code is dependent on multiple python local libs

# Run local source code using DirectRunner

```bash
/github.com/toransahu/apache-beam-eg/python/using_flex_template_adv2
$ pip install -r requirements.txt
$ pip install sample-0.1-py3-none-any.whl

$ python run.py \
--runner DirectRunner

# OR
$ python -m example.etl \
--runner DirectRunner
```

# Run local source code using Dataflow

```bash
/github.com/toransahu/apache-beam-eg/python/using_flex_template_adv2
$ python run.py \
--runner DataflowRunner \
--region us-central1 \
--project apache-beam-eg \
--temp_location gs://apache-beam-eg/tmp \
--experiments=use_runner_v2 \
--setup_file ./setup.py \
--sdk_container_image=$WORKER_IMAGE

# OR - NOT RECOMMENDED
$ python run.py \
--runner DataflowRunner \
--region us-central1 \
--project apache-beam-eg \
--temp_location gs://apache-beam-eg/tmp \
--experiments=use_runner_v2 \
--setup_file ./setup.py \
--requirements_file ./requirements.txt \
--extra_package ./sample-0.1-py3-none-any.whl
```

# Build Dataflow Flex Template

## Create launcher Dockerfile

Refer to the [Dockerfile.dataflowLauncher](https://github.com/toransahu/apache-beam-eg/blob/master/python/using_flex_template_adv2/Dockerfile.dataflowLauncher)

## Build image out of Dockerfile.dataflowLauncher

```bash
$ gcloud config configurations activate <config name>
$ export GOOGLE_APPLICATION_CREDENTIALS=~/Downloads/apache-beam-eg-7c9aae5fbeb3.json  # Using Service Account auth
$ gcloud auth configure-docker

/github.com/toransahu/apache-beam-eg/python/using_flex_template
$ export TEMPLATE_IMAGE="gcr.io/apache-beam-eg/dataflow/python/using_flex_template_adv2/flex_template_launcher:v0.0.1" && \
export TEMPLATE_PATH="gs://apache-beam-eg/dataflow/python/using_flex_template_adv2/flex_template_launcher.json"
$ docker image build -t $TEMPLATE_IMAGE -f Dockerfile.dataflowLauncher .
```

## Push the launcher image to the registry 

```bash
$ docker push $TEMPLATE_IMAGE
```

## Create worker Dockerfile

Refer to the [Dockerfile.dataflowWorker](https://github.com/toransahu/apache-beam-eg/blob/master/python/using_flex_template_adv2/Dockerfile.dataflowWorker)

## Build image out of Dockerfile.dataflowWorker

```bash
/github.com/toransahu/apache-beam-eg/python/using_flex_template
$ export WORKER_IMAGE="gcr.io/apache-beam-eg/dataflow/python/using_flex_template_adv2/flex_template_worker:v0.0.1" && \
$ docker image build -t $WORKER_IMAGE -f Dockerfile.dataflowWorker .
```

## Push the worker image to the registry 

```bash
$ docker push $WORKER_IMAGE
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
$ gcloud dataflow flex-template run "etl-using-flex-template-adv2-`date +%Y%m%d-%H%M%S`" \
--template-file-gcs-location "$TEMPLATE_PATH" \
--region "us-central1" \
--additional-experiments=use_runner_v2 \
--parameters=sdk_container_image=$WORKER_IMAGE \
--parameters=setup_file=/dataflow/python/using_flex_template_adv2/setup.py \
--parameters=input=gs://dataflow-samples/shakespeare/kinglear.txt \
--parameters=output=gs://apache-beam-eg/results/python/examples/using_flex_template_adv2/output
```
