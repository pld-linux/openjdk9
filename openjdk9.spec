%bcond_with	bootstrap	# build a bootstrap version, using icedtea6
%bcond_without	cacerts		# don't include the default CA certificates

%if %{with bootstrap}
%define		use_jdk	icedtea8
%else
%define		use_jdk	openjdk9
%endif

%ifarch %{x8664}
%define		with_aot	1
%endif

%ifarch x32
%define		with_zero	1
%endif

# class data version seen with file(1) that this jvm is able to load
%define		_classdataversion 53.0

%define	ver_u	9.0.4
%define	ver_b	12

# JDK/JRE version, as returned with `java -version`, '_' replaced with '.'
%define		_jdkversion %{ver_u}

Summary:	Open-source implementation of the Java Platform, Standard Edition
Summary(pl.UTF-8):	Wolnoźródłowa implementacja Java 9 SE
Name:		openjdk9
Version:	%{ver_u}.%{ver_b}
Release:	2
License:	GPL v2
Group:		Development/Languages/Java
Source0:	https://hg.openjdk.java.net/jdk-updates/jdk9u/archive/jdk-%{ver_u}+%{ver_b}.tar.bz2?/%{name}-%{version}.tar.bz2
# Source0-md5:	f71280d31603efeffdadea56fab8436e
Source1:	https://hg.openjdk.java.net/jdk-updates/jdk9u/corba/archive/jdk-%{ver_u}+%{ver_b}.tar.bz2?/%{name}-corba-%{version}.tar.bz2
# Source1-md5:	2bc0a490f71eaa17fcae9387b354ccfd
Source2:	https://hg.openjdk.java.net/jdk-updates/jdk9u/hotspot/archive/jdk-%{ver_u}+%{ver_b}.tar.bz2?/%{name}-hotspot-%{version}.tar.bz2
# Source2-md5:	37ff0144a673417c793d282d12aba6a1
Source3:	https://hg.openjdk.java.net/jdk-updates/jdk9u/jaxp/archive/jdk-%{ver_u}+%{ver_b}.tar.bz2?/%{name}-jaxp-%{version}.tar.bz2
# Source3-md5:	c6c4ee8ef80f10fc4fbc9d151436c89a
Source4:	https://hg.openjdk.java.net/jdk-updates/jdk9u/jaxws/archive/jdk-%{ver_u}+%{ver_b}.tar.bz2?/%{name}-jaxws-%{version}.tar.bz2
# Source4-md5:	3cf0375c3bba7d028c8408e41bbbb352
Source5:	https://hg.openjdk.java.net/jdk-updates/jdk9u/jdk/archive/jdk-%{ver_u}+%{ver_b}.tar.bz2?/%{name}-jdk-%{version}.tar.bz2
# Source5-md5:	74d33ad39f5b67596c5269585811cfab
Source6:	https://hg.openjdk.java.net/jdk-updates/jdk9u/langtools/archive/jdk-%{ver_u}+%{ver_b}.tar.bz2?/%{name}-langtools-%{version}.tar.bz2
# Source6-md5:	95d7011a050602218b5400c632339e2c
Source7:	https://hg.openjdk.java.net/jdk-updates/jdk9u/nashorn/archive/jdk-%{ver_u}+%{ver_b}.tar.bz2?/%{name}-nashorn-%{version}.tar.bz2
# Source7-md5:	5fbaceceb82449806263ba99188b7139
Source10:	make-cacerts.sh
Patch0:		libpath.patch
Patch1:		make-4.3.patch
Patch2:		x32.patch
Patch3:		aarch64.patch
Patch4:		default-assumemp.patch
URL:		http://openjdk.java.net/
BuildRequires:	/usr/bin/jar
BuildRequires:	alsa-lib-devel
BuildRequires:	ant
BuildRequires:	autoconf
BuildRequires:	bash
%{?with_cacerts:BuildRequires:	ca-certificates-update}
BuildRequires:	cups-devel
BuildRequires:	elfutils-devel
BuildRequires:	freetype-devel >= 2.3
BuildRequires:	gawk
BuildRequires:	giflib-devel >= 5.1
BuildRequires:	glibc-misc
%{?buildrequires_jdk}
BuildRequires:	lcms2-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	lsb-release
BuildRequires:	pcsc-lite-devel
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
Obsoletes:	java-gcj-compat
Obsoletes:	java-gcj-compat-devel
Obsoletes:	java-sun
Obsoletes:	java-sun-demos
Obsoletes:	java-sun-jre
Obsoletes:	java-sun-jre-X11
Obsoletes:	java-sun-jre-alsa
Obsoletes:	java-sun-jre-jdbc
Obsoletes:	java-sun-tools
Obsoletes:	java5-sun
Obsoletes:	java5-sun-jre
Obsoletes:	java5-sun-jre-X11
Obsoletes:	java5-sun-jre-jdbc
Obsoletes:	java5-sun-tools
Obsoletes:	oracle-java7
Obsoletes:	oracle-java7-jre
Obsoletes:	oracle-java7-jre-X11
Obsoletes:	oracle-java7-jre-alsa
Obsoletes:	oracle-java7-jre-jdbc
Obsoletes:	oracle-java7-tools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dstreldir	%{name}-%{version}
%define		dstdir		%{_jvmdir}/%{dstreldir}
%define		jvmjardir	%{_jvmjardir}/%{name}-%{version}

