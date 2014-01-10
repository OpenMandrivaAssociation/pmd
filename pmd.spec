%{?_javapackages_macros:%_javapackages_macros}
# Copyright (c) 2000-2005, JPackage Project
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
Name:           pmd
Version:        5.0.5
Release:        1.0%{?dist}
Epoch:          0
Summary:        Scans Java source code and looks for potential problems
License:        BSD

BuildArch:      noarch

Source0:        http://downloads.sourceforge.net/project/pmd/pmd/%{version}/pmd-src-%{version}.zip
URL:            http://pmd.sourceforge.net/

# fix incorrect token replacement when building with javacc 5.0
# patch sent upstream: https://sourceforge.net/p/pmd/bugs/1109/
Patch0:         javacc.patch
# fix api incompatibilities with newer saxon
# not sent upstream
Patch1:         saxon.patch

BuildRequires:  jpackage-utils
BuildRequires:  java-devel
BuildRequires:  maven-local
BuildRequires:  maven-deploy-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-plugin-build-helper
BuildRequires:  ant-testutil
BuildRequires:  apache-commons-lang3
BuildRequires:  apache-commons-io
BuildRequires:  beust-jcommander
BuildRequires:  mockito
BuildRequires:  javacc
BuildRequires:  jaxen
BuildRequires:  saxon
BuildRequires:  objectweb-asm
Requires:       jpackage-utils
Requires:       java
Requires:       ant-testutil
Requires:       apache-commons-io
Requires:       beust-jcommander
Requires:       javacc
Requires:       jaxen
Requires:       saxon
Requires:       objectweb-asm

%description
PMD scans Java source code and looks for potential problems like:
* Possible bugs: empty try/catch/finally/switch statements
+ Dead code: unused local variables, parameters and private methods
+ Suboptimal code: wasteful String/StringBuffer usage
+ Overcomplicated expressions: unnecessary if statements, for loops
  that could be while loops
+ Duplicate code: copied/pasted code means copied/pasted bugs

PMD has plugins for JDeveloper, Eclipse, JEdit, JBuilder, BlueJ,
CodeGuide, NetBeans/Sun Java Studio Enterprise/Creator, IntelliJ IDEA,
TextPad, Maven, Ant, Gel, JCreator, and Emacs.

%package javadoc
Summary:        API documentation for %{name}

Requires:       objectweb-asm-javadoc

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n %{name}-src-%{version}

%patch0 -p0
%patch1 -p0

# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;
find . -name "*.class" -exec rm -f {} \;

%mvn_alias : pmd:pmd

%build
# some tests are failing so ignore them
# this may be because fedora has a newer rhino than pmd expects
%mvn_build -X -- -Dmaven.test.failure.ignore=true -Dmaven.clover.skip=true

%install
%mvn_install

%files -f .mfiles
%doc LICENSE.txt etc/changelog.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Tue Aug 13 2013 Alexander Kurtakov <akurtako@redhat.com> 0:5.0.5-1
- Update to latest upstream.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:5.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 01 2013 Mat Booth <fedora@matbooth.co.uk> - 0:5.0.4-2
- Add missing requires on ant and javacc

* Sun Jun 30 2013 Mat Booth <fedora@matbooth.co.uk> - 0:5.0.4-1
- Update to latest upstream version

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.2.5-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.2.5-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 22 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:4.2.5-13
- Use unversioned jars to prevent further build breakages
- Update to current guidelines

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.2.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 28 2011 Alexander Kurtakov <akurtako@redhat.com> 0:4.2.5-11
- Fix FTBFS.
- Current guidelines updates.

* Thu Feb 24 2011 Alexander Kurtakov <akurtako@redhat.com> 0:4.2.5-10
- Let it conform to new packaging guidelines.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.2.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 29 2010 Jerry James <loganjerry@gmail.com> - 0:4.2.5-8
- Fix maven ant dep (bz 643748).
- Add LICENSE.txt to -javadoc package.
- Remove BuildRoot tag.

* Tue Sep  7 2010 Jerry James <loganjerry@gmail.com> - 0:4.2.5-7
- Update junit4 dependency for junit 4.8.2.

* Wed Jun  2 2010 Jerry James <loganjerry@gmail.com> - 0:4.2.5-6
- Update objectweb-asm dependency for version 3.2.

* Fri Nov 20 2009 Jerry James <loganjerry@gmail.com> - 0:4.2.5-5
- Update junit4 dependency for junit 4.6.

* Wed Aug 19 2009 Andrew Overholt <overholt@redhat.com> 0:4.2.5-4
- Install POM file and depmap entry

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Jerry James <loganjerry@gmail.com> - 0:4.2.5-1
- Upgrade to 4.2.5

* Wed Jan 14 2009 Jerry James <loganjerry@gmail.com> - 0:4.2.4-1
- Upgrade to 4.2.4
- Drop unnecessary scripts/files in etc
- Add more documentation files
- Drop useless manual subpackage; it's really small, and contains files that
  should be docs for the main package

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:3.6-1.4
- fix license tag
- drop disttag

* Mon Mar 26 2007 Matt Wringe <mwringe@redhat.com> - 0:3.6-1jpp.3
- Fix unowned doc directory for pmd

* Mon Mar 19 2007 Matt Wringe <mwringe@redhat.com> - 0:3.6-1jpp.2
- Add missing jakarta-commons-oro build requires

* Tue Mar 13 2007 Jeff Johnston <jjohnstn@redhat.com> - 0:3.6-1jpp.1
- Updated per Fedora package review process
- Resolves: #227109

* Mon Jun 19 2006 Deepak Bhole <dbhole@redhat.com> - 0:3.6-1jpp
- Upgrade to 3.6

* Fri Mar 10 2006 Fernando Nasser <fnasser@redhat.com> - 0:3.3-2jpp
- First JPP 1.7 build

* Wed Nov 09 2005 Ralph Apel <r.apel at r-apel.de> - 0:3.3-1jpp
- Upgrade to 3.3
- Fix Groups

* Tue Feb 22 2005 Laurent Goujon <laurent at gobio2.net> - 2.3-1jpp
- Upgrade to 2.3
- Use bin/build.xml

* Mon Sep 13 2004 Ralph Apel <r.apel at r-apel.de> - 1.9-2jpp
- Drop saxpath requirements
- Require jaxen >= 0:1.1
- Relax some versioned requirements

* Wed Aug 25 2004 Fernando Nasser <fnasser@redhat.com> - 1.9-1jpp
- Upgrade to 1.9

* Tue Aug 24 2004 Fernando Nasser <fnasser@redhat.com> - 0:1.5-4jpp
- Rebuild with Ant 1.6.2

* Fri Aug 06 2004 Ralph Apel <r.apel at r-apel.de> - 1.5-3jpp
- Void change

* Tue Jun 01 2004 Randy Watler <rwatler at finali.com> - 1.5-2jpp
- Upgrade to Ant 1.6.X

* Wed Mar 24 2004 Ralph Apel <r.apel at r-apel.de> 1.5-1jpp
- first JPackage release
