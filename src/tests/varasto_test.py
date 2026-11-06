"""Tests for Varasto"""

import unittest
from varasto import Varasto


class TestVarasto(unittest.TestCase):
    """Tests if the varasto setup works"""

    def setUp(self):
        self.varasto = Varasto(10)

    def test_konstruktori_luo_tyhjan_varaston(self):
        """Tests if the constructor creates an empty stock"""
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertAlmostEqual
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_uudella_varastolla_oikea_tilavuus(self):
        """Tests if the new stock has correct space"""

        self.assertAlmostEqual(self.varasto.tilavuus, 10)

    def test_negatiivinen_alkusaldo_nollaus(self):
        """Tests if negative balance creates a 0 balance"""

        varasto = Varasto(10, -5)

        self.assertAlmostEqual(varasto.saldo, 0)

    def test_negatiivinen_tilavuus_nollavarasto(self):
        """Tests if negative space in stock creates a 0 stock"""

        varasto = Varasto(-1)

        self.assertAlmostEqual(varasto.tilavuus, 0)

    def test_liian_suuri_alkusaldo_taysi_saldo(self):
        """Tests if balance over stock space creates full stock"""

        varasto = Varasto(10, 15)

        self.assertAlmostEqual(varasto.saldo, 10)

    def test_negatiivinen_lisays_ei_muuta_saldoa(self):
        """Tests if negative balance add changes the balance"""

        self.varasto.lisaa_varastoon(-5)

        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_lisays_lisaa_saldoa(self):
        """Tests if adding balance works"""

        self.varasto.lisaa_varastoon(8)

        self.assertAlmostEqual(self.varasto.saldo, 8)

    def test_liikaa_varastoon_taysi_varasto(self):
        """
        Tests if adding too much to stock creates a full stock (not overfull)
        """

        self.varasto.lisaa_varastoon(20)

        self.assertAlmostEqual(self.varasto.saldo, 10)

    def test_lisays_lisaa_pienentaa_vapaata_tilaa(self):
        """Tests if adding balance to stock removes free space from stock"""

        self.varasto.lisaa_varastoon(8)

        # vapaata tilaa pitäisi vielä olla tilavuus-lisättävä määrä eli 2
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 2)

    def test_ottaminen_palauttaa_oikean_maaran(self):
        """Tests if removing from stock returns right amount"""

        self.varasto.lisaa_varastoon(8)

        saatu_maara = self.varasto.ota_varastosta(2)

        self.assertAlmostEqual(saatu_maara, 2)

    def test_ottaminen_lisaa_tilaa(self):
        """Tests if removing from stock adds space"""

        self.varasto.lisaa_varastoon(8)

        self.varasto.ota_varastosta(2)

        # varastossa pitäisi olla tilaa 10 - 8 + 2 eli 4
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 4)

    def test_liikaa_ottaminen_antaa_saldon(self):
        """Tests of taking too much only removes the balance amount"""

        self.varasto.lisaa_varastoon(8)

        saatu = self.varasto.ota_varastosta(80)

        self.assertAlmostEqual(saatu, 8)
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_negatiivinen_otto_ei_muuta_maaraa(self):
        """Tests if negative remove changes the balance"""

        self.varasto.lisaa_varastoon(8)
        self.varasto.ota_varastosta(-2)

        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 2)

    def test_str_palauttaa_oikein(self):
        """Tests if str returns correctly"""

        self.varasto.lisaa_varastoon(5)

        self.assertEqual(str(self.varasto), "saldo = 5, vielä tilaa 5")
