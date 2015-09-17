#!/bin/sh -e

if [ -z "$1" -o "${1#b}" = "${1}" ] ; then
	echo "Usage:" >&2
	echo "   $0 <version>" >&2
	echo "e.g:" >&2
	echo "   $0 b132" >&2
	exit 1
fi

version="$1"

curl -o "openjdk8-${version}.tar.bz2" "http://hg.openjdk.java.net/jdk8/jdk8/archive/jdk8-${version}.tar.bz2"

for component in corba hotspot jaxp jaxws jdk langtools nashorn ; do
	curl -o "openjdk8-${component}-${version}.tar.bz2" "http://hg.openjdk.java.net/jdk8/jdk8/${component}/archive/jdk8-${version}.tar.bz2"
done
