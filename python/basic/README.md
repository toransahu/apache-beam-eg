# Run local source code using DirectRunner

```bash
/github.com/toransahu/apache-beam-eg
$ python python/basic/example/etl.py \
--runner DirectRunner
```

# Run local source code using Dataflow

```bash
/github.com/toransahu/apache-beam-eg
$ python python/basic/example/etl.py \
--runner DataflowRunner \
--region us-central1 \
--project apache-beam-eg \
--temp_location gs://apache-beam-eg/tmp
```
