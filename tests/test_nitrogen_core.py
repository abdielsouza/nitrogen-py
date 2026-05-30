import nitrogen.core as nt
from pytest import Subtests

def test_core(subtests: Subtests):
    class Products(nt.Sheet):
        quantity = nt.Column(int)
        price = nt.Column(float)
        total = nt.Formula(quantity * price)
    
    with subtests.test("get formula variables"):
        print(f"\n{Products.total.dependencies}")
    
    with subtests.test("get graph properties"):
        print(f"\n{Products.graph().nodes}")
        print(f"\n{Products.graph().execution_order()}")
        print(f"\n{Products.graph().affected_by("quantity")}")