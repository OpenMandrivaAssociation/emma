#!/bin/sh

echo -n "app.build.id=" > $1
var=`echo "($(date +%Y) - 2001) * 12 + $(date +%m)" | bc`
var2=`echo "$var*100 + 25" | bc`
echo $var2 >> $1
echo "app.build.date=`date +\"%Y/%m/%d %T\"`" >> $1
