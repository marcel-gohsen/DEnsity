SHELL:=/bin/bash

dep:
	python3 -m venv .venv
	source .venv/bin/activate && pip install gdown

build: dep
ifeq (,$(wildcard ./logs.tar.gz))
	source .venv/bin/activate && gdown 1sbaAOStPvN1yb-76u4UIbA8PB3RyBb0T
	tar -xzvf logs.tar.gz
endif
ifeq (,$(wildcard ./results.tar.gz))
	source .venv/bin/activate && gdown 1-gDjaSjwUd6EnQj8Gq5WNi0eUFTVgKbC
	tar -xzvf results.tar.gz
endif
	docker build -t registry.webis.de/code-research/conversational-search/multi-turn-system-prompts:density-latest .

push:
	docker push registry.webis.de/code-research/conversational-search/multi-turn-system-prompts:density-latest

test:
	docker run -v "$(shell pwd)/data":/app/data --gpus all density:latest