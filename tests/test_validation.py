import pytest
from pydantic import ValidationError
from credit.schema import ClientInput

def test_invalid_age():
    with pytest.raises(ValidationError):
        ClientInput(
            idade=15, estado_civil="solteiro", escolaridade="medio", profissao="clt",
            tempo_emprego_meses=0, renda_mensal=2000, gastos_mensais=500, dividas_ativas=0,
            score_credito=600, historico_inadimplencia=0, atrasos_anteriores=0, pct_renda_comprometida=0.25
        )
