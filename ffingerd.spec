%define fullname %{name}-%{version}
%define version 1.28
%define release %mkrel 10
%define name ffingerd

Name: %{name}
Summary: Secure finger daemon
Version: %{version}
Release: %{release}
Source: %{fullname}.tar.bz2
Group: Networking/Other
URL: http://www.fefe.de/ffingerd/
License: GPL
BuildRoot: %{_tmppath}/%{name}-buildroot

%description
Fefe's Finger Daemon is a secure fingerd which doesn't run as root,
doesn't give away vital info about your system, and does syslogging.

%prep

%setup -q %{fullname}

%build

%configure

%make

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_prefix}/sbin
install -d $RPM_BUILD_ROOT%{_mandir}/man8
install -m 644 ffingerd.8 $RPM_BUILD_ROOT/%{_mandir}/man8
install -m 755 ffingerd $RPM_BUILD_ROOT%{_sbindir}/

%post
# remove other fingerd's and add ffingerd. make a backup, too
cat /etc/inetd.conf | grep ffingerd > /tmp/ffingerd.test
if [ ! -s /tmp/ffingerd.test ]; then
     cp -f /etc/inetd.conf /etc/inetd.conf.rpmsave
     cat /etc/inetd.conf | grep -v in.fingerd | grep -v "End of inetd.conf" > /etc/inetd.conf
     echo "#" >> /etc/inetd.conf
     echo "# Fefe's finger daemon, a secure finger daemon" >> /etc/inetd.conf
     echo "#" >> /etc/inetd.conf
     echo "finger  stream  tcp     nowait  nobody  /usr/sbin/tcpd  /usr/sbin/ffingerd" >> /etc/inetd.conf
     echo >> /etc/inetd.conf
     echo "# End of inetd.conf" >> /etc/inetd.conf
fi
rm /tmp/ffingerd.test

# now restart inetd
if [ -f /var/run/inetd.pid ]; then
     kill -HUP `cat /var/run/inetd.pid` ;
else
     echo "Now you need to restart inetd" ;
fi

%postun
# restore the old config file, or try to at least
if [ -f /etc/inetd.conf.rpmsave ]; then
     mv /etc/inetd.conf.rpmsave /etc/inetd.conf ;
fi

# now restart inetd
if [ -f /var/run/inetd.pid ]; then
     kill -HUP `cat /var/run/inetd.pid` ;
else
     echo "Now you need to restart inetd" ;
fi

%files
%defattr(-,root,root)
%doc NEWS README TODO
%{_sbindir}/*
%{_mandir}/man8/*

%clean
rm -rf $RPM_BUILD_ROOT

