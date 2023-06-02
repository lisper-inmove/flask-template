update-submodule:
	git submodule update --init --recursive
dev:
	bash bin/dev.sh
gdev:
	bash bin/gdev.sh
prod:
	bash bin/prod.sh $(PORT)
build:
	sudo docker build -t config-center . -f Containerfile
run:
	sudo docker run --rm -d --name config-center --network host config-center:latest
