%define         gst_minver      0.10.11.2
%define         gstpy_minver    0.10.0
%define         pygtk_minver    2.8.0
%define build_plf 0
%{?_with_plf: %{expand: %%global build_plf 1}}
%if %build_plf
%define distsuffix plf
%endif

Name:           codeina
Version:        0.10.6
Release:        %mkrel 4
Summary:        Codeina - Codec Installation Application

Group:          Sound
License:        GPLv2+
URL:            https://core.fluendo.com/gstreamer/trac/browser/codeina
# Upstream SVN repository is at https://core.fluendo.com/gstreamer/svn/codeina/trunk/
Source0:        http://core.fluendo.com/gstreamer/src/codeina/%{name}-%{version}.tar.bz2
Source1: http://plf.zarb.org/logo3.png
# (fc) 0.10.2-1mdv delay codeina startup at session start
Patch0:		codeina-0.10.2-delaystartup.patch
#gw fix crash on startup trying to load xulrunner
#https://qa.mandriva.com/show_bug.cgi?id=53213
Patch1: codeina-0.10.6-xulrunner.patch
# (fc) fix python version used for codeina
Patch10: codeina-0.10.2-python-version.patch
#gw update for new distribution releases
# to regenerate this patch, run scripts/gst-scanpackages directory where directory contains packages containing all available gstreamer plugins, for all supported arch
Patch9: codeina-0.10.6-mandriva.patch
# same patch as mandriva patch, for plf packages
Patch11: codeina-0.10.6-plf.patch
Patch12: codeina-0.10.5-pt_BR-fixes.patch
# various bug fixes (fcrozat)
Patch13: 0001-remove-deprecated-python-calls-sets.patch
Patch14: 0002-sha-is-deprecated-use-hashlib-instead.patch
Patch15: 0003-fix-infinite-loop.patch
Patch16: 0004-fix-deprecation-ensure-urpmi-installer-is-working.patch
Patch17: 0005-rewrite-lsb_release-parsing-code-to-not-call-lsb_rel.patch
Patch18: 0006-strip-package-name.patch

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
Requires:	gurpmi
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
%setup -q 
%patch0 -p1 -b .delaystartup
%patch1 -p1
%patch10 -p1 -b .version
%patch9 -p1 -b .mandriva
%patch11 -p1 -b .plf
%patch12 -p1 -b .pt_BR_fixes
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1

#needed by patch11
aclocal -I common/m4
autoconf
automake

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
# remove autostart in /usr/share, use those in /etc/xdg
rm -rf %buildroot%{_datadir}/autostart

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
