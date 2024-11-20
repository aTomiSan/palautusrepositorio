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
        self.kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

    def test_ostoksen_paaytyttya_pankin_metodia_tilisiirto_kutsutaan(self):
        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)

        # otetaan toteutukset käyttöön
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        self.pankki_mock.tilisiirto.assert_called()
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    def test_ostoksen_paaytyttya_pankin_metodia_tilisiirto_kutsutaan_oikeilla_arvoilla(self):

        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10

        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)

        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 5)


    def test_kahden_ostoksen_päätyttyä_pankin_metodia_tilisiirto_kutsutaan_oikeilla_arvoilla(self):

        def varasto_saldo(tuote_id):
            if tuote_id == 1 or tuote_id == 2:
                return 5

        def varasto_hae_tuote(tuote_id): 
            if tuote_id == 1: 
               return Tuote(1, "keksi", 2)
            if tuote_id == 2:
                return Tuote(2, "limu", 3)

        self.varasto_mock.saldo.side_effect = varasto_saldo 
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote 

        self.kauppa.aloita_asiointi() 
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 5)


    def test_kahden_saman_ostoksen_päätyttyä_pankin_metodia_tilisiirto_kutsutaan_oikeilla_arvoilla(self): 

        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            
        def varasto_hae_tuote(tuote_id): 
            if tuote_id == 1: 
                return Tuote(1, "keksi", 2)
            
        self.varasto_mock.saldo.side_effect = varasto_saldo 
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote 

        self.kauppa.aloita_asiointi() 
        self.kauppa.lisaa_koriin(1) 
        self.kauppa.lisaa_koriin(1) 
        self.kauppa.tilimaksu("pekka", "12345") 

        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 4)


    def test_toisen_loppuneen_ostoksen_päätyttyä_pankin_metodia_tilisiirto_kutsutaan_oikeilla_arvoilla(self): 

        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 0
            
        def varasto_hae_tuote(tuote_id): 
            if tuote_id == 1: 
                return Tuote(1, "keksi", 2)
            if tuote_id == 2: 
                return Tuote(2, "limu", 3)
            
        self.varasto_mock.saldo.side_effect = varasto_saldo 
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote 

        self.kauppa.aloita_asiointi() 
        self.kauppa.lisaa_koriin(1) 
        self.kauppa.lisaa_koriin(2) 
        self.kauppa.tilimaksu("pekka", "12345") 

        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 2)

