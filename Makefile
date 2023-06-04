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
build:
	sudo docker build -t template . -f Containerfile
run:
	sudo docker run --rm -d --name template --network host template:latest
uwsgi:
	bash bin/uwsgi.sh $(PORT)
check-trade:
	export PYTHONPATH=`pwd` && source bin/util.sh && source bin/payment.sh && python scripts/trade_check_helper.py
recharge-config-help:
	export PYTHONPATH=`pwd` &&  source bin/util.sh && source bin/payment.sh && python scripts/recharge_config_helper.py
