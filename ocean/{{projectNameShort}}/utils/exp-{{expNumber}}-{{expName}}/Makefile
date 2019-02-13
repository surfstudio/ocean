SHELL := /bin/bash
ENV_PATH := env/bin/activate

.DEFAULT: help

help:
	@echo "     USAGE"
	@echo "==============="
	@echo "make -B train"
	@echo "       Starts train.py"
	@echo "make -B dashboard"
	@echo "       Starts MLFlow UI on 0.0.0.0, port 8011"
	@echo "make -B show_venv"
	@echo "       Show all virtual env"
	@echo "make -B create_venv"
	@echo "       Creates new environment in the folder 'env'"
	@echo "make -B remove_env"
	@echo "       Removes environment"

train:
	@python3 scripts/train.py #-c <some_path> \
#                             -d <some_path> \
#                             -s <some_path> \
#                             -u <username>

dashboard:
	@mlflow ui -h 0.0.0.0 -p 8011

show_venv:
	@jupyter kernelspec list

create_venv:
	@python3 -m venv env && source $(ENV_PATH) && pip install ipykernel && python3 utils/create_kernel.py && pip install -r requirements.txt && deactivate

delete_venv:
	@python3 utils/remove_kernel.py && rm -rf env
