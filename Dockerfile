FROM alexxxnf/spa-builder as frontend

WORKDIR app/frontend
COPY ./frontend/package.json .
RUN yarn

COPY ./frontend .
RUN yarn run build && for i in `find | grep -E "\.css$|\.html$|\.js$|\.svg$|\.txt$|\.ttf$"`; do gzip -9kf "$i" \
    && brotli -fZ "$i" ; done

FROM python:3.8-slim as backend
WORKDIR app/

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install ocrmypdf
RUN apt-get -y install tesseract-ocr-rus

COPY ./requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt
COPY . .
COPY --from=frontend /app/frontend/public /app/frontend/public

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]