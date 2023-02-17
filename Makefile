update-submodule:
	git submodule update --init --recursive
dev:
	bash bin/dev.sh
gdev:
	bash bin/gdev.sh
gdoc:
	protoc --doc_out=/home/inmove/www/api --doc_opt=html,api.html gproto/*.proto proto/common/*.proto
