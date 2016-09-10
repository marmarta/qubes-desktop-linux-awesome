%if 0%{?qubes_builder}
%define _sourcedir %(pwd)
%endif

Name:		awesome
Version:	3.5.9
Release:	1%{?dist}
Epoch:		1000
Summary:	Highly configurable, framework window manager for X. Fast, light and extensible
Group:		User Interface/Desktops
# common/buffer.[ch]: BSD
License:	GPLv2+ and BSD
URL:		http://awesome.naquadah.org
Source0:	http://awesome.naquadah.org/download/%{name}-%{version}.tar.xz
Patch0:		awesome-3.5.9-lua-generic.patch
Patch1:		awesome-3.5.5-use-vi-instead-of-nano.patch
Patch100:	awesome-3.5.5-qubes-prefix.patch
Patch110:	awesome-3.5.5-qubes.patch
Patch120:	awesome-3.5.5-dex-autostart.patch

BuildRequires:	cmake >= 3.0.0

BuildRequires:	ImageMagick
BuildRequires:	asciidoc
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	lua-devel >= 5.2
BuildRequires:	lua-ldoc
BuildRequires:	xmlto
BuildRequires:	gcc-c++

BuildRequires:	pkgconfig(xcb) >= 1.6
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(xcb-randr)
BuildRequires:	pkgconfig(xcb-xtest)
BuildRequires:	pkgconfig(xcb-xinerama)
BuildRequires:	pkgconfig(xcb-shape)
BuildRequires:	pkgconfig(xcb-util) >= 0.3.8
BuildRequires:	pkgconfig(xcb-keysyms) >= 0.3.4
BuildRequires:	pkgconfig(xcb-icccm) >= 0.3.8
BuildRequires:	pkgconfig(xcb-cursor)
BuildRequires:	pkgconfig(cairo-xcb)
BuildRequires:	pkgconfig(libstartup-notification-1.0) >= 0.10
BuildRequires:	pkgconfig(xproto) >= 7.0.15
BuildRequires:	pkgconfig(libxdg-basedir) >= 1.0.0
BuildRequires:	pkgconfig(dbus-1)

BuildRequires:	lua-lgi
BuildRequires:	pkgconfig(pango) >= 1.19.3
BuildRequires:	pkgconfig(pangocairo) >= 1.19.3
Requires:	lua-lgi
# next two loaded via lgi
Requires:	pango%{?_isa} >= 1.19.3
Requires:	cairo-gobject%{?_isa}

BuildRequires:	desktop-file-utils
Requires:	startup-notification >= 0.10
# terminal used in the default configuration
Requires:	xterm
# optional but useful
Requires:	rlwrap
# default editor
Requires:	vi
# XDG Autostart functionality
Requires:	dex-autostart


%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}


%description
Awesome is a highly configurable, next generation framework window
manager for X. It is very fast, light and extensible.

It is primary targeted at power users, developers and any people
dealing with every day computing tasks and want to have fine-grained
control on its graphical environment.


%package	doc
Summary:	API doc files
Group:		Documentation
BuildArch:	noarch
Requires:	%{name} = %{version}-%{release}

%description	doc
API doc files for awesome generated by luadoc.


%prep
%setup -q
%patch0 -p1 -b .lua-generic
%patch1 -p1 -b .use-vi-instead-of-nano

%patch100 -p1 -b .qubes-prefix
%patch110 -p1 -b .qubes
%patch120 -p1 -b .dex-autostart


%build
mkdir build; pushd build
%cmake -DAWESOME_DOC_PATH=%{_pkgdocdir} \
       -DSYSCONFDIR=%{_sysconfdir} \
       ..
popd
make -C build VERBOSE=1 %{?_smp_mflags} awesome


%install
make -C build DESTDIR="%{buildroot}" INSTALL="install -p" install

# verify desktop file
desktop-file-validate %{buildroot}%{_datadir}/xsessions/%{name}.desktop


