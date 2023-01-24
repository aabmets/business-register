from rik_app.utils.classutils import SingletonMeta


# -------------------------------------------------------------------------------- #
class MyClass(metaclass=SingletonMeta):
    def __init__(self, **_):
        self.data = {'abc': [1, 0]}


# -------------------------------------------------------------------------------- #
def test_class_1():
    first = MyClass()
    second = MyClass()

    first.data['abc'][0] = 9
    assert first.data == {'abc': [9, 0]}
    assert second.data == {'abc': [9, 0]}
    second.data['abc'][0] = 1
    assert first.data == {'abc': [1, 0]}
    SingletonMeta.purge_instance(MyClass)


# -------------------------------------------------------------------------------- #
def test_class_2():
    first = MyClass(should_clone=True)
    second = MyClass()

    assert first.data == {'abc': [1, 0]}
    first.data['abc'][0] = 9
    assert second.data == {'abc': [1, 0]}
    second.data['abc'][0] = 5
    assert first.data == {'abc': [9, 0]}
    first.data['abc'][0] = 1
    assert second.data == {'abc': [5, 0]}
    SingletonMeta.purge_instance(MyClass)
