Name:           wakeonlan
Version:        0.50
Release:        1%{?dist}
Summary:        Perl script to wake up computers through Magic Packets

License:        Artistic-2.0
URL:            https://github.com/jpoliv/wakeonlan/
# Source0:        https://github.com/jpoliv/wakeonlan/archive/refs/tags/v%{version}.tar.gz
# For the GitHub action
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker)

# Test suite
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Perl::Critic)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(Test::Spelling)


%description
This script sends 'magic packets' to wake-on-lan enabled Ethernet
adapters and motherboards, in order to switch on the called PC.


%prep
%autosetup


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
%doc Changes README.md examples/
%{_bindir}/wakeonlan
%{_mandir}/man1/wakeonlan.1*


%changelog
* Mon Aug 10 2026 Jose Pedro Oliveira - 0.50-1
- Update to 0.50.
- Update license to Artistic-2.0 (same as Artistic)
  (https://www.perlfoundation.org/artistic-notes-20.html)

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
