#Python parent image
FROM python:3.10-slim

#set working dir
WORKDIR /app

#copy current dir content
COPY . /app

#Install pip dep
RUN pip install --no-cache-dir -r requirements.txt

#Expose port
EXPOSE 8501

#Run the app
CMD ["streamlit","run","streamlit_server.py","--server.port=8501", "--server.address=0.0.0.0"]
