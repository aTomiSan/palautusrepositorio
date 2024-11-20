import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote

class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        self.viitegeneraattori_mock.uusi.return_value = 42
        self.varasto_mock = Mock()
        self.varasto_mock.saldo.side_effect = self.varasto_saldo 
        self.varasto_mock.hae_tuote.side_effect = self.varasto_hae_tuote 
        self.kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

    def varasto_saldo(self, tuote_id):
        if tuote_id <= 2:
            return 10
        if tuote_id == 3:
            return 0        

    def varasto_hae_tuote(self, tuote_id):
        if tuote_id == 1:
            return Tuote(1, "maito", 5)
        if tuote_id == 2:
            return Tuote(2, "keksi", 2)
        if tuote_id == 3:
            return Tuote(3, "limu", 3)


    def test_ostoksen_paaytyttya_pankin_metodia_tilisiirto_kutsutaan(self):

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called()

    def test_ostoksen_paaytyttya_pankin_metodia_tilisiirto_kutsutaan_oikeilla_arvoilla(self):

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 5)


    def test_kahden_ostoksen_päätyttyä_pankin_metodia_tilisiirto_kutsutaan_oikeilla_arvoilla(self):

        self.kauppa.aloita_asiointi() 
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 7)


    def test_kahden_saman_ostoksen_päätyttyä_pankin_metodia_tilisiirto_kutsutaan_oikeilla_arvoilla(self): 

        self.kauppa.aloita_asiointi() 
        self.kauppa.lisaa_koriin(1) 
        self.kauppa.lisaa_koriin(1) 
        self.kauppa.tilimaksu("pekka", "12345") 

        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 10)


    def test_toisen_loppuneen_ostoksen_päätyttyä_pankin_metodia_tilisiirto_kutsutaan_oikeilla_arvoilla(self): 

        self.kauppa.aloita_asiointi() 
        self.kauppa.lisaa_koriin(1) 
        self.kauppa.lisaa_koriin(3) 
        self.kauppa.tilimaksu("pekka", "12345") 

        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 5)

    def test_edellisen_ostoksen_hinta_ei_näy_seuraavassa(self): 
        self.kauppa.aloita_asiointi() 
        self.kauppa.lisaa_koriin(1) 
        self.kauppa.aloita_asiointi() 
        self.kauppa.lisaa_koriin(2) 
        self.kauppa.tilimaksu("pekka", "12345") 

        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 2)

    def test_kauppa_pyytaa_uuden_viitenumeron_jokaiselle_maksutapahtumalle(self): 
        viitegeneraattori_wrap = Mock(wraps=Viitegeneraattori())
        uusi_kauppa = Kauppa(self.varasto_mock, self.pankki_mock, viitegeneraattori_wrap)
        for x in range (2,5):
            print("X =", x)
            uusi_kauppa.aloita_asiointi() 
            uusi_kauppa.lisaa_koriin(1)
            uusi_kauppa.tilimaksu("pekka", "12345") 
            self.pankki_mock.tilisiirto.assert_called_with(ANY, x, ANY, ANY, ANY)

    def test_poistettu_tuote_ei_nay_lopullisessa_hinnassa(self): 
        self.kauppa.aloita_asiointi() 
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.poista_korista(1) 
        self.kauppa.tilimaksu("pekka", "12345") 
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 2)

