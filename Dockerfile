FROM python:3.9-alpine
# Or any preferred Python version.
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN mkdir /in-stock-notifier
WORKDIR /in-stock-notifier
COPY src/main.py ./
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python3", "main.py"]
# Or enter the name of your unique directory and parameter set.