FROM python:3.9-alpine3.15
WORKDIR /app
COPY . /app
RUN apk add --no-cache gcc g++ musl-dev libxml2-dev libxslt-dev python3-dev
RUN apk add --no-cache nodejs npm
RUN npm install -g typescript
RUN pip3 install Flask beautifulsoup4 requests lxml cchardet chardet
RUN tsc static/ts/script.ts --outDir static/js/
ENV FLASK_APP=app
EXPOSE 5000
CMD ["flask", "run", "--host", "0.0.0.0"]

