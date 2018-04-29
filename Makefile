ENV = . .env/bin/activate &&
ENVDEV = . .envdev/bin/activate &&

.env:
	virtualenv -p python3 .env
	${ENV} pip install -r requirements.txt

.envdev:
	virtualenv -p python3 .envdev
	${ENVDEV} pip install -r requirements.txt
	${ENVDEV} pip install -r requirements.dev.txt

run: .env
	${ENV} python run.py

lint: .envdev
	$(ENVDEV) pylint run.py
	$(ENVDEV) pylint matrups/*.py
	$(ENVDEV) yamllint config.sample.yml

clean:
	rm -rf .env
	rm -rf .envdev
