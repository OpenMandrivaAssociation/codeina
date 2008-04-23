%define         gst_minver      0.10.11.2
%define         gstpy_minver    0.10.0
%define         pygtk_minver    2.8.0
%define build_plf 0
%{?_with_plf: %{expand: %%global build_plf 1}}
%if %build_plf
%define distsuffix plf
%endif

Name:           codeina
Version:        0.10.2
Release:        %mkrel 10
Summary:        Codeina - Codec Installation Application

Group:          Sound
License:        GPLv2+
URL:            https://core.fluendo.com/gstreamer/trac/browser/codeina
# Upstream SVN repository is at https://core.fluendo.com/gstreamer/svn/codeina/trunk/
Source0:         http://www.fluendo.com/downloads/codeina/%{name}-%{version}.tar.bz2
Source1: http://plf.zarb.org/logo3.png
# (fc) 0.10.2-2mdv additional translations (forwarded upstream)
Source2:	codeina-0.10.2-po.tar.bz2
# (fc) 0.10.2-1mdv delay codeina startup at session start
Patch0:		codeina-0.10.2-delaystartup.patch
# (fc) 0.10.2-1mdv improve button in install dialog
Patch1:		codeina-0.10.2-improvelayout.patch
# (fc) 0.10.2-1mdv don't complain about missing network when checking update at session startup
Patch2:		codeina-0.10.2-nonetworknoupdate.patch
# (fc) 0.10.2-2mdv improve Gecko detection (Mdv bug #39239)
Patch3:		codeina-0.10.2-improvegeckodetection.patch
# (fc) 0.10.2-2mdv don't open a popup when no codec is found (Mdv bug #39237)
Patch4:		codeina-0.10.2-nopopup.patch
# (fc) 0.10.2-5mdv SVN fixes (change default size for browser windows, add distribution version to url)
Patch5:		codeina-0.10.2-svnfixes.patch
# (fc) 0.10.2-6mdv handle more http return value (SVN)
Patch6:		codeina-0.10.2-httpcode.patch
# (fc) 0.10.2-8mdv handle multiple codec request in one transaction (SVN)
Patch7:		codeina-0.10.2-multiplecodec.patch
# (fc) 0.10.2-9mdv only notify updates for Fluendo media (Mdv bug #39746) (SVN)
Patch8:		codeina-0.10.2-notifyonlyfluendo.patch
#gw update for 2009.0 distribution version
Patch9: codeina-0.10.2-2009.0.patch
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
Suggests:	libstdc++5

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

%if %build_plf
This package is in PLF as it contains a list of packages that violate patents.
%endif


%prep
%setup -q -b 2
%patch0 -p1 -b .delaystartup
%patch1 -p1 -b .improvelayout
%patch2 -p1 -b .nonetworknoupdate
%patch3 -p1 -b .improvegeckodetection
%patch4 -p1 -b .nopopup
%patch5 -p1 -b .svnfixes
%patch6 -p1 -b .httpcode
%patch7 -p1 -b .multiplecodec
%patch8 -p1 -b .notifyonlyfluendo
cp providers/mandrivalinux_2008.1.tmpl providers/mandrivalinux_2009.0.tmpl
cp providers/plf_2008.1.tmpl providers/plf_2009.0.tmpl
cp providers/plf_2008.1.yaml providers/plf_2009.0.yaml
%patch9 -p0 -b .2009.0

%build

export PROVIDER_FILES="mandrivalinux_%mandriva_release.xml fluendo.xml" 
%if %build_plf
export PROVIDER_FILES="$PROVIDER_FILES plf_%mandriva_release.xml"
%endif
%configure2_5x

make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std

rm -f $RPM_BUILD_ROOT%{_datadir}/codeina/logo/ubuntu.png

%find_lang %{name} 

%if %build_plf
install -m 644 %SOURCE1 %buildroot%_datadir/codeina/logo/plf.png
%endif

# no longer needed 
rm -f %buildroot%{_sysconfdir}/codeina/codeina_legal.html

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc ChangeLog COPYING README AUTHORS
%dir %{_sysconfdir}/codeina
%dir %{_sysconfdir}/codeina/providers
%config (noreplace) %{_sysconfdir}/codeina/providers/fluendo.xml
%config (noreplace) %{_sysconfdir}/codeina/providers/mandrivalinux_%mandriva_release.xml
%config (noreplace) %{_sysconfdir}/codeina/restricted-products.xml
%if %build_plf
%config (noreplace) %{_sysconfdir}/codeina/providers/plf_%mandriva_release.xml
%endif
%config (noreplace) %{_sysconfdir}/xdg/autostart/codeina*.desktop
%{_bindir}/%{name}
%{_bindir}/%{name}.bin
%{python_sitelib}/codeina
%{_datadir}/codeina
%{_datadir}/applications/*.desktop
%{_datadir}/autostart/*.desktop
