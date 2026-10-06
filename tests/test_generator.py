from services.password_generator import generate_password

def test_generator_length():
    p = generate_password(20)
    assert len(p) == 20

def test_generator_selected_types():
    p = generate_password(20, uppercase=True, lowercase=False, digits=False, symbols=False)
    assert p.isupper()

def test_generator_not_constant():
    a = generate_password(20)
    b = generate_password(20)
    assert a != b
