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
Version:	1.15.2
Release:	1
License:	BSD
Group:		Development/Languages/Python
#Source0Download: https://github.com/scipy/scipy/releases/
Source0:	https://github.com/scipy/scipy/releases/download/v%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	515fc1544d7617b38fe5a9328538047b
URL:		https://www.scipy.org/
BuildRequires:	blas-devel >= 3.6.0
BuildRequires:	cblas-devel
BuildRequires:	f2py3 >= 1:1.14.5
BuildRequires:	gcc-fortran
BuildRequires:	lapack-devel >= 3.6.0
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	python3 >= 1:3.10
BuildRequires:	python3-Cython >= 3.0.8
BuildRequires:	python3-build
BuildRequires:	python3-devel >= 1:3.8
BuildRequires:	python3-installer
BuildRequires:	python3-meson-python >= 0.15.0
BuildRequires:	python3-numpy >= 1:2.0.0
BuildRequires:	python3-numpy-devel >= 1:2.0.0
BuildRequires:	python3-numpy-devel < 1:2.5
BuildRequires:	python3-pybind11 >= 2.13.2
BuildRequires:	python3-pythran >= 0.14.0
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.044
BuildRequires:	tar >= 1:1.22
%if %{with doc}
BuildRequires:	pydoc3
BuildRequires:	python3-intersphinx_registry
BuildRequires:	python3-jupyterlite_pyodide_kernel
BuildRequires:	python3-jupyterlite_sphinx >= 0.16.55
BuildRequires:	python3-jupytext
BuildRequires:	python3-matplotlib >= 3.5
BuildRequires:	python3-myst_nb
BuildRequires:	python3-numpydoc
BuildRequires:	python3-pooch
BuildRequires:	python3-pydata_sphinx_theme >= 0.6.1
BuildRequires:	python3-sphinx_copybutton
BuildRequires:	python3-sphinx_design
BuildRequires:	sphinx-pdg-3 >= 5.0.0
%endif
Requires:	lapack >= 3.6.0
Requires:	python3-modules >= 1:3.10
Requires:	python3-numpy >= 1:2.0.0
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

%build
%py3_build_pyproject -Csetup-args="-Dblas=blas" -Csetup-args="-Dlapack=lapack"

