%define debug_package %{nil}

Name:       node_exporter
Version:    0.16.0
Release:    2%{?dist}
Summary:    Prometheus exporter for machine metrics, written in Go with pluggable metric collectors.
Group:      System Environment/Daemons
License:    ASL 2.0
URL:        https://github.com/prometheus/node_exporter
Source0:    https://github.com/prometheus/node_exporter/releases/download/v%{version}/node_exporter-%{version}.linux-amd64.tar.gz
Source1:    node_exporter.initd
Source2:    node_exporter.env

# Requires:   supervisor

Provides:   %{name}

%description
Prometheus exporter for machine metrics, written in Go with pluggable metric collectors.

%prep
%setup -q -n node_exporter-%{version}.linux-amd64


%build
/bin/true

%install

# Install Binary
mkdir -p %{buildroot}%{_bindir}
%{__install} -p node_exporter %{buildroot}%{_bindir}

# Install Service
mkdir -p %{buildroot}%{_initddir}
%{__install} -p %{SOURCE1} %{buildroot}%{_initddir}/%{name}

# Install Configuration
%{__install} -d %{buildroot}%{_sysconfdir}/sysconfig/prometheus
%{__install} -p %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/prometheus/node_exporter.env

# Create Logging Location
%{__install} -d %{buildroot}%{_localstatedir}/log/prometheus

# Create Runtime Details Location
%{__install} -d %{buildroot}%{_localstatedir}/run/prometheus

%files
%defattr(644, %{name}, %{name}, 755)

# Binary
%attr(755, %{name}, %{name}) %{_bindir}/%{name} 

# Init.d
%attr(755, %{name}, %{name}) %{_initddir}/%{name}

# Configuration
%dir %{_sysconfdir}/sysconfig/prometheus/
%config %attr(755, %{name}, %{name}) %{_sysconfdir}/sysconfig/prometheus/node_exporter.env

# Logging Location
%dir %{_localstatedir}/log/prometheus

# Runtime Details Location
%dir %{_localstatedir}/run/prometheus

%pre
# If app user does not exist, create
id %{name} >/dev/null 2>&1
if [ $? != 0 ]; then
    /usr/sbin/groupadd -r %{name} >/dev/null 2>&1
    /usr/sbin/useradd -d /var/run/%{name} -r -g %{name} %{name} >/dev/null 2>&1
fi


%post
if [ $1 = 1 ]; then
    /sbin/chkconfig --add %{name}
fi

%preun
# Stop service if running
if [ -e /etc/init.d/%{name} ]; then
    /sbin/service %{name} stop > /dev/null 2>&1
    true
fi

# If not an upgrade, then delete
if [ $1 = 0 ]; then
    /sbin/chkconfig --del %{name} > /dev/null 2>&1
    true
fi

%postun
# Do not remove anything if this is not an uninstall
if [ $1 = 0 ]; then
    /usr/sbin/userdel -r %{name} >/dev/null 2>&1
    /usr/sbin/groupdel %{name} >/dev/null 2>&1
    # Ignore errors from above
    true
fi

%changelog
* Fri Oct 5 2018 Kenneth Pianeta - 0.0.1
- initial creation