%files
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/*
%exclude %{_pkgdocdir}/doc
%dir %{_sysconfdir}/xdg/%{name}
%config(noreplace) %{_sysconfdir}/xdg/%{name}/rc.lua
%{_bindir}/awesome
%{_bindir}/awesome-client
%{_datadir}/%{name}
%{_mandir}/man?/*
%{_mandir}/*/man1/*
%{_mandir}/*/man5/*
%{_datadir}/xsessions/%{name}.desktop


%files doc
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/doc


%changelog
* Sat Oct 25 2014 Wojciech Porczyk <woju@invisiblethingslab.com> - 3.5.5-4
- qubes patches

* Fri Oct 24 2014 Wojciech Porczyk <woju@invisiblethingslab.com> - 3.5.5-3
- qubes builder features

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 11 2014 Thomas Moschny <thomas.moschny@gmx.de> - 3.5.5-1
- Update to 3.5.5.

* Wed Apr  2 2014 Thomas Moschny <thomas.moschny@gmx.de> - 3.5.4-1
- Update to 3.5.4.

* Wed Apr  2 2014 Thomas Moschny <thomas.moschny@gmx.de> - 3.5.3-1
- Update to 3.5.3.
- Remove dependency on libev, and a related patch.
- Remove dependency on xcb-image.
- Add dependency on xcb-cursor.
- Simplify cmake invocation.

* Sun Aug 18 2013 Thomas Moschny <thomas.moschny@gmx.de> - 3.5.1-8
- Define (if undefined) and use _pkgdocdir macro (rhbz#993678).
- Fix bogus dates in the %%changelog.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 28 2013 Thomas Moschny <thomas.moschny@gmx.de> - 3.5.1-6
- Add vi as explicit requirement.
- Add requirement on cairo-gobject, should fix rhbz#959169.

* Sat May 25 2013 Thomas Moschny <thomas.moschny@gmx.de> - 3.5.1-5
- Remove obsolete BR on gperf.

* Mon May 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.5.1-4
- Set default editor to vi
- Resolves: rhbz#964945

* Mon May 13 2013 Tom Callaway <spot@fedoraproject.org> - 3.5.1-3
- rebuild for lua 5.2

* Thu Apr  4 2013 Thomas Moschny <thomas.moschny@gmx.de> - 3.5.1-2
- The Lua GObject introspection package is needed at runtime.

* Wed Apr  3 2013 Thomas Moschny <thomas.moschny@gmx.de> - 3.5.1-1
- Update to 3.5.1.
- Rework BR section:
  - Replace imlib2 with gdk-pixbuf-2.0.
  - Replace luadoc with lua-ldoc.
  - Add lua-lgi.

* Sat Mar 16 2013 Thomas Moschny <thomas.moschny@gmx.de> - 3.4.15-1
- Update to 3.4.15.
- Add patch from upstream to fix rhbz#901434.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan  4 2013 Thomas Moschny <thomas.moschny@gmx.de> - 3.4.14-1
- Update to 3.4.14.
- Update buildrequires.

* Tue Aug 21 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.4.13-2
- Rebuilt for libxcb-util soname bump

* Wed Jul 18 2012 Thomas Moschny <thomas.moschny@gmx.de> - 3.4.13-1
- Update to 3.4.13.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 16 2012 Thomas Moschny <thomas.moschny@gmx.de> - 3.4.12-1
- Update to 3.4.12.
- Remove patches applied upstream.

* Wed May 30 2012 Thomas Moschny <thomas.moschny@gmx.de> - 3.4.11-5
- Update License tag.
- Fix permissions of generated HTML docs.
- Patch and validate the .desktop file.

* Thu May 24 2012 Thomas Moschny <thomas.moschny@gmx.de> - 3.4.11-4
- Specfile cleanups.

* Fri Apr  6 2012 Thomas Moschny <thomas.moschny@gmx.de> - 3.4.11-3
- Rebuilt.

* Wed Dec 14 2011 Thomas Moschny <thomas.moschny@gmx.de> - 3.4.11-2
- Add patch to build against glib2 2.31.0 and later.

* Mon Dec  5 2011 Thomas Moschny <thomas.moschny@gmx.de> - 3.4.11-1
- Update to 3.4.11, add patch for older Fedora releases.
- Add dependencies on xterm and rlwrap.
- Rework BR section.

* Tue Sep 27 2011 Thomas Moschny <thomas.moschny@gmx.de> - 3.4.10-3
- Remove dependency on xsri.

* Mon Sep 26 2011 Thomas Moschny <thomas.moschny@gmx.de> - 3.4.10-2
- Rebuilt for newer cairo rpm.

* Sun May 22 2011 Thomas Moschny <thomas.moschny@gmx.de> - 3.4.10-1
- Update to 3.4.10.
- Add dependencies to ease installation.

* Mon Jan 17 2011 Michal Nowak <mnowak@redhat.com> 3.4.9-1
- 3.4.9
- require cmake >= 2.8.0

* Mon Oct 18 2010 Michal Nowak <mnowak@redhat.com> 3.4.8-1
- 3.4.8

* Thu Aug 26 2010 Michal Nowak <mnowak@redhat.com> 3.4.7-1
- 3.4.7

* Fri Jul 23 2010 Michal Nowak <mnowak@redhat.com> 3.4.6-1
- 3.4.6

* Mon May 17 2010 Michal Nowak <mnowak@redhat.com> 3.4.5-1
- 3.4.5
- we ship non-English man pages with this release

* Thu Mar  4 2010 Michal Nowak <mnowak@redhat.com> 3.4.4-1
- 3.4.4

* Mon Jan  4 2010 Michal Nowak <mnowak@redhat.com> 3.4.3-1
- 3.4.3
- .in files are finally not installed anymore

* Wed Dec  2 2009 Michal Nowak <mnowak@redhat.com> 3.4.2-1
- 3.4.2
- use xz instead of bz2

* Sun Nov 22 2009 Michal Nowak <mnowak@redhat.com> 3.4.1-1
- 3.4.1

* Thu Oct 22 2009 Michal Nowak <mnowak@redhat.com> 3.4-1
- 3.4

* Mon Oct 12 2009 Michal Nowak <mnowak@redhat.com> 3.4-0.3.rc3
- 3.4~rc3

* Tue Oct  6 2009 Michal Nowak <mnowak@redhat.com> 3.4-0.2.rc2
- remove .in files in build root rather in source dir

* Mon Oct  5 2009 Michal Nowak <mnowak@redhat.com> 3.4-0.1.rc2
- 3.4-rc2

* Fri Sep 18 2009 Jens Petersen <petersen@redhat.com> - 3.3.4-3
- integrate rctag macro
- simplify removal of .in files and filelist

* Wed Sep 16 2009 Michal Nowak <mnowak@redhat.com> 3.3.4-2
- libxdg-basedir-devel as BR

* Wed Sep 16 2009 Michal Nowak <mnowak@redhat.com> 3.3.4-1
- 3.3.4
- BuildRequire: ImageMagick, libxdg-basedir

* Sat Aug 29 2009 Michal Nowak <mnowak@redhat.com> 3.3.3-1
- 3.3.3

* Sat Aug  1 2009 Michal Nowak <mnowak@redhat.com> 3.3.2-1
- 3.3.2

* Mon Jun 22 2009 Michal Nowak <mnowak@redhat.com> 3.3.1-1
- 3.3.1

* Fri Jun 12 2009 Michal Nowak <mnowak@redhat.com> 3.3-1
- 3.3

* Thu May 28 2009 Michal Nowak <mnowak@redhat.com> 3.3-0.4.rc4
- 3.3-rc4

* Tue May 19 2009 Michal Nowak <mnowak@redhat.com> 3.3-0.3.rc3
- 3.3-rc3

* Wed May 13 2009 Michal Nowak <mnowak@redhat.com> 3.3-0.2.rc2
- 3.3-rc2

* Thu May  7 2009 Michal Nowak <mnowak@redhat.com> 3.3-0.1.rc1
- 3.3-rc1

* Mon Mar 16 2009 Michal Nowak <mnowak@redhat.com> 3.2-1
- 3.2

* Mon Mar  2 2009 Michal Nowak <mnowak@redhat.com> 3.2-0.2.rc4
- 3.2-rc4

* Fri Feb 20 2009 Michal Nowak <mnowak@redhat.com> 3.2-0.1.rc3
- 3.2-rc3
- more docs files

* Tue Jan 13 2009 Michal Nowak <mnowak@redhat.com> 3.1.1-1
- 3.1.1

* Wed Dec 24 2008 Michal Nowak <mnowak@redhat.com> 3.1-2
- minor SPEC-file changes

* Sun Dec 14 2008 Michal Nowak <mnowak@redhat.com> 3.1-1
- 3.1

* Fri Sep 19 2008 Michal Nowak <mnowak@redhat.com> 3.0-1
- bump to 3.0

* Sat Sep 06 2008 Michal Nowak <mnowak@redhat.com> 3.0-0.8.rc6
- bump to RC6
- /usr/share/awesome/themes/default is now, again, config file

* Fri Aug 29 2008 Michal Nowak <mnowak@redhat.com> 3.0-0.7.rc5
- bump to RC5

* Sun Aug 24 2008 Michal Nowak <mnowak@redhat.com> 3.0-0.6.rc4
- bump to RC4
- rejecting awesome-3.0-rc3-enhance-wallpaper-cmd.patch -- solved
  upstream via awsetbg script
- using imlib2 instead of GTK+ pixbuf

* Mon Aug 18 2008 Michal Nowak <mnowak@redhat.com> 3.0-0.5.rc3
- buildepend on readline-devel, glib2-devel, gtk2-devel, luadoc
- install via "install -p"
- %%{_datadir}/%%{name}/themes/default is not a config file no more,
  having config file in /usr is kinda weird
- added sub-package awesome-doc to handle API doc files

* Sat Aug 16 2008 Michal Nowak <mnowak@redhat.com> 3.0-0.4.rc3
- awesome-3.0-rc3-enhance-wallpaper-cmd.patch: enhance setting of wallpaper
- new dep: xsri
- %%{_datadir}/%%{name}/themes/default is now handled configfile

* Fri Aug 15 2008 Michal Nowak <mnowak@redhat.com> 3.0-0.3.rc3
- bump to RC3
- xsession desktop file is now provided by upstream
- dumped patches
	awesome-3.0-rc1-fedora-doc-path.patch
	awesome-3.0-rc2-fedora-xsession-path.patch
  both are now in upstream
- cmake is now need >2.6 (present in rawhide)

* Mon Aug 11 2008 Michal Nowak <mnowak@redhat.com> 3.0-0.2.rc2
- bump to RC2

* Mon Aug 04 2008 Michal Nowak <mnowak@redhat.com> 3.0-0.1.rc1
- bump to awesome v3-the new generation

* Mon Jul 28 2008 Michal Nowak <mnowak@redhat.com> 2.3.3-1
- version bump fixes two bugs
- give floating dialogs of maximized windows focus
- awesomerc: fix xterm -e in case of others terms

* Thu Jul 17 2008 Michal Nowak <mnowak@redhat.com> 2.3.2-7
- after some discussion I removed explicit dependency on libconfuse >= 2.6;
  the thing is that awesome runs fine with libconfuse-2.5 but does not
  build with < 2.6. Some build-time hack might be possible but I am obviously
  not going to be involved in this auto*magic. (thx Hans Ulrich Niedermann)

* Wed Jul 16 2008 Michal Nowak <mnowak@redhat.com> 2.3.2-6
- added libXinerama-devel, hopefully last BuildRequire

* Wed Jul 16 2008 Michal Nowak <mnowak@redhat.com> 2.3.2-5
- by mistake I removed BuildRequire on libconfuse-devel,
  now is back again (thanks Mamoru Tasaka)

* Tue Jul 15 2008 Michal Nowak <mnowak@redhat.com> 2.3.2-4
- small polishing in %%doc line

* Mon Jul 14 2008 Michal Nowak <mnowak@redhat.com> 2.3.2-3
- removed redundant libconfuse-devel in BuildRequires
- %%{__install} .desktop file instead of install via desktop-file-install
- changed the license to GPLv2+
- changes in .desktop file
- updated --docdir to include %%{version} too

* Thu Jul 10 2008 Michal Nowak <mnowak@redhat.com> 2.3.2-2
- bumped libconfuse BuildDependency to insist on version 2.6
- changed buildroot to not to have random one
- enhanced %%description

* Thu Jul 3 2008 Michal Nowak <mnowak@redhat.com> 2.3.2-1
- version bump
- add libconfuse-devel as a build dep.
- removed Fedora as a vendor from .desktop file

* Sun Jun 22 2008 Michal Nowak <mnowak@redhat.com> 2.3.1-1
- Initial package
