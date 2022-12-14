#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

# Pylint doesn't play well with fixtures and dependency injection from pytest
# pylint: disable=redefined-outer-name

import os
import pytest

from buildstream._testing.integration import assert_contains
from buildstream._testing.integration import integration_cache  # pylint: disable=unused-import
from buildstream._testing.runcli import cli_integration as cli  # pylint: disable=unused-import
from buildstream._testing._utils.site import HAVE_SANDBOX

pytestmark = pytest.mark.integration


DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "make")


# Test that a make build 'works' - we use the make sample
# makehello project for this.
@pytest.mark.datafiles(DATA_DIR)
@pytest.mark.skipif(not HAVE_SANDBOX, reason="Only available with a functioning sandbox")
def test_make_build(cli, datafiles):
    project = str(datafiles)
    checkout = os.path.join(cli.directory, "checkout")
    element_name = "makehello.bst"

    result = cli.run(project=project, args=["build", element_name])
    assert result.exit_code == 0

    result = cli.run(
        project=project,
        args=["artifact", "checkout", element_name, "--directory", checkout],
    )
    assert result.exit_code == 0

    assert_contains(checkout, ["/usr", "/usr/bin", "/usr/bin/hello"])


# Test running an executable built with make
@pytest.mark.datafiles(DATA_DIR)
@pytest.mark.skipif(not HAVE_SANDBOX, reason="Only available with a functioning sandbox")
def test_make_run(cli, datafiles):
    project = str(datafiles)
    element_name = "makehello.bst"

    result = cli.run(project=project, args=["build", element_name])
    assert result.exit_code == 0

    result = cli.run(project=project, args=["shell", element_name, "/usr/bin/hello"])
    assert result.exit_code == 0
    assert result.output == "Hello, world\n"
