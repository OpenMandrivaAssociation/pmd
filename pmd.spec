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
Version:        3.6
Release:        %mkrel 1.3.1
Epoch:          0
Summary:        Scans Java source code and looks for potential problems
License:        BSD Style

# cvs -z3 -d:pserver:anonymous@pmd.cvs.sourceforge.net:/cvsroot/pmd export \
# -r pmd_release_3_6 pmd
# tar -czvf pmd-src.tar.gz pmd
Source0:        %{name}-src.tar.gz
Url:            http://pmd.sourceforge.net/

BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-junit
BuildRequires:  junit
BuildRequires:  jaxen >= 0:1.1
BuildRequires:  xerces-j2
BuildRequires:  xml-commons-apis >= 1.3.02
BuildRequires:  jakarta-oro
Requires:       jaxen >= 0:1.1
Requires:       xerces-j2
Requires:       xml-commons-apis >= 1.3.02
Requires:       jakarta-oro
Group:          Development/Java
%if %{gcj_support}
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
BuildRequires:  java-devel
%endif
Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}-root

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
%setup -q -n %{name}

# set right permissions
find . -name "*.sh" -exec chmod 755 \{\} \;
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;

%build
export OPT_JAR_LIST="ant/ant-junit junit"
export CLASSPATH=$(build-classpath \
jaxen \
oro \
xerces-j2 \
xml-commons-apis)
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
cd bin
%{ant} -Dbuild.sysclasspath=only dist javadoc

%install
rm -rf $RPM_BUILD_ROOT

# jar
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 lib/%{name}-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; \
   do ln -sf ${jar} ${jar/-%{version}/}; done)
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/etc
cp -pr etc/* $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/etc
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/rulesets
cp -pr rulesets/* $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/rulesets

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# manual
install -d -m 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -p LICENSE.txt $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

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
%{_datadir}/%{name}-%{version}

%files manual
%defattr(0644,root,root,0755)
%doc %{_docdir}/%{name}-%{version}

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/*
