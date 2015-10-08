Name: ari-backup
Version: 1.0.10
Release: 2%{?dist}
Summary: A helpful wrapper around rdiff-backup
License: BSD
URL: https://github.com/jpwoodbu/ari-backup
Source0: https://github.com/jpwoodbu/%{name}/archive/%{version}.tar.gz
Patch0: ari-backup.change_default_destination.patch
BuildArch: noarch
BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: rpm-python
Requires: crontabs
Requires: python-gflags
Requires: python-setuptools
Requires: PyYAML
Requires: rdiff-backup


%description
A helpful wrapper around rdiff-backup that allows backup jobs to be simple
Python modules.


%prep
%setup -q

%patch0 -p0

# We want to install the example jobs as documentation instead of putting them
# in /etc/ari-backup/jobs.d.
mv include%{_sysconfdir}/%{name}/jobs.d/* .


%build
%{__python2} setup.py build


%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

# Directories
mkdir -p %{buildroot}/%{_sharedstatedir}/%{name}
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/jobs.d
mkdir -p %{buildroot}/%{_sysconfdir}/cron.daily

# Configuration
cp -R include%{_sysconfdir}/%{name}/* %{buildroot}/%{_sysconfdir}/%{name}

# Cron
cp include/cron/ari-backup %{buildroot}/%{_sysconfdir}/cron.daily/


%files
%license LICENSE.txt
%doc README.md ari-backup-local-demo ari-backup-local-lvm-demo ari-backup-remote-demo ari-backup-remote-lvm-demo
%{python_sitelib}/ari_backup
%{python_sitelib}/*.egg-info
%config(noreplace) %{_sysconfdir}/%{name}/ari-backup.conf.yaml

# Because ari-backup may be used as a central backup service, its job
# configuration files are protected to only be readable by the root user. The
# configuration files describe information about other hosts on the network
# (such as which paths on them are backed up or not backed up).
%defattr(0644,root,root,0700)
%{_sysconfdir}/%{name}/jobs.d

# The cron job can be executed by anyone, since the jobs folder is protected.
%defattr(0755,root,root,-)
%{_sysconfdir}/cron.daily/ari-backup

# All of the backups for all hosts that ari-backup manages are kept in this
# path by default. It is protected from other system users since it is
# assumed that there may be sensitive information within it.
%defattr(0600,root,root,0700)
%{_sharedstatedir}/%{name}


%changelog
* Thu Oct 8 2015 Randy Barlow <randy@electronsweatshop.com> 1.0.10-2
- Install examples as documentation instead of to the jobs folder
- BuildRequire python2-devel and use the python2 macro in the spec file
- Relax the executable permissions on the daily cron job, relying on the jobs
  individual permissions to control who can execute backup jobs.

* Wed Oct 7 2015 Randy Barlow <randy@electronsweatshop.com> 1.0.10-1
- Initial release
