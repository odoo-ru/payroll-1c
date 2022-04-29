import pathlib

import pytest

from payroll_1c import Payroll1C


@pytest.fixture(scope='session')
def export_file_path():
    return pathlib.Path(__file__).parent / '1c-payroll.xml'


@pytest.fixture(params=['file-path', 'from-string'])
def payroll(export_file_path, request):
    if request.param == 'file-path':
        return Payroll1C(export_file_path)
    elif request.param == 'from-string':
        with open(export_file_path, 'rb') as export_file:
            return Payroll1C(fromstring=export_file.read())


def test_parse(payroll):
    assert payroll['ДатаФормирования'] == '2022-02-24'
    assert payroll.attrs() == {
        'ДатаФормирования': '2022-02-24',
        'ИНН': '6401',
        'НаименованиеОрганизации': 'Factory',
        'НомерДоговора': '1',
        'БИК': '6402',
        'РасчетныйСчетОрганизации': '123',
        'ИдПервичногоДокумента': '361ffab8-5bcd-11ec-9ee6-309c23b5725b',
    }
    assert list(payroll) == [
        {
            'Фамилия': 'Рогов',
            'Имя': 'Василий',
            'Отчество': 'Георгиевич',
            'ОтделениеБанка': '1',
            'ЛицевойСчет': '4201',
            'Сумма': 13890.0,
        },
        {
            'Фамилия': 'Уриевский',
            'Имя': 'Василий',
            'Отчество': 'Викторович',
            'ОтделениеБанка': '1',
            'ЛицевойСчет': '4202',
            'Сумма': 13890.0,
        },
    ]
