# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import os
import froi


def dir():
    froi_dir = os.path.dirname(froi.__file__)
    _icon_dir = os.path.join(froi_dir,'gui','icon')
    return _icon_dir