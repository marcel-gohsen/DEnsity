FROM python:3.8-slim

COPY requirements.txt /app/
WORKDIR /app/

RUN pip install -r requirements.txt

COPY evaluators /app/evaluators
COPY logs /app/logs
COPY preprocess /app/preprocess
COPY reranker /app/reranker
COPY results /app/results
COPY scripts /app/scripts
COPY utils /app/utils
COPY evaluate_conversations.py /app/

ENV INPUT_FILE="data/input.json" OUTPUT_FILE="data/output.json"

ENTRYPOINT python3 evaluate_conversations.py -f ${INPUT_FILE} -o ${OUTPUT_FILE}



