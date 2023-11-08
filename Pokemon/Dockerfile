FROM python:3



COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# # install FreeTDS and dependencies
# RUN apt-get update \
#  && apt-get install unixodbc -y \
#  && apt-get install unixodbc-dev -y \
#  && apt-get install freetds-dev -y \
#  && apt-get install freetds-bin -y \
#  && apt-get install tdsodbc -y \
#  && apt-get install --reinstall build-essential -y

# # populate "ocbcinst.ini"
# RUN echo "[FreeTDS]\n\
# Description = FreeTDS unixODBC Driver\n\
# Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so\n\
# Setup = /usr/lib/x86_64-linux-gnu/odbc/libtdsS.so" >> /etc/odbcinst.ini

RUN apt-get -y update && apt-get install -y curl gnupg

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

# download appropriate package for the OS version
# Debian 11
RUN curl https://packages.microsoft.com/config/debian/11/prod.list  \
    > /etc/apt/sources.list.d/mssql-release.list

RUN exit
RUN apt-get -y update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql18

RUN pip install pyodbc

# RUN echo MinProtocol = TLSv1.0 >> /etc/ssl/openssl.cnf
# RUN echo CipherString = DEFAULT@SECLEVEL=1 >> /etc/ssl/openssl.cnf

COPY src/app.py ./


EXPOSE 5000


CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0" ]

