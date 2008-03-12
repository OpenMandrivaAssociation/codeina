%define         gst_minver      0.10.11.2
%define         gstpy_minver    0.10.0
%define         pygtk_minver    2.8.0

Name:           codeina
Version:        0.10.2
Release:        %mkrel 0.beta3.1
Summary:        Codeina - Codec Installation Application

Group:          Sound
License:        GPLv2+
URL:            https://core.fluendo.com/gstreamer/trac/browser/codeina
# Upstream SVN repository is at https://core.fluendo.com/gstreamer/svn/codeina/trunk/
Source0:         http://www.fluendo.com/downloads/codeina/%{name}-%{version}~beta3.tar.bz2
# (fc) 0.10.2-0.beta3.1mdv use gurpmi for package install
Patch0:		codeina-0.10.2-gurpmi.patch
# (fc) 0.12.2-0.beta3.1mdv allow transient option
Patch1:		codeina-0.10.2-transient.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

Requires:       python >= 2.5
Requires:       gstreamer0.10-python >= %{gstpy_minver}
Requires:       pygtk2 >= %{pygtk_minver}
Requires:       pyxdg
Requires:       gnome-python-gtkmozembed
Requires:       python-OpenSSL
Requires:       python-notify
Requires:       python-twisted-web

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
%setup -q -n %{name}-%{version}~beta3
%patch0 -p1 -b .gurpmi
%patch1 -p1 -b .transient

%build
%configure2_5x

make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std

# only ship mandriva file for this distribution
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/codeina/providers/{fedora*,ubuntu*}.xml
sed -e 's/2008\.0/2008.1/g' $RPM_BUILD_ROOT%{_sysconfdir}/codeina/providers/mandrivalinux_2008.0.xml > $RPM_BUILD_ROOT%{_sysconfdir}/codeina/providers/mandrivalinux_2008.1.xml 
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/codeina/providers/mandrivalinux_2008.0.xml
rm -f $RPM_BUILD_ROOT%{_datadir}/codeina/logo/ubuntu.png


%find_lang %{name} 

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc ChangeLog COPYING README AUTHORS
%config (noreplace) %{_sysconfdir}/codeina
%{_bindir}/%{name}
%{_bindir}/%{name}.bin
%{python_sitelib}/codeina
%{_datadir}/codeina

