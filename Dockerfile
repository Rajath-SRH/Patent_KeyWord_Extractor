FROM python:3.8-slim

WORKDIR /Patent_KeyWord_Extractor

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt
ADD patents /Patent_KeyWord_Extractor
COPY requirements.txt /Patent_KeyWord_Extractor
COPY extract_rake.py /Patent_KeyWord_Extractor

EXPOSE 27017



