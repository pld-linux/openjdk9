#!/bin/sh -e

tag="$1"

if [ -z "$tag" -a -x /usr/bin/rpm-specdump ] ; then
	version=$(rpm-specdump openjdk8.spec | awk '/^h PACKAGE_VERSION/ { sub(/.b/, "-b", $3); print $3 }')
	if [ -n "$version" ] ; then
		tag="jdk$version"
		echo "Using spec version: $tag"
	fi
fi


if [ -z "$tag" -o "${tag#jdk8}" = "${tag}" ] ; then
	echo "Usage:" >&2
	echo "   $0 <tag>" >&2
	echo "e.g:" >&2
	echo "   $0 jdk8u66-b02" >&2
	exit 1
fi

if [ "${tag#jdk8u}" != "${tag}" ] ; then
	repo="jdk8u"
else
	repo="jdk8"
fi

curl -o "openjdk8-${tag}.tar.bz2" "http://hg.openjdk.java.net/$repo/$repo/archive/${tag}.tar.bz2"

for component in corba hotspot jaxp jaxws jdk langtools nashorn ; do
	curl -o "openjdk8-${component}-${tag}.tar.bz2" "http://hg.openjdk.java.net/$repo/$repo/${component}/archive/${tag}.tar.bz2"
done