# to break artificial subpackage dependency loops
%define		_noautoreq	'libmawt.so' java\\\\(ClassDataVersion\\\\)

# openjdk build system handles _FORTIFY_SOURCE internally
%undefine	_fortify_cflags

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
Obsoletes:	jdk
Obsoletes:	kaffe
Obsoletes:	oracle-java7

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
Requires:	jpackage-utils >= 0:1.7.5-8
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
Obsoletes:	icedtea8-jre
Obsoletes:	jaas
Obsoletes:	jaf
Obsoletes:	java5-sun-jre
Obsoletes:	java-gcj-compat
Obsoletes:	java-jaxp
Obsoletes:	java-jdbc-stdext
Obsoletes:	java-sun-jre
Obsoletes:	jce
Obsoletes:	jdbc-stdext
Obsoletes:	jmx
Obsoletes:	jndi
Obsoletes:	jre
Obsoletes:	jsse
Obsoletes:	oracle-java7-jre

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
Requires:	jpackage-utils >= 0:1.7.5-8
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
BuildArch:	noarch

%description jdk-sources
Source code for the OpenJDK development kit and Java standard library.

%description jdk-sources -l pl.UTF-8
Kod źródłowy narzędzi programistycznych OpenJDK oraz standardowej
biblioteki Javy.

%package examples
Summary:	OpenJDK - examples
Summary(pl.UTF-8):	OpenJDK - przykłady
Group:		Documentation
BuildArch:	noarch

%description examples
Code examples for OpenJDK.

%description examples -l pl.UTF-8
Przykłady dla OpenJDK.

%prep
%setup -qn jdk9u-jdk-%{ver_u}+%{ver_b} -a1 -a2 -a3 -a4 -a5 -a6 -a7

for d in *-jdk-%{ver_u}+%{ver_b}* ; do
	mv "$d" "${d%%-jdk-%{ver_u}+%{ver_b}}"
done

%patch0 -p1
%patch1 -p1
%patch2 -p1
%ifarch aarch64
%patch3 -p1
%endif
%patch4 -p1

%build
# Make sure we have /proc mounted - otherwise idlc will fail later.
if [ ! -f /proc/self/stat ]; then
	echo "You need to have /proc mounted in order to build this package!"
	exit 1
fi

cd common/autoconf
rm generated-configure.sh
%{__autoconf} -o generated-configure.sh
cd ../..

mkdir -p build-bin

# unset CLASSPATH to be safe, gnustep puts garbage there, which openjdk hates
unset CLASSPATH

export SHELL=/bin/bash

chmod a+x configure

