%{?_javapackages_macros:%_javapackages_macros}
%global base_name httpcomponents

Name:              httpcomponents-core
Summary:           Set of low level Java HTTP transport components for HTTP services
Version:           4.3.2
Release:           3.4
Group:		   Development/Java
# The project is licensed under ASL 2.0, but it contains annotations
# in the package org.apache.http.annotation which are derived
# from JCIP-ANNOTATIONS project (CC-BY licensed)
License:           ASL 2.0 and CC-BY
URL:               https://hc.apache.org/
Source0:           http://www.apache.org/dist/httpcomponents/httpcore/source/httpcomponents-core-%{version}-src.tar.gz
BuildArch:         noarch

BuildRequires:     maven-local
BuildRequires:     httpcomponents-project
BuildRequires:     java >= 1:1.6.0
BuildRequires:     jpackage-utils
BuildRequires:     apache-commons-logging
BuildRequires:     junit
BuildRequires:     mvn(org.codehaus.mojo:build-helper-maven-plugin)
%if 0%{?fedora}
BuildRequires:     mockito
%endif

%description
HttpCore is a set of low level HTTP transport components that can be
used to build custom client and server side HTTP services with a
minimal footprint. HttpCore supports two I/O models: blocking I/O
model based on the classic Java I/O and non-blocking, event driven I/O
model based on Java NIO.

The blocking I/O model may be more appropriate for data intensive, low
latency scenarios, whereas the non-blocking model may be more
appropriate for high latency scenarios where raw data throughput is
less important than the ability to handle thousands of simultaneous
HTTP connections in a resource efficient manner.

%package        javadoc
Summary:        API documentation for %{name}

%description    javadoc
%{summary}.


%prep
%setup -q

%pom_remove_plugin :maven-checkstyle-plugin

# we don't need these artifacts right now
%pom_disable_module httpcore-osgi
%pom_disable_module httpcore-ab

# OSGify modules
for module in httpcore httpcore-nio; do
    %pom_xpath_remove "pom:project/pom:packaging" $module
    %pom_xpath_inject "pom:project" "<packaging>bundle</packaging>" $module
    %pom_xpath_inject "pom:build/pom:plugins" "
        <plugin>
          <groupId>org.apache.felix</groupId>
          <artifactId>maven-bundle-plugin</artifactId>
          <extensions>true</extensions>
          <configuration>
            <instructions>
              <Export-Package>*</Export-Package>
              <Private-Package></Private-Package>
              <_nouses>true</_nouses>
            </instructions>
          </configuration>
        </plugin>" $module
done

# install JARs to httpcomponents/ for compatibility reasons
# several other packages expect to find the JARs there
%mvn_file ":{*}" httpcomponents/@1

%build
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%dir %{_javadir}/httpcomponents
%doc LICENSE.txt NOTICE.txt README.txt RELEASE_NOTES.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.3.2-2
- Remove BuildRequires on maven-surefire-provider-junit4

* Mon May 12 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.3.2-1
- Update to upstream version 4.3.2

* Tue Sep 03 2013 Michal Srb <msrb@redhat.com> - 4.3-1
- Update to upstream version 4.3

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 10 2013 Michal Srb <msrb@redhat.com> - 4.2.4-4
- Fix license tag (CC-BY added)

* Fri May 17 2013 Alexander Kurtakov <akurtako@redhat.com> 4.2.4-3
- Fix bundle plugin configuration to produce sane manifest.
- Do not duplicate javadoc files list.

* Mon Mar 25 2013 Michal Srb <msrb@redhat.com> - 4.2.4-2
- Build with xmvn

* Mon Mar 25 2013 Michal Srb <msrb@redhat.com> - 4.2.4-1
- Update to upstream version 4.2.4

* Mon Feb 25 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.3-3
- Add missing BR: maven-local

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec  3 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.3-1
- Update to upstream version 4.2.3

* Fri Oct  5 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.2-1
- Update to upstream version 4.2.2

* Mon Aug 27 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 4.2.1-3
- Remove mockito from Requires (not needed really)
- BR on mockito is now conditional on Fedora

* Fri Jul 27 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.1-2
- Install NOTICE.txt file
- Fix javadir directory ownership
- Preserve timestamps

* Mon Jul 23 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.1-1
- Update to upstream version 4.2.1
- Convert patches to POM macros

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar 23 2012 Krzysztof Daniel <kdaniel@redhat.com> 4.1.4-1
- Update to latest upstream (4.1.4)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 16 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 4.1.3-1
- Update to latest upstream (4.1.3)

* Tue Jul 26 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 4.1.2-1
- Update to latest upstream (4.1.2)

* Mon Jul  4 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 4.1.1-2
- Fix forgotten add_to_maven_depmap

* Fri Jul  1 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 4.1.1-1
- Update to latest upstream (4.1.1)
- Use new maven macros
- Tweaks according to new guidelines
- Enable tests again (seem to work OK even in koji now)

* Tue Mar 15 2011 Severin Gehwolf <sgehwolf@redhat.com> 4.1-6
- Explicitly set PrivatePackage to the empty set, so as to
  export all packages.

* Fri Mar 11 2011 Alexander Kurtakov <akurtako@redhat.com> 4.1-5
- Bump release to fix my mistake with the release.

* Thu Mar 10 2011 Alexander Kurtakov <akurtako@redhat.com> 4.1-3
- Export all packages.

* Fri Feb 18 2011 Alexander Kurtakov <akurtako@redhat.com> 4.1-2
- Don't use basename it's part of coreutils.

* Fri Feb 18 2011 Alexander Kurtakov <akurtako@redhat.com> 4.1-4
- Install into %{_javadir}/httpcomponents. We will use it for client libs too.
- Proper osgi info.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 4.1-2
- Added license to javadoc subpackage

* Fri Dec 17 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 4.1-1
- Initial package

