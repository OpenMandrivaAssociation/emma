# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%global shortver 2.0

Summary:        Code Coverage Tool
Name:           emma
Version:        %{shortver}.5312
Release:        9
Group:          Development/Java
License:        CPL
URL:            http://emma.sourceforge.net/
Source0:        http://downloads.sourceforge.net/emma/%{name}-%{version}-src.zip
Source1:        emma-2.0.5312.pom
Source2:        emma_ant-2.0.5312.pom
# These are hacks until we get the source for the timestamping class
# http://sourceforge.net/tracker/index.php?func=detail&aid=1953619&group_id=108932&atid=651900
Source3:        emma-timestamp.sh
Source4:        emma-timestamp2.sh

Patch0:         emma-2.0.5312-dependencies_xml.patch
Patch1:         emma-2.0.5312-build_xml.patch
# Taken from Gentoo package to allow us to build on a JDK > 1.4
Patch2:         emma-2.0.5312-java15api.patch
# From eclemma's emmapatch directory
Patch3:         %{name}-eclemma.patch
# This is a hack until we get the source for the timestamping class
# http://sourceforge.net/tracker/index.php?func=detail&aid=1953619&group_id=108932&atid=651900
Patch4:         %{name}-timestamp.patch
# This patch fixes ArrayIndexOutOfBoundExceptions on 64-bit.  I modified
# the patch against HEAD to apply to this version -- overholt
# http://sourceforge.net/tracker/index.php?func=detail&aid=2119913&group_id=108932&atid=651897
Patch5:         %{name}-%{version}-64_bit_fix.patch
Requires:       java >= 0:1.4.2
Requires:       jaxp_parser_impl
BuildRequires:  ant >= 0:1.6.5
BuildRequires:  java-devel >= 0:1.6
BuildRequires:  jpackage-utils >= 0:1.7.5-1jpp.3
# For the timestamp hack (see above)
BuildRequires:  bc
Requires(post):    jpackage-utils >= 0:1.7.5-1jpp.3
Requires(postun):  jpackage-utils >= 0:1.7.5-1jpp.3

BuildArch:      noarch

%description
EMMA is an open-source toolkit for measuring and reporting Java
code coverage. EMMA distinguishes itself from other tools by going
after a unique feature combination: support for large-scale
enterprise software development while keeping individual developer's
work fast and iterative.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
Requires:       jpackage-utils

%description javadoc
%{summary}.

%prep
%setup -q
cp -p %{SOURCE3} .
cp -p %{SOURCE4} .

# Make sure we don't use this no-source jar
rm lib/internal/stamptool.jar

%patch0 -p0 -b .orig
%patch1 -p0 -b .orig
%patch2 -p1 -b .orig
%patch3 -p0 -b .orig
%patch4 -p0 -b .orig
%patch5 -p0 -b .orig

%build
[ -z "$JAVA_HOME" ] && export JAVA_HOME=%{_jvmdir}/java
ant -Dbuild.compiler=modern build javadoc

%install
rm -rf $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 dist/%{name}.jar \
               $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
install -m 644 dist/%{name}_ant.jar \
               $RPM_BUILD_ROOT%{_javadir}/%{name}_ant.jar
%add_to_maven_depmap emma emma %{version} JPP %{name}
%add_to_maven_depmap emma emma_ant %{version} JPP %{name}_ant


# poms
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 %{SOURCE1} \
    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom
install -pm 644 %{SOURCE2} \
    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}_ant.pom

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr out/javadocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%doc cpl-v10.html
%{_javadir}/*
%{_mavenpomdir}/JPP-%{name}*
%{_mavendepmapfragdir}/%{name}

%files javadoc
%doc cpl-v10.html
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}*

