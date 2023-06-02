update-submodule:
	git submodule update --init --recursive
dev:
	bash bin/dev.sh
gdev:
	bash bin/gdev.sh
help:
	bash bin/helper.sh
prod:
	bash bin/prod.sh $(PORT)
uwsgi:
	bash bin/uwsgi.sh $(PORT)
