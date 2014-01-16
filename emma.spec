%{?_javapackages_macros:%_javapackages_macros}
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
Release:        12.0%{?dist}
Epoch:          0
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
Requires:       jpackage-utils >= 0:1.7.5-1jpp.3


BuildArch:      noarch

%description
EMMA is an open-source toolkit for measuring and reporting Java
code coverage. EMMA distinguishes itself from other tools by going
after a unique feature combination: support for large-scale
enterprise software development while keeping individual developer's
work fast and iterative.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
%{summary}.

%prep
%setup -q
cp -p %{SOURCE3} .
cp -p %{SOURCE4} .

# Make sure we don't use this no-source jar
rm lib/internal/stamptool.jar

%patch0
%patch1
%patch2 -p1
%patch3 -b
%patch4 -b
%patch5 -b

%build
[ -z "$JAVA_HOME" ] && export JAVA_HOME=%{_jvmdir}/java
ant -Dbuild.compiler=modern build javadoc

%install

install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 dist/%{name}.jar \
               $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
install -m 644 dist/%{name}_ant.jar \
               $RPM_BUILD_ROOT%{_javadir}/%{name}_ant.jar

# poms
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 %{SOURCE1} \
    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom
install -pm 644 %{SOURCE2} \
    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}_ant.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar
%add_maven_depmap JPP-%{name}_ant.pom %{name}_ant.jar

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr out/javadocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%files
%doc cpl-v10.html
%{_javadir}/*
%{_mavenpomdir}/JPP-%{name}*
%{_mavendepmapfragdir}/%{name}

%files javadoc
%doc cpl-v10.html
%doc %{_javadocdir}/%{name}*

%changelog
* Wed Aug 07 2013 gil cattaneo <puntogil@libero.it> 0:2.0.5312-12
- fix rhbz#992213
- update ant references in emma_ant pom file (gId only)
- minor changes to adapt to current guideline

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.0.5312-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.0.5312-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.0.5312-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.0.5312-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.0.5312-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 26 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.0.5312-6
- Fix pom filenames (Resolves rhbz#655797)
- Make few tweaks according to new guidelines
- Make jar unversioned

* Mon Jul 12 2010 Andrew Overholt <overholt@redhat.com> 0:2.0.5312-5
- Ensure license is also in -javadoc package

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.0.5312-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.0.5312-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 10 2008 Andrew Overholt <overholt@redhat.com> 0:2.0.5312-2
- Add patch to fix 64-bit AIOOB.

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.0.5312-1
- drop repotag
- fix version, release to be sane

* Mon Jul 07 2008 Andrew Overholt <overholt@redhat.com> 2.0-0.5312.2jpp.4
- Remove requirement on maven2 as jpackage-utils now owns the maven POMs
  and fragments directories.

* Fri May 30 2008 Andrew Overholt <overholt@redhat.com> 2.0-0.5312.2jpp.3
- Bump release because I forgot to add a source file.

* Wed May 28 2008 Andrew Overholt <overholt@redhat.com> 2.0-0.5312.2jpp.2
- Review (rhbz#444511) fixes:  '-' in permissions, maven2 requirement,
  file ownership of maven stuff, require OpenJDK.

* Fri Apr 25 2008 Andrew Overholt <overholt@redhat.com> 0:2.0-0.5312.2jpp.1
- Fedora-ify (remove Vendor, Distribution, javadoc %%post{,un}, license
  -> "CPL", add 1.%%{?dist} to release, change groups to shut up rpmlint,
  remove %%section free).
- Remove gnu-crypto requirement for GCJ.
- Copy patch from Gentoo build for 1.5 API changes.
- Add hacks to avoid having to use no-source class during build.

* Fri Jul 06 2007 Ralph Apel <r.apel at r-apel.de> 0:2.0-0.5312.2jpp
- Make Vendor, Distribution based on macro
- Add -javadoc subpackage
- Add gcj_support option
- Add poms and depmap frags

* Wed Feb 01 2006 Ralph Apel <r.apel at r-apel.de> 0:2.0-0.5312.1jpp
- First JPackage release.
