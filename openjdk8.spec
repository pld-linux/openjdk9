#
# TODO:
# 	- fix BuildRequires
#	- fix build with system giflib
#	- use other system libs (libjpeg, liblcms, libsctp)
#	- build alternative VM for x32
#	- include icedtea-sound?
#	- port PLD-specific changes from icedtea7?
#	- '*** WARNING: no sources found for ...'

%bcond_with bootstrap   # build a bootstrap version, using icedtea6
%bcond_without cacerts	# don't include the default CA certificates

%if %{with bootstrap}
%define		use_jdk	icedtea7
%else
%define		use_jdk	openjdk8
%endif

# class data version seen with file(1) that this jvm is able to load
%define		_classdataversion 52.0
# JDK/JRE version, as returned with `java -version`, '_' replaced with '.'
%define		_jdkversion 1.8.0.internal

Summary:	Open-source implementation of the Java Platform, Standard Edition
Summary(pl.UTF-8):	Wolnoźródłowa implementacja Java 8 SE
Name:		openjdk8
%define	ver_u	66
%define	ver_b	02
Version:	8u%{ver_u}.b%{ver_b}
Release:	0.1
License:	GPL v2
Group:		Development/Languages/Java
Source0:	openjdk8-jdk8u%{ver_u}-b%{ver_b}.tar.bz2
# Source0-md5:	1d115662e175470270e89a4da8e0fce2
Source1:	openjdk8-corba-jdk8u%{ver_u}-b%{ver_b}.tar.bz2
# Source1-md5:	e14d8f51b9ca30d798094a2867f3f5d0
Source2:	openjdk8-hotspot-jdk8u%{ver_u}-b%{ver_b}.tar.bz2
# Source2-md5:	b49a7b7f2db5b07306b7b5739e87ccc0
Source3:	openjdk8-jaxp-jdk8u%{ver_u}-b%{ver_b}.tar.bz2
# Source3-md5:	6bd5ae187272a209439d1a95ac6c9025
Source4:	openjdk8-jaxws-jdk8u%{ver_u}-b%{ver_b}.tar.bz2
Source5:	openjdk8-jdk-jdk8u%{ver_u}-b%{ver_b}.tar.bz2
# Source5-md5:	74f2cf3815659b83993c4187e7fc4f6b
Source6:	openjdk8-langtools-jdk8u%{ver_u}-b%{ver_b}.tar.bz2
# Source6-md5:	de5c9b5fdbcd75028b71ed667d4b99d2
Source7:	openjdk8-nashorn-jdk8u%{ver_u}-b%{ver_b}.tar.bz2
# Source7-md5:	7da4e88349cfc45ee9726eaa4386be03
Source10:	make-cacerts.sh
Patch0:		adjust-mflags.patch
Patch1:		format_strings.patch
Patch2:		CompileDemos.patch
Patch3:		libpath.patch
URL:		http://openjdk.java.net/
BuildRequires:	alsa-lib-devel
BuildRequires:	ant
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bash
%{?with_cacerts:BuildRequires:	ca-certificates-update}
BuildRequires:	cups-devel
BuildRequires:	/usr/bin/jar
BuildRequires:	freetype-devel >= 2.3
BuildRequires:	gawk
#BuildRequires:	giflib-devel >= 5.1
BuildRequires:	glibc-misc
%buildrequires_jdk
BuildRequires:	libjpeg-devel
BuildRequires:	lsb-release
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.557
BuildRequires:	unzip
BuildRequires:	util-linux
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXp-devel
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	xorg-lib-libXtst-devel
BuildRequires:	xorg-proto-printproto-devel
BuildRequires:	xorg-proto-xproto-devel
BuildRequires:	zip
BuildRequires:	zlib-devel
Requires:	%{name}-appletviewer = %{version}-%{release}
Requires:	%{name}-jdk = %{version}-%{release}
Suggests:	%{name}-jre-X11
Suggests:	icedtea-web
Obsoletes:	icedtea6
Obsoletes:	icedtea7
Obsoletes:	java5-sun
Obsoletes:	java5-sun-jre
Obsoletes:	java5-sun-jre-jdbc
Obsoletes:	java5-sun-jre-X11
Obsoletes:	java5-sun-tools
Obsoletes:	java-gcj-compat
Obsoletes:	java-gcj-compat-devel
Obsoletes:	java-sun
Obsoletes:	java-sun-demos
Obsoletes:	java-sun-jre
Obsoletes:	java-sun-jre-alsa
Obsoletes:	java-sun-jre-jdbc
Obsoletes:	java-sun-jre-X11
Obsoletes:	java-sun-tools
Obsoletes:	oracle-java7
Obsoletes:	oracle-java7-jre
Obsoletes:	oracle-java7-jre-alsa
Obsoletes:	oracle-java7-jre-jdbc
Obsoletes:	oracle-java7-jre-X11
Obsoletes:	oracle-java7-tools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dstreldir	%{name}-%{version}
%define		dstdir		%{_jvmdir}/%{dstreldir}
%define		jrereldir	%{dstreldir}/jre
%define		jredir		%{_jvmdir}/%{jrereldir}
%define		jvmjardir	%{_jvmjardir}/%{name}-%{version}

