import os, shutil

import click
from click.testing import CliRunner

from cogent3.util.unit_test import TestCase, main
from cogent3 import LoadTable

from mutation_motif.mutation_analysis import main as mut_main
from mutation_motif.draw import main as draw_main
from mutation_motif.all_counts import main as all_count_main


class TestCounting(TestCase):
    dirname = "_delme_counts"
    def test_all_counts(self):
        """exercising all_acounts"""
        runner = CliRunner()
        # should fail, as data files not in this directory
        r = runner.invoke(all_count_main, ["-cdata/*.txt", "-o%s" % self.dirname])
        self.assertNotEqual(r.exit_code, 0)
        r = runner.invoke(all_count_main, ["-cdata/directions/*.txt", "-o%s" % self.dirname])
        # should produce directory containing two files
        dirlist = os.listdir(self.dirname)
        self.assertEqual(set(dirlist),
                         set(["combined_counts.txt", "combined_counts.log"]))
        # check the contents of combined_counts
        counts = LoadTable(os.path.join(self.dirname, "combined_counts.txt"), sep="\t")
        # 4**4 nbrs x 12 mutations x 2 (M/R groups) = 6144
        counts = LoadTable(os.path.join(self.dirname, "combined_counts.txt"), sep="\t")
        self.assertEqual(counts.shape[0], 6144)
        shutil.rmtree(self.dirname)


class TestMutationAnalysis(TestCase):
    dirname = "_delme"
    def test_nbr(self):
        '''exercising, making sure output generated'''
        runner = CliRunner()
        r = runner.invoke(mut_main, ["-1data/counts-CtoT.txt", "-o%s" % self.dirname, "nbr"])
        self.assertEqual(r.exit_code, 0)
        # expect the following file names
        fnames = ["1.json", "1.pdf", "2.json", "2.pdf", "3.json", "3.pdf", "4.json", "4.pdf",
                 "summary.txt", "summary.pdf", "analysis.log"]
        for fn in fnames:
            path = os.path.join(self.dirname, fn)
            self.assertTrue(os.path.exists(path))
            self.assertTrue(os.path.getsize(path) > 0)
        shutil.rmtree(self.dirname)

    def test_nbr_ssym(self):
        '''exercising, nbr strand symmetric analysis'''
        runner = CliRunner()
        r = runner.invoke(mut_main, ["-1data/counts-CtoT-ss.txt", "-o%s" % self.dirname,
                        "--strand_symmetry", "nbr"])
        self.assertEqual(r.exit_code, 0)
        # expect the following file names
        fnames = ["1.json", "1.pdf", "2.json", "2.pdf", "3.json", "3.pdf", "4.json", "4.pdf",
                 "summary.txt", "summary.pdf", "analysis.log"]
        for fn in fnames:
            path = os.path.join(self.dirname, fn)
            self.assertTrue(os.path.exists(path))
            self.assertTrue(os.path.getsize(path) > 0)
        shutil.rmtree(self.dirname)
    
    def test_spectra(self):
        """exercising spectra analysis code"""
        runner = CliRunner()
        r = runner.invoke(mut_main, ["-1data/counts-combined.txt", "-o%s" % self.dirname,
                        "--strand_symmetry", "spectra"])
        self.assertEqual(r.exit_code, 0)
        
        # expect the following file names
        fnames = ["spectra_analysis.json", "spectra_analysis.log", "spectra_summary.txt"]
        for fn in fnames:
            path = os.path.join(self.dirname, fn)
            self.assertTrue(os.path.exists(path))
            self.assertTrue(os.path.getsize(path) > 0)
        shutil.rmtree(self.dirname)
    
class TestDrawGrid(TestCase):
    dirname = "_delme"
    def test_spectra_grid(self):
        """exercising draw spectra grid"""
        # first
        runner = CliRunner()
        r = runner.invoke(draw_main, ["--figpath=%s/spectra_grid.pdf" % self.dirname,
                    "spectra_grid", "--json_path=data/spectra_analysis.json",
                    "--group_label=strand"])
        self.assertEqual(r.exit_code, 0)
        fnames = ["spectra_grid.pdf", "spectra_grid.log"]
        for fn in fnames:
            path = os.path.join(self.dirname, fn)
            self.assertTrue(os.path.exists(path))
            self.assertTrue(os.path.getsize(path) > 0)
        shutil.rmtree(self.dirname)

if __name__ == '__main__':
    main()
