import nitrogen.core as nt
from pytest import Subtests

def test_core(subtests: Subtests):
    class Products(nt.Sheet):
        id = nt.Column(str)
        quantity = nt.Column(int)
        price = nt.Column(float)
        total = nt.Formula(quantity * price)

    class Users(nt.Sheet):
        name = nt.Column(str)
        product_id = nt.Column(str)
        product = nt.Relationship(Products, "product_id")
    
    with subtests.test("get formula variables"):
        print(f"\n{Products.total.dependencies}")
    
    with subtests.test("get graph properties"):
        print(f"\n{Products.graph().nodes}")
        print(f"\n{Products.graph().execution_order()}")
        print(f"\n{Products.graph().affected_by("quantity")}")

    with subtests.test("test for relationships"):
        Products.insert(id="soap", quantity=4, price=3.50)
        Users.insert(name="john", product_id="soap")

    with subtests.test("'filter' and 'all' functions"):
        Products.insert(id="rice", quantity=10, price=4.00)
        Products.insert(id="beans", quantity=15, price=4.00)

        assert len(Products.filter(price=4.00)) == 2