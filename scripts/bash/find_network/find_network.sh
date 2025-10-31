#!/usr/bin/env bash

if [ $# -ne 2  ]; then
	echo "Usage: $0 <IP> <MASK>"
fi

IP=$1
MASK=$2

IFS=. read -r i1 i2 i3 i4 <<< "$IP"
IFS=. read -r m1 m2 m3 m4 <<< "$MASK"

network=$((i1 & m1)).$((i2 & m2)).$((i3 & m3)).$((i4 & m4))

echo "Network Address: $network"

exit 0
