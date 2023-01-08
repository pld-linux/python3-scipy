# TODO:
# - atlas support
# - tests
#
# Conditional build:
%bcond_without	doc	# Sphinx documentation

%define		module	scipy
Summary:	A library of scientific tools
Summary(pl.UTF-8):	Biblioteka narzędzi naukowych
Name:		python3-%{module}
Version:	1.8.1
Release:	1
License:	BSD
Group:		Development/Languages/Python
#Source0Download: https://github.com/scipy/scipy/releases/
Source0:	https://github.com/scipy/scipy/releases/download/v%{version}/%{module}-%{version}.tar.xz
# Source0-md5:	15c3e57656dbd1626ae33971f2e80ab1
Patch0:		numpy-deprecation-warnings.patch
Patch1:		%{name}-cython3.patch
# https://github.com/scipy/scipy/pull/16646
Patch2:		scipy-pythran.patch
Patch3:		scipy-numpydoc-update.patch
URL:		https://www.scipy.org/
BuildRequires:	blas-devel >= 3.6.0
BuildRequires:	f2py3 >= 1:1.14.5
BuildRequires:	gcc-fortran
BuildRequires:	lapack-devel >= 3.6.0
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	python3 >= 1:3.8
BuildRequires:	python3-devel >= 1:3.8
BuildRequires:	python3-numpy >= 1:1.17.3
BuildRequires:	python3-numpy-devel >= 1:1.17.3
BuildRequires:	python3-numpy-devel < 1:1.25
BuildRequires:	python3-pybind11 >= 2.4.3
BuildRequires:	python3-pythran >= 0.10.0
BuildRequires:	python3-setuptools
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%if %{with doc}
BuildRequires:	pydoc3
BuildRequires:	python3-matplotlib >= 2
# local version is used
#BuildRequires:	python3-numpydoc
BuildRequires:	python3-pydata_sphinx_theme >= 0.6.1
BuildRequires:	python3-sphinx_panels
BuildRequires:	sphinx-pdg-3 >= 2.0
%endif
Requires:	lapack >= 3.6.0
Requires:	python3-modules >= 1:3.8
Requires:	python3-numpy >= 1:1.17.3
Suggests:	python3-pillow
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SciPy is an open source library of scientific tools for Python. SciPy
supplements the popular numpy module, gathering a variety of high
level science and engineering modules together as a single package.

%description -l pl.UTF-8
SciPy to biblioteka narzędzi naukowych z otwartymi źródłami dla
Pythona. SciPy uzupełnia popularny moduł numpy, gromadząc razem
wiele wysokopoziomowych modułów naukowych i inżynierskich w jeden
pakiet.

%package apidocs
Summary:	API documentation for SciPy module
Summary(pl.UTF-8):	Dokumentacja API modułu SciPy
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for SciPy module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu SciPy.

%prep
%setup -q -n scipy-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
# numpy.distutils uses LDFLAGS as its own flags replacement,
# instead of appending proper options (like -shared)
CFLAGS="%{rpmcflags}"
LDFLAGS="%{rpmldflags} -shared"
export CFLAGS LDFLAGS

export BLAS=%{_libdir}
export LAPACK=%{_libdir}

%py3_build

%if %{with doc}
cp -pr scipy/io/tests build-3/lib.*/scipy/io
cp -p scipy/misc/*.dat build-3/lib.*/scipy/misc
cp -p scipy/stats/_sobol_direction_numbers.npz build-3/lib.*/scipy/stats
LANG=C \
PYTHONPATH=$(readlink -f build-3/lib.*) \
%{__make} -C doc html-build \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

export BLAS=%{_libdir}
export LAPACK=%{_libdir}