%ifarch %{x8664}
%define		jre_arch	amd64
%endif
%ifarch %{ix86}
%define		jre_arch	i386
%endif
%ifarch x32
%define		jre_arch	x32
%endif

# to break artificial subpackage dependency loops
%define		_noautoreq	'libmawt.so' java\\\\(ClassDataVersion\\\\)

%description
Open-source implementation of the Java Platform, Standard Edition.

This is a meta-package which provides, by its dependencies, all the
OpenJDK components including the OpenJDK, Java 8 developement kit and
runtime environment.

%description -l pl.UTF-8
Wolnoźródłowa implementacja Java 8 SE.

To jest meta-pakiet, który, za pośrednictwem zależności, dostarcza
wszystkie komponenty OpenJDK, w tym środowisko programistyczne
(OpenJDK) i uruchomieniowe (JRE).

%package jdk
Summary:	OpenJDK - software development kit
Summary(pl.UTF-8):	OpenJDK - środowisko programistyczne
Group:		Development/Languages/Java
Requires:	%{name}-jar = %{version}-%{release}
Requires:	%{name}-jdk-base = %{version}-%{release}
Requires:	%{name}-jre = %{version}-%{release}
Provides:	j2sdk = %{_jdkversion}
Provides:	jdk = %{_jdkversion}
Obsoletes:	blackdown-java-sdk
Obsoletes:	ibm-java
Obsoletes:	icedtea6-jdk
Obsoletes:	icedtea7-jdk
Obsoletes:	java-blackdown
Obsoletes:	java-gcj-compat-devel
Obsoletes:	java-sun
Obsoletes:	java5-sun
Obsoletes:	oracle-java7
Obsoletes:	jdk
Obsoletes:	kaffe

%description jdk
This package symlinks OpenJDK development tools provided by
%{name}-jdk-base to system-wide directories like %{_bindir}, making
OpenJDK the default JDK.

%description jdk -l pl.UTF-8
Ten pakiet tworzy symboliczne dowiązania do narzędzi programistycznych
OpenJDK, dostarczanych przez pakiet %{name}-jdk-base, w standardowych
systemowych ścieżkach takich jak %{_bindir}, sprawiając tym samym, że
OpenJDK staje się domyślnym JDK w systemie.

%package jdk-base
Summary:	OpenJDK - software development kit
Summary(pl.UTF-8):	Kod OpenJDK - środowisko programistyczne
Group:		Development/Languages/Java
Requires:	%{name}-jre-base = %{version}-%{release}
Requires:	jpackage-utils >= 0:1.7.5-4
Provides:	jdk(%{name})

%description jdk-base
OpenJDK development tools built using free software only.

%description jdk-base -l pl.UTF-8
OpenJDK skompilowane wyłącznie przy użyciu wolnego oprogramowania.

%package jre
Summary:	OpenJDK - runtime environment
Summary(pl.UTF-8):	OpenJDK - środowisko uruchomieniowe
Group:		Development/Languages/Java
Requires:	%{name}-jre-base = %{version}-%{release}
Requires:	nss >= 1:3.13.4
# Require zoneinfo data provided by java-tzdata subpackage.
Requires:	java-tzdata
Provides:	java
Provides:	java(ClassDataVersion) = %{_classdataversion}
Provides:	java(jaas) = %{version}
Provides:	java(jaf) = 1.1.1
Provides:	java(jaxp) = 1.3
Provides:	java(jaxp_parser_impl)
Provides:	java(jce) = %{version}
Provides:	java(jdbc-stdext) = %{version}
Provides:	java(jdbc-stdext) = 3.0
Provides:	java(jmx) = 1.4
Provides:	java(jndi) = %{version}
Provides:	java(jsse) = %{version}
Provides:	java1.4
Provides:	jre = %{_jdkversion}
Obsoletes:	icedtea6-jre
Obsoletes:	icedtea7-jre
Obsoletes:	java(jaas)
Obsoletes:	java(jaf)
Obsoletes:	java(jaxp)
Obsoletes:	java(jce)
Obsoletes:	java(jdbc-stdext)
Obsoletes:	java(jdbc-stdext)
Obsoletes:	java(jmx)
Obsoletes:	java(jndi)
Obsoletes:	java(jsse)
Obsoletes:	java-gcj-compat
Obsoletes:	java-sun-jre
Obsoletes:	java5-sun-jre
Obsoletes:	oracle-java7-jre
Obsoletes:	jre

