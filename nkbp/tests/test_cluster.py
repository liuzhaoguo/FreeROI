"""Test for cluster/base.

Author: Yangzetian @ BNU/BUAA
"""

import unittest as ut
from os.path import join as pjoin
import subprocess
import pickle as pk

from numpy.testing import assert_array_equal, assert_array_almost_equal
from nose.tools import assert_equal, assert_false
import nibabel as nib

from ..cluster.base import BpVolume, VoxelInfo
from ..testing import data_path, bench_path, tmp_path



def assert_vox_list_equal(v1, v2):
    assert_equal(len(v1), len(v2))
    for v in zip(v1, v2):
        assert_vox_equal(v[0], v[1])

def assert_vox_equal(lmax1, lmax2):
    assert_equal(lmax1.coord, lmax2.coord)
    assert_equal(lmax1.value, lmax2.value)
    assert_equal(lmax1.vox_x, lmax2.vox_x)
    assert_equal(lmax1.vox_y, lmax2.vox_y)
    assert_equal(lmax1.vox_z, lmax2.vox_z)
    assert_false((hasattr(lmax1,'mm_x') - hasattr(lmax2,'mm_x') and
                  hasattr(lmax1,'mm_y') - hasattr(lmax2,'mm_y') and
                  hasattr(lmax1,'mm_z') - hasattr(lmax2,'mm_z')))
    if hasattr(lmax1,'mm_x'):
        assert_equal(lmax1.mm_x, lmax2.mm_x)
        assert_equal(lmax1.mm_y, lmax2.mm_y)
        assert_equal(lmax1.mm_z, lmax2.mm_z)

class TestBpVolume(ut.TestCase):
    def setUp(self):
        self.img1 = BpVolume(pjoin(data_path, '3D_example.nii.gz'))
        self.img2 = BpVolume(pjoin(data_path, '4D_example.nii.gz'))
        self.img3 = BpVolume(pjoin(data_path, 'zstat1.nii.gz'),
                             pjoin(data_path, 'cluster_mask_zstat1.nii.gz'))
        self.bench_coo = [(50.0, 12.0, 28.0), (34.0, -2.0, -40.0),
                          (-48.0, 16.0, 28.0), (2.0, 34.0, 34.0),
                          (-22.0, -4.0, -16.0), (0.0, 46.0, -16.0),
                          (-18.0, 0.0, 68.0)]
        self.bench_ind = [(20, 69, 50), (28, 62, 16), (69, 71, 50),
                          (44, 80, 53), (56, 61, 28), (45, 86, 28),
                          (54, 63, 70)]
        subprocess.call(['mkdir', tmp_path])

    def tearDown(self):
        subprocess.call(['rm', '-r', tmp_path])

    def test_get_clusters(self):
        clusters1 = self.img1.get_clusters_volumes(ithr=0.1, sthr=100)
        self.assertEqual(len(clusters1), 1)
        clusters2 = self.img2.get_clusters_volumes(ithr=0.1, sthr=100)
        self.assertEqual(len(clusters2), 2)
        self.assertRaises(KeyError, self.img1.get_clusters_volumes, cluster_conn=10)

    def test_ishomo(self):
        atlas = nib.load(pjoin(data_path,
                               'HarvardOxford-cort-maxprob-thr25-2mm.nii.gz'))
        atlas_bug = nib.load(pjoin(data_path,
                                   'HarvardOxford-cort-maxprob-thr25-1mm.nii.gz'))
        self.assertTrue(self.img1.ishomo(atlas))
        self.assertFalse(self.img1.ishomo(atlas_bug))

    def test_get_voxels_infos(self):
        bench = [VoxelInfo('Unknown', None, z[0], None, z[1]) for z in
                 zip(self.bench_ind, self.bench_coo)]
        assert_vox_list_equal(self.img2.get_voxels_infos(self.bench_coo), bench)
        filename = pjoin(data_path, '4D_cluster1_lmax50.txt')
        assert_vox_list_equal(self.img2.get_voxels_infos(filename), bench)

    def test_get_voxels_indices(self):
        voxels = [VoxelInfo('Unknown', None, z[0], None, z[1]) for z in
                  zip(self.bench_ind, self.bench_coo)]
        assert_equal(self.img2.get_voxels_indices(voxels), self.bench_ind)
        filename = pjoin(data_path, '4D_cluster1_lmax50.txt')
        assert_equal(self.img2.get_voxels_indices(filename), self.bench_ind)

    def test_write_roi(self):
        lmaxfile = pjoin(data_path, '4D_cluster1_lmax50.txt')
        bf_pre = '4D_cluster1_lmax50_'

        tmpfile = pjoin(tmp_path, 'tmp_plain.nii.gz')
        self.img2.write_roi(lmaxfile, algorithm='sphere', save_as=tmpfile)
        tmp = nib.load(tmpfile)
        bench = nib.load(pjoin(bench_path, bf_pre+'plain.nii.gz'))
        assert_array_equal(tmp.get_data(), bench.get_data())

        tmpfile = pjoin(tmp_path, 'tmp_sphere.nii.gz')
        self.img2.write_roi(lmaxfile, 'sphere', 20, save_as=tmpfile)
        tmp = nib.load(tmpfile)
        bench = nib.load(pjoin(bench_path, bf_pre+'sphere.nii.gz'))
        assert_array_equal(tmp.get_data(), bench.get_data())

        tmpfile = pjoin(tmp_path, 'tmp_region_grow.nii.gz')
        self.img2.write_roi(lmaxfile, 'region_grow', 20, 6, tmpfile)
        tmp = nib.load(tmpfile)
        bench = nib.load(pjoin(bench_path, bf_pre+'region_grow.nii.gz'))
        assert_array_equal(tmp.get_data(), bench.get_data())

        self.assertRaises(ValueError, self.img2.write_roi, lmaxfile, 'haha')
        

