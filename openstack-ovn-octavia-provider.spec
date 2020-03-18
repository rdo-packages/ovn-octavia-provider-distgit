# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver 3
%else
%global pyver 2
%endif

%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility

%{!?upstream_version: %global upstream_version %{version}}
%global upstream_name ovn-octavia-provider
%global sum OVN provider driver for Openstack Octavia
%global library ovn_octavia_provider

Name:           openstack-%{upstream_name}
Summary:        %{sum}
Version:        XXX
Release:        XXX
License:        ASL 2.0
URL:            https://opendev.org/openstack/ovn-octavia-provider
Source0:        https://tarballs.opendev.org/openstack/%{upstream_name}/%{upstream_name}-%{upstream_version}.tar.gz

BuildArch:      noarch

%description
OVN Octavia provider is OVN driver for Openstack Octavia.

%package -n     python%{pyver}-%{upstream_name}
Summary:        %{sum}
%{?python_provide:%python_provide python%{pyver}-%{upstream_name}}

BuildRequires:  git
BuildRequires:  openstack-macros
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-neutron-lib
BuildRequires:  python%{pyver}-octavia-lib
BuildRequires:  python%{pyver}-oslo-config
BuildRequires:  python%{pyver}-oslo-log
BuildRequires:  python%{pyver}-oslo-serialization
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-ovsdbapp
BuildRequires:  python%{pyver}-pbr >= 2.0.0
BuildRequires:  python%{pyver}-tenacity >= 4.4.0

Requires:       python%{pyver}-babel >= 2.3.4
Requires:       python%{pyver}-netaddr >= 0.7.18
Requires:       python%{pyver}-neutron-lib >= 1.28.0
Requires:       python%{pyver}-neutronclient >= 6.7.0
Requires:       python%{pyver}-octavia-lib >= 1.3.1
Requires:       python%{pyver}-oslo-config >= 2:5.2.0
Requires:       python%{pyver}-oslo-log >= 3.36.0
Requires:       python%{pyver}-oslo-serialization >= 2.18.0
Requires:       python%{pyver}-ovsdbapp >= 0.17.0
Requires:       python%{pyver}-pbr >= 2.0.0
Requires:       python%{pyver}-tenacity >= 4.4.0

%description -n python%{pyver}-%{upstream_name}
OVN Octavia provider is OVN driver for Openstack Octavia.

%prep
%autosetup -n %{upstream_name}-%{upstream_version} -S git

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%build
%{pyver_build}

%install
%{pyver_install}

# Remove setuptools installed data_files
rm -rf %{buildroot}%{_datadir}/%{library}/LICENSE
rm -rf %{buildroot}%{_datadir}/%{library}/README.rst

%check
export OS_TEST_PATH='./ovn_octavia_provider/tests/unit'
export PATH=$PATH:%{buildroot}/usr/bin
export PYTHONPATH=$PWD
PYTHON=%{pyver_bin} stestr-%{pyver} --test-path $OS_TEST_PATH run

%files -n python%{pyver}-%{upstream_name}
%license LICENSE
%{pyver_sitelib}/%{library}
%{pyver_sitelib}/%{library}-*.egg-info
%exclude %{pyver_sitelib}/%{library}/tests

%files -n python%{pyver}-%{upstream_name}-tests
%license LICENSE
%{pyver_sitelib}/%{module}/tests

%changelog
