import pytest

from src.config import NCDC_ROOT
from src.extractor import GFSExtractor

class TestExtractor:

    EXPECTED_MONTHS = [
        '201704',
        '201703',
        '201702',
        '201701',
        '201612',
        '201611',
        '201610',
        '201609',
        '201608',
        '201607',
        '201606',
        '201605',
        '201604',
        '201603',
        '201602',
        '201601',
        '201512',
        '201511',
        '201510',
        '201509',
        '201508',
        '201507',
        '201506',
        '201505'
    ]

    def test_months(self):
        m_ext = GFSExtractor(root=NCDC_ROOT)
        mts = m_ext.extract_months()
        assert sorted(mts) == sorted(self.EXPECTED_MONTHS)

    def test_months_to_fail(self):
        m_ext = GFSExtractor(root=NCDC_ROOT)
        mts = m_ext.extract_months()
        assert sorted(mts) != ['201704', '201703']

