PIDLIST=`ps -ef|grep 'homehue/main.py'|grep -v grep|awk '{print $2}'`;

SERVERCODE=`curl -s 10.0.1.85:8989`

ERRORCODE="500"

echo [$(date +"%Y-%m-%d %H:%M:%S")]

echo $PIDLIST

echo $SERVERCODE

echo "$SERVERCODE" |grep -q "$ERRORCODE"
if [ $? -eq 0 ]
then
    echo "Error"
    /etc/init.d/homehue stop
    sleep 1
    /etc/init.d/homehue start
fi

if [ ! ${PIDLIST} ]
then
    echo 'Not Running'
    /etc/init.d/homehue start
else
    echo 'Running'
fi