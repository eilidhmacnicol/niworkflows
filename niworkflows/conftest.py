# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
#
# Copyright 2021 The NiPreps Developers <nipreps@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# We support and encourage derived works from this project, please read
# about our expectations at
#
#     https://www.nipreps.org/community/licensing/
#
"""py.test configuration"""
import os
from sys import version_info
from pathlib import Path
import numpy as np
import nibabel as nb
import pandas as pd
import pytest
import tempfile
import pkg_resources

from .utils.bids import collect_data

test_data_env = os.getenv(
    "TEST_DATA_HOME", str(Path.home() / ".cache" / "stanford-crn")
)
test_output_dir = os.getenv("TEST_OUTPUT_DIR")
test_workdir = os.getenv("TEST_WORK_DIR")

data_dir = Path(test_data_env) / "BIDS-examples-1-enh-ds054"


@pytest.fixture(autouse=True)
def add_np(doctest_namespace):
    doctest_namespace["PY_VERSION"] = version_info
    doctest_namespace["np"] = np
    doctest_namespace["nb"] = nb
    doctest_namespace["pd"] = pd
    doctest_namespace["os"] = os
    doctest_namespace["pytest"] = pytest
    doctest_namespace["Path"] = Path
    doctest_namespace["datadir"] = data_dir
    doctest_namespace["bids_collect_data"] = collect_data
    doctest_namespace["test_data"] = pkg_resources.resource_filename(
        "niworkflows", "tests/data"
    )

    tmpdir = tempfile.TemporaryDirectory()

    doctest_namespace["tmpdir"] = tmpdir.name

    nifti_fname = str(Path(tmpdir.name) / "test.nii.gz")
    nii = nb.Nifti1Image(np.random.random((5, 5)).astype("f4"), np.eye(4))
    nii.header.set_qform(np.diag([1, 1, 1, 1]), code=1)
    nii.header.set_sform(np.diag([-1, 1, 1, 1]), code=1)
    nii.to_filename(nifti_fname)
    doctest_namespace["nifti_fname"] = nifti_fname

    cwd = os.getcwd()
    os.chdir(tmpdir.name)
    yield
    os.chdir(cwd)
    tmpdir.cleanup()


@pytest.fixture
def testdata_dir():
    return data_dir


@pytest.fixture
def ds000030_dir():
    return Path(test_data_env) / "ds000030"


@pytest.fixture
def workdir():
    return None if test_workdir is None else Path(test_workdir)


@pytest.fixture
def outdir():
    return None if test_output_dir is None else Path(test_output_dir)
