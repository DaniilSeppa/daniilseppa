FROM python:3.8

RUN mkdir -p /Users/DSeppa/Documents/bot
WORKDIR /Users/DSeppa/Documents/bot

COPY . /Users/Dseppa/Documents/bot
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "bot.py"]