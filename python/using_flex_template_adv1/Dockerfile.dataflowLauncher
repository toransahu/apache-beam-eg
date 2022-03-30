# USAGE:
# $ docker image build -t <TEMPLATE_IMAGE_GCR_URL> -f <DOCKERFILE> <DOCKER_BUILD_CONTEXT_DIR>
# $ docker push <TEMPLATE_IMAGE_GCR_URL>
#
# eg.
# /github.com/toransahu/apache-beam-eg/python/using_flex_template
# $ export TEMPLATE_IMAGE="gcr.io/apache-beam-eg/dataflow/python/using_flex_template/flex_template_launcher:v0.0.1"
# $ docker image build -t $TEMPLATE_IMAGE -f dataflowLauncher.Dockerfile .
# $ docker push $TEMPLATE_IMAGE


FROM gcr.io/dataflow-templates-base/python38-template-launcher-base


ARG WORKDIR=/dataflow/python/using_flex_template_adv1
RUN mkdir -p ${WORKDIR}
WORKDIR ${WORKDIR}

COPY . .

ENV FLEX_TEMPLATE_PYTHON_PY_FILE="${WORKDIR}/run.py"
ENV PYTHON_REQUIREMENTS_FILE="${WORKDIR}/requirements.txt"
# NOTE: RuntimeError: The --setup_file option expects the full path to
#       a file named **setup.py** instead of /dataflow/python/using_flex_template_adv1/<ANY_NAME>.py;
# NOTE: Also this ENV var is NOT getting honored though its documented,
#       thus pass the parameter `--setup_file` explicitely while building the template
ENV FLEX_TEMPLATE_PYTHON_SETUP_FILE="${WORKDIR}/setup.py"

# We could get rid of installing libffi-dev and git, or we could leave them.
RUN apt-get update \
    && apt-get install -y libffi-dev git \
    && rm -rf /var/lib/apt/lists/* \
    # Upgrade pip and install the requirements.
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r $PYTHON_REQUIREMENTS_FILE \
    # Download the requirements to speed up launching the Dataflow job.
    && pip download --no-cache-dir --dest /tmp/dataflow-requirements-cache -r $PYTHON_REQUIREMENTS_FILE

# Since we already downloaded all the dependencies, there's no need to rebuild everything.
ENV PIP_NO_DEPS=True

# (default with default base image) explicitely mentioning for readability
ENTRYPOINT ["/opt/google/dataflow/python_template_launcher"]