%if %{with doc}
%__unzip -qo build-3/*.whl -d build-3/build-path
LANG=C \
PYTHONPATH=$(pwd)/build-3/build-path \
%{__make} -C doc html-build \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/_lib/_uarray/LICENSE
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/fft/_pocketfft/LICENSE.md
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
%doc LICENSE.txt README.rst
%dir %{py3_sitedir}/%{module}
%{py3_sitedir}/%{module}/*.py
%{py3_sitedir}/%{module}/__pycache__
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
%dir %{py3_sitedir}/%{module}/_lib/array_api_compat
%{py3_sitedir}/%{module}/_lib/array_api_compat/*.py
%{py3_sitedir}/%{module}/_lib/array_api_compat/__pycache__
%dir %{py3_sitedir}/%{module}/_lib/array_api_compat/common
%{py3_sitedir}/%{module}/_lib/array_api_compat/common/*.py
%{py3_sitedir}/%{module}/_lib/array_api_compat/common/__pycache__
%dir %{py3_sitedir}/%{module}/_lib/array_api_compat/cupy
%{py3_sitedir}/%{module}/_lib/array_api_compat/cupy/*.py
%{py3_sitedir}/%{module}/_lib/array_api_compat/cupy/__pycache__
%dir %{py3_sitedir}/%{module}/_lib/array_api_compat/dask
%{py3_sitedir}/%{module}/_lib/array_api_compat/dask/*.py
%{py3_sitedir}/%{module}/_lib/array_api_compat/dask/__pycache__
%dir %{py3_sitedir}/%{module}/_lib/array_api_compat/dask/array
%{py3_sitedir}/%{module}/_lib/array_api_compat/dask/array/*.py
%{py3_sitedir}/%{module}/_lib/array_api_compat/dask/array/__pycache__
%dir %{py3_sitedir}/%{module}/_lib/array_api_compat/numpy
%{py3_sitedir}/%{module}/_lib/array_api_compat/numpy/*.py
%{py3_sitedir}/%{module}/_lib/array_api_compat/numpy/__pycache__
%dir %{py3_sitedir}/%{module}/_lib/array_api_compat/torch
%{py3_sitedir}/%{module}/_lib/array_api_compat/torch/*.py
%{py3_sitedir}/%{module}/_lib/array_api_compat/torch/__pycache__
%dir %{py3_sitedir}/%{module}/_lib/array_api_extra
%{py3_sitedir}/%{module}/_lib/array_api_extra/*.py
%{py3_sitedir}/%{module}/_lib/array_api_extra/__pycache__
%dir %{py3_sitedir}/%{module}/_lib/cobyqa
%{py3_sitedir}/%{module}/_lib/cobyqa/*.py
%{py3_sitedir}/%{module}/_lib/cobyqa/__pycache__
%dir %{py3_sitedir}/%{module}/_lib/cobyqa/subsolvers
%{py3_sitedir}/%{module}/_lib/cobyqa/subsolvers/*.py
%{py3_sitedir}/%{module}/_lib/cobyqa/subsolvers/__pycache__
%dir %{py3_sitedir}/%{module}/_lib/cobyqa/utils
%{py3_sitedir}/%{module}/_lib/cobyqa/utils/*.py
%{py3_sitedir}/%{module}/_lib/cobyqa/utils/__pycache__
%dir %{py3_sitedir}/%{module}/cluster
%attr(755,root,root) %{py3_sitedir}/%{module}/cluster/*.so
%{py3_sitedir}/%{module}/cluster/*.py
%{py3_sitedir}/%{module}/cluster/__pycache__
%dir %{py3_sitedir}/%{module}/constants
%{py3_sitedir}/%{module}/constants/*.py
%{py3_sitedir}/%{module}/constants/__pycache__
%dir %{py3_sitedir}/%{module}/datasets
%{py3_sitedir}/%{module}/datasets/*.py
%{py3_sitedir}/%{module}/datasets/__pycache__
%dir %{py3_sitedir}/%{module}/differentiate
%{py3_sitedir}/%{module}/differentiate/*.py
%{py3_sitedir}/%{module}/differentiate/__pycache__
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
%dir %{py3_sitedir}/%{module}/integrate/_rules
%{py3_sitedir}/%{module}/integrate/_rules/*.py
%{py3_sitedir}/%{module}/integrate/_rules/__pycache__
%dir %{py3_sitedir}/%{module}/interpolate
%attr(755,root,root) %{py3_sitedir}/%{module}/interpolate/*.so
%{py3_sitedir}/%{module}/interpolate/*.py
%{py3_sitedir}/%{module}/interpolate/__pycache__
%dir %{py3_sitedir}/%{module}/io
%{py3_sitedir}/%{module}/io/*.py
%{py3_sitedir}/%{module}/io/__pycache__
%attr(755,root,root) %{py3_sitedir}/%{module}/io/*.so
%dir %{py3_sitedir}/%{module}/io/_fast_matrix_market
%{py3_sitedir}/%{module}/io/_fast_matrix_market/*.py
%{py3_sitedir}/%{module}/io/_fast_matrix_market/__pycache__
%attr(755,root,root) %{py3_sitedir}/%{module}/io/_fast_matrix_market/*.so
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
%{py3_sitedir}/%{module}/optimize/__pycache__
%dir %{py3_sitedir}/%{module}/optimize/_highspy
%attr(755,root,root) %{py3_sitedir}/%{module}/optimize/_highspy/*.so
%{py3_sitedir}/%{module}/optimize/_highspy/*.py
%{py3_sitedir}/%{module}/optimize/_highspy/__pycache__
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
%{py3_sitedir}/%{module}/signal/*.pyi
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
%dir %{py3_sitedir}/%{module}/stats/_levy_stable
%attr(755,root,root) %{py3_sitedir}/%{module}/stats/_levy_stable/*.so
%{py3_sitedir}/%{module}/stats/_levy_stable/*.py
%{py3_sitedir}/%{module}/stats/_levy_stable/__pycache__
%dir %{py3_sitedir}/%{module}/stats/_rcont
%attr(755,root,root) %{py3_sitedir}/%{module}/stats/_rcont/*.so
%{py3_sitedir}/%{module}/stats/_rcont/*.py
%{py3_sitedir}/%{module}/stats/_rcont/__pycache__
%dir %{py3_sitedir}/%{module}/stats/_unuran
%attr(755,root,root) %{py3_sitedir}/%{module}/stats/_unuran/*.so
%{py3_sitedir}/%{module}/stats/_unuran/*.py
%{py3_sitedir}/%{module}/stats/_unuran/*.pyi
%{py3_sitedir}/%{module}/stats/_unuran/__pycache__
%{py3_sitedir}/scipy-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/build/html/{_images,_panels_static,_static,building,dev,reference,tutorial,*.html,*.js}
%endif