# disable-debug-symbols so openjdk debuginfo handling won't conflict with ours
%configure \
	%{?with_zero:--with-jvm-variants=zero} \
	--with-boot-jdk="%{java_home}" \
	--with-extra-cflags="%{rpmcppflags} %{rpmcflags} -fcommon -fno-tree-dse" \
	--with-extra-cxxflags="%{rpmcppflags} %{rpmcxxflags} -fcommon -fno-tree-dse" \
	--with-extra-ldflags="%{rpmldflags}" \
	--with-native-debug-symbols=none \
	--disable-full-docs \
	--disable-javac-server \
	--disable-hotspot-gtest \
	--disable-warnings-as-errors \
	--with-jobs="%{__jobs}" \
	--with-giflib=system \
	--with-libjpeg=system \
	--with-libpng=system \
	--with-lcms=system \
	--with-zlib=system \
	--with-version-pre="" \
	--with-version-opt="" \
	--with-version-build="%{release}"

specdir="$(dirname build/*-release/spec.gmk)"
cat > $specdir/custom-spec.gmk <<EOF
# OpenJDK build system depends on bash
SHELL=/bin/bash
EOF
[ -L tmp-bin ] || ln -s "$specdir/jdk/bin" tmp-bin

%{__make} -j1 all \
	LOG=debug \
	# these are normally set when --disable-debug-symbols is not used \
	LIBMANAGEMENT_OPTIMIZATION=LOW \
	LIBHPROF_OPTIMIZATION=LOW \
	LIBVERIFY_OPTIMIZATION=LOW

# smoke test
tmp-bin/java -version

export PATH="$(pwd)/build-bin:$PATH"
%{?with_cacerts:%{__sh} %{SOURCE10}}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{dstdir},%{_mandir}/ja} \
	$RPM_BUILD_ROOT{%{jvmjardir},%{_examplesdir}/%{name}-%{version},%{_javasrcdir}} \
	$RPM_BUILD_ROOT%{_sysconfdir}/%{name}

