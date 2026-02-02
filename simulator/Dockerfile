FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY gcode_samples ./gcode_samples

ENV PYTHONPATH=/app/src

CMD ["python", "-c", "import asyncio; from cnc_machine import CNCMachine; asyncio.run(CNCMachine().run())"]
