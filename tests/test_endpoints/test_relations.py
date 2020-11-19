#
# Gramps Web API - A RESTful API for the Gramps genealogy program
#
# Copyright (C) 2020      Christopher Horn
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

"""Tests for the /api/relations endpoints using example_gramps."""

import unittest

from . import get_test_client


class TestRelation(unittest.TestCase):
    """Test cases for the /api/relations/{handle1}/{handle2} endpoint."""

    @classmethod
    def setUpClass(cls):
        """Test class setup."""
        cls.client = get_test_client()

    def test_relations_endpoint_404(self):
        """Test response for missing or bad handles."""
        # check various handle issues
        result = self.client.get("/api/relations/9BXKQC1PVLPYFMD6IX")
        self.assertEqual(result.status_code, 404)
        result = self.client.get("/api/relations/9BXKQC1PVLPYFMD6IX/ORFKQC4KLWEGTGR1")
        self.assertEqual(result.status_code, 404)
        result = self.client.get("/api/relations/9BXKQC1PVLPYFMD6I/ORFKQC4KLWEGTGR19L")
        self.assertEqual(result.status_code, 404)

    def test_relations_endpoint(self):
        """Test response for valid request."""
        # check expected response which also confirms response schema
        result = self.client.get("/api/relations/9BXKQC1PVLPYFMD6IX/ORFKQC4KLWEGTGR19L")
        self.assertEqual(
            result.json,
            {
                "distance_common_origin": 5,
                "distance_common_other": 1,
                "relationship_string": "second great stepgrandaunt",
            },
        )

    def test_relations_endpoint_parms(self):
        """Test responses for query parms."""
        # check bad or invalid query parm
        result = self.client.get(
            "/api/relations/9BXKQC1PVLPYFMD6IX/ORFKQC4KLWEGTGR19L?junk=1"
        )
        self.assertEqual(result.status_code, 422)
        # check depth parm working as expected
        result = self.client.get(
            "/api/relations/9BXKQC1PVLPYFMD6IX/ORFKQC4KLWEGTGR19L?depth"
        )
        self.assertEqual(result.status_code, 422)
        result = self.client.get(
            "/api/relations/9BXKQC1PVLPYFMD6IX/ORFKQC4KLWEGTGR19L?depth=5"
        )
        self.assertEqual(result.json["relationship_string"], "")
        result = self.client.get(
            "/api/relations/9BXKQC1PVLPYFMD6IX/ORFKQC4KLWEGTGR19L?depth=6"
        )
        self.assertEqual(
            result.json["relationship_string"], "second great stepgrandaunt"
        )
        # check locale parm working
        result = self.client.get(
            "/api/relations/9BXKQC1PVLPYFMD6IX/ORFKQC4KLWEGTGR19L?locale"
        )
        self.assertEqual(result.status_code, 422)
        result = self.client.get(
            "/api/relations/9BXKQC1PVLPYFMD6IX/ORFKQC4KLWEGTGR19L?locale=1"
        )
        self.assertEqual(result.status_code, 200)


class TestRelations(unittest.TestCase):
    """Test cases for the /api/relations/{handle1}/{handle2}/all endpoint."""

    @classmethod
    def setUpClass(cls):
        """Test class setup."""
        cls.client = get_test_client()

    def test_relations_all_endpoint_404(self):
        """Test response for missing or bad handles."""
        # check various handle issues
        result = self.client.get("/api/relations/9BXKQC1PVLPYFMD6IX/all")
        self.assertEqual(result.status_code, 404)
        result = self.client.get(
            "/api/relations/9BXKQC1PVLPYFMD6IX/ORFKQC4KLWEGTGR1/all"
        )
        self.assertEqual(result.status_code, 404)
        result = self.client.get(
            "/api/relations/9BXKQC1PVLPYFMD6I/ORFKQC4KLWEGTGR19L/all"
        )
        self.assertEqual(result.status_code, 404)

    def test_relations_all_endpoint(self):
        """Test response for valid request."""
        # check expected response which also confirms response schema
        result = self.client.get(
            "/api/relations/9BXKQC1PVLPYFMD6IX/ORFKQC4KLWEGTGR19L/all"
        )
        self.assertIn("common_ancestors", result.json[0])
        self.assertEqual(
            result.json[0]["relationship_string"], "second great stepgrandaunt"
        )

    def test_relations_all_endpoint_parms(self):
        """Test responses for query parms."""
        # check bad or invalid query parm
        result = self.client.get(
            "/api/relations/9BXKQC1PVLPYFMD6IX/ORFKQC4KLWEGTGR19L/all?junk=1"
        )
        self.assertEqual(result.status_code, 422)
        # check depth parm working as expected
        result = self.client.get(
            "/api/relations/9BXKQC1PVLPYFMD6IX/ORFKQC4KLWEGTGR19L/all?depth"
        )
        self.assertEqual(result.status_code, 422)
        result = self.client.get(
            "/api/relations/9BXKQC1PVLPYFMD6IX/ORFKQC4KLWEGTGR19L/all?depth=5"
        )
        self.assertEqual(result.json, [{}])
        result = self.client.get(
            "/api/relations/9BXKQC1PVLPYFMD6IX/ORFKQC4KLWEGTGR19L/all?depth=6"
        )
        self.assertEqual(
            result.json[0]["relationship_string"], "second great stepgrandaunt"
        )