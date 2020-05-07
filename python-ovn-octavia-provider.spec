
%{!?upstream_version: %global upstream_version %{version}}
%global upstream_name ovn-octavia-provider
%global sum OVN provider driver for Openstack Octavia
%global library ovn_octavia_provider

Name:           python-%{upstream_name}
Summary:        %{sum}
Version:        0.1.0
Release:        1%{?dist}
License:        ASL 2.0
URL:            https://opendev.org/openstack/ovn-octavia-provider
Source0:        https://tarballs.opendev.org/openstack/%{upstream_name}/%{upstream_name}-%{upstream_version}.tar.gz

BuildArch:      noarch

%description
OVN Octavia provider is OVN driver for Openstack Octavia.

%package -n     python3-%{upstream_name}
Summary:        %{sum}
%{?python_provide:%python_provide python3-%{upstream_name}}

BuildRequires:  git
BuildRequires:  openstack-macros
BuildRequires:  python3-devel
BuildRequires:  python3-pbr >= 2.0.0

Requires:       python3-babel >= 2.3.4
Requires:       python3-keystoneauth1 >= 3.4.0
Requires:       python3-netaddr >= 0.7.18
Requires:       python3-neutron-lib >= 1.28.0
Requires:       python3-neutronclient >= 6.7.0
Requires:       python3-octavia-lib >= 1.3.1
Requires:       python3-openvswitch >= 2.8.0
Requires:       python3-oslo-config >= 2:5.2.0
Requires:       python3-oslo-log >= 3.36.0
Requires:       python3-oslo-utils >= 3.33.0
Requires:       python3-oslo-serialization >= 2.28.1
Requires:       python3-ovsdbapp >= 0.17.0
Requires:       python3-pbr >= 2.0.0
Requires:       python3-tenacity >= 5.0.2
%description -n python3-%{upstream_name}
OVN Octavia provider is OVN driver for Openstack Octavia.

%package -n python3-%{upstream_name}-tests
Summary:  %{sum} unit tests
%{?python_provide:%python_provide python3-%{upstream_name}-tests}
BuildRequires:  python3-neutron-tests
BuildRequires:  python3-neutron-lib-tests
BuildRequires:  python3-octavia-lib
BuildRequires:  python3-oslo-config
BuildRequires:  python3-oslo-log
BuildRequires:  python3-oslo-serialization
BuildRequires:  python3-oslotest
BuildRequires:  python3-ovsdbapp
BuildRequires:  python3-stestr
BuildRequires:  python3-tenacity
BuildRequires:  python3-testresources
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools
BuildRequires:  python3-webtest

Requires: python3-%{upstream_name} = %{version}-%{release}
Requires: python3-neutron-tests >= 1:15.0.0
Requires: python3-neutron-lib-tests >= 1.28.0
Requires: python3-oslotest >= 3.2.0
Requires: python3-stestr >= 1.0.0
Requires: python3-testresources
Requires: python3-testscenarios >= 0.4
Requires: python3-testtools >= 2.2.0
Requires: python3-webtest >= 2.0.27

%description -n python3-%{upstream_name}-tests
This package contains the OVN Octavia test files.

%prep
%autosetup -n %{upstream_name}-%{upstream_version} -S git

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%build
%{py3_build}

%install
%{py3_install}

# Remove setuptools installed data_files
rm -rf %{buildroot}%{_datadir}/%{library}/LICENSE
rm -rf %{buildroot}%{_datadir}/%{library}/README.rst

%check
rm -f ./ovn_octavia_provider/tests/unit/hacking/test_checks.py
export OS_TEST_PATH='./ovn_octavia_provider/tests/unit'
export PATH=$PATH:%{buildroot}/usr/bin
export PYTHONPATH=$PWD
PYTHON=%{__python3} stestr --test-path $OS_TEST_PATH run

%files -n python3-%{upstream_name}-tests
%license LICENSE
%{python3_sitelib}/%{library}/tests

%files -n python3-%{upstream_name}
%license LICENSE
%{python3_sitelib}/%{library}
%{python3_sitelib}/%{library}-*.egg-info
%exclude %{python3_sitelib}/%{library}/tests

%changelog
* Thu May 07 2020 RDO <dev@lists.rdoproject.org> 0.1.0-1
- Update to 0.1.0

