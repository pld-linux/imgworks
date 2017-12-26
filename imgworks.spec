Summary:	ImgWorks - graphical batch image converter
Summary(pl.UTF-8):	ImgWorks - graficzny wsadowy konwerter obrazów
Name:		imgworks
Version:	0.8.1
Release:	7
License:	GPL v2
Group:		X11/Applications/Graphics
Source0:	http://wolfsinger.com/~wolfpack/packages/%{name}-%{version}.tar.bz2
# Source0-md5:	4badf90fe08ae8fceb4cabc032558285
Patch0:		%{name}-verbose.patch
Patch1:		imagemagick7.patch
URL:		http://freecode.com/projects/imgworks
BuildRequires:	ImageMagick-devel
BuildRequires:	endeavour-devel >= 3
BuildRequires:	gtk+-devel >= 1.2
BuildRequires:	libstdc++-devel
Requires:	endeavour >= 3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ImgWorks is a graphical batch image converter that uses ImageMagick
along with Endeavour Mark II to conveniently convert and edit a
user-specified list of image/video files. Features include converting
images from one format to another, adjusting the compression level,
adjusting the gamma, rotating, cropping, resizing, and adding frames
and text.

%description -l pl.UTF-8
ImgWorks to graficzny wsadowy konwerter obrazów, wykorzystujący pakiet
ImageMagick wraz z Endeavour Mark II do wygodnej konwersji i edycji
podanej przez użytkownika listy plików obrazów/wideo. Możliwości
obejmują konwersję z jednego formatu do innego, modyfikowanie poziomu
kompresji, modyfikowanie współczynnika gamma, obracanie, przycinanie,
zmianę orzmiaru oraz dodawanie ramek i tekstu.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__make} \
	CC="%{__cc}" \
	CPP="%{__cxx}" \
	CFLAGS="%{rpmcflags} -Wall -DPREFIX=\\\"%{_prefix}\\\" \
		-DHAVE_IMAGE_MAGICK `MagickCore-config --cflags` `MagickWand-config --cflags` \
		`gtk-config --cflags` \
		-DHAVE_LIBENDEAVOUR2 `endeavour2-base-config --cflags`"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

%{__make} install \
	PREFIX=$RPM_BUILD_ROOT%{_prefix} \
	EDV_BIN_DIR=$RPM_BUILD_ROOT%{_libdir}/endeavour2/bin \
	MAN_DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
	INSTBINFLAGS="-m755"

# fix symlink to buildroot
ln -sf ../%{_lib}/endeavour2/bin/imgworks $RPM_BUILD_ROOT%{_bindir}/imgworks

bzip2 -d $RPM_BUILD_ROOT%{_mandir}/man1/*.bz2

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/imgworks
%attr(755,root,root) %{_libdir}/endeavour2/bin/imgworks
%{_datadir}/endeavour2/help/imgworks
%{_datadir}/endeavour2/icons/icon_imgworks_*.xpm
%{_mandir}/man1/imgworks.1*
