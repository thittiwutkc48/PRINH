#!/usr/bin/env bash

# wait-for-it.sh is a script that will wait for a given host and port to be available
# before executing another command.
# Usage example: wait-for-it.sh postgres:5432 -- echo "Postgres is up"

TIMEOUT=15
QUIET=0
CHILD=0

usage()
{
    echo "Usage: $0 host:port [-t timeout] [-q] -- command args"
    exit 1
}

wait_for()
{
    for i in `seq $TIMEOUT` ; do
        nc -z $HOST $PORT
        result=$?
        if [ $result -eq 0 ] ; then
            if [ $CHILD -gt 0 ] ; then
                exec "${@}"
            fi
            exit 0
        fi
        sleep 1
    done
    echo "Operation timed out" >&2
    exit 1
}

while [ $# -gt 0 ]
do
    case "$1" in
        *:* )
        HOST=$(echo $1 | cut -d : -f 1)
        PORT=$(echo $1 | cut -d : -f 2)
        shift 1
        ;;
        -q)
        QUIET=1
        shift 1
        ;;
        -t)
        TIMEOUT=$2
        if [ $TIMEOUT -lt 1 ] ; then
            echo "Error: invalid timeout '$TIMEOUT'"
            exit 1
        fi
        shift 2
        ;;
        --)
        shift
        CHILD=$$
        break
        ;;
        *)
        usage
        ;;
    esac
done

if [ "$HOST" = "" -o "$PORT" = "" ] ; then
    echo "Error: you need to provide a host and port to test."
    usage
fi

wait_for "${@}"
