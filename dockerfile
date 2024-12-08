FROM python
WORKDIR /usr/src/check_in
COPY . .
RUN pip install requests beautifulsoup4
CMD [ "python", "./check.py" ]
