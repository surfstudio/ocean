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
	@echo "make -B showenv"
	@echo "       Show all virtual env"
	@echo "make -B createenv"
	@echo "       Creates new environment in the folder 'env'"
	@echo "make -B removeenv"
	@echo "       Removes environment"

train:
	@python3 scripts/train.py #-c <some_path> \
#                             -d <some_path> \
#                             -s <some_path>

dashboard:
	@mlflow ui -h 0.0.0.0 -p 8011

showenv:
	@jupyter kernelspec list

createenv:
	@python3 -m venv env && source $(ENV_PATH) && pip install ipykernel && python3 scripts/create_kernel.py && pip install -r requirements.txt && deactivate

removeenv:
	@python3 scripts/remove_kernel.py && rm -rf env
