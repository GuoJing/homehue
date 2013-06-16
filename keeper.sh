PIDLIST=`ps -ef|grep 'homehue'|grep -v grep|awk '{print $2}'`;

echo ${PIDLIST}

if [ ! ${PIDLIST} ]
then
    echo 'Not Running'
    /etc/init.d/homehue start
else
    echo 'Running'
fi