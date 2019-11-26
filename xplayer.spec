%define major		0
%define gi_major	1.0
%define libname		%mklibname %{name} %{major}
%define develname	%mklibname %{name} -d
%define girname		%mklibname %{name}-gir %{gi_major}

%define build_zeitgeist_plugin 1

Name:           xplayer
Version:        2.0.2
Release:        %mkrel 3
Summary:        Generic media player
License:        GPL-2.0+ and LGPL-2.1+
Group:          Video/Players
Url:            https://github.com/linuxmint/xplayer
Source:         https://github.com/linuxmint/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  gcc-c++
BuildRequires:  gnome-common
BuildRequires:  gstreamer1.0-plugins-good >= 0.11.93
# For gst-inspect tool
BuildRequires:  gstreamer1.0-tools >= 0.11.93
BuildRequires:  pkgconfig(liblircclient0)
BuildRequires:  vala >= 0.14.1
BuildRequires:  yelp-tools
BuildRequires:  pkgconfig(%{name}-plparser)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(clutter-1.0) >= 1.10.0
BuildRequires:  pkgconfig(clutter-gtk-1.0) >= 1.0.2
BuildRequires:  pkgconfig(dbus-glib-1) >= 0.82
BuildRequires:  pkgconfig(glib-2.0) >= 2.33.0
BuildRequires:  pkgconfig(grilo-0.3)
BuildRequires:  pkgconfig(gsettings-desktop-schemas)
BuildRequires:  pkgconfig(gstreamer-1.0) >= 0.11.93
BuildRequires:  pkgconfig(gstreamer-plugins-bad-1.0) >= 1.0.2
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0) >= 0.11.93
BuildRequires:  pkgconfig(gstreamer-tag-1.0)
BuildRequires:  pkgconfig(gtk+-3.0) >= 3.5.2
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(iso-codes)
BuildRequires:  pkgconfig(libepc-ui-1.0) > 0.4.0
BuildRequires:  pkgconfig(libpeas-1.0) >= 1.1.0
BuildRequires:  pkgconfig(libxml-2.0) >= 2.6.0
BuildRequires:  pkgconfig(pygobject-3.0) >= 2.90.3
BuildRequires:  pkgconfig(shared-mime-info)
BuildRequires:  pkgconfig(sm)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xapp)
# Needed for scaletempo (boo#810378, boo#809854).
Requires:       gstreamer1.0-plugins-bad
# We want a useful set of plugins.
Requires:       gstreamer1.0-plugins-base
Requires:       gstreamer1.0-plugins-good
Requires:       iso-codes
Requires:	grilo-plugins
Requires:	gstreamer1.0-soundtouch
Requires:	%arch_tagged gstreamer1(element-scaletempo)
Requires:	gstreamer1.0-soup
Recommends:	gstreamer1.0-resindvd
Recommends:	gstreamer1.0-a52dec
Recommends:	gstreamer1.0-libav
Recommends:     %{name}-lang
Recommends:     %{name}-plugins
Suggests:       gnome-dvb-daemon
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(clutter-gst-3.0) >= 2.99.2
# Required for cluttersink.
Requires:       gstreamer1.0-gstclutter3
BuildRequires:  itstool

%if %{build_zeitgeist_plugin}
BuildRequires:  pkgconfig(zeitgeist-2.0) >= 0.9.12
%else
Obsoletes:      xplayer-plugin-zeitgeist <= %{version}
%endif

Obsoletes:	xplayer-browser-plugin <= %{version}-%{release}
Obsoletes:	xplayer-browser-plugin-gmp <= %{version}-%{release}
Obsoletes:	xplayer-browser-plugin-vegas <= %{version}-%{release}

BuildRequires:	python3-devel
BuildRequires:	python3-pylint

%description
xplayer is a media player based on GStreamer for the Cinnamon
desktop and others. It features a playlist, a full-screen mode,
seek and volume controls, and complete keyboard navigation.

%package plugins
Summary:        Plugins for xplayer media player
Group:          Video/Players
Requires:       %{name} = %{version}
# Brasero plugin.
Recommends:     brasero
# BBC iPlayer plugin.
Recommends:     python3-beautifulsoup
Recommends:     python3-httplib2
# Gromit Annotation plugin.
Suggests:       gromit

%description plugins
xplayer is a media player based on GStreamer for the Cinnamon
desktop and others. It features a playlist, a full-screen mode,
seek and volume controls, and complete keyboard navigation.

This package includes plugins for xplayer, to add advanced features.

%if %{build_zeitgeist_plugin}
%package plugin-zeitgeist
Summary:        Plugins for xplayer media player -- Zeitgeist Support
Group:          Video/Players
Requires:       %{name} = %{version}
Supplements:    packageand(%{name}:zeitgeist)

