FROM prefecthq/prefect:2.7.7-python3.10

COPY requirements-roma-dev.txt .

RUN pip install -r requirements-roma-dev.txt --trusted-host pypi.python.org --no-cache-dir

COPY flows /opt/prefect/flows
# COPY data /opt/prefect/data

