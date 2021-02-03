%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary: Common XenServer Python classes
Name: xcp-python-libs
Version: 2.3.4
Release: 1

Source0: https://code.citrite.net/rest/archive/latest/projects/XS/repos/xcp-python-libs/archive?at=v2.3.4&format=tar.gz&prefix=xcp-python-libs-2.3.4#/xcp-python-libs-2.3.4.tar.gz


Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XS/repos/xcp-python-libs/archive?at=v2.3.4&format=tar.gz&prefix=xcp-python-libs-2.3.4#/xcp-python-libs-2.3.4.tar.gz) = 0b1609499d4dfabe024149c25566cd0e38752988

License: GPL

Group: Applications/System
BuildArch: noarch

BuildRequires: python-devel python-setuptools python2-mock

Obsoletes: xcp-python-libs-incloudsphere

%description
Common XenServer Python classes.

%prep
%autosetup -p1

%build
%{__python} setup.py build

%check
cd tests
./run-all-tests.sh

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O2 --skip-build --root %{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%{python_sitelib}


%changelog
* Thu Sep 10 2020 Ross Lagerwall <ross.lagerwall@citrix.com> - 2.3.4-1
- CA-343343: Handle PCI rules when device is missing
- CP-34657: Fix running tests on CentOS 7

* Fri Aug 14 2020 Ross Lagerwall <ross.lagerwall@citrix.com> - 2.3.3-2
- CP-34657: Run tests during the build

* Mon Jun 01 2020 Ross Lagerwall <ross.lagerwall@citrix.com> - 2.3.3-1
- CA-339540: Fail NFS mounts faster

* Thu Oct 31 2019 Ross Lagerwall <ross.lagerwall@citrix.com> - 2.3.2-1
- CA-329771: Fix HTTP access with username but no password

* Thu Oct 24 2019 Ross Lagerwall <ross.lagerwall@citrix.com> - 2.3.1-1
- Remove compat_urlsplit()
- CA-329412: Avoid potential leak of passwords

* Wed Feb 06 2019 jenniferhe <jennifer.herbert@citrix.com> - 2.3.0-1
- add errno.IO to errors passed to host-upgrade
- CP-29627: Increase the amount of memory assigned to dom0
- CP-29836: Expose the product version of a Yum repository
- CP-30501: Add API to get dom0 default memory by version
- CP-30557: Make default_memory base its recomendation based on platform version

* Tue Jan 15 2019 rossla <ross.lagerwall@citrix.com> - 2.2.1-1
- CP-23016 Update API to store last error code
- Set lastError on IOError, OSError & Exception, then return false

* Fri Oct 12 2018 Simon Rowe <simon.rowe@citrix.com> - 2.1.1-1
- CA-299167: fix creating Version from string

* Thu Aug 30 2018 Simon Rowe <simon.rowe@citrix.com> - 2.1.0-1
- Take a copy of the boilerplate
- CP-21760: add one-shot boot method

* Tue Jul 17 2018 Simon Rowe <simon.rowe@citrix.com> - 2.0.5-1
- CP-28832: Enable the use of an index after PCI bus location

* Mon Jun 25 2018 Simon Rowe <simon.rowe@citrix.com> - 2.0.4-1
- PAR-244 Use branding in xen-cmdline

* Wed Jun 13 2018 Tim Smith <tim.smith@citrix.com> - 2.0.3-4
- Removed Provides for xcp-python-libs-incloudsphere; Obsoletes should be
  sufficient

* Mon Apr 30 2018 Simon <simon.rowe@citrix.com> - 2.0.3-3
- Removed branding.py

* Wed Jan 01 2018 Owen Smith <owen.smith@citrix.com> - 2.0.3-2
- CA-281789: Bump release, so that Jura will include an updated package

* Mon Oct 16 2017 Simon Rowe <simon.rowe@citrix.com> - 2.0.3-1
- Fix typo in log message

* Tue Apr 11 2017 Simon Rowe <simon.rowe@citrix.com> - 2.0.2-1
- CA-246490: version: Change the build number to a build identifier
- CA-249794: Don't ignore errors from URL port parsing