%description plugin-zeitgeist
xplayer is a media player based on GStreamer for the Cinnamon
desktop and others. It features a playlist, a full-screen mode,
seek and volume controls, and complete keyboard navigation.

This package includes the Zeitgeist plugin for xplayer.
%endif

%package devel
Summary:        Development files for xplayer media player
Group:          System/Libraries
Requires:       %{name} = %{version}

%description devel
xplayer is a media player based on GStreamer for the Cinnamon
desktop and others. It features a playlist, a full-screen mode,
seek and volume controls, and complete keyboard navigation.

This package contains files for development.

%package doc
Summary:	Documentation files for %{name}
BuildArch:	noarch
BuildRequires:	gtk-doc

%description doc
This package contains the documentation files for %{name}.



%lang_package

%prep
%autosetup -p1

# Fix shebang to python3.
f="data/%{name}-bugreport.py"
%{__sed} -e 's~^#!%{_bindir}/python$~#!%{__python3}~'		\
	< ${f} > ${f}.new
/bin/touch -r ${f} ${f}.new
%{__mv} -f ${f}.new ${f}

%build
NOCONFIGURE=1 gnome-autogen.sh
export BROWSER_PLUGIN_DIR=%{_libdir}/browser-plugins/
export PYTHON=%{__python3}
%configure2_5x \
  --disable-static \
  --disable-Werror \
  --enable-gtk-doc \
  --enable-introspection
%make_build

%install
%make_install
# Remove SWF (#72417) and any Real (#72985) MIME types.
sed -i ':1;s/^\(MimeType=.*\);[^;]*\(real\|shockwave-flash\)[^;]*/\1/;t1' \
  %{buildroot}%{_datadir}/applications/%{name}.desktop
%find_lang %{name} --with-gnome
find %{buildroot} -type f -name "*.la" -delete -print

%files -f %{name}.lang
%doc AUTHORS COPYING ChangeLog NEWS README
%{_bindir}/%{name}*
%{_datadir}/applications/*.desktop
%{_datadir}/glib-2.0/schemas/org.x.player.enums.xml
%{_datadir}/glib-2.0/schemas/org.x.player.gschema.xml
%{_datadir}/icons/hicolor/*/apps/%{name}*.*
%{_datadir}/icons/hicolor/*/devices/%{name}*.*
%{_datadir}/icons/hicolor/*/actions/%{name}*.*
%dir %{_datadir}/thumbnailers/
%{_datadir}/thumbnailers/%{name}.thumbnailer
%{_datadir}/%{name}/
%{_mandir}/man?/%{name}*.*
# Own directories for plugins.
%dir %{_libdir}/%{name}/
%dir %{_libdir}/%{name}/plugins/
# Be careful here: libdir contains plugins while libexecdir
# contains a small utility for the main package.
%if "%{_libdir}" != "%{_libexecdir}"
%dir %{_libexecdir}/%{name}/
%endif
%{_libexecdir}/%{name}/%{name}-bugreport.py*
%{_libexecdir}/%{name}/__pycache__/
%{_libdir}/lib%{name}.so.*
%{_libdir}/girepository-1.0/Xplayer-1.0.typelib

%files plugins
# Explicitly list plugins.
%{_libdir}/%{name}/plugins/apple-trailers/
%{_libdir}/%{name}/plugins/autoload-subtitles/
%{_libdir}/%{name}/plugins/brasero-disc-recorder/
%{_libdir}/%{name}/plugins/chapters/
%{_libdir}/%{name}/plugins/dbus/
%{_libdir}/%{name}/plugins/grilo/
%{_libdir}/%{name}/plugins/gromit/
%{_libdir}/%{name}/plugins/im-status/
%{_libdir}/%{name}/plugins/lirc/
%{_libdir}/%{name}/plugins/media-player-keys/
%{_libdir}/%{name}/plugins/ontop/
%{_libdir}/%{name}/plugins/opensubtitles/
%{_libdir}/%{name}/plugins/properties/
%{_libdir}/%{name}/plugins/pythonconsole/
%{_libdir}/%{name}/plugins/recent/
%{_libdir}/%{name}/plugins/rotation/
%{_libdir}/%{name}/plugins/screensaver/
%{_libdir}/%{name}/plugins/screenshot/
%{_libdir}/%{name}/plugins/skipto/
%{_libdir}/%{name}/plugins/vimeo/
%{_datadir}/glib-2.0/schemas/org.x.player.plugins.opensubtitles.gschema.xml
%{_datadir}/glib-2.0/schemas/org.x.player.plugins.pythonconsole.gschema.xml

%if %{build_zeitgeist_plugin}
%files plugin-zeitgeist
%{_libdir}/%{name}/plugins/zeitgeist-dp/
%endif

%files devel
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/gir-1.0/*.gir

%files doc
%doc %{_datadir}/doc/%{name}*
%doc %{_datadir}/gtk-doc
