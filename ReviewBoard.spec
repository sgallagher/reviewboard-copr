%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           ReviewBoard
Version:        1.5.2
Release:        21%{?dist}
Summary:        Web-based code review tool
Group:          Applications/Internet
License:        MIT
URL:            http://www.review-board.org
Source0:        http://downloads.review-board.org/releases/%{name}/1.5/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       Django >= 1.1.3
Requires:       python-djblets >= 0.6.7
Requires:       python-imaging
Requires:       httpd
Requires:       python-sqlite
Requires:       patchutils
Requires:       pysvn
Requires:       python-flup
Requires:       python-nose
Requires:       pytz
Requires:       python-pygments >= 1.1.1
Requires:       django-evolution >= 0.6.2
Requires:       python-recaptcha-client
Requires:       python-paramiko
Requires:       python-memcached
Requires:       python-dateutil

Patch1001: FED01-Disable-ez_setup-when-installing-by-RPM.patch
Patch1002: FED02-Notify-WSGI-users-that-config-changes-are-needed.patch

%description
Review Board is a powerful web-based code review tool that offers
developers an easy way to handle code reviews. It scales well from small
projects to large companies and offers a variety of tools to take much
of the stress and time out of the code review process.

%prep
%setup -q -n %{name}-%{version}
%patch1001 -p1
%patch1002 -p1

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT

# --skip-build causes bad stuff in siteconfig.py as of 0.8.4
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

# These scripts have a shebang and are meaningful to run; make them executable:
chmod +x $RPM_BUILD_ROOT/%{python_sitelib}/reviewboard/manage.py
chmod +x $RPM_BUILD_ROOT/%{python_sitelib}/reviewboard/cmdline/rbssh.py
chmod +x $RPM_BUILD_ROOT/%{python_sitelib}/reviewboard/cmdline/rbsite.py

# RHEL 5 packages don't have egg-info files, so remove the requires.txt
# It isn't needed, because RPM will guarantee the dependency itself
%if 0%{?rhel} > 0
%if 0%{?rhel} <= 5
rm -f $RPM_BUILD_ROOT/%{python_sitelib}/%{name}*.egg-info/requires.txt
%endif
%endif

# Remove test data from the installed packages
rm -Rf $RPM_BUILD_ROOT/%{python_sitelib}/reviewboard/diffviewer/testdata \
       $RPM_BUILD_ROOT/%{python_sitelib}/reviewboard/scmtools/testdata

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
%{_bindir}/rbssh
%{python_sitelib}/reviewboard/
%{python_sitelib}/ReviewBoard*.egg-info/
%{python_sitelib}/webtests/*.py*

%changelog
* Tue Jan 18 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.2-21
- Change mod_wsgi notification patch to the version submitted upstream
- This warning will now only be displayed if upgrading from an affected
- version, rather than on all upgrades.
- Don't install files used only for test purposes

* Mon Jan 10 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.2-20
- Add message to upgrade script to alert users that manual edits may be
- required if using mod_wsgi

* Mon Jan 10 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.2-19
- Important Updates
-     Users using existing WSGI configurations must update their configuration
-     for authentication with the new API to work.
- New Features
-     Added SSH key management for SSH-backed repositories
-     Authentication failures when setting up repositories are now more useful
-     Added our own SSH replacement for standardizing on behavior and working
-     around OpenSSH limitations
-     The Repository page in the administration UI now talks about API Tokens
-     and links to the GitHub Account page for Git repositories, making it
-     easier to set up a GitHub repository
- API Fixes
-     Fixed logging in on requests using HTTP Basic Auth
-     Fixed wrong responses when performing a request requiring authentication
-     as an anonymous user
-     Fixed anonymous access to the API when anonymous access is enabled
-     Fixed replies to screenshot comments in the new web API
-     Fixed removing screenshots from review requests
-     Changed the request when doing a HTTP PUT on a review request draft
-     Fixed search queries in /api/users/
- Bug Fixes
-     Fixed a problem with SSH host checking on Git repositories
-     Fixed support for private GitHub repositories
-     The API Token for GitHub repositories are now extracted properly in the
-     Repository page in the administration UI
-     Fixed extra whitespace highlight toggling
-     Images on the dashboard are now cached, reducing the number of requests
-     made to the server
-     Disabled auto-complete and default values for the repository
-     username/password fields
-     Support for Amazon S3 now works again with new versions of Django
-     Storages
-     Authentication with the new API now works with new Apache+wsgi setups
-     Fixed some rewrite rule for fastcgi
-     Fix 404 errors with newly generated lighttpd.conf files
-     Fixed errrors when passing a non-integer value for ?show_submitted= on
-     the dashboard or other review request listings
-     Fixed a crash when attempting to log SSH-related problems
-     The contributed svn-hook-postcommit-review script wasn't parsing the
-     base path correctly
- Release Notes
-     http://www.reviewboard.org/docs/releasenotes/dev/reviewboard/1.5.2/

* Mon Nov 22 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.5.1-18
- New Features
-      Permission denied errors are shown when accessing unreachable local Git
-      repositories. (Bug #1765)
-      Previously, if a Git repository was used and there wasn’t sufficient
-      file permissions to access it, a vague error saying that the repository
-      was unreachable would appear. Now we check to find out if it’s a
-      permissions error, and display an appropriate error message.
- Performance Improvements
-      Reduce the number of SQL queries in the legacy JSON API.
-      Some of the legacy API handlers performed more queries than necessary.
-      We now perform fewer queries. Patch by Ben Hollis.
- Bug Fixes
-      Fixed several small problems in the Admin UI from bundling Django media
-      files.
-      For historical reasons, we’ve always shipped the Django Admin media
-      files as part of Review Board. This comes from a time before rb-site
-      existed, when we needed a single media directory with everything inside
-      it. However, it just introduces various compatibility problems these
-      days. We now make use of the media files that are installed with Django
-      Fixed a breakage in the diff viewer with SCons files. (Bug #1864)
-      Any SCons files put up for review would break the diff viewer, due to a
-      typo when looking up information on that type of file.
-      Added the Parent Diff field to the New Review Request page. (Bug #1651)
-      The Parent Diff field was missing for Git, Bazaar, and Mercurial,
-      making it impossible to upload a parent diff through the web UI when
-      creating a new review request.
-      Fixed some common installation problems with the generated
-      lighttpd.conf file. (Bug #1618, Bug #1639)
-      Several installs with lighttpd would give 404 Not Found errors, due to
-      some configuration problems in the sample config file.
-      Fixed support for multiple e-mail addresses assigned to a group.
-      (Bug #1661)
-      Multiple e-mail addresses for a group were supported, but broken in
-      1.5. We now split them out properly.
-      The screenshot area is no longer hidden immediately after uploading a
-      screenshot.
-      Fixed an error in the web API when serializing to XML.
-      Fixed broken intervals for search updating in the generated crontab
-      file.
-      The intervals would cause a full index to happen at every minute at 2AM
-      on Sundays, rather than only at 2AM.
-      Fixed an error when permanently deleting a review request.
-      The administrator-specific ability to permanently delete a review
-      request would succeed but generate an error page.

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
- Specfile change: more specific %%files section

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
