env:
ifndef VIRTUAL_ENV
	@chmod +x manage_shell.sh
	@./manage_shell.sh
else
	@echo "Virtual environment $$(basename $$VIRTUAL_ENV) is already active"
endif

env-update:
	@. venv/bin/activate && pip install pip -r requirements.txt --upgrade

env-freeze: env-update
	@. venv/bin/activate && pip freeze > requirements.txt

build-image:
	@docker build -t jpm-stocks:latest -f Dockerfile .

run-image: build-image
	@docker run -it jpm-stocks:latest

format:
	@black . --exclude=venv

tests:
	@. venv/bin/activate && python -m unittest discover -s tests -p 'test_*.py' -v

.PHONY: tests format run-image