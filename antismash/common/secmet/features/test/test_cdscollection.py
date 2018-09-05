# License: GNU Affero General Public License v3 or later
# A copy of GNU AGPL v3 should have been included in this software package in LICENSE.txt.

# for test files, silence irrelevant and noisy pylint warnings
# pylint: disable=no-self-use,protected-access,missing-docstring

import unittest

from antismash.common.secmet.features import CDSCollection, CDSFeature, FeatureLocation


class TestCDSCollection(unittest.TestCase):
    def test_parent_linkage(self):
        child = CDSCollection(FeatureLocation(20, 40), feature_type="test", child_collections=[])
        assert child.parent is None
        parent = CDSCollection(FeatureLocation(10, 50), feature_type="test", child_collections=[child])
        assert child.parent is parent

    def test_bad_child(self):
        with self.assertRaises(AssertionError):
            child = CDSCollection(FeatureLocation(10, 50), feature_type="test", child_collections=[])
            CDSCollection(FeatureLocation(20, 40), feature_type="test", child_collections=[child])

        with self.assertRaises(AssertionError):
            cds = CDSFeature(FeatureLocation(25, 35, strand=1), locus_tag="test")
            CDSCollection(FeatureLocation(20, 40), feature_type="test", child_collections=[cds])

    def test_root(self):
        child = CDSCollection(FeatureLocation(20, 40), feature_type="test", child_collections=[])
        assert child.get_root() is child
        parent = CDSCollection(FeatureLocation(10, 50), feature_type="test", child_collections=[child])
        assert child.get_root() is parent
        grandparent = CDSCollection(FeatureLocation(0, 60), feature_type="test", child_collections=[parent])
        for col in [child, parent, grandparent]:
            assert col.get_root() is grandparent

    def test_add_cds(self):
        collection = CDSCollection(FeatureLocation(20, 40), feature_type="test", child_collections=[])
        cds = CDSFeature(FeatureLocation(20, 40, strand=1), locus_tag="test")
        collection.add_cds(cds)
        assert cds in collection.cds_children

        cds = CDSFeature(FeatureLocation(120, 140, strand=1), locus_tag="test")
        with self.assertRaisesRegex(ValueError, "not contained by"):
            collection.add_cds(cds)
