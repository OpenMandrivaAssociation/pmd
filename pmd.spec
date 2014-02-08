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

%define gcj_support 1

Name:           pmd
Version:        4.2.1
Release:        2.0.7
Epoch:          0
Summary:        Scans Java source code and looks for potential problems
License:        BSD Style
URL:            http://pmd.sourceforge.net/
## svn export https://pmd.svn.sourceforge.net/svnroot/pmd/tags/pmd/pmd_release_4_2_1 pmd && tar cvjf pmd-src.tar.bz2 pmd
#Source0:        %{name}-src.tar.bz2
Source0:        http://downloads.sourceforge.net/pmd/pmd-src-4.2.1.zip
Patch0:         %{name}-asm.patch
Patch1:         %{name}-4.2.1-no-retroweaver.patch
BuildRequires:  java-rpmbuild >= 0:1.6
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-nodeps
BuildRequires:  javacc
BuildRequires:  junit4
BuildRequires:  jaxen >= 0:1.1
BuildRequires:  xerces-j2
BuildRequires:  xml-commons-jaxp-1.3-apis >= 1.3.02
BuildRequires:  jakarta-oro
BuildRequires:  asm2
BuildRequires:  locales-en
Requires:       jaxen >= 0:1.1
Requires:       xerces-j2
Requires:       xml-commons-jaxp-1.3-apis >= 1.3.02
Requires:       jakarta-oro
Group:          Development/Java
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
BuildRequires:  java-devel
%endif

%description
PMD scans Java source code and looks for potential 
problems like:
+ Unused local variables 
+ Empty catch blocks 
+ Unused parameters 
+ Empty 'if' statements 
+ Duplicate import statements 
+ Unused private methods 
+ Classes which could be Singletons 
+ Short/long variable and method names 
PMD has plugins for JDeveloper, JEdit, JBuilder, 
NetBeans/Sun ONE Studio, IntelliJ IDEA, TextPad, 
Maven, Ant, Eclipse, Gel, and Emacs. 

%package manual
Summary:        Manual for %{name}
Group:          Development/Java

%description manual
Documentation for %{name}.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
# XXX: uses internal junit4 API
%{__rm} -r regress/test/net/sourceforge/pmd/*
##%{_bindir}/find . -type d -name "*.svn" | %{_bindir}/xargs -t %{__rm} -r
%{__perl} -pi -e 's/\r\n$/\n/g' src/net/sourceforge/pmd/dcd/graph/UsageGraphBuilder.java
%patch0 -p1
%patch1 -p1
%{__perl} -pi -e 's/<javac( |$)/<javac nowarn="true" /g' bin/build.xml
%{__perl} -pi -e 's/JavaCharStream\.java/CharStream.java/g' bin/build.xml

# set right permissions
%{_bindir}/find . -name "*.sh" | %{_bindir}/xargs -t %{__chmod} 755
# remove all binary libs
%{_bindir}/find . -name "*.jar" | %{_bindir}/xargs -t %{__rm}

#%{__rm} src/net/sourceforge/pmd/ast/*

%build
export LC_ALL=ISO-8859-1
export OPT_JAR_LIST="ant/ant-nodeps"
export CLASSPATH=$(%{_bindir}/build-classpath \
javacc \
jaxen \
oro \
junit4 \
xerces-j2 \
xml-commons-jaxp-1.3-apis \
asm2 )
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
cd bin
%{ant} -Dbuild.sysclasspath=only -Djavacc-home.path=%{_javadir} jjtree jspjjtree cppjavacc jar javadoc

%install
rm -rf $RPM_BUILD_ROOT

# jar
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 lib/%{name}-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; \
   do ln -sf ${jar} ${jar/-%{version}/}; done)
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/etc
cp -a etc/* $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/etc
%{__perl} -pi -e 's|/usr/local/bin|%{_bindir}|' $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/etc/*.rb
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/rulesets
cp -a rulesets/* $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/rulesets

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# manual
install -d -m 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -a LICENSE.txt $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt
%{_javadir}/*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif
%dir %{_datadir}/%{name}-%{version}
%attr(-,root,root) %{_datadir}/%{name}-%{version}/*
#E: pmd non-executable-script /usr/share/pmd-4.0/etc/fr_docs/copy_up.sh 0644
#E: pmd wrong-script-interpreter /usr/share/pmd-4.0/etc/rule_summary.rb "/usr/local/bin/ruby"
#E: pmd non-executable-script /usr/share/pmd-4.0/etc/rule_summary.rb 0644
#E: pmd invalid-dependency /usr/local/bin/ruby

%files manual
%defattr(0644,root,root,0755)
%doc %{_docdir}/%{name}-%{version}

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/*


%changelog
* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0:4.2.1-2.0.5mdv2011.0
+ Revision: 607185
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:4.2.1-2.0.4mdv2010.1
+ Revision: 523691
- rebuilt for 2010.1

* Mon Oct 05 2009 Funda Wang <fwang@mandriva.org> 0:4.2.1-2.0.3mdv2010.0
+ Revision: 453746
- rebuild

  + Christophe Fergeau <cfergeau@mandriva.com>
    - rebuild

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 0:4.2.1-2.0.1mdv2009.0
+ Revision: 265471
- rebuild early 2009.0 package (before pixel changes)

* Mon Apr 21 2008 David Walluck <walluck@mandriva.org> 0:4.2.1-0.0.1mdv2009.0
+ Revision: 196032
- 4.2.1

* Fri Jan 25 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:4.0-0.0.4mdv2008.1
+ Revision: 157960
- fix build - BR asm2

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

  + Anssi Hannula <anssi@mandriva.org>
    - buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:4.0-0.0.2mdv2008.0
+ Revision: 87336
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Wed Jul 25 2007 David Walluck <walluck@mandriva.org> 0:4.0-0.0.1mdv2008.0
+ Revision: 55248
- 4.0

* Wed Jul 18 2007 Anssi Hannula <anssi@mandriva.org> 0:3.6-1.3.2mdv2008.0
+ Revision: 53204
- use xml-commons-jaxp-1.3-apis explicitely instead of the generic
  xml-commons-apis which is provided by multiple packages (see bug #31473)

* Wed Jul 04 2007 David Walluck <walluck@mandriva.org> 0:3.6-1.3.1mdv2008.0
+ Revision: 47972
- Import pmd



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

* Wed Aug 24 2004 Fernando Nasser <fnasser@redhat.com> - 0:1.5-4jpp
- Rebuild with Ant 1.6.2

* Fri Aug 06 2004 Ralph Apel <r.apel at r-apel.de> - 1.5-3jpp
- Void change

* Tue Jun 01 2004 Randy Watler <rwatler at finali.com> - 1.5-2jpp
- Upgrade to Ant 1.6.X

* Wed Mar 24 2004 Ralph Apel <r.apel at r-apel.de> 1.5-1jpp
- first JPackage release
