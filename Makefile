.DEFAULT_GOAL := help
SHELL := bash
.ONESHELL:

install:        ## Install dependencies and apt packages
	@echo "installing apt packages..."
	@sudo apt-get install -y git python3-pip python3-rpi.gpio zbar-tools 
	@sudo apt-get install -y python3-picamera2 --no-install-recommends
	@echo "installing dependencies..."
	@echo "creating virtualenv using python3..."
	@pip install -U pip virtualenv
	@virtualenv .venv -p python3
	@echo "virtualenv created successfully."
	@echo "to activate virtualenv, run: source .venv/bin/activate"
	@echo "activating virtualenv..."
	@source .venv/bin/activate
	@pip install --upgrade pip setuptools wheel
	@pip install --upgrade pip
	@pip install -r requirements.txt --extra-index-url https://www.piwheels.org/simple
	@echo "python dependencies installed successfully."
	@echo "------------------------------------------"
	@echo "REOPEN THE TERMINAL IN VSCODE TO HAVE (.venv) ACTIVATED"
	@echo " (OR) Run below command to activate virtualenv"
	@echo "------------------------------------------"
	@echo "source .venv/bin/activate"
	@echo "------------------------------------------"


test:		   ## Run tests
	@echo "running tests..."