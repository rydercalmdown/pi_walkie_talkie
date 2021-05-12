IMAGE_NAME=rydercalmdown/walkie-talkie-server
SERVER_HOST=0.0.0.0
SERVER_PORT=5000

.PHONY: build
build:
	@docker build -t $(IMAGE_NAME) .

.PHONY: run-server-docker
run-server-docker:
	@docker run --env SERVER_HOST=$(SERVER_HOST) -p 5000:5000 $(IMAGE_NAME)

.PHONY: run-server
run-server:
	@. env/bin/activate \
		&& export SERVER_HOST=$(SERVER_HOST) \
		&& export SERVER_PORT=$(SERVER_PORT) \
		&& cd src && python WalkieTalkieServer.py

.PHONY: run-client
run-client:
	@. env/bin/activate \
		&& export SERVER_HOST=$(SERVER_HOST) \
		&& export SERVER_PORT=$(SERVER_PORT) \
		&& cd src && python WalkieTalkieClient.py

.PHONY: install
install:
	@cd deployment && bash install.sh

.PHONY: configure-audio
configure-audio:
	@cd deployment && bash configure_usb_audio.sh

.PHONY: configure-on-boot
configure-on-boot:
	@echo "Configuring /etc/rc.local"
	@cd deployment && bash configure_on_boot.sh
