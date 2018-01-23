#!/bin/bash

cd `dirname $0`
DEPLOY_DIR=`pwd`

start(){
    PIDS=`ps aux | grep uwsgi | grep "2600" | awk '{print $2}'`
    if [ -n "$PIDS" ]; then
        echo "ERROR: The server already started!"
        echo "PID: $PIDS"
        exit 1
    fi

    SERVER_PORT=2600
    if [ -n "$SERVER_PORT" ]; then
        SERVER_PORT_COUNT=`netstat -tln | grep $SERVER_PORT | wc -l`
        if [ $SERVER_PORT_COUNT -gt 0 ]; then
            echo "ERROR: The server port $SERVER_PORT already used!"
            exit 1
        fi
    fi

    LOG_DIR=$DEPLOY_DIR/../log/tianqi_server
    LOG_FILE=$LOG_DIR/uwsgi.log
    if [ ! -d $LOG_DIR ]; then
        mkdir -p $LOG_DIR
    fi

    #uwsgi -d $LOG_FILE --http 127.0.0.1:$SERVER_PORT -w api_main -t 20 -M -p 4 --pidfile $DEPLOY_DIR/master.pid
    uwsgi -d $LOG_FILE -s 127.0.0.1:$SERVER_PORT -w test_uwsgi -t 1 -M -p 1 --pidfile $DEPLOY_DIR/master.pid
    sleep 0.2s
    chmod o+r $LOG_FILE
}
stop(){
    uwsgi --stop $DEPLOY_DIR/master.pid
}
restart(){
    uwsgi --reload $DEPLOY_DIR/master.pid
}
case "$1" in
    start)
        start;;
    stop)
        stop;;
    restart)
        restart;;
    *)
        echo "usage: $0 start|stop|restart" >&2
        exit 1
        ;;
esac
