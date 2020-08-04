from decimal import Decimal

from electrum_dash.util import (format_satoshis, format_fee_satoshis, parse_URI,
                                is_hash256_str, chunks, InvalidBitcoinURI)

from . import SequentialTestCase


class TestUtil(SequentialTestCase):

    def test_format_satoshis(self):
        self.assertEqual("0.00001234", format_satoshis(1234))

    def test_format_satoshis_negative(self):
        self.assertEqual("-0.00001234", format_satoshis(-1234))

    def test_format_fee_float(self):
        self.assertEqual("1.7", format_fee_satoshis(1700/1000))

    def test_format_fee_decimal(self):
        self.assertEqual("1.7", format_fee_satoshis(Decimal("1.7")))

    def test_format_fee_precision(self):
        self.assertEqual("1.666",
                         format_fee_satoshis(1666/1000, precision=6))
        self.assertEqual("1.7",
                         format_fee_satoshis(1666/1000, precision=1))

    def test_format_satoshis_whitespaces(self):
        self.assertEqual("     0.0001234 ",
                         format_satoshis(12340, whitespaces=True))
        self.assertEqual("     0.00001234",
                         format_satoshis(1234, whitespaces=True))

    def test_format_satoshis_whitespaces_negative(self):
        self.assertEqual("    -0.0001234 ",
                         format_satoshis(-12340, whitespaces=True))
        self.assertEqual("    -0.00001234",
                         format_satoshis(-1234, whitespaces=True))

    def test_format_satoshis_diff_positive(self):
        self.assertEqual("+0.00001234",
                         format_satoshis(1234, is_diff=True))

    def test_format_satoshis_diff_negative(self):
        self.assertEqual("-0.00001234", format_satoshis(-1234, is_diff=True))

    def _do_test_parse_URI(self, uri, expected):
        result = parse_URI(uri)
        self.assertEqual(expected, result)

    def test_parse_URI_address(self):
        part_URI = 'XfTA9qgYmaEHfWhUakwcoTtyquez8SowY1'
        URI = f'dash:{part_URI}'
        self._do_test_parse_URI(
            URI, {'address': 'XfTA9qgYmaEHfWhUakwcoTtyquez8SowY1'})

        URI = f'pay:{part_URI}'
        with self.assertRaises(InvalidBitcoinURI):
            self._do_test_parse_URI(URI, None)

    def test_parse_URI_only_address(self):
        URI = 'XfTA9qgYmaEHfWhUakwcoTtyquez8SowY1'
        self._do_test_parse_URI(
            URI, {'address': 'XfTA9qgYmaEHfWhUakwcoTtyquez8SowY1'})

    def test_parse_URI_address_label(self):
        part_URI = 'XfTA9qgYmaEHfWhUakwcoTtyquez8SowY1?label=electrum%20test'
        URI = f'dash:{part_URI}'
        self._do_test_parse_URI(
            URI, {'address': 'XfTA9qgYmaEHfWhUakwcoTtyquez8SowY1',
                  'label': 'electrum test'})

        URI = f'pay:{part_URI}'
        with self.assertRaises(InvalidBitcoinURI):
            self._do_test_parse_URI(URI, None)

    def test_parse_URI_address_message(self):
        part_URI = 'XfTA9qgYmaEHfWhUakwcoTtyquez8SowY1?message=electrum%20test'
        URI = f'dash:{part_URI}'
        self._do_test_parse_URI(
            URI, {'address': 'XfTA9qgYmaEHfWhUakwcoTtyquez8SowY1',
                  'message': 'electrum test', 'memo': 'electrum test'})

        URI = f'pay:{part_URI}'
        with self.assertRaises(InvalidBitcoinURI):
            self._do_test_parse_URI(URI, None)

    def test_parse_URI_address_amount(self):
        part_URI = 'XfTA9qgYmaEHfWhUakwcoTtyquez8SowY1?amount=0.0003'
        URI = f'dash:{part_URI}'
        self._do_test_parse_URI(
            URI, {'address': 'XfTA9qgYmaEHfWhUakwcoTtyquez8SowY1',
                  'amount': 30000})

        URI = f'pay:{part_URI}'
        with self.assertRaises(InvalidBitcoinURI):
            self._do_test_parse_URI(URI, None)

    def test_parse_URI_address_request_url(self):
        part_URI = ('XfTA9qgYmaEHfWhUakwcoTtyquez8SowY1'
                    '?r=http://domain.tld/page?h%3D2a8628fc2fbe')
        URI = f'dash:{part_URI}'
        self._do_test_parse_URI(
            URI, {'address': 'XfTA9qgYmaEHfWhUakwcoTtyquez8SowY1',
                  'r': 'http://domain.tld/page?h=2a8628fc2fbe'})

        URI = f'pay:{part_URI}'
        with self.assertRaises(InvalidBitcoinURI):
            self._do_test_parse_URI(URI, None)

    def test_parse_URI_ignore_args(self):
        part_URI ='XfTA9qgYmaEHfWhUakwcoTtyquez8SowY1?test=test'
        URI = f'dash:{part_URI}'
        self._do_test_parse_URI(
            URI, {'address': 'XfTA9qgYmaEHfWhUakwcoTtyquez8SowY1',
                  'test': 'test'})

        URI = f'pay:{part_URI}'
        with self.assertRaises(InvalidBitcoinURI):
            self._do_test_parse_URI(URI, None)

    def test_parse_URI_multiple_args(self):
        part_URI = ('XfTA9qgYmaEHfWhUakwcoTtyquez8SowY1'
                    '?amount=0.00004&label=electrum-test'
                    '&message=electrum%20test&test=none'
                    '&r=http://domain.tld/page')
        URI = f'dash:{part_URI}'
        self._do_test_parse_URI(
            URI, {'address': 'XfTA9qgYmaEHfWhUakwcoTtyquez8SowY1',
                  'amount': 4000, 'label': 'electrum-test',
                  'message': u'electrum test', 'memo': u'electrum test',
                  'r': 'http://domain.tld/page', 'test': 'none'})

        URI = f'pay:{part_URI}'
        with self.assertRaises(InvalidBitcoinURI):
            self._do_test_parse_URI(URI, None)

    def test_parse_URI_no_address_request_url(self):
        part_URI = '?r=http://domain.tld/page?h%3D2a8628fc2fbe'
        URI = f'dash:{part_URI}'
        self._do_test_parse_URI(
            URI, {'r': 'http://domain.tld/page?h=2a8628fc2fbe'})

        URI = f'pay:{part_URI}'
        self._do_test_parse_URI(
            URI, {'r': 'http://domain.tld/page?h=2a8628fc2fbe'})

    def test_parse_URI_invalid_address(self):
        self.assertRaises(BaseException, parse_URI, 'dash:invalidaddress')

    def test_parse_URI_invalid(self):
        self.assertRaises(BaseException, parse_URI, 'notdash:XfTA9qgYmaEHfWhUakwcoTtyquez8SowY1')

    def test_parse_URI_parameter_polution(self):
        self.assertRaises(Exception, parse_URI, 'dash:XfTA9qgYmaEHfWhUakwcoTtyquez8SowY1?amount=0.0003&label=test&amount=30.0')

    def test_is_hash256_str(self):
        self.assertTrue(is_hash256_str('09a4c03e3bdf83bbe3955f907ee52da4fc12f4813d459bc75228b64ad08617c7'))
        self.assertTrue(is_hash256_str('2A5C3F4062E4F2FCCE7A1C7B4310CB647B327409F580F4ED72CB8FC0B1804DFA'))
        self.assertTrue(is_hash256_str('00' * 32))

        self.assertFalse(is_hash256_str('00' * 33))
        self.assertFalse(is_hash256_str('qweqwe'))
        self.assertFalse(is_hash256_str(None))
        self.assertFalse(is_hash256_str(7))

    def test_chunks(self):
        self.assertEqual([[1, 2], [3, 4], [5]],
                         list(chunks([1, 2, 3, 4, 5], 2)))
        with self.assertRaises(ValueError):
            list(chunks([1, 2, 3], 0))
