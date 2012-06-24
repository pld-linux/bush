#
##
Summary:	Business Shell (BUSH)
Summary(pl):	Pow�oka Biznesowa (BUSH)
Name:		bush
Version:	0.9.3
Release:	1
License:	GPL
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

%description
BUSH, the Business Shell, is a powerful Linux/UNIX shell for designing
secure, reliable scripts that can be later compiled as a fast
executable programs. It can also be used an an interactive login shell
or to generate Java Virtual Machine or .Net applications. BUSH is a
robust and readable alternative to BASH, CSH, and (to a certain
extent) Python and PERL. BUSH comes with 12 built-in packages
including numerics, string processing, sound and database access.

%description -l pl
BUSH, Pow�oka Biznesowa jest pow�ok� dla system�w Linux/UNIX o
bogatych mo�liwo�ciach. Stworzona jest z my�l� o konstruowaniu
bezpiecznych i niezawodnych skrypt�w, kt�re mog� potem zosta�
skompilowane do postaci szybkich program�w wykonywalnych. Mo�e by� ona
r�wnie� u�ywana jako pow�oka zg�oszeniowa, lub u�yta do generowania
aplikacji Java Virtual Machine lub .Net. BUSH jest mocn� i czyteln�
alternatyw� w stosunku do pow�ok BASH, CSH, a tak�e (w pewnym sensie)
do j�zyk�w takich jak Python czy PERL. BUSH zawiera 12 wbudowanych
pakiet�w w��czaj�c w to operacje na liczbach, przetwarzanie ci�g�w
znak�w, d�wi�ki, oraz dost�p do baz danych.

%prep
%setup -q
%patch0 -p1

%build
%{__make} linux
%{__make} \
	CC="%{__cc}" CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/bin

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
%doc TODO README COPYING html

%attr(755,root,root) /bin/bush
