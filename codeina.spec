%define         gst_minver      0.10.11.2
%define         gstpy_minver    0.10.0
%define         pygtk_minver    2.8.0

Name:           codeina
Version:        0.10.2
Release:        %mkrel 0.beta3.2
Summary:        Codeina - Codec Installation Application

Group:          Sound
License:        GPLv2+
URL:            https://core.fluendo.com/gstreamer/trac/browser/codeina
# Upstream SVN repository is at https://core.fluendo.com/gstreamer/svn/codeina/trunk/
Source0:         http://www.fluendo.com/downloads/codeina/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

Requires:       python >= 2.5
Requires:       gstreamer0.10-python >= %{gstpy_minver}
Requires:       pygtk2 >= %{pygtk_minver}
Requires:       pyxdg
Requires:       gnome-python-gtkmozembed
Requires:       python-OpenSSL
Requires:       python-notify
Requires:       python-twisted-web
Requires:	lsb-release

BuildRequires:  python-OpenSSL
BuildRequires:  python-twisted-web
BuildRequires:  gstreamer0.10-python >= %{gstpy_minver}
BuildRequires:  python-yaml
BuildRequires:  gnome-python-gtkmozembed
BuildRequires:  python-notify
BuildRequires:  python-pyxml
BuildRequires:  pyxdg

# sigh, libtool
BuildRequires:  gcc-c++

BuildRequires:  intltool
BuildRequires:  gettext
BuildRequires:  desktop-file-utils

BuildArch:      noarch

%description
Codeina installs codecs from the Fluendo webshop or distribution package
for GStreamer.

%prep
%setup -q -n %{name}-%{version}

%build
%configure2_5x

make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std

# only ship mandriva file for this distribution
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/codeina/providers/{fedora*,ubuntu*}.xml
%if %mdkversion >= 200800
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/codeina/providers/mandrivalinux_2008.0.xml
%endif
rm -f $RPM_BUILD_ROOT%{_datadir}/codeina/logo/ubuntu.png

rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/xdg/menus

sed -i -e 's/Comment=.*$/Comment=Codec Installer/g' $RPM_BUILD_ROOT%{_datadir}/applications/codeina-shop.desktop


%find_lang %{name} 

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc ChangeLog COPYING README AUTHORS
%config (noreplace) %{_sysconfdir}/codeina
%config (noreplace) %{_sysconfdir}/xdg/autostart/codeina.desktop
%{_bindir}/%{name}
%{_bindir}/%{name}.bin
%{python_sitelib}/codeina
%{_datadir}/codeina
%{_datadir}/applications/*.desktop
%{_datadir}/autostart/*.desktop
