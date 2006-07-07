# Copyright (c) 2001-2003, Patrick K. O'Brien and Contributors
# Distributed under the terms of the BSD License
# $Header: /cvsroot/pydispatcher/pydispatch/pydispatcher-2.0.0.ebuild,v 1.1.1.1 2006/07/07 15:59:38 mcfletch Exp $

# This is a pretty trivial ebuild, as the python distutils support takes care of
# just about everything for us.  Our only real problem is that the project name
# as far as distutils is concerned is PyDispatcher rather than pydispatcher.
# We get around that by defining DISTUTILS_NAME as the capitalised name,
# and then provide a similar customisation point DISTUTILS_VERSION which
# lets us define e.g. 1.0.0a1 (which is how the package is normally numbered)
# when an alpha/beta/etc version comes out with only minimal changes to this
# file.

inherit distutils
DISTUTILS_NAME="PyDispatcher"
DISTUTILS_VERSION="${PV}" # change when version has an a1 or similar extension

DESCRIPTION="Multi-producer-multi-consumer signal dispatching mechanism for Python"
HOMEPAGE="http://${PN}.sourceforge.net/"
SRC_URI="mirror://sourceforge/${PN}/${DISTUTILS_NAME}-${DISTUTILS_VERSION}.tar.gz"
# This is only temporary during my local testing phase, the sourceforge project will be the final location
#SRC_URI="http://members.rogers.com/mcfletch/programming/${DISTUTILS_NAME}-${DISTUTILS_VERSION}.tar.gz"

LICENSE="BSD"
SLOT="0" # should only be the one version installed
# testing under Gentoo, though the package should be stable
KEYWORDS="~x86 ~amd64" # should work on all python-support (i.e. Gentoo) architectures 

IUSE=""
DEPEND="virtual/python"

S="${WORKDIR}/${DISTUTILS_NAME}-${DISTUTILS_VERSION}"

src_install() {
    distutils_src_install
}
