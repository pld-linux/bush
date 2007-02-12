Summary:	Business Shell (BUSH)
Summary(pl.UTF-8):	Powłoka Biznesowa (BUSH)
Name:		bush
Version:	0.9.3
Release:	1
License:	GPL v2+
Group:		Applications/Shells
Source0:	http://tardis.dyn.dhs.org/smiab_download/other_projects/%{name}-%{version}-src.tgz
# Source0-md5:	05f4719e91b7e0f3194d8c4a16c2720d
Patch0:		%{name}-Makefile.patch
URL:		http://www.pegasoft.ca/bush.html
BuildRequires:	gcc-ada
BuildRequires:	postgresql-devel
Requires(post,preun):	grep
Requires(preun):	fileutils
Requires:	libgnat
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_bindir		/bin

%description
BUSH, the Business Shell, is a powerful Linux/UNIX shell for designing
secure, reliable scripts that can be later compiled as a fast
executable programs. It can also be used an an interactive login shell
or to generate Java Virtual Machine or .Net applications. BUSH is a
robust and readable alternative to BASH, CSH, and (to a certain
extent) Python and PERL. BUSH comes with 12 built-in packages
including numerics, string processing, sound and database access.

%description -l pl.UTF-8
BUSH, Powłoka Biznesowa jest powłoką dla systemów Linux/UNIX o
bogatych możliwościach. Stworzona jest z myślą o konstruowaniu
bezpiecznych i niezawodnych skryptów, które mogą potem zostać
skompilowane do postaci szybkich programów wykonywalnych. Może być ona
również używana jako powłoka zgłoszeniowa, lub użyta do generowania
aplikacji Java Virtual Machine lub .Net. BUSH jest mocną i czytelną
alternatywą w stosunku do powłok BASH, CSH, a także (w pewnym sensie)
do języków takich jak Python czy PERL. BUSH zawiera 12 wbudowanych
pakietów włączając w to operacje na liczbach, przetwarzanie ciągów
znaków, dźwięki, oraz dostęp do baz danych.

%prep
%setup -q
%patch0 -p1

%build
%{__make} linux
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

mv -f doc html

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
if [ ! -f /etc/shells ]; then
	echo "/bin/bush" > /etc/shells
else
	if ! grep -q '^/bin/bush$' /etc/shells; then
		echo "/bin/bush" >> /etc/shells
	fi
fi

%preun
if [ "$1" = "0" ]; then
	umask 022
	grep -v /bin/bush /etc/shells > /etc/shells.new
	mv -f /etc/shells.new /etc/shells
fi

%files
%defattr(644,root,root,755)
%doc README TODO html
%attr(755,root,root) %{_bindir}/bush
