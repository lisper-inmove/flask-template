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
build-docker-hub:
	sudo docker build -t inmove/config-center . -f Containerfile
push:
	sudo docker push inmove/config-center:latest
run:
	sudo docker run --rm -d --name config-center --network host config-center:latest
uwsgi:
	bash bin/uwsgi.sh $(PORT)
build-c:
	sudo nerdctl build -t config-center .
k8s-restart:
	kubectl delete -f k8s/deployment.yaml && kubectl apply -f k8s/deployment.yaml
