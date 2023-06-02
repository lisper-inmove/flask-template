update-submodule:
	git submodule update --init --recursive
dev:
	bash bin/dev.sh
gdev:
	bash bin/gdev.sh
chatbot:
	bash bin/chatbot.sh
help:
	bash bin/helper.sh
prod:
	bash bin/prod.sh $(PORT)
