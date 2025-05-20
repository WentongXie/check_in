FROM python
WORKDIR /usr/src/check_in
RUN pip install requests beautifulsoup4 requests[socks]
CMD [ "python", "./check.py" ]
#docker build -t check:latest .
#docker run -d --name check -v ./log/:/log/ -v ./:/usr/src/check_in/ check
