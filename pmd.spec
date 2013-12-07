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

Summary:	Scans Java source code and looks for potential problems
Name:		pmd
Version:	4.2.1
Release:	2.0.9
License:	BSD Style
Group:		Development/Java
Url:		http://pmd.sourceforge.net/
## svn export https://pmd.svn.sourceforge.net/svnroot/pmd/tags/pmd/pmd_release_4_2_1 pmd && tar cvjf pmd-src.tar.bz2 pmd
#Source0:	%{name}-src.tar.bz2
Source0:	http://downloads.sourceforge.net/pmd/pmd-src-4.2.1.zip
Patch0:		%{name}-asm.patch
Patch1:		%{name}-4.2.1-no-retroweaver.patch
%if !%{gcj_support}
BuildArch:	noarch
BuildRequires:	java-devel
%else
BuildRequires:	java-gcj-compat-devel
%endif
BuildRequires:	java-rpmbuild >= 0:1.6
BuildRequires:	ant >= 0:1.6
BuildRequires:	ant-nodeps
BuildRequires:	javacc
BuildRequires:	junit4
BuildRequires:	jaxen >= 0:1.1
BuildRequires:	xerces-j2
BuildRequires:	xml-commons-jaxp-1.3-apis >= 1.3.02
BuildRequires:	jakarta-oro
BuildRequires:	asm2
BuildRequires:	locales-en
Requires:	jaxen >= 0:1.1
Requires:	xerces-j2
Requires:	xml-commons-jaxp-1.3-apis >= 1.3.02
Requires:	jakarta-oro

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
Summary:	Manual for %{name}
Group:		Development/Java

%description manual
Documentation for %{name}.

%package javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
# XXX:	uses internal junit4 API
rm -r regress/test/net/sourceforge/pmd/*
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

#rm src/net/sourceforge/pmd/ast/*

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
# jar
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 lib/%{name}-%{version}.jar \
  %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}.jar; \
   do ln -sf ${jar} ${jar/-%{version}/}; done)
install -d -m 755 %{buildroot}%{_datadir}/%{name}-%{version}/etc
cp -a etc/* %{buildroot}%{_datadir}/%{name}-%{version}/etc
%{__perl} -pi -e 's|/usr/local/bin|%{_bindir}|' %{buildroot}%{_datadir}/%{name}-%{version}/etc/*.rb
install -d -m 755 %{buildroot}%{_datadir}/%{name}-%{version}/rulesets
cp -a rulesets/* %{buildroot}%{_datadir}/%{name}-%{version}/rulesets

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -a docs/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

# manual
install -d -m 755 %{buildroot}%{_docdir}/%{name}-%{version}
cp -a LICENSE.txt %{buildroot}%{_docdir}/%{name}-%{version}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%doc LICENSE.txt
%{_javadir}/*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif
%dir %{_datadir}/%{name}-%{version}
%attr(-,root,root) %{_datadir}/%{name}-%{version}/*
#E:	pmd non-executable-script /usr/share/pmd-4.0/etc/fr_docs/copy_up.sh 0644
#E:	pmd wrong-script-interpreter /usr/share/pmd-4.0/etc/rule_summary.rb "/usr/local/bin/ruby"
#E:	pmd non-executable-script /usr/share/pmd-4.0/etc/rule_summary.rb 0644
#E:	pmd invalid-dependency /usr/local/bin/ruby

%files manual
%doc %{_docdir}/%{name}-%{version}

%files javadoc
%{_javadocdir}/*

