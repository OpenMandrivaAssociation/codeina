%define         gst_minver      0.10.11.2
%define         gstpy_minver    0.10.0
%define         pygtk_minver    2.8.0
%define build_plf 0
%{?_with_plf: %{expand: %%global build_plf 1}}
%if %build_plf
%define distsuffix plf
%endif

Name:           codeina
Version:        0.10.7
Release:        %mkrel 10
Summary:        Codeina - Codec Installation Application

Group:          Sound
License:        GPLv2+
URL:            https://core.fluendo.com/gstreamer/trac/browser/codeina
# Upstream SVN repository is at https://core.fluendo.com/gstreamer/svn/codeina/trunk/
Source0:        http://core.fluendo.com/gstreamer/src/codeina/%{name}-%{version}.tar.bz2
Source1: http://plf.zarb.org/logo3.png
# (fc) 0.10.2-1mdv delay codeina startup at session start
Patch0:		codeina-0.10.2-delaystartup.patch
# fwang: force basename on main binary
Patch1:		codeina-0.10.7-realbasename.patch
#gw update for new distribution releases
# to regenerate this patch, run scripts/gst-scanpackages directory where directory contains packages containing all available gstreamer plugins, for all supported arch
# make sure to remove gstreamer0.10-python* package for scanned directory (GNOME bug #590806)
Patch9: codeina-0.10.7-mandriva.patch
# same patch as mandriva patch, for plf packages
Patch11: codeina-0.10.7-plf.patch

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
Provides:	gst-install-plugins-helper
Requires(post):	update-alternatives
Requires(postun): update-alternatives
BuildRequires:  python-OpenSSL
BuildRequires:  python-twisted-web
BuildRequires:  gstreamer0.10-python >= %{gstpy_minver}
BuildRequires:  python-yaml
BuildRequires:  gnome-python-gtkmozembed
BuildRequires:  python-notify
BuildRequires:  python-pyxml
BuildRequires:  pyxdg
BuildRequires:  xulrunner-devel

# sigh, libtool
BuildRequires:  gcc-c++

BuildRequires:  intltool
BuildRequires:  gettext
BuildRequires:  desktop-file-utils
Obsoletes: %name < %version-%release

%description
Codeina installs codecs from the Fluendo webshop or distribution package
for GStreamer.

%if %build_plf
This package is in PLF as it contains a list of packages that violate patents.
%endif


%prep
%setup -q 
%patch0 -p1 -b .delaystartup
%patch1 -p0 -b .orig
%patch9 -p1 -b .mandriva
%patch11 -p1 -b .plf

#needed by patches 9 & 11
aclocal -I common/m4
autoconf
automake

%build

export PROVIDER_FILES="mandrivalinux_2011.0.xml fluendo.xml" 
%if %build_plf
export PROVIDER_FILES="$PROVIDER_FILES plf_2011.0.xml"
%endif
export LD_LIBRARY_PATH=%xulrunner_mozappdir
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

%post
update-alternatives --install %{_libexecdir}/gst-install-plugins-helper gst-install-plugins-helper %{_bindir}/codeina 5

