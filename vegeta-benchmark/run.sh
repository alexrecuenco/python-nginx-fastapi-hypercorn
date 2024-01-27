set -eux

vegeta attack -duration=1m -rate=50/1s -workers 20 -format=json -targets targets.jsonl  | tee results.bin | vegeta report


vegeta plot results.bin > results.html
