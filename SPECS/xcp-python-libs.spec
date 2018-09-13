%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary: Common XenServer Python classes
Name: xcp-python-libs
Version: 2.0.5
Release: 1
Source0: https://code.citrite.net/rest/archive/latest/projects/XS/repos/%{name}/archive?at=v%{version}&format=tar.gz&prefix=%{name}-%{version}#/%{name}-%{version}.tar.gz
License: GPL

Group: Applications/System
BuildArch: noarch

BuildRequires: python-devel python-setuptools

Obsoletes: xcp-python-libs-incloudsphere

%description
Common XenServer Python classes.

%prep
%autosetup -p1

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O2 --skip-build --root %{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%{python_sitelib}


%changelog
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

