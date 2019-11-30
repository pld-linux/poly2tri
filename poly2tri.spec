Summary:	A 2D constrained Delaunay triangulation library
Summary(pl.UTF-8):	Biblioteka triangulacji Delaunaya z ograniczeniami w 2D
Name:		poly2tri
# see wscript
Version:	0.3.3
%define	snap	20150515
Release:	0.%{snap}.1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/jhasse/poly2tri/releases
#Source0:	https://poly2tri.googlecode.com/archive/26242d0aa7b85fe3bf8c64a343dbe8a88055de37.tar.gz
Source0:	26242d0aa7b85fe3bf8c64a343dbe8a88055de37.tar.gz
# Source0-md5:	41a410f8b4de7cd6a3d64546c43a058b
Patch0:		%{name}-glfw3.patch
URL:		https://github.com/jhasse/poly2tri
BuildRequires:	OpenGL-devel
BuildRequires:	glfw-devel >= 3
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Library based on the paper "Sweep-line algorithm for constrained
Delaunay triangulation" by V. Domiter and B. Zalik.

%description
Biblioteka oparta na dokumencie "Sweep-line algorithm for constrained
Delaunay triangulation" (Algorytm zamiatania płaszczyzny do
triangulacji Delaunaya z ograniczeniami) autorstwa V. Domitera oraz B.
Zalika.

%package devel
Summary:	Development files for poly2tri library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki poly2tri
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Development files for poly2tri library.

%description devel -l pl.UTF-8
Pliki programistyczne biblioteki poly2tri.

%package static
Summary:	Static poly2tri library
Summary(pl.UTF-8):	Statyczna biblioteka poly2tri
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static poly2tri library.

%description static -l pl.UTF-8
Statyczna biblioteka poly2tri.

%prep
%setup -q -n %{name}-26242d0aa7b8
%patch0 -p1

%build
# it doesn't actually build the library
#waf configure
#waf build

# ...so do it manually
for f in poly2tri/common/shapes.cc poly2tri/sweep/{cdt,advancing_front,sweep_context,sweep}.cc ; do
	libtool --mode=compile --tag=CXX %{__cxx} %{rpmcxxflags} %{rpmcppflags} -c $f
done
libtool --mode=link --tag=CXX %{__cxx} %{rpmldflags} %{rpmcxxflags} %{rpmcppflags} -o libpoly2tri.la shapes.lo cdt.lo advancing_front.lo sweep_context.lo sweep.lo -rpath %{_libdir}

libtool --mode=link --tag=CXX %{__cxx} %{rpmldflags} %{rpmcxxflags} %{rpmcppflags} -o p2t testbed/main.cc libpoly2tri.la -lGL -lglfw

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir}/poly2tri/{common,sweep}}

#waf install

libtool --mode=install install libpoly2tri.la $RPM_BUILD_ROOT%{_libdir}
libtool --mode=install install p2t $RPM_BUILD_ROOT%{_bindir}
cp -p poly2tri/poly2tri.h $RPM_BUILD_ROOT%{_includedir}/poly2tri
cp -p poly2tri/common/shapes.h $RPM_BUILD_ROOT%{_includedir}/poly2tri/common
cp -p poly2tri/common/shapes.h $RPM_BUILD_ROOT%{_includedir}/poly2tri/common
cp -p poly2tri/sweep/{cdt,advancing_front,sweep_context,sweep}.h $RPM_BUILD_ROOT%{_includedir}/poly2tri/sweep

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libpoly2tri.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README
%attr(755,root,root) %{_bindir}/p2t
%attr(755,root,root) %{_libdir}/libpoly2tri.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpoly2tri.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpoly2tri.so
%{_includedir}/poly2tri

%files static
%defattr(644,root,root,755)
%{_libdir}/libpoly2tri.a
