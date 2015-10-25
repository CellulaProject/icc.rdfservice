""" Cornice services.
"""
from cornice import Service


hello = Service(name='hello', path='/', description="Simplest app")
test = Service(name='test_dir', path='/test/', description="Test dir")


@hello.get()
def get_info(request):
    """Returns Hello in JSON."""
    return {'Hello': 'World'}

@test.get()
def get_test(request):
    return {'test':'nice'}