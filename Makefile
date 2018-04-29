PIP = . .env/bin/activate && pip
PYTHON = . .env/bin/activate && python

.env:
	virtualenv -p python3 .env
	${PIP} install -r requirements.txt

run: .env
	${PYTHON} run.py
