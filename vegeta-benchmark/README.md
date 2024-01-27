# Benchmark using vegeta

Using https://github.com/tsenart/vegeta

This is mostly following https://github.com/ovrdoz/vegeta-upload-multipart-data

Using


## How to run

You must `cd` to this folder, then run

```bash
vegeta attack -duration=10s -targets upload.tgt | tee results.bin | vegeta report
```

Afterwards, run to see a plot:

```bash
vegeta plot results.bin > results.html
```

Open that html file to see the result of the attack


## Generating targets

The JSON format seems to be more readable, sometimes


You would need to use to regenerate all targets (`brew install jq` to install)

```bash
jq -c . *.target.json >upload.targets.jsonl
```


Then you would run with

```bash
vegeta attack -duration=1s -rate=1/1s -workers 1 -format=json -targets target.jsonl
```

The body needs to be base64 generated, so I took the body.txt and just sent it as `base64 -i body.txt` and used that as body
