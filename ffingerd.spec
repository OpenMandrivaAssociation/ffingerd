%define fullname %{name}-%{version}
%define version 1.28
%define release %mkrel 11
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



%changelog
* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 1.28-11mdv2011.0
+ Revision: 618279
- the mass rebuild of 2010.0 packages

* Thu Sep 03 2009 Thierry Vignaud <tv@mandriva.org> 1.28-10mdv2010.0
+ Revision: 428723
- rebuild

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 1.28-9mdv2009.0
+ Revision: 245118
- rebuild

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 1.28-7mdv2008.1
+ Revision: 136415
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Tue Aug 08 2006 Lenny Cartier <lenny@mandriva.com> 1.28-7mdv2007.0
- rebuild

* Wed Apr 20 2005 Lenny Cartier <lenny@mandriva.com> 1.28-6mdk
- rebuild

* Fri Feb 20 2004 Lenny Cartier <lenny@mandrakesoft.com> 1.28-5mdk
- rebuild

