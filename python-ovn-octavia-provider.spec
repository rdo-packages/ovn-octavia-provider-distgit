%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order pylint

%global upstream_name ovn-octavia-provider
%global sum OVN provider driver for Openstack Octavia
%global library ovn_octavia_provider

Name:           python-%{upstream_name}
Summary:        %{sum}
Version:        XXX
Release:        XXX
License:        Apache-2.0
URL:            https://opendev.org/openstack/ovn-octavia-provider
Source0:        https://tarballs.opendev.org/openstack/%{upstream_name}/%{upstream_name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.opendev.org/openstack/%{upstream_name}/%{upstream_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

%description
OVN Octavia provider is OVN driver for Openstack Octavia.

%package -n     python3-%{upstream_name}
Summary:        %{sum}

BuildRequires:  git-core
BuildRequires:  openstack-macros
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
%description -n python3-%{upstream_name}
OVN Octavia provider is OVN driver for Openstack Octavia.

%package -n python3-%{upstream_name}-tests
Summary:  %{sum} unit tests
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
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{upstream_name}-%{upstream_version} -S git


sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs};do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

%generate_buildrequires
%pyproject_buildrequires -t -e %{default_toxenv}

%build
%pyproject_wheel

%install
%pyproject_install

# Remove setuptools installed data_files
rm -rf %{buildroot}%{_datadir}/%{library}/LICENSE
rm -rf %{buildroot}%{_datadir}/%{library}/README.rst

%check
rm -f ./ovn_octavia_provider/tests/unit/hacking/test_checks.py
export OS_TEST_PATH='./ovn_octavia_provider/tests/unit'
export PATH=$PATH:%{buildroot}/usr/bin
export PYTHONPATH=$PWD
%tox -e %{default_toxenv}

%files -n python3-%{upstream_name}-tests
%license LICENSE
%{python3_sitelib}/%{library}/tests

%files -n python3-%{upstream_name}
%license LICENSE
%{python3_sitelib}/%{library}
%{python3_sitelib}/%{library}-*.dist-info
%exclude %{python3_sitelib}/%{library}/tests

%changelog
