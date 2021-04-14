FROM python:3.8
COPY ./*.py ./
CMD ["python", "main.py"]