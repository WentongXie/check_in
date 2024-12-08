FROM python
WORKDIR /usr/src/check_in
COPY . .
RUN pip install requests beautifulsoup4 requests[socks]
CMD [ "python", "./check.py" ]
