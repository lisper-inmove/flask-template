update-submodule:
	git submodule update --init --recursive
dev:
	bash bin/dev.sh
gdev:
	bash bin/gdev.sh
prod:
	bash bin/prod.sh $(PORT)
build:
	sudo docker build -t template . -f Containerfile
run:
	sudo docker run --rm -d --name template --network host template:latest
uwsgi:
	bash bin/uwsgi.sh $(PORT)
