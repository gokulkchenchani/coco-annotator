#!/bin/bash
echo "=> Restore database from $1"
OPTS="--gzip"

if [ -f "/env.sh" ]
then
  source /env.sh
fi

if [ ! -z "$RESTORE_OPTS" ]
then
  OPTS="$RESTORE_OPTS"
fi

if [ ! -z "${MONGO_USER}" ] && [ ! -z "${MONGO_PASS}" ]
then
  AUTH_OPTS="-u $MONGO_USER -p $PASS"
fi

if mongorestore $OPTS --host "$MONGO_HOST" --port "$MONGO_PORT" "$AUTH_OPTS" --archive=$1
then
    echo "=> Restore succeeded"
else
    echo "=> Restore failed"
fi
