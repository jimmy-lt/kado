# kado/store/mixin.py
# ===================
#
# Copying
# -------
#
# Copyright (c) 2018 kado authors.
#
# This file is part of the *kado* project.
#
# kado is a free software project. You can redistribute it and/or
# modify if under the terms of the MIT License.
#
# This software project is distributed *as is*, WITHOUT WARRANTY OF ANY
# KIND; including but not limited to the WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE and NONINFRINGEMENT.
#
# You should have received a copy of the MIT License along with kado.
# If not, see <http://opensource.org/licenses/MIT>.
#
import uuid


class HasID(object):
    """Store mixin to provide a unique identifier."""

    def __init__(self):
        """Constructor for :class:`kado.store.mixin.HasID`."""
        self._id = self._id_get()


    @staticmethod
    def _id_get():
        """Internal method to get the identifier value. This method is meant to
        be overridden by subclasses in order to generate their own identifier.


        :returns: The generated identifier.
        :rtype: ~typing.Any

        """
        return uuid.uuid4()


    @property
    def id(self):
        """Get the object's unique identifier.


        :returns: The object's unique identifier.
        :rtype: ~typing.Any

        """
        return self._id
