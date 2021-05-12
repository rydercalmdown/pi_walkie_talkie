IMAGE_NAME=rydercalmdown/walkie-talkie-server
SERVER_HOST=0.0.0.0

.PHONY: build
build:
	@docker build -t $(IMAGE_NAME) .

.PHONY: run-server
run-server:
	@docker run --env SERVER_HOST=$(SERVER_HOST) -p 5000:5000 $(IMAGE_NAME)

.PHONY: run-client
run-client:
	@. env/bin/activate && export SERVER_HOST=$(SERVER_HOST) && cd src && python WalkieTalkieClient.py

.PHONY: install
install:
	@virtualenv -p python3 env && . env/bin/activate && pip install -r src/requirements.txt