%description jre
This package symlinks OpenJDK runtime environment tools provided by
%{name}-jre-base to system-wide directories like %{_bindir}, making
OpenJDK the default JRE.

%description jre -l pl.UTF-8
Ten pakiet tworzy symboliczne dowiązania do środowiska
uruchomieniowego OpenJDK, dostarczanych przez pakiet %{name}-jre-base,
w standardowych systemowych ścieżkach takich jak %{_bindir},
sprawiając tym samym, że OpenJDK staje się domyślnym JRE w systemie.

%package jre-X11
Summary:	OpenJDK - runtime environment - X11 support
Summary(pl.UTF-8):	OpenJDK - środowisko uruchomieniowe - obsługa X11
Group:		Development/Languages/Java
Requires:	%{name}-jre = %{version}-%{release}
Requires:	%{name}-jre-base-X11 = %{version}-%{release}
Provides:	jre-X11 = %{_jdkversion}
Obsoletes:	icedtea6-jre-X11
Obsoletes:	icedtea7-jre-X11
Obsoletes:	java-sun-jre-X11
Obsoletes:	oracle-java7-jre-X11

%description jre-X11
X11 support for OpenJDK runtime environment built using free software
only.

%description jre-X11 -l pl.UTF-8
Biblioteki X11 dla środowiska OpenJDK zbudowany wyłocznie przy uzyciu
wolnego oprogramowania.

%package jre-base
Summary:	OpenJDK - runtime environment
Summary(pl.UTF-8):	OpenJDK - środowisko uruchomieniowe
Group:		Development/Languages/Java
Requires:	jpackage-utils >= 0:1.7.5-4
Provides:	jre(%{name})

%description jre-base
OpenJDK runtime environment built using free software only.

%description jre-base -l pl.UTF-8
Środowisko uruchomieniowe OpenJDK zbudowany wyłącznie przy użyciu
wolnego oprogramowania.

%package jre-base-X11
Summary:	OpenJDK - runtime environment - X11 support
Summary(pl.UTF-8):	OpenJDK - środowisko uruchomieniowe - obsługa X11
Group:		Development/Languages/Java
Requires:	%{name}-jre-base = %{version}-%{release}
Requires:	%{name}-jre-base-freetype = %{version}-%{release}

%description jre-base-X11
X11 support for OpenJDK runtime environment built using free software
only.

%description jre-base-X11 -l pl.UTF-8
Biblioteki X11 dla środowiska OpenJDK zbudowany wyłocznie przy uzyciu
wolnego oprogramowania.

%package jre-base-alsa
Summary:	OpenJDK - runtime environment - ALSA support
Summary(pl.UTF-8):	OpenJDK - środowisko uruchomieniowe - obsługa ALSA
Group:		Development/Languages/Java
Requires:	%{name}-jre-base = %{version}-%{release}

%description jre-base-alsa
ALSA sound support for OpenJDK runtime environment build using free
software only.

%description jre-base-alsa -l pl.UTF-8
Biblioteki ALSA rozszerzające środowisko OpenJDK o obsługę dźwięku
zbudowane przy uzyciu wyłącznie wolnego oprogramowania.

%package jre-base-freetype
Summary:	OpenJDK - runtime environment - font support
Summary(pl.UTF-8):	OpenJDK - środowisko uruchomieniowe - obsługa fontów
Group:		Development/Languages/Java
Requires:	%{name}-jre-base = %{version}-%{release}

%description jre-base-freetype
Font handling library for OpenJDK runtime environment built using free
software only.

%description jre-base-freetype -l pl.UTF-8
Biblioteki obsługi czcionek dla OpenJDK zbudowane wyłącznie przy
użyciu wolnego oprogramowania.

%package jre-base-gtk
Summary:	OpenJDK - runtime environment - GTK support
Summary(pl.UTF-8):	OpenJDK - środowisko uruchomieniowe - obsługa GTK
Group:		Development/Languages/Java
Requires:	%{name}-jre-base = %{version}-%{release}

%description jre-base-gtk
GTK support for OpenJDK runtime environment.

