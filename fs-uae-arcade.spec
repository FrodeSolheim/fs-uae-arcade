# Copyright © 2013–2025 Frode Solheim <frode@fs-uae.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

%define name fs-uae-arcade
%define version 3.2.21
%define release 1%{?dist}

Summary: Fullscreen game browser for FS-UAE
Name: %{name}
Version: %{version}
Release: %{release}
URL: http://fs-uae.net/
Source0: %{name}_%{version}.orig.tar.xz
License: GPL-2.0+
Group: Applications/Emulators
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Frode Solheim <frode@fs-uae.net>
Requires: fs-uae-launcher

%description
FS-UAE Arcade is a fullscreen Amiga game browser for FS-UAE.

%prep
%setup -n %{name}-%{version}

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} prefix=%{_prefix}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%_bindir/*

%doc

%changelog