# install the 'JDK image', it contains the JRE too
cp -a build/*-release/images/jdk/* $RPM_BUILD_ROOT%{dstdir}

find $RPM_BUILD_ROOT%{dstdir} -name '*.diz' -delete

# convenience symlinks without version number
ln -s %{dstreldir} $RPM_BUILD_ROOT%{_jvmdir}/%{name}
ln -s %{dstreldir} $RPM_BUILD_ROOT%{_jvmdir}/%{name}-jre

ln -s %{dstreldir} $RPM_BUILD_ROOT%{_jvmdir}/java

# move JDK sources and demo to %{_prefix}/src
mv $RPM_BUILD_ROOT%{dstdir}/demo $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
mv $RPM_BUILD_ROOT%{dstdir}/lib/src.zip $RPM_BUILD_ROOT%{_javasrcdir}/%{name}-jdk.zip

# move manual pages to its place
mv $RPM_BUILD_ROOT%{dstdir}/man/ja_JP.UTF-8/man1 $RPM_BUILD_ROOT%{_mandir}/ja/man1
rmdir $RPM_BUILD_ROOT%{dstdir}/man/ja_JP.UTF-8
rm $RPM_BUILD_ROOT%{dstdir}/man/ja
mv $RPM_BUILD_ROOT%{dstdir}/man/man1 $RPM_BUILD_ROOT%{_mandir}/man1
rmdir $RPM_BUILD_ROOT%{dstdir}/man

# replace duplicates with symlinks, link to %{_bindir}
for path in $RPM_BUILD_ROOT%{dstdir}/bin/*; do
	filename=$(basename $path)
        ln -sf "%{dstdir}/bin/$filename" $RPM_BUILD_ROOT%{_bindir}
done

# keep configuration in %{_sysconfdir} (not all *.properties go there)
for config in management security \
		logging.properties net.properties sound.properties; do

	mv $RPM_BUILD_ROOT%{dstdir}/conf/$config $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/$config
	ln -s %{_sysconfdir}/%{name}/$config $RPM_BUILD_ROOT%{dstdir}/conf/$config
done

%{?with_cacerts:install cacerts $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/security}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)

%files jdk
%defattr(644,root,root,755)
%{?with_aot:%attr(755,root,root) %{_bindir}/jaotc}
%attr(755,root,root) %{_bindir}/jarsigner
%attr(755,root,root) %{_bindir}/javac
%attr(755,root,root) %{_bindir}/javadoc
%attr(755,root,root) %{_bindir}/javah
%attr(755,root,root) %{_bindir}/javap
%attr(755,root,root) %{_bindir}/jcmd
%attr(755,root,root) %{_bindir}/jconsole
%attr(755,root,root) %{_bindir}/jdb
%attr(755,root,root) %{_bindir}/jdeprscan
%attr(755,root,root) %{_bindir}/jdeps
%{!?with_zero:%attr(755,root,root) %{_bindir}/jhsdb}
%attr(755,root,root) %{_bindir}/jimage
%attr(755,root,root) %{_bindir}/jinfo
%attr(755,root,root) %{_bindir}/jlink
%attr(755,root,root) %{_bindir}/jmap
%attr(755,root,root) %{_bindir}/jmod
%attr(755,root,root) %{_bindir}/jps
%attr(755,root,root) %{_bindir}/jshell
%attr(755,root,root) %{_bindir}/jstack
%attr(755,root,root) %{_bindir}/jstat
%attr(755,root,root) %{_bindir}/jstatd
%attr(755,root,root) %{_bindir}/rmic
%attr(755,root,root) %{_bindir}/schemagen
%attr(755,root,root) %{_bindir}/serialver
%attr(755,root,root) %{_bindir}/wsgen
%attr(755,root,root) %{_bindir}/wsimport
%attr(755,root,root) %{_bindir}/xjc
%{_jvmdir}/java
%{_mandir}/man1/jarsigner.1*
%{_mandir}/man1/javac.1*
%{_mandir}/man1/javadoc.1*
%{_mandir}/man1/javah.1*
%{_mandir}/man1/javap.1*
%{_mandir}/man1/jcmd.1*
%{_mandir}/man1/jconsole.1*
%{_mandir}/man1/jdb.1*
%{_mandir}/man1/jdeps.1*
%{_mandir}/man1/jinfo.1*
%{_mandir}/man1/jmap.1*
%{_mandir}/man1/jps.1*
%{_mandir}/man1/jstack.1*
%{_mandir}/man1/jstat.1*
%{_mandir}/man1/jstatd.1*
%{_mandir}/man1/schemagen.1*
%{_mandir}/man1/serialver.1*
%{_mandir}/man1/rmic.1*
%{_mandir}/man1/wsgen.1*
%{_mandir}/man1/wsimport.1*
%{_mandir}/man1/xjc.1*
%lang(ja) %{_mandir}/ja/man1/jarsigner.1*
%lang(ja) %{_mandir}/ja/man1/javac.1*
%lang(ja) %{_mandir}/ja/man1/javadoc.1*
%lang(ja) %{_mandir}/ja/man1/javah.1*
%lang(ja) %{_mandir}/ja/man1/javap.1*
%lang(ja) %{_mandir}/ja/man1/jcmd.1*
%lang(ja) %{_mandir}/ja/man1/jconsole.1*
%lang(ja) %{_mandir}/ja/man1/jdb.1*
%lang(ja) %{_mandir}/ja/man1/jdeps.1*
%lang(ja) %{_mandir}/ja/man1/jinfo.1*
%lang(ja) %{_mandir}/ja/man1/jmap.1*
%lang(ja) %{_mandir}/ja/man1/jps.1*
%lang(ja) %{_mandir}/ja/man1/jstack.1*
%lang(ja) %{_mandir}/ja/man1/jstat.1*
%lang(ja) %{_mandir}/ja/man1/jstatd.1*
%lang(ja) %{_mandir}/ja/man1/schemagen.1*
%lang(ja) %{_mandir}/ja/man1/serialver.1*
%lang(ja) %{_mandir}/ja/man1/rmic.1*
%lang(ja) %{_mandir}/ja/man1/wsgen.1*
%lang(ja) %{_mandir}/ja/man1/wsimport.1*
%lang(ja) %{_mandir}/ja/man1/xjc.1*

%files jdk-base
%defattr(644,root,root,755)
%dir %{dstdir}
%{_jvmdir}/%{name}
%attr(755,root,root) %{dstdir}/bin/appletviewer
%{?with_aot:%attr(755,root,root) %{dstdir}/bin/jaotc}
%attr(755,root,root) %{dstdir}/bin/jar
%attr(755,root,root) %{dstdir}/bin/jarsigner
%attr(755,root,root) %{dstdir}/bin/javac
%attr(755,root,root) %{dstdir}/bin/javadoc
%attr(755,root,root) %{dstdir}/bin/javah
%attr(755,root,root) %{dstdir}/bin/javap
%attr(755,root,root) %{dstdir}/bin/jconsole
%attr(755,root,root) %{dstdir}/bin/jcmd
%attr(755,root,root) %{dstdir}/bin/jdb
%attr(755,root,root) %{dstdir}/bin/jdeprscan
%attr(755,root,root) %{dstdir}/bin/jdeps
%{!?with_zero:%attr(755,root,root) %{dstdir}/bin/jhsdb}
%attr(755,root,root) %{dstdir}/bin/jimage
%attr(755,root,root) %{dstdir}/bin/jinfo
%attr(755,root,root) %{dstdir}/bin/jlink
%attr(755,root,root) %{dstdir}/bin/jmap
%attr(755,root,root) %{dstdir}/bin/jmod
%attr(755,root,root) %{dstdir}/bin/jps
%attr(755,root,root) %{dstdir}/bin/jshell
%attr(755,root,root) %{dstdir}/bin/jstack
%attr(755,root,root) %{dstdir}/bin/jstat
%attr(755,root,root) %{dstdir}/bin/jstatd
%attr(755,root,root) %{dstdir}/bin/rmic
%attr(755,root,root) %{dstdir}/bin/schemagen
%attr(755,root,root) %{dstdir}/bin/serialver
%attr(755,root,root) %{dstdir}/bin/wsgen
%attr(755,root,root) %{dstdir}/bin/wsimport
%attr(755,root,root) %{dstdir}/bin/xjc
%{dstdir}/include
%{dstdir}/jmods
%{?with_aot:%attr(755,root,root) %{dstdir}/lib/libjelfshim.so}
%{dstdir}/lib/ct.sym

%files jre
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/idlj
%attr(755,root,root) %{_bindir}/java
%attr(755,root,root) %{_bindir}/jjs
%attr(755,root,root) %{_bindir}/jrunscript
%attr(755,root,root) %{_bindir}/keytool
%attr(755,root,root) %{_bindir}/orbd
%attr(755,root,root) %{_bindir}/pack200
%attr(755,root,root) %{_bindir}/rmid
%attr(755,root,root) %{_bindir}/rmiregistry
%attr(755,root,root) %{_bindir}/servertool
%attr(755,root,root) %{_bindir}/tnameserv
%attr(755,root,root) %{_bindir}/unpack200
%{_mandir}/man1/idlj.1*
%{_mandir}/man1/java.1*
%{_mandir}/man1/jjs.1*
%{_mandir}/man1/jrunscript.1*
%{_mandir}/man1/keytool.1*
%{_mandir}/man1/orbd.1*
%{_mandir}/man1/pack200.1*
%{_mandir}/man1/rmid.1*
%{_mandir}/man1/rmiregistry.1*
%{_mandir}/man1/servertool.1*
%{_mandir}/man1/tnameserv.1*
%{_mandir}/man1/unpack200.1*
%lang(ja) %{_mandir}/ja/man1/idlj.1*
%lang(ja) %{_mandir}/ja/man1/java.1*
%lang(ja) %{_mandir}/ja/man1/jjs.1*
%lang(ja) %{_mandir}/ja/man1/jrunscript.1*
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
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*
%dir %{dstdir}
%{dstdir}/release
%{_jvmdir}/%{name}-jre
%dir %{dstdir}/bin
%attr(755,root,root) %{dstdir}/bin/idlj
%attr(755,root,root) %{dstdir}/bin/java
%attr(755,root,root) %{dstdir}/bin/jjs
%attr(755,root,root) %{dstdir}/bin/jrunscript
%attr(755,root,root) %{dstdir}/bin/keytool
%attr(755,root,root) %{dstdir}/bin/orbd
%attr(755,root,root) %{dstdir}/bin/pack200
%attr(755,root,root) %{dstdir}/bin/rmid
%attr(755,root,root) %{dstdir}/bin/rmiregistry
%attr(755,root,root) %{dstdir}/bin/servertool
%attr(755,root,root) %{dstdir}/bin/tnameserv
%attr(755,root,root) %{dstdir}/bin/unpack200
%{dstdir}/conf
%{dstdir}/legal
%dir %{dstdir}/lib
%dir %{dstdir}/lib/jli
%attr(755,root,root) %{dstdir}/lib/jli/libjli.so
%{dstdir}/lib/security
%dir %{dstdir}/lib/server
%attr(755,root,root) %{dstdir}/lib/server/*.so
%{dstdir}/lib/server/Xusage.txt
%{!?with_zero:%{dstdir}/lib/classlist}
%{dstdir}/lib/jrt-fs.jar
%{dstdir}/lib/jvm.cfg
%attr(755,root,root) %{dstdir}/lib/libattach.so
%attr(755,root,root) %{dstdir}/lib/libawt.so
%attr(755,root,root) %{dstdir}/lib/libawt_headless.so
%attr(755,root,root) %{dstdir}/lib/libdt_socket.so
%attr(755,root,root) %{dstdir}/lib/libinstrument.so
%attr(755,root,root) %{dstdir}/lib/libj2gss.so
%attr(755,root,root) %{dstdir}/lib/libj2pcsc.so
%attr(755,root,root) %{dstdir}/lib/libj2pkcs11.so
%attr(755,root,root) %{dstdir}/lib/libjaas_unix.so
%attr(755,root,root) %{dstdir}/lib/libjava.so
%attr(755,root,root) %{dstdir}/lib/libjimage.so
%attr(755,root,root) %{dstdir}/lib/liblcms.so
%attr(755,root,root) %{dstdir}/lib/libmanagement_agent.so
%attr(755,root,root) %{dstdir}/lib/libmanagement_ext.so
%attr(755,root,root) %{dstdir}/lib/libprefs.so
%attr(755,root,root) %{dstdir}/lib/librmi.so
%attr(755,root,root) %{dstdir}/lib/libsctp.so
%attr(755,root,root) %{dstdir}/lib/libsunec.so
%attr(755,root,root) %{dstdir}/lib/libjavajpeg.so
%attr(755,root,root) %{dstdir}/lib/libjdwp.so
%attr(755,root,root) %{dstdir}/lib/libjsig.so
%attr(755,root,root) %{dstdir}/lib/libjsound.so
%attr(755,root,root) %{dstdir}/lib/libmanagement.so
%attr(755,root,root) %{dstdir}/lib/libmlib_image.so
%attr(755,root,root) %{dstdir}/lib/libnet.so
%attr(755,root,root) %{dstdir}/lib/libnio.so
%{!?with_zero:%attr(755,root,root) %{dstdir}/lib/libsaproc.so}
%{?with_sunec:%attr(755,root,root) %{dstdir}/lib/libsunec.so}
%attr(755,root,root) %{dstdir}/lib/libunpack.so
%attr(755,root,root) %{dstdir}/lib/libverify.so
%attr(755,root,root) %{dstdir}/lib/libzip.so
%attr(755,root,root) %{dstdir}/lib/jexec
%{dstdir}/lib/modules
%{dstdir}/lib/psfont.properties.ja
%{dstdir}/lib/psfontj2d.properties
%{dstdir}/lib/tzdb.dat
%{jvmjardir}

%files jre-X11
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/policytool
%{_mandir}/man1/policytool.1*
%lang(ja) %{_mandir}/ja/man1/policytool.1*

%files jre-base-X11
%defattr(644,root,root,755)
%attr(755,root,root) %{dstdir}/bin/policytool
%attr(755,root,root) %{dstdir}/lib/libsplashscreen.so
%attr(755,root,root) %{dstdir}/lib/libawt_xawt.so
%attr(755,root,root) %{dstdir}/lib/libjawt.so

%files jre-base-alsa
%defattr(644,root,root,755)
%attr(755,root,root) %{dstdir}/lib/libjsoundalsa.so

%files jre-base-freetype
%defattr(644,root,root,755)
%attr(755,root,root) %{dstdir}/lib/libfontmanager.so

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
