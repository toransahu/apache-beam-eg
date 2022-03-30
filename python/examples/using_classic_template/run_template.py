from googleapiclient.discovery import build

project = 'apache-beam-eg'
job = 'etl-template-python-client'
template = 'gs://apache-beam-eg/templates/etl'
parameters = {
    'input': 'gs://dataflow-samples/shakespeare/kinglear.txt',
    'output': 'gs://apache-beam-eg/results/python/examples/using_classic_template/output',
}

dataflow = build('dataflow', 'v1b3')
request = dataflow.projects().templates().launch(
    projectId=project,
    gcsPath=template,
    body={
        'jobName': job,
        'parameters': parameters,
    }
)

response = request.execute()
