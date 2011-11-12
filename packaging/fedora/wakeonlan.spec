Name:           wakeonlan
Version:        0.41
Release:        0.fdr.1
Epoch:          0
Summary:        Perl script to wake up computers through Magic Packets

Group:          Development/Libraries
License:        Artistic
URL:            http://gsd.di.uminho.pt/jpo/software/wakeonlan/
Source0:   http://gsd.di.uminho.pt/jpo/software/wakeonlan/wakeonlan-0.41.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl >= 1:5.6.1

%description
This script sends 'magic packets' to wake-on-lan enabled ethernet
adapters and motherboards, in order to switch on the called PC.


%prep
%setup -q


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check || :
make test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes README examples/
%{_bindir}/*
%{_mandir}/man1/*.1*


%changelog
* Fri Jan 28 2005 Jose Pedro Oliveira - 0:0.41-0.fdr.1
- Update to 0.41.

* Tue Jun 08 2004 Jose Pedro Oliveira - 0:0.40_09-0.fdr.1
- First build.
