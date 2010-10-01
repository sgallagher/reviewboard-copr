%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           ReviewBoard
Version:        1.5
Release:        17%{?dist}
Summary:        Web-based code review tool
Group:          Applications/Internet
License:        MIT
URL:            http://www.review-board.org
Source0:        http://downloads.review-board.org/releases/%{name}/1.5/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       Django >= 1.1.1
Requires:       python-djblets >= 0.6.4
Requires:       python-imaging
Requires:       httpd
Requires:       python-sqlite
Requires:       patchutils
Requires:       pysvn
Requires:       python-flup
Requires:       python-nose
Requires:       pytz
Requires:       python-pygments >= 1.1.1
Requires:       django-evolution >= 0.5
Requires:       python-recaptcha-client
Requires:       python-paramiko
Requires:       python-memcached
Requires:       python-dateutil

Patch1000: FED01-Disable-ez_setup-when-installing-by-RPM.patch

%description
Review Board is a powerful web-based code review tool that offers
developers an easy way to handle code reviews. It scales well from small
projects to large companies and offers a variety of tools to take much
of the stress and time out of the code review process.

%prep
%setup -q -n %{name}-%{version}
%patch1000 -p1

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT

# --skip-build causes bad stuff in siteconfig.py as of 0.8.4
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

# manage.py has a shebang and is meaningful to run; make it executable:
chmod +x $RPM_BUILD_ROOT/%{python_sitelib}/reviewboard/manage.py

# RHEL 5 packages don't have egg-info files, so remove the requires.txt
# It isn't needed, because RPM will guarantee the dependency itself
%if 0%{?rhel} > 0
%if 0%{?rhel} <= 5
rm -f $RPM_BUILD_ROOT/%{python_sitelib}/%{name}*.egg-info/requires.txt
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
# The rb-site executable has a PyGTK GUI, so would normally
# require us to ship a .desktop file.  However it can only be run when supplied
# a directory as a command-line argument, hence it wouldn't be meaningful to
# create a .desktop file for it.
%defattr(-,root,root,-)
%doc AUTHORS COPYING INSTALL NEWS README
%{_bindir}/rb-site
%{python_sitelib}/reviewboard/
%{python_sitelib}/ReviewBoard*.egg-info/
%{python_sitelib}/webtests/*.py*

%changelog
* Fri Oct 01 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.5-17
- Release ReviewBoard 1.5 final
- Full release notes:
- http://www.reviewboard.org/docs/releasenotes/dev/reviewboard/1.5/

* Mon Sep 20 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.5-16.rc2
- Fix specfile typo causing build break

* Mon Sep 20 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.5-15.rc2
- Update to new upstream release 1.5rc2
- Added Python 2.7 compatibility.
- Added compatibility with PyLucene 3.x. Support for 2.x still remains.
- Added support for review requests without diffs, for image/screenshot review
- Assorted API improvements and bugfixes
- Update Djblets requirement to 0.6.4
- http://www.reviewboard.org/docs/releasenotes/dev/reviewboard/1.5-rc-2/

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.5-14.rc1.1
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 09 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.5-14.rc1
- Add missing Requires: python-dateutil

* Mon Jul 06 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.5-13.rc1
- Specfile change: more specific %files section

* Mon Jul 06 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.5-12.rc1
- Added support for the iPhone and iPad
- Improved move detection in diff viewer
- Support for WSGI installations
- Improvements to the JSON API
- Assorted bugfixes
- http://www.reviewboard.org/docs/releasenotes/dev/reviewboard/1.5-rc-1/

* Fri May 14 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.5-11.beta2
- Added support for custom site-specific management commands
- Set the HOME directory for Review Board to be he site directory’s
- data directory by default
- Multiple review requests can now be closed or reopened at once by
- administrators in the administration UI’s database browser
- Added a new REST API
- Usability Improvements
- Assorted bugfixes
- http://www.reviewboard.org/docs/releasenotes/dev/reviewboard/1.5-beta-2/

* Sat Apr 17 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.5-7.beta1
- Remove previous patch. It was actually already in the source tree

* Sat Apr 17 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.5-6.beta1
- Include upstream patch to drastically reduce the number of
- SQL lookups

* Tue Mar 16 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.5-5.beta1
- Add Requires: python-paramiko

* Fri Mar 12 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.5-3.beta1
- Fix some places where 'beta1' was missing, causing build failure

* Fri Mar 12 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.5-2.beta1
- Correct version to meet naming guidelines

* Fri Mar 12 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.5beta1-1
- Add missing dependency on python-recaptcha-client

* Mon Feb 15 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.5beta1-0
- New upstream release
- Complete release notes at
- http://www.reviewboard.org/docs/releasenotes/dev/reviewboard/1.5-beta-1/

* Tue Dec 22 2009 Stephen Gallagher <sgallagh@redhat.com> - 1.0.5.1-2
- Fix source tarball location
- Add comment to spec file regarding the lack of .desktop file
- Update changelog

* Tue Dec 15 2009 Stephen Gallagher <sgallagh@redhat.com> - 1.0.5.1-1
- Update to latest upstream (1.0.5.1)
- Require Django >= 1.1.1 for security fixes

* Fri Oct 16 2009 Dan Young <dyoung@mesd.k12.or.us> - 1.0.1-2
- add builddep on python-setuptools to avoid "ImportError: No module named
  setuptools" in mock build
- Add Requires: python-pygments for syntax highlighting
- Add Requires: django-evolution for schema migrations

* Fri Sep 11 2009 David Malcolm <dmalcolm@redhat.com> - 1.0.1-1
- bump to latest upstream (1.0.1), and delete usage of "alphatag" from the
specfile
- drop build-time dependency on python-setuptools-devel

* Thu May  7 2009 David Malcolm <dmalcolm@redhat.com> - 1.0-0.4.rc1
- update to rc1
- avoid trying to bootstrap setup.py; we get this via RPM
- update djblets dep based on my proposed renaming (see bug 487098)
- make manage.py executable
- add requirement on pytz

* Tue Feb  24 2009 Dan Young <dyoung@mesd.k12.or.us> - 1.0-0.3.alpha4
- change _alphaver to alphatag
- fix Djblets dep w/ correct pre-release package naming

* Tue Feb  24 2009 Dan Young <dyoung@mesd.k12.or.us> - 1.0-0.2.alpha4
- Fix version number
- Fix rpmlint administriva (spaces/tabs, description length, capitalization)
- Include docs

* Sat Feb  21 2009 Ramez Hanna <rhanna@informatiq.org> 
- First build.
