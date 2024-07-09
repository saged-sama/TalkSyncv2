FROM okteto/python-fastapi

WORKDIR /backend

COPY requirements.txt requirements.txt
RUN python -m venv env
ENV PATH="/backend/env/bin:$PATH"
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.app:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
