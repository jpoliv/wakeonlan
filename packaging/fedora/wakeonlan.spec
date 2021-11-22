Name:           wakeonlan
Version:        0.42
Release:        1%{?dist}
Summary:        Perl script to wake up computers through Magic Packets

License:        Artistic
URL:            https://github.com/jpoliv/wakeonlan/
Source0:        https://github.com/jpoliv/wakeonlan/archive/%{name}-%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(warnings)
BuildRequires:  perl(strict)

# Test suite
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Perl::Critic)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Spelling)

Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))


%description
This script sends 'magic packets' to wake-on-lan enabled ethernet
adapters and motherboards, in order to switch on the called PC.


%prep
%setup -q


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}


%check
make test


%files
%defattr(-,root,root,-)
%doc Changes README.md examples/
%{_bindir}/*
%{_mandir}/man1/*.1*


%changelog
* Mon Nov 22 2021 Jose Pedro Oliveira - 0.42-1
- Update to 0.42.
- Update specfile to follow recent Fedora's packaging guidelines
  (https://docs.fedoraproject.org/en-US/packaging-guidelines/Perl/)

* Tue Nov 19 2013 Jose Pedro Oliveira - 0.41-1
- Drop deprecated packaging guidelines (from fedora.us days)

* Fri Jan 28 2005 Jose Pedro Oliveira - 0:0.41-0.fdr.1
- Update to 0.41.

* Tue Jun 08 2004 Jose Pedro Oliveira - 0:0.40_09-0.fdr.1
- First build.