%description jre-base-gtk -l pl.UTF-8
Biblioteki GTK dla OpenJDK.

%package jar
Summary:	OpenJDK - JAR tool
Summary(pl.UTF-8):	OpenJDK - narzędzie JAR
Group:		Development/Languages/Java
Requires:	%{name}-jdk-base = %{version}-%{release}
Provides:	jar
Obsoletes:	fastjar
Obsoletes:	icedtea6-jar
Obsoletes:	icedtea7-jar
Obsoletes:	jar

%description jar
JAR tool from OpenJDK built using free software only.

JAR is an archiver used to merge Java classes into a single library.

%description jar -l pl.UTF-8
Narzędzie jar z OpenJDK zbudowane przy uzyciu wyłącznie wolnego
oprogramowania.

JAR jest narzędziem pozwalającym wykonywać podstawowe operacje na
archiwach javy .jar takie jak na przykład tworzenie lub rozpakowywanie
archiwów.

%package appletviewer
Summary:	OpenJDK - appletviewer tool
Summary(pl.UTF-8):	OpenJDK - narzędzie appletviewer
Group:		Development/Languages/Java
Requires:	%{name}-jdk-base = %{version}-%{release}
Requires:	%{name}-jre-X11 = %{version}-%{release}
Obsoletes:	icedtea6-appletviewer
Obsoletes:	icedtea7-appletviewer
Obsoletes:	java-sun-appletviewer
Obsoletes:	oracle-java7-appletviewer

%description appletviewer
Appletviewer from OpenJDK build using free software only.

%description appletviewer -l pl.UTF-8
Appletviewer pozwala uruchamiać aplety javy niezależnie od
przeglądarki www. Ten appletviewer pochodzi z zestawu narzędzi OpenJDK
i został zbudowany wyłącznie przy użyciu wolnego oprogramowania.

%package jdk-sources
Summary:	OpenJDK - sources
Summary(pl.UTF-8):	OpenJDK - kod źródłowy
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description jdk-sources
Source code for the OpenJDK development kit and Java standard library.

%description jdk-sources -l pl.UTF-8
Kod źródłowy narzędzi programistycznych OpenJDK oraz standardowej
biblioteki Javy.

%package examples
Summary:	OpenJDK - examples
Summary(pl.UTF-8):	OpenJDK - przykłady
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description examples
Code examples for OpenJDK.

%description examples -l pl.UTF-8
Przykłady dla OpenJDK.

%prep
%setup -qn jdk8u-jdk8u%{ver_u}-b%{ver_b} -a1 -a2 -a3 -a4 -a5 -a6 -a7

for d in *-jdk8u*-b* ; do
	mv "$d" "${d%%-jdk8u*-b*}"
done

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
# Make sure we have /proc mounted - otherwise idlc will fail later.
if [ ! -f /proc/self/stat ]; then
	echo "You need to have /proc mounted in order to build this package!"
	exit 1
fi

mkdir -p build-bin
export JAVA_HOME=%{java_home}
export PATH="$JAVA_HOME/bin:$PATH"
export SHELL=/bin/bash

chmod a+x configure

%configure \
	--with-extra-cflags="%{rpmcflags}" \
	--with-extra-cxxflags="%{rpmcxxflags}" \
	--with-extra-ldflags="%{rpmldflags}" \
	--with-giflib=bundled \
	--with-zlib=system

specdir="$(dirname build/*-release/spec.gmk)"
cat > $specdir/custom-spec.gmk <<EOF
SHELL=/bin/bash
EOF
[ -d tmp-bin ] || ln -s "$specdir/jdk/bin" tmp-bin

%{__make} all \
	LOG=debug

export PATH="$(pwd)/build-bin:$PATH"
%{?with_cacerts:%{__sh} %{SOURCE10}}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{dstdir},%{_mandir}/ja} \
	$RPM_BUILD_ROOT{%{jvmjardir},%{_examplesdir}/%{name}-%{version},%{_javasrcdir}} \
	$RPM_BUILD_ROOT%{_sysconfdir}/%{name}