%py3_install

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/*.txt
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/_lib/_uarray/LICENSE
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/fft/_pocketfft/LICENSE.md
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/linalg/src/{id_dist/doc/doc.tex,lapack_deprecations/LICENSE}
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/optimize/lbfgsb_src/README
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/sparse/linalg/{_dsolve/SuperLU/License.txt,_eigen/arpack/ARPACK/COPYING}
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/spatial/qhull_src/COPYING.txt
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/_lib/_test_deprecation_*.so
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/*/tests
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/*/*/tests
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/*/*/*/tests
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/*/*/*/*/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files -n python3-%{module}
%defattr(644,root,root,755)
%doc INSTALL.rst.txt LICENSE.txt README.rst doc/{API.rst.txt,ROADMAP.rst.txt}
%dir %{py3_sitedir}/%{module}
%{py3_sitedir}/%{module}/*.py
%{py3_sitedir}/%{module}/__pycache__
%{py3_sitedir}/%{module}/*.pxd
%dir %{py3_sitedir}/%{module}/_build_utils
%{py3_sitedir}/%{module}/_build_utils/*.py
%{py3_sitedir}/%{module}/_build_utils/__pycache__
%dir %{py3_sitedir}/%{module}/_lib
%attr(755,root,root) %{py3_sitedir}/%{module}/_lib/_ccallback_c.*.so
%attr(755,root,root) %{py3_sitedir}/%{module}/_lib/_fpumode.*.so
%attr(755,root,root) %{py3_sitedir}/%{module}/_lib/_test_ccallback.*.so
%attr(755,root,root) %{py3_sitedir}/%{module}/_lib/messagestream.*.so
%{py3_sitedir}/%{module}/_lib/*.py
%{py3_sitedir}/%{module}/_lib/__pycache__
%dir %{py3_sitedir}/%{module}/_lib/_uarray
%attr(755,root,root) %{py3_sitedir}/%{module}/_lib/_uarray/_uarray.cpython-*.so
%{py3_sitedir}/%{module}/_lib/_uarray/*.py
%{py3_sitedir}/%{module}/_lib/_uarray/__pycache__
%dir %{py3_sitedir}/%{module}/cluster
%attr(755,root,root) %{py3_sitedir}/%{module}/cluster/*.so
%{py3_sitedir}/%{module}/cluster/*.py
%{py3_sitedir}/%{module}/cluster/__pycache__
%dir %{py3_sitedir}/%{module}/constants
%{py3_sitedir}/%{module}/constants/*.py
%{py3_sitedir}/%{module}/constants/__pycache__
%dir %{py3_sitedir}/%{module}/fft
%{py3_sitedir}/%{module}/fft/*.py
%{py3_sitedir}/%{module}/fft/__pycache__
%dir %{py3_sitedir}/%{module}/fft/_pocketfft
%attr(755,root,root) %{py3_sitedir}/%{module}/fft/_pocketfft/pypocketfft.cpython-*.so
%{py3_sitedir}/%{module}/fft/_pocketfft/*.py
%{py3_sitedir}/%{module}/fft/_pocketfft/__pycache__
%dir %{py3_sitedir}/%{module}/fftpack
%attr(755,root,root) %{py3_sitedir}/%{module}/fftpack/*.so
%{py3_sitedir}/%{module}/fftpack/*.py
%{py3_sitedir}/%{module}/fftpack/__pycache__
%dir %{py3_sitedir}/%{module}/integrate
%attr(755,root,root) %{py3_sitedir}/%{module}/integrate/*.so
%{py3_sitedir}/%{module}/integrate/*.py
%{py3_sitedir}/%{module}/integrate/__pycache__
%dir %{py3_sitedir}/%{module}/integrate/_ivp
%{py3_sitedir}/%{module}/integrate/_ivp/*.py
%{py3_sitedir}/%{module}/integrate/_ivp/__pycache__
%dir %{py3_sitedir}/%{module}/interpolate
%attr(755,root,root) %{py3_sitedir}/%{module}/interpolate/*.so
%{py3_sitedir}/%{module}/interpolate/*.py
%{py3_sitedir}/%{module}/interpolate/__pycache__
%dir %{py3_sitedir}/%{module}/io
%{py3_sitedir}/%{module}/io/*.py
%{py3_sitedir}/%{module}/io/__pycache__
%attr(755,root,root) %{py3_sitedir}/%{module}/io/*.so
%dir %{py3_sitedir}/%{module}/io/_harwell_boeing
%{py3_sitedir}/%{module}/io/_harwell_boeing/*.py
%{py3_sitedir}/%{module}/io/_harwell_boeing/__pycache__
%dir %{py3_sitedir}/%{module}/io/arff
%{py3_sitedir}/%{module}/io/arff/*.py
%{py3_sitedir}/%{module}/io/arff/__pycache__
%dir %{py3_sitedir}/%{module}/io/matlab
%attr(755,root,root) %{py3_sitedir}/%{module}/io/matlab/*.so
%{py3_sitedir}/%{module}/io/matlab/*.py
%{py3_sitedir}/%{module}/io/matlab/__pycache__
%dir %{py3_sitedir}/%{module}/linalg
%{py3_sitedir}/%{module}/linalg/*.pxd
%attr(755,root,root) %{py3_sitedir}/%{module}/linalg/*.so
%{py3_sitedir}/%{module}/linalg/*.py
%{py3_sitedir}/%{module}/linalg/*.pyi
%{py3_sitedir}/%{module}/linalg/__pycache__
%dir %{py3_sitedir}/%{module}/misc
%{py3_sitedir}/%{module}/misc/ascent.dat
%{py3_sitedir}/%{module}/misc/ecg.dat
%{py3_sitedir}/%{module}/misc/face.dat
%{py3_sitedir}/%{module}/misc/*.py
%{py3_sitedir}/%{module}/misc/__pycache__
%dir %{py3_sitedir}/%{module}/ndimage
%attr(755,root,root) %{py3_sitedir}/%{module}/ndimage/*.so
%{py3_sitedir}/%{module}/ndimage/*.py
%{py3_sitedir}/%{module}/ndimage/__pycache__
%dir %{py3_sitedir}/%{module}/odr
%attr(755,root,root) %{py3_sitedir}/%{module}/odr/*.so
%{py3_sitedir}/%{module}/odr/*.py
%{py3_sitedir}/%{module}/odr/__pycache__
%dir %{py3_sitedir}/%{module}/optimize
%attr(755,root,root) %{py3_sitedir}/%{module}/optimize/*.so
%{py3_sitedir}/%{module}/optimize/*.py
%{py3_sitedir}/%{module}/optimize/*.pyi
%{py3_sitedir}/%{module}/optimize/__pycache__
%dir %{py3_sitedir}/%{module}/optimize/_highs
%attr(755,root,root) %{py3_sitedir}/%{module}/optimize/_highs/*.so
%{py3_sitedir}/%{module}/optimize/_highs/*.py
%{py3_sitedir}/%{module}/optimize/_highs/__pycache__
%{py3_sitedir}/%{module}/optimize/_highs/cython
%dir %{py3_sitedir}/%{module}/optimize/_lsq
%attr(755,root,root) %{py3_sitedir}/%{module}/optimize/_lsq/*.so
%{py3_sitedir}/%{module}/optimize/_lsq/*.py
%{py3_sitedir}/%{module}/optimize/_lsq/__pycache__
%dir %{py3_sitedir}/%{module}/optimize/_shgo_lib
%{py3_sitedir}/%{module}/optimize/_shgo_lib/*.py
%{py3_sitedir}/%{module}/optimize/_shgo_lib/__pycache__
%dir %{py3_sitedir}/%{module}/optimize/_trlib
%attr(755,root,root) %{py3_sitedir}/%{module}/optimize/_trlib/*.so
%{py3_sitedir}/%{module}/optimize/_trlib/*.py
%{py3_sitedir}/%{module}/optimize/_trlib/__pycache__
%dir %{py3_sitedir}/%{module}/optimize/_trustregion_constr
%{py3_sitedir}/%{module}/optimize/_trustregion_constr/*.py
%{py3_sitedir}/%{module}/optimize/_trustregion_constr/__pycache__
%{py3_sitedir}/%{module}/optimize/cython_optimize.pxd
%dir %{py3_sitedir}/%{module}/optimize/cython_optimize
%attr(755,root,root) %{py3_sitedir}/%{module}/optimize/cython_optimize/*.so
%{py3_sitedir}/%{module}/optimize/cython_optimize/*.py
%{py3_sitedir}/%{module}/optimize/cython_optimize/*.pxd
%{py3_sitedir}/%{module}/optimize/cython_optimize/__pycache__
%dir %{py3_sitedir}/%{module}/signal
%attr(755,root,root) %{py3_sitedir}/%{module}/signal/*.so
%{py3_sitedir}/%{module}/signal/*.py
%{py3_sitedir}/%{module}/signal/__pycache__
%dir %{py3_sitedir}/%{module}/signal/windows
%{py3_sitedir}/%{module}/signal/windows/*.py
%{py3_sitedir}/%{module}/signal/windows/__pycache__
%dir %{py3_sitedir}/%{module}/sparse
%attr(755,root,root) %{py3_sitedir}/%{module}/sparse/*.so
%{py3_sitedir}/%{module}/sparse/*.py
%{py3_sitedir}/%{module}/sparse/__pycache__
%dir %{py3_sitedir}/%{module}/sparse/linalg
%{py3_sitedir}/%{module}/sparse/linalg/*.py
%{py3_sitedir}/%{module}/sparse/linalg/__pycache__
%dir %{py3_sitedir}/%{module}/sparse/csgraph
%{py3_sitedir}/%{module}/sparse/csgraph/*.py
%{py3_sitedir}/%{module}/sparse/csgraph/__pycache__
%attr(755,root,root) %{py3_sitedir}/%{module}/sparse/csgraph/*.so
%dir %{py3_sitedir}/%{module}/sparse/linalg/_dsolve
%attr(755,root,root) %{py3_sitedir}/%{module}/sparse/linalg/_dsolve/*.so
%{py3_sitedir}/%{module}/sparse/linalg/_dsolve/*.py
%{py3_sitedir}/%{module}/sparse/linalg/_dsolve/__pycache__
%dir %{py3_sitedir}/%{module}/sparse/linalg/_eigen
%{py3_sitedir}/%{module}/sparse/linalg/_eigen/*.py
%{py3_sitedir}/%{module}/sparse/linalg/_eigen/__pycache__
%dir %{py3_sitedir}/%{module}/sparse/linalg/_eigen/arpack
%attr(755,root,root) %{py3_sitedir}/%{module}/sparse/linalg/_eigen/arpack/*.so
%{py3_sitedir}/%{module}/sparse/linalg/_eigen/arpack/*.py
%{py3_sitedir}/%{module}/sparse/linalg/_eigen/arpack/__pycache__
%dir %{py3_sitedir}/%{module}/sparse/linalg/_eigen/lobpcg
%{py3_sitedir}/%{module}/sparse/linalg/_eigen/lobpcg/*.py
%{py3_sitedir}/%{module}/sparse/linalg/_eigen/lobpcg/__pycache__
%dir %{py3_sitedir}/%{module}/sparse/linalg/_isolve
%attr(755,root,root) %{py3_sitedir}/%{module}/sparse/linalg/_isolve/*.so
%{py3_sitedir}/%{module}/sparse/linalg/_isolve/*.py
%{py3_sitedir}/%{module}/sparse/linalg/_isolve/__pycache__
%dir %{py3_sitedir}/%{module}/sparse/linalg/_propack
%attr(755,root,root) %{py3_sitedir}/%{module}/sparse/linalg/_propack/*.so
%dir %{py3_sitedir}/%{module}/spatial
%attr(755,root,root) %{py3_sitedir}/%{module}/spatial/*.so
%{py3_sitedir}/%{module}/spatial/*.py
%{py3_sitedir}/%{module}/spatial/*.pyi
%{py3_sitedir}/%{module}/spatial/__pycache__
%dir %{py3_sitedir}/%{module}/spatial/transform
%attr(755,root,root) %{py3_sitedir}/%{module}/spatial/transform/*.so
%{py3_sitedir}/%{module}/spatial/transform/*.py
%{py3_sitedir}/%{module}/spatial/transform/*.pyi
%{py3_sitedir}/%{module}/spatial/transform/__pycache__
%dir %{py3_sitedir}/%{module}/special
%attr(755,root,root) %{py3_sitedir}/%{module}/special/*.so
%{py3_sitedir}/%{module}/special/*.pxd
%{py3_sitedir}/%{module}/special/*.py
%{py3_sitedir}/%{module}/special/*.pyi
%{py3_sitedir}/%{module}/special/__pycache__
%dir %{py3_sitedir}/%{module}/special/_precompute
%{py3_sitedir}/%{module}/special/_precompute/*.py
%{py3_sitedir}/%{module}/special/_precompute/__pycache__
%dir %{py3_sitedir}/%{module}/stats
%attr(755,root,root) %{py3_sitedir}/%{module}/stats/*.so
%{py3_sitedir}/%{module}/stats/*.py
%{py3_sitedir}/%{module}/stats/*.pyi
%{py3_sitedir}/%{module}/stats/*.pxd
%{py3_sitedir}/%{module}/stats/_sobol_direction_numbers.npz
%{py3_sitedir}/%{module}/stats/__pycache__
%dir %{py3_sitedir}/%{module}/stats/_boost
%attr(755,root,root) %{py3_sitedir}/%{module}/stats/_boost/*.so
%{py3_sitedir}/%{module}/stats/_boost/*.py
%{py3_sitedir}/%{module}/stats/_boost/__pycache__
%dir %{py3_sitedir}/%{module}/stats/_unuran
%attr(755,root,root) %{py3_sitedir}/%{module}/stats/_unuran/*.so
%{py3_sitedir}/%{module}/stats/_unuran/*.pxd
%{py3_sitedir}/%{module}/stats/_unuran/*.py
%{py3_sitedir}/%{module}/stats/_unuran/*.pyi
%{py3_sitedir}/%{module}/stats/_unuran/__pycache__
%{py3_sitedir}/SciPy-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/build/html/{_images,_panels_static,_static,building,dev,reference,tutorial,*.html,*.js}
%endif