class TestClustersVolume(ut.TestCase):
    def setUp(self):
        self.img = BpVolume(pjoin(data_path, 'zstat1.nii.gz'),
                            pjoin(data_path, 'cluster_mask_zstat1.nii.gz'))
        self.clusters = self.img.get_clusters_volumes()[0] # 3D is also 4D
        subprocess.call(['mkdir', tmp_path])

    def tearDown(self):
        subprocess.call(['rm', '-r', tmp_path])

    def test_clusters_info(self):
        info = self.clusters.clusters_info
        f = pjoin(bench_path, 'zstat1_masked_clusters_info.dump')
        with open(f, 'r') as f:
            bench = pk.load(f)
            self.assertEqual(info.cluster_id, bench.cluster_id)
            self.assertEqual(info.label_idx, bench.label_idx)
            assert_array_equal(info.label, bench.label)

    def test_clusters_lmax(self):
        lmax = self.clusters.get_clusters_lmax()
        lmax_b = self.clusters.get_clusters_lmax(border=False)
        lmax20 = self.clusters.get_clusters_lmax(dthr=20)
        self.assertRaises(KeyError, self.clusters.get_clusters_lmax, lmax_conn=10)

        f = pjoin(bench_path, 'zstat1_masked_clusters_lmax.dump')
        with open(f, 'r') as f:
            bench_lmax = pk.load(f)
            bench_lmax_b = pk.load(f)
            bench_lmax20 = pk.load(f)
            self.assert_clusters_lmax_equal(lmax, bench_lmax)
            self.assert_clusters_lmax_equal(lmax_b, bench_lmax_b)
            self.assert_clusters_lmax_equal(lmax20, bench_lmax20)
            
    def test_clusters_stat(self):
        stat = self.clusters.get_clusters_stat()
        f = pjoin(bench_path, 'zstat1_masked_clusters_stat.dump')
        with open(f, 'r') as f:
            bench_stat = pk.load(f)
            self.assert_clusters_stat_equal(stat, bench_stat)

    def test_clusters_areas(self):
        img = BpVolume(pjoin(data_path, '4D_example.nii.gz'))
        clusters = img.get_clusters_volumes()[0]
        atlas = nib.load(pjoin(data_path, 
                               'HarvardOxford-cort-maxprob-thr25-2mm.nii.gz'))
        self.assertTrue(img.ishomo(atlas))

        clusters_areas = clusters.get_clusters_areas(atlas, range(1, 49))
        voxel_area = [c.get_area(atlas) for c in clusters.get_clusters_lmax()[0]]
        f = pjoin(bench_path, '4D_example_areas.dump')
        with open(f, 'r') as f:
            bench_clu = pk.load(f)
            bench_vox = pk.load(f)
            self.assert_clusters_areas_equal(clusters_areas, bench_clu)
            self.assertEqual(voxel_area, bench_vox)
        
    def test_save_clusters(self):
        img = BpVolume(pjoin(data_path, '4D_example.nii.gz'))
        clusters100 = img.get_clusters_volumes(ithr=0.1, sthr=100)
        clusters = clusters100[0]
        clusters.save_clusters(tmp_path)
        
        for n in range(1, len(clusters.clusters_info.cluster_id)+1):
            tmp = nib.load(pjoin(tmp_path, 'cluster{0}.nii.gz'.format(n)))
            bench = nib.load(pjoin(bench_path, 'cluster{0}.nii.gz'.format(n)))
            assert_array_equal(tmp.get_data(), bench.get_data())

    def assert_clusters_lmax_equal(self, lmax1, lmax2):
        self.assertEqual(len(lmax1), len(lmax2))
        for c in zip(lmax1, lmax2):
            assert_vox_list_equal(c[0], c[1])

    def assert_clusters_stat_equal(self, stat1, stat2):
        self.assertEqual(len(stat1), len(stat2))
        for c in zip(stat1, stat2):
            self.assert_stat_equal(c[0], c[1])

    def assert_stat_equal(self, stat1, stat2):
        assert_vox_equal(stat1.minimum, stat2.minimum)
        assert_vox_equal(stat1.maximum, stat2.maximum)
        self.assertEqual(stat1.sum, stat2.sum)
        self.assertEqual(stat1.mean, stat2.mean)
        self.assertEqual(stat1.median, stat2.median)
        self.assertEqual(stat1.variance, stat2.variance)
        self.assertEqual(stat1.sd, stat2.sd)
        assert_vox_equal(stat1.center_of_mass, stat2.center_of_mass)
        self.assertEqual(stat1.size, stat2.size)

    def assert_clusters_areas_equal(self, area1, area2):
        self.assertEqual(len(area1), len(area2))
        for a in zip(area1, area2):
            self.assertEqual(len(a[0]), len(a[1]))
            for b in zip(a[0], a[1]):
                self.assert_area_equal(b[0], b[1])

    def assert_area_equal(self, area1, area2):
        self.assertEqual(area1.area, area2.area)
        self.assertEqual(area1.overlap, area2.overlap)
        self.assertEqual(area1.cluster_per, area2.cluster_per)
        self.assertEqual(area1.area_per, area2.area_per)

