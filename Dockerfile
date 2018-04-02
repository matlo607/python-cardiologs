FROM python:3.6.5-jessie

RUN pip install "pipenv" \
 && git clone "https://github.com/matlo607/python-cardiologs.git"

WORKDIR python-cardiologs

RUN pipenv install --dev

CMD ["pipenv", "run", "./analyse.py", "-f", "record.csv"]
