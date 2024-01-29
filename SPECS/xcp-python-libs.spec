%global package_speccommit 4667fd527d3183fdb1968f2be7041a5a0ebe927c
%global usver 3.0.2
%global xsver 4
%global xsrel %{xsver}%{?xscount}%{?xshash}
%bcond_with test

Summary: Common XCP-ng Python classes
Name: xcp-python-libs
Version: 3.0.2
Release: %{?xsrel}%{?dist}
Source0: xcp-python-libs-3.0.2.tar.gz
Patch0: 0001-Remove-setuptools_scm.patch
%define __python python3

# XCP-ng
# This repo is the upstream for updategrub.py, for now
Source1: updategrub.py

License: GPL

Group: Applications/System
BuildArch: noarch

Obsoletes: xcp-python-libs-incloudsphere
BuildRequires: python3-devel python3-setuptools python3-pip

%if 0%{?xenserver} >= 9
BuildRequires: pyproject-rpm-macros
%endif

%description
Common XCP-ng Python classes for python3

%package -n python3-xcp-libs
Summary: Common XCP-ng Python classes for Python3
# See https://github.com/xenserver/python-libs/blob/master/pyproject.toml:
Requires: python3-six
Requires: biosdevname
%description -n python3-xcp-libs
Common XenServer Python classes for Python3

%prep
%autosetup -p1
%if 0%{?xenserver} < 9
ln -s setup27.py setup.py
%else
# We do not generate the version dynamically, but set the version statically
sed -i "s/dynamic *= *\[\"version\"\]/version = \"%{version}\"/g" pyproject.toml
%generate_buildrequires
%pyproject_buildrequires
%endif

%build
%if 0%{?xenserver} < 9
%{__python} setup.py build
%else
%pyproject_wheel
%endif

%install
%if 0%{?xenserver} < 9
%{__python} setup.py install -O2 --skip-build --root %{buildroot}
%else
%pyproject_install xcp
%endif

# XCP-ng: FIXME. Needs to be ported to python3 and packaged properly.
#install -m 0775 %{SOURCE1} %{buildroot}%{python_sitelib}/xcp/updategrub.py

%check
%if %{with test}
cd tests
./run-all-tests.sh
%endif

%clean
%{__rm} -rf %{buildroot}

%files -n python3-xcp-libs
%defattr(-,root,root)
%{python3_sitelib}/python_libs-*
%{python3_sitelib}/xcp

%changelog
* Mon Jan 22 2024 Samuel Verschelde <stormi-xcp@ylix.fr> - 3.0.2-4.1
- Update to 3.0.2-4
- Keep updategrub.py sources but don't install it until ported to python3

* Thu Nov 16 2023 Lin Liu <lin.liu@citrix.com> - 3.0.2-4
- Rebuild to requires biosdevname for package

* Thu Nov 16 2023 Lin Liu <lin.liu@citrix.com> - 3.0.2-3
- CA-384331: Requires biosdevname

* Tue Oct 31 2023 Lin Liu <lin.liu@citrix.com> - 3.0.2-2
- Build python3 package for XS8 & XS9

* Fri Oct 27 2023 Lin Liu <lin.liu@citrix.com> - 3.0.2-1
- Fixup `None` in bootup MenuEntry

* Mon Sep 25 2023 Gerald Elder-Vass <gerald.elder-vass@citrix.com> - 3.0.1-1
- CP-41302: Use absolute import for branding.py

* Thu Sep 7 2023 Lin Liu <Lin.Liu01@cloud.com> - 3.0.0-2
- CP-45003: Fixup release number

* Thu Aug 17 2023 Bernhard Kaindl <bernhard.kaindl@cloud.com> - 3.0.0-1
- CP-45003: build xcp-python-libs for Python3

* Mon Nov 29 2021 Deli Zhang <deli.zhang@citrix.com> - 2.3.5-1
- CP-37849: Support .treeinfo new format

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

* Mon Jan 01 2018 Owen Smith <owen.smith@citrix.com> - 2.0.3-2
- CA-281789: Bump release, so that Jura will include an updated package

* Mon Oct 16 2017 Simon Rowe <simon.rowe@citrix.com> - 2.0.3-1
- Fix typo in log message

* Tue Apr 11 2017 Simon Rowe <simon.rowe@citrix.com> - 2.0.2-1
- CA-246490: version: Change the build number to a build identifier
- CA-249794: Don't ignore errors from URL port parsing