# install the 'JDK image', it contains the JRE too
cp -a build/*-release/images/j2sdk-image/* $RPM_BUILD_ROOT%{dstdir}

# convenience symlinks without version number
ln -s %{dstreldir} $RPM_BUILD_ROOT%{_jvmdir}/%{name}
ln -s %{jrereldir} $RPM_BUILD_ROOT%{_jvmdir}/%{name}-jre

ln -s %{dstreldir} $RPM_BUILD_ROOT%{_jvmdir}/java

# move JDK sources and demo to /usr/src
mv $RPM_BUILD_ROOT%{dstdir}/demo $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
mv $RPM_BUILD_ROOT%{dstdir}/sample $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
mv $RPM_BUILD_ROOT%{dstdir}/src.zip $RPM_BUILD_ROOT%{_javasrcdir}/%{name}-jdk.zip

# move manual pages to its place
mv $RPM_BUILD_ROOT%{dstdir}/man/ja_JP.UTF-8/man1 $RPM_BUILD_ROOT%{_mandir}/ja/man1
rmdir $RPM_BUILD_ROOT%{dstdir}/man/ja_JP.UTF-8
rm $RPM_BUILD_ROOT%{dstdir}/man/ja
mv $RPM_BUILD_ROOT%{dstdir}/man/man1 $RPM_BUILD_ROOT%{_mandir}/man1
rmdir $RPM_BUILD_ROOT%{dstdir}/man

# replace duplicates with symlinks, link to %{_bindir}
for path in $RPM_BUILD_ROOT%{dstdir}/bin/*; do
	filename=$(basename $path)
	if diff -q "$path" "$RPM_BUILD_ROOT%{jredir}/bin/$filename" > /dev/null; then
		ln -sf "../jre/bin/$filename" "$path"
		ln -sf "%{jredir}/bin/$filename" $RPM_BUILD_ROOT%{_bindir}
	else
		ln -sf "%{dstdir}/bin/$filename" $RPM_BUILD_ROOT%{_bindir}
	fi
done
ln -sf ../jre/lib/jexec $RPM_BUILD_ROOT%{dstdir}/lib/jexec

# keep configuration in /etc (not all *.properties go there)
for config in management security content-types.properties \
		logging.properties net.properties sound.properties; do

	mv $RPM_BUILD_ROOT%{jredir}/lib/$config $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/$config
	ln -s %{_sysconfdir}/%{name}/$config $RPM_BUILD_ROOT%{jredir}/lib/$config
done

ln -sf %{jredir}/lib/jsse.jar $RPM_BUILD_ROOT%{jvmjardir}/jsse.jar
ln -sf %{jredir}/lib/jsse.jar $RPM_BUILD_ROOT%{jvmjardir}/jcert.jar
ln -sf %{jredir}/lib/jsse.jar $RPM_BUILD_ROOT%{jvmjardir}/jnet.jar
ln -sf %{jredir}/lib/jce.jar $RPM_BUILD_ROOT%{jvmjardir}/jce.jar
for f in jndi jndi-ldap jndi-cos jndi-rmi jaas jdbc-stdext jdbc-stdext-3.0 \
	sasl jaxp_parser_impl jaxp_transform_impl jaxp jmx activation xml-commons-apis \
	jndi-dns jndi-rmi; do
	ln -sf %{jredir}/lib/rt.jar $RPM_BUILD_ROOT%{jvmjardir}/$f.jar
done

# some apps (like opera) looks for it in different place
ln -s server/libjvm.so $RPM_BUILD_ROOT%{jredir}/lib/%{jre_arch}/libjvm.so

%{__rm} $RPM_BUILD_ROOT%{dstdir}/{,jre/}{ASSEMBLY_EXCEPTION,LICENSE,THIRD_PARTY_README}

%{?with_cacerts:install cacerts $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/security}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc THIRD_PARTY_README ASSEMBLY_EXCEPTION

%files jdk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/extcheck
%attr(755,root,root) %{_bindir}/idlj
%attr(755,root,root) %{_bindir}/jarsigner
%attr(755,root,root) %{_bindir}/java-rmi.cgi
%attr(755,root,root) %{_bindir}/javac
%attr(755,root,root) %{_bindir}/javadoc
%attr(755,root,root) %{_bindir}/javah
%attr(755,root,root) %{_bindir}/javap
%attr(755,root,root) %{_bindir}/jcmd
%attr(755,root,root) %{_bindir}/jconsole
%attr(755,root,root) %{_bindir}/jdb
%attr(755,root,root) %{_bindir}/jdeps
%attr(755,root,root) %{_bindir}/jhat
%attr(755,root,root) %{_bindir}/jinfo
%attr(755,root,root) %{_bindir}/jmap
%attr(755,root,root) %{_bindir}/jps
%attr(755,root,root) %{_bindir}/jrunscript
%attr(755,root,root) %{_bindir}/jsadebugd
%attr(755,root,root) %{_bindir}/jstack
%attr(755,root,root) %{_bindir}/jstat
%attr(755,root,root) %{_bindir}/jstatd
%attr(755,root,root) %{_bindir}/native2ascii
%attr(755,root,root) %{_bindir}/rmic
%attr(755,root,root) %{_bindir}/schemagen
%attr(755,root,root) %{_bindir}/serialver
%attr(755,root,root) %{_bindir}/wsgen
%attr(755,root,root) %{_bindir}/wsimport
%attr(755,root,root) %{_bindir}/xjc
%{_jvmdir}/java
%{_mandir}/man1/extcheck.1*
%{_mandir}/man1/idlj.1*
%{_mandir}/man1/jarsigner.1*
%{_mandir}/man1/javac.1*
%{_mandir}/man1/javadoc.1*
%{_mandir}/man1/javah.1*
%{_mandir}/man1/javap.1*
%{_mandir}/man1/jcmd.1*
%{_mandir}/man1/jconsole.1*
%{_mandir}/man1/jdb.1*
%{_mandir}/man1/jdeps.1*
%{_mandir}/man1/jhat.1*
%{_mandir}/man1/jinfo.1*
%{_mandir}/man1/jmap.1*
%{_mandir}/man1/jps.1*
%{_mandir}/man1/jrunscript.1*
%{_mandir}/man1/jsadebugd.1*
%{_mandir}/man1/jstack.1*
%{_mandir}/man1/jstat.1*
%{_mandir}/man1/jstatd.1*
%{_mandir}/man1/native2ascii.1*
%{_mandir}/man1/schemagen.1*
%{_mandir}/man1/serialver.1*
%{_mandir}/man1/rmic.1*
%{_mandir}/man1/wsgen.1*
%{_mandir}/man1/wsimport.1*
%{_mandir}/man1/xjc.1*
%lang(ja) %{_mandir}/ja/man1/extcheck.1*
%lang(ja) %{_mandir}/ja/man1/idlj.1*
%lang(ja) %{_mandir}/ja/man1/jarsigner.1*
%lang(ja) %{_mandir}/ja/man1/javac.1*
%lang(ja) %{_mandir}/ja/man1/javadoc.1*
%lang(ja) %{_mandir}/ja/man1/javah.1*
%lang(ja) %{_mandir}/ja/man1/javap.1*
%lang(ja) %{_mandir}/ja/man1/jcmd.1*
%lang(ja) %{_mandir}/ja/man1/jconsole.1*
%lang(ja) %{_mandir}/ja/man1/jdb.1*
%lang(ja) %{_mandir}/ja/man1/jdeps.1*
%lang(ja) %{_mandir}/ja/man1/jhat.1*
%lang(ja) %{_mandir}/ja/man1/jinfo.1*
%lang(ja) %{_mandir}/ja/man1/jmap.1*
%lang(ja) %{_mandir}/ja/man1/jps.1*
%lang(ja) %{_mandir}/ja/man1/jrunscript.1*
%lang(ja) %{_mandir}/ja/man1/jsadebugd.1*
%lang(ja) %{_mandir}/ja/man1/jstack.1*
%lang(ja) %{_mandir}/ja/man1/jstat.1*
%lang(ja) %{_mandir}/ja/man1/jstatd.1*
%lang(ja) %{_mandir}/ja/man1/native2ascii.1*
%lang(ja) %{_mandir}/ja/man1/schemagen.1*
%lang(ja) %{_mandir}/ja/man1/serialver.1*
%lang(ja) %{_mandir}/ja/man1/rmic.1*
%lang(ja) %{_mandir}/ja/man1/wsgen.1*
%lang(ja) %{_mandir}/ja/man1/wsimport.1*
%lang(ja) %{_mandir}/ja/man1/xjc.1*

%files jdk-base
%defattr(644,root,root,755)
%doc build/*-release/images/j2sdk-image/THIRD_PARTY_README
%doc build/*-release/images/j2sdk-image/ASSEMBLY_EXCEPTION
%dir %{dstdir}
%{_jvmdir}/%{name}
%attr(755,root,root) %{dstdir}/bin/appletviewer
%attr(755,root,root) %{dstdir}/bin/extcheck
%attr(755,root,root) %{dstdir}/bin/idlj
%attr(755,root,root) %{dstdir}/bin/jar
%attr(755,root,root) %{dstdir}/bin/jarsigner
%attr(755,root,root) %{dstdir}/bin/java-rmi.cgi
%attr(755,root,root) %{dstdir}/bin/javac
%attr(755,root,root) %{dstdir}/bin/javadoc
%attr(755,root,root) %{dstdir}/bin/javah
%attr(755,root,root) %{dstdir}/bin/javap
%attr(755,root,root) %{dstdir}/bin/jconsole
%attr(755,root,root) %{dstdir}/bin/jcmd
%attr(755,root,root) %{dstdir}/bin/jdb
%attr(755,root,root) %{dstdir}/bin/jdeps
%attr(755,root,root) %{dstdir}/bin/jhat
%attr(755,root,root) %{dstdir}/bin/jinfo
%attr(755,root,root) %{dstdir}/bin/jmap
%attr(755,root,root) %{dstdir}/bin/jps
%attr(755,root,root) %{dstdir}/bin/jrunscript
%attr(755,root,root) %{dstdir}/bin/jsadebugd
%attr(755,root,root) %{dstdir}/bin/jstack
%attr(755,root,root) %{dstdir}/bin/jstat
%attr(755,root,root) %{dstdir}/bin/jstatd
%attr(755,root,root) %{dstdir}/bin/native2ascii
%attr(755,root,root) %{dstdir}/bin/rmic
%attr(755,root,root) %{dstdir}/bin/schemagen
%attr(755,root,root) %{dstdir}/bin/serialver
%attr(755,root,root) %{dstdir}/bin/wsgen
%attr(755,root,root) %{dstdir}/bin/wsimport
%attr(755,root,root) %{dstdir}/bin/xjc
%{dstdir}/include
%dir %{dstdir}/lib
%{dstdir}/lib/ct.sym
%{dstdir}/lib/dt.jar
%{dstdir}/lib/ir.idl
%{dstdir}/lib/jconsole.jar
%attr(755,root,root) %{dstdir}/lib/jexec
%{dstdir}/lib/orb.idl
%ifnarch x32
%{dstdir}/lib/sa-jdi.jar
%endif
%{dstdir}/lib/tools.jar
%dir %{dstdir}/lib/%{jre_arch}
%dir %{dstdir}/lib/%{jre_arch}/jli
%attr(755,root,root) %{dstdir}/lib/%{jre_arch}/jli/*.so

%files jre
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/java
%attr(755,root,root) %{_bindir}/jjs
%attr(755,root,root) %{_bindir}/keytool
%attr(755,root,root) %{_bindir}/orbd
%attr(755,root,root) %{_bindir}/pack200
%attr(755,root,root) %{_bindir}/rmid
%attr(755,root,root) %{_bindir}/rmiregistry
%attr(755,root,root) %{_bindir}/servertool
%attr(755,root,root) %{_bindir}/tnameserv
%attr(755,root,root) %{_bindir}/unpack200
%{_mandir}/man1/java.1*
%{_mandir}/man1/jjs.1*
%{_mandir}/man1/keytool.1*
%{_mandir}/man1/orbd.1*
%{_mandir}/man1/pack200.1*
%{_mandir}/man1/rmid.1*
%{_mandir}/man1/rmiregistry.1*
%{_mandir}/man1/servertool.1*
%{_mandir}/man1/tnameserv.1*
%{_mandir}/man1/unpack200.1*
%lang(ja) %{_mandir}/ja/man1/java.1*
%lang(ja) %{_mandir}/ja/man1/jjs.1*
%lang(ja) %{_mandir}/ja/man1/keytool.1*
%lang(ja) %{_mandir}/ja/man1/orbd.1*
%lang(ja) %{_mandir}/ja/man1/pack200.1*
%lang(ja) %{_mandir}/ja/man1/rmid.1*
%lang(ja) %{_mandir}/ja/man1/rmiregistry.1*
%lang(ja) %{_mandir}/ja/man1/servertool.1*
%lang(ja) %{_mandir}/ja/man1/tnameserv.1*
%lang(ja) %{_mandir}/ja/man1/unpack200.1*

%files jre-base
%defattr(644,root,root,755)
%doc openjdk.build/j2sdk-image/THIRD_PARTY_README
%doc openjdk.build/j2sdk-image/ASSEMBLY_EXCEPTION
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*
%dir %{dstdir}
%{dstdir}/release
%dir %{jredir}
%{_jvmdir}/%{name}-jre
%dir %{jredir}/bin
%dir %{dstdir}/bin
%attr(755,root,root) %{jredir}/bin/java
%attr(755,root,root) %{dstdir}/bin/java
%attr(755,root,root) %{jredir}/bin/jjs
%attr(755,root,root) %{dstdir}/bin/jjs
%attr(755,root,root) %{jredir}/bin/keytool
%attr(755,root,root) %{dstdir}/bin/keytool
%attr(755,root,root) %{jredir}/bin/orbd
%attr(755,root,root) %{dstdir}/bin/orbd
%attr(755,root,root) %{jredir}/bin/pack200
%attr(755,root,root) %{dstdir}/bin/pack200
%attr(755,root,root) %{jredir}/bin/rmid
%attr(755,root,root) %{dstdir}/bin/rmid
%attr(755,root,root) %{jredir}/bin/rmiregistry
%attr(755,root,root) %{dstdir}/bin/rmiregistry
%attr(755,root,root) %{jredir}/bin/servertool
%attr(755,root,root) %{dstdir}/bin/servertool
%attr(755,root,root) %{jredir}/bin/tnameserv
%attr(755,root,root) %{dstdir}/bin/tnameserv
%attr(755,root,root) %{jredir}/bin/unpack200
%attr(755,root,root) %{dstdir}/bin/unpack200
%dir %{jredir}/lib
%dir %{jredir}/lib/applet
%{jredir}/lib/cmm
%{jredir}/lib/ext
%dir %{jredir}/lib/%{jre_arch}
%ifnarch %{x8664} x32
%dir %{jredir}/lib/%{jre_arch}/client
%{jredir}/lib/%{jre_arch}/client/Xusage.txt
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/client/*.so
%endif
%dir %{jredir}/lib/%{jre_arch}/jli
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/jli/*.so
%{jredir}/lib/%{jre_arch}/jli/*.diz
%dir %{jredir}/lib/%{jre_arch}/server
%{jredir}/lib/%{jre_arch}/server/Xusage.txt
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/server/*.so
%{jredir}/lib/%{jre_arch}/server/*.diz
%{jredir}/lib/%{jre_arch}/jvm.cfg
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libattach.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libawt.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libawt_headless.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libdt_socket.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libhprof.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libinstrument.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libj2gss.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libj2pcsc.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libj2pkcs11.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjaas_unix.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjava.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjpeg.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/liblcms.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libsctp.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libsunec.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjava_crw_demo.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjawt.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjdwp.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjsdt.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjsig.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjsound.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjvm.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libmanagement.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libmlib_image.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libnet.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libnio.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libnpt.so
%ifnarch x32
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libsaproc.so
%endif
%{?with_sunec:%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libsunec.so}
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libunpack.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libverify.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libzip.so
%{jredir}/lib/%{jre_arch}/*.diz
%{jredir}/lib/images
%{jredir}/lib/management
%{jredir}/lib/security
%if %{with webstart}
%{jredir}/lib/about.jar
%{jredir}/lib/about.jnlp
%endif
%{jredir}/lib/calendars.properties
%{jredir}/lib/charsets.jar
%{jredir}/lib/classlist
%{jredir}/lib/content-types.properties
%{jredir}/lib/currency.data
%{jredir}/lib/flavormap.properties
%{jredir}/lib/hijrah-config-umalqura.properties
%{jredir}/lib/jce.jar
%attr(755, root, root) %{jredir}/lib/jexec
%{jredir}/lib/jsse.jar
%{jredir}/lib/jvm.hprof.txt
%{jredir}/lib/logging.properties
%{jredir}/lib/management-agent.jar
%{jredir}/lib/meta-index
%{jredir}/lib/net.properties
%{jredir}/lib/psfont.properties.ja
%{jredir}/lib/psfontj2d.properties
%{jredir}/lib/resources.jar
%{jredir}/lib/rt.jar
%{jredir}/lib/sound.properties
%{jredir}/lib/tzdb.dat
%{jredir}/lib/*.diz
%{jvmjardir}

%files jre-X11
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/policytool
%{_mandir}/man1/policytool.1*
%lang(ja) %{_mandir}/ja/man1/policytool.1*

%files jre-base-X11
%defattr(644,root,root,755)
%attr(755,root,root) %{jredir}/bin/policytool
%attr(755,root,root) %{dstdir}/bin/policytool
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libsplashscreen.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libawt_xawt.so
%attr(755,root,root) %{dstdir}/lib/%{jre_arch}/libjawt.so

%files jre-base-alsa
%defattr(644,root,root,755)
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjsoundalsa.so

%files jre-base-freetype
%defattr(644,root,root,755)
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libfontmanager.so

%if 0
%files jre-base-gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjavagtk.so
%endif

%files jar
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/jar
%{_mandir}/man1/jar.1*
%lang(ja) %{_mandir}/ja/man1/jar.1*

%files appletviewer
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/appletviewer
%{_mandir}/man1/appletviewer.1*
%lang(ja) %{_mandir}/ja/man1/appletviewer.1*

%files jdk-sources
%defattr(644,root,root,755)
%{_javasrcdir}/%{name}-jdk.zip

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
