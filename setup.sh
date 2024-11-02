#!/bin/bash
if ! [ -x "$(command -v psql)" ];then
    tput setaf 4;
    echo "psql is n ot installed";
    echo "To install psql. Run: sudo apt install postgresql-client -y";
    exit 1;
fi

source .env

tput setaf 4;
echo "#########################################################################"
echo "Init database"
echo "#########################################################################"
tput sgr0;
# psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER -d $POSTGRES_DB < vul_template.sql
psql -h 127.0.0.1 -p $POSTGRES_PORT -U $POSTGRES_USER -d $POSTGRES_DB < vul_template.sql


tput setaf 4;
echo "#########################################################################"
echo "Create API key. Save this key. You cannot get it again"
echo "#########################################################################"
tput sgr0;

key_name=rengine
docker exec rengine-web python3 manage.py apikey --create $key_name