%postun
if [ "$1" = "0" ]; then
    if ! [ -e %{_bindir}/codeina ]; then
        update-alternatives --remove gst-install-plugins-helper %{_bindir}/codeina
    fi
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%dir %{_sysconfdir}/codeina
%dir %{_sysconfdir}/codeina/providers
%config (noreplace) %{_sysconfdir}/codeina/providers/fluendo.xml
%config (noreplace) %{_sysconfdir}/codeina/providers/mandrivalinux_2011.0.xml
%config (noreplace) %{_sysconfdir}/codeina/restricted-products.xml
%if %build_plf
%config (noreplace) %{_sysconfdir}/codeina/providers/plf_2011.0.xml
%endif
%config (noreplace) %{_sysconfdir}/xdg/autostart/codeina*.desktop
%{_bindir}/%{name}
%{_bindir}/%{name}.bin
%{python_sitelib}/codeina
%{_datadir}/codeina
%{_datadir}/applications/*.desktop
%defattr(644,root,root,755)
%doc ChangeLog COPYING README AUTHORS


%changelog
* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.10.7-8mdv2011.0
+ Revision: 663389
- mass rebuild

* Tue Mar 22 2011 Funda Wang <fwang@mandriva.org> 0.10.7-7
+ Revision: 647471
- rebuild

* Sat Nov 06 2010 Funda Wang <fwang@mandriva.org> 0.10.7-6mdv2011.0
+ Revision: 593818
- cannot be a noarch package

* Fri Nov 05 2010 Funda Wang <fwang@mandriva.org> 0.10.7-5mdv2011.0
+ Revision: 593625
- more specific binary name
- use alternative to setup gst plugins helper

* Thu Nov 04 2010 Götz Waschk <waschk@mandriva.org> 0.10.7-4mdv2011.0
+ Revision: 593235
- update patches 9 and 11 for 2011.0

  + Michael Scherer <misc@mandriva.org>
    - rebuild for python 2.7

  + Funda Wang <fwang@mandriva.org>
    - rebuild for py 2.7

* Thu Jun 24 2010 Frederic Crozat <fcrozat@mandriva.com> 0.10.7-1mdv2010.1
+ Revision: 549096
- Use official tarball

* Wed Jun 23 2010 Frederic Crozat <fcrozat@mandriva.com> 0.10.7-0.1mdv2010.1
+ Revision: 548691
- Release 0.10.7 (snapshot from svn, official tarball should be available soon)
- Remove patches 1, 10, 12, 13, 14, 15, 16, 17, 18 (merged upstream)

* Wed Jun 09 2010 Christophe Fergeau <cfergeau@mandriva.com> 0.10.6-6mdv2010.1
+ Revision: 547362
- fix default permissions

* Wed Jun 02 2010 Frederic Crozat <fcrozat@mandriva.com> 0.10.6-5mdv2010.1
+ Revision: 546972
- Update plf patch for 2010.1

  + Christophe Fergeau <cfergeau@mandriva.com>
    - fix file permission for doc files, fixes #59587

* Wed Feb 24 2010 Frederic Crozat <fcrozat@mandriva.com> 0.10.6-4mdv2010.1
+ Revision: 510704
- Fix build (needs xulrunner-devel)
- Regenerate patches 9 & 11 for 2010.1
- Patches 13, 14 : fix deprecated python warnings
- Patch15: fix infinite loop
- Patch16: fix urpmi installer (and fix python warnings)
- Patch17: rewrite lsb_release parser
- Patch18: strip package name
- cleanup python 2.6 warning
- rewrite lsb_release
- try to fix urpmi installer

* Thu Oct 08 2009 Frederic Crozat <fcrozat@mandriva.com> 0.10.6-3mdv2010.0
+ Revision: 456026
- Update yaml files (goetz)

* Fri Sep 11 2009 Frederic Crozat <fcrozat@mandriva.com> 0.10.6-2mdv2010.0
+ Revision: 438103
- Regenerate patches 9 and 10 for 2010.0

  + Götz Waschk <waschk@mandriva.org>
    - fix xulrunner detection (bug #53213)

* Wed Aug 26 2009 Götz Waschk <waschk@mandriva.org> 0.10.6-1mdv2010.0
+ Revision: 421545
- new version
- drop patch 13

* Wed Aug 26 2009 Götz Waschk <waschk@mandriva.org> 0.10.5.1-1mdv2010.0
+ Revision: 421493
- new version
- make it work on x86_64 (bug #52876)

  + Wanderlei Cavassin <cavassin@mandriva.com.br>
    - pt_BR translation fixes

* Fri Jun 05 2009 Frederic Crozat <fcrozat@mandriva.com> 0.10.5-2mdv2010.0
+ Revision: 383029
- Remove translations tarball, was merged upstream

* Fri Jun 05 2009 Frederic Crozat <fcrozat@mandriva.com> 0.10.5-1mdv2010.0
+ Revision: 383027
- Update patch11
- Release 0.10.5
- Fix url for source file
- Remove patches 1, 2, 3, 4, 5, 6, 7, 8 (merged upstream)
- Regenerate patches 9 and 11 for cooker and add missing packages

* Sun Apr 12 2009 Götz Waschk <waschk@mandriva.org> 0.10.2-24mdv2009.1
+ Revision: 366491
- fix plf patch

* Sun Mar 29 2009 Götz Waschk <waschk@mandriva.org> 0.10.2-23mdv2009.1
+ Revision: 362107
- update providers without non-free packages (bug #49272)

* Sun Mar 22 2009 Götz Waschk <waschk@mandriva.org> 0.10.2-22mdv2009.1
+ Revision: 360534
- fix patch 11
- silent: bump
- regenerate data

* Fri Mar 06 2009 Frederic Crozat <fcrozat@mandriva.com> 0.10.2-20mdv2009.1
+ Revision: 349768
- Only ship autostart file in /etc/xdg, otherwise codeina is started twice in KDE4

* Mon Feb 16 2009 Götz Waschk <waschk@mandriva.org> 0.10.2-19mdv2009.1
+ Revision: 340818
- update plf patch

  + Frederic Crozat <fcrozat@mandriva.com>
    - Split patch9 in two parts, one Mandriva, another PLF
    - Update patch9 with latest package list for 2009.1 (Mdv bug #38625)

* Tue Jan 06 2009 Götz Waschk <waschk@mandriva.org> 0.10.2-18mdv2009.1
+ Revision: 326444
- don't depend on python 2.5 anymore

* Fri Dec 26 2008 Adam Williamson <awilliamson@mandriva.org> 0.10.2-17mdv2009.1
+ Revision: 319466
- rebuild with python 2.6

* Thu Oct 23 2008 Götz Waschk <waschk@mandriva.org> 0.10.2-16mdv2009.1
+ Revision: 296692
- initial 2009.1 support

* Wed Sep 03 2008 Götz Waschk <waschk@mandriva.org> 0.10.2-15mdv2009.0
+ Revision: 279705
- update 2009.0 patch

* Tue Aug 19 2008 Frederic Crozat <fcrozat@mandriva.com> 0.10.2-14mdv2009.0
+ Revision: 273862
- Add dependency on gurpmi

* Thu Aug 07 2008 Götz Waschk <waschk@mandriva.org> 0.10.2-13mdv2009.0
+ Revision: 266360
- update patch 3 for xulrunner (bug #42567)

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 0.10.2-12mdv2009.0
+ Revision: 264357
- rebuild early 2009.0 package (before pixel changes)

* Wed May 14 2008 Götz Waschk <waschk@mandriva.org> 0.10.2-11mdv2009.0
+ Revision: 207314
- update 2009.0 patch

* Wed Apr 23 2008 Götz Waschk <waschk@mandriva.org> 0.10.2-10mdv2009.0
+ Revision: 196790
- initial patch for 2009.0 support

* Thu Apr 03 2008 Frederic Crozat <fcrozat@mandriva.com> 0.10.2-10mdv2008.1
+ Revision: 192277
- Update patch10 with new version from upstream, fix Mdv bug #39765

* Thu Apr 03 2008 Frederic Crozat <fcrozat@mandriva.com> 0.10.2-9mdv2008.1
+ Revision: 192211
- Patch8 (SVN): only notify updates for Fluendo media (Mdv bug #39746)

* Thu Apr 03 2008 Frederic Crozat <fcrozat@mandriva.com> 0.10.2-8mdv2008.1
+ Revision: 192177
- Patch7 (SVN); handle multiple codec requests in one transaction

* Wed Apr 02 2008 Frederic Crozat <fcrozat@mandriva.com> 0.10.2-7mdv2008.1
+ Revision: 191701
- Suggests libstdc++5, needed for some fluendo codec

* Wed Apr 02 2008 Frederic Crozat <fcrozat@mandriva.com> 0.10.2-6mdv2008.1
+ Revision: 191679
- Patch6 (SVN): handle more http return code

* Fri Mar 28 2008 Frederic Crozat <fcrozat@mandriva.com> 0.10.2-5mdv2008.1
+ Revision: 190826
- Patch5: fixes from SVN : reduce browser window size, add distro version to url
- Add more translations

* Wed Mar 26 2008 Frederic Crozat <fcrozat@mandriva.com> 0.10.2-4mdv2008.1
+ Revision: 190253
- Translation updates

* Tue Mar 25 2008 Frederic Crozat <fcrozat@mandriva.com> 0.10.2-3mdv2008.1
+ Revision: 190015
- Update patch3 to not crash on x86 system
- Patch4 (SVN): don't popup when not finding codec (Mdv bug #39237)

* Tue Mar 25 2008 Frederic Crozat <fcrozat@mandriva.com> 0.10.2-2mdv2008.1
+ Revision: 189978
- Patch3 (Eric Pielbug): fix firefox detection (Mdv bug #39239)
- Source2: translations for Mandriva i18n teams

* Fri Mar 21 2008 Frederic Crozat <fcrozat@mandriva.com> 0.10.2-1mdv2008.1
+ Revision: 189407
- Release 0.10.2 final
- Patch0: delay checking update 5min after session startup
- Patch1: improve buttons and layout in install dialog
- Patch2: don't complain about missing network when only checking updates at startup

* Tue Mar 18 2008 Frederic Crozat <fcrozat@mandriva.com> 0.10.2-0.beta4.3mdv2008.1
+ Revision: 188578
- Patch0 (SVN): handle lib64 install (Mdv bug #38989)

* Mon Mar 17 2008 Götz Waschk <waschk@mandriva.org> 0.10.2-0.beta4.2mdv2008.1
+ Revision: 188403
- drop the patch
- fix plf build

* Mon Mar 17 2008 Frederic Crozat <fcrozat@mandriva.com> 0.10.2-0.beta4.1mdv2008.1
+ Revision: 188377
- Release 0.10.2 beta4

* Fri Mar 14 2008 Götz Waschk <waschk@mandriva.org> 0.10.2-0.beta3.2mdv2008.1
+ Revision: 187838
- add plf id and logo support
- add third party plf repo support (disabled by default

  + Frederic Crozat <fcrozat@mandriva.com>
    - New snapshot :
     - add menu entry and auto-updater at session start
     - official support for 2008.1
     - change comment for codeina-shop.desktop

* Wed Mar 12 2008 Frederic Crozat <fcrozat@mandriva.com> 0.10.2-0.beta3.1mdv2008.1
+ Revision: 187151
- import codeina


