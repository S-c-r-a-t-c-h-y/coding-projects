class ClassName:
    def __init__(self):
        """The __init__ is the initialization function :
        add arguments after the "self" to
        add parameters when creating an instance
        of your class.

        You can then transform these arguments in
        attributes of the class by writing :
        "self.argument_name" just below

        This function is called each time you
        create an instance of this class
        """

        pass

    def __str__(self):
        """
        The __str__ method is used to get the "informal" value as a string.

        It is called with the "str()" built-in function and
        whenever print(an_instance_of_the_class) is called.

        Let x be an instance of the class:
        both str(x) and print(x) will call x.__str__()
        """

        pass

    def __repr__(self):
        """
        The __repr__ method is used to get the "official" value as a string.

        By convention, the __repr__() method should return a string
        that is a valid Python expression.

        It is called with the "repr()" built-in function.

        Let x be an instance of the class:
        repr(x) will call x.__repr__()
        """

        pass

    def __bytes__(self):
        """
        The __bytes__ method is used to get the "informal" value as a byte array.

        This method is new in Python 3.

        It is called with the "bytes()" built-in function.

        Let x be an instance of the class:
        bytes(x) will call x.__bytes__()
        """

        pass

    def __format__(self, format_spec):
        """
        The __format__ method is used to get the value as a formatted string.

        By convention, format_spec should conform to
        the Format Specification Mini-Language.

        It is called with the "format()" built-in function.

        Let x be an instance of the class:
        format(x, format_spec) will call x.__format__(format_spec)
        """

        pass

    """ ----- The following methods are reserved to classes that act like iterators ----- """

    def __iter__(self):
        """
        The __iter__ method create an iterable object
        of your class when iter(instance_of_your_class)
        is called.

        You can then use the built-in function next() with your
        newly created iterator the iterate threw the class
        (You need to define the __next__() method in your class)

        This method should always return "self"
        """

        # a variable to keep track of the index of the
        #  current iteration
        return self

    def __next__(self):
        """
        The __next__ method is paired with the __iter__()
        method.

        It is called with the next() built-in function
        by passing an iterator of your class
        created by the __iter__() method as argument.

        The __next__() method must return the next item
        in the sequence. On reaching the end, and in subsequent
        calls, it must raise StopIteration except if your class
        is an infinte iterator.

        """

        """ Here is an exemple of what it should look like
			if it isn't an infinite iterator :

			if current_iteration <= max_iteration: # if this isn't the last iteration
				# calculate the next item 
				return item
			else: # if the last iteration as been executed
				raise StopIteration
		"""

        pass

    def __reversed__(self):
        """
        The __reversed__ method is the same as the __iter__ one
        except that it returns an iterator that yields
        the items in the sequence in reverse order, from last to first.

        This method is called with the "reversed()" built-in function.

        Exemple:
        reversed(x) will call x.__reversed__()
        """

        pass

    """ ----- The following methods are reserved for classes that act like sequences ----- """

    def __contains__(self, request):
        """The __contain__ method define the behaviour of
        the "in" built-in keyword with an instance
        of this class.

        Exemple:
        if your class is similar to a liste:

        return request in self.attribute_that_stock_the_values

        """
        pass

    def __len__(self):
        """The __len__ method is called with the "len()" built-in function.

        Ideally it returns the number of object in the class.

        Exemple:
        len(x) will call x.__len__()
        """
        pass

    """ ----- The following methods are reserved for classes that act like dictionaries ----- """

    def __getitem__(self, key):
        """
        The __getitem__ method is called when you try
        to get a value by its key.

        Its the same method used in the lists too, except that the
        key represent an index

        Exemple:
        x[key] will call x.__getitem__(key)
        """

        # here is a template that you can complete to fit your needs

        found = []

        # some code that will append all of the matching
        # values to the "found" list

        if not found:
            raise KeyError(key)  # if there if no value that respond to the key, it throws a KeyError
        if len(found) == 1:
            return found[0]  # if there is only one item found, it doesn't returns it as a list
        else:
            return found

    def __setitem__(self, key, value):
        """
        The __setitem__ method is called to set a value by its key,
        even if the key is inexistant.

        Its the same method used in the lists too, except that the
        key represent an index.

        Exemple:
        x[key] = value will call x.__setitem__(key, value)
        """

        pass

    def __delitem__(self, key):
        """
        The __delitem__ method is called to delete a key-value pair
        by specifying its key.

        Exemple:
        del x[key] will call x.__delitem__(key)
        """

        pass

    def __missing__(self, nonexistent_key):
        """
        The __missing__ method is called to provide a default
        value for missing keys.

        The type "list" doesn't implement this function.

        Exemple:
        x[nonexistent_key] will call x.__missing__(nonexistent_key)
        """

        pass

    """ ----- Methods related to attributes ----- """

    def __getattribute__(self, attribute):
        """
        The __getattribute__ method is called to get a computed attribute (unconditionally).

        If your class defines a __getattribute__() method, Python will call
        it on every reference to any attribute or method name
        (except special method names, since that would cause an unpleasant infinite loop).

        Exemple:
        x.my_attribute will call x.__getattribute('my_attribute')
        """

        pass

    def __getattr__(self, attribute):
        """
        The __getattr__ method is called to get a computed attribute (fallback).

        If your class defines a __getattr__() method, Python will call
        it only after looking for the attribute in all the normal places.
        If an instance x defines an attribute color, x.color will not call
        x.__getattr__('color'); it will simply return the already-defined value of x.color.

        The difference with the __getattribute__ method is subtle but really important,
        check it out at :
        https://stackoverflow.com/questions/4295678/understanding-the-difference-between-getattr-and-getattribute/4295743

        Exemple:
        x.my_attribute will call x.__getattr('my_attribute')
        """

        pass

    def __setattr__(self, attribute, value):
        """
        The __setattr__() method is called whenever you assign a value to an attribute.

        Exemple:
        x.my_attribute = value will call x.__setattr__('my_attribute', value)
        """

        pass

    def __delattr__(self, attribute):
        """
        The __delattr__() method is called whenever you delete an attribute.

        Exemple:
        del x.my_attribute will call x.__delattr__('my_attribute')
        """

        pass

    def __dir__(self):
        """
        The __dir__() method is useful if you define a __getattr__()
        or __getattribute__() method. Normally, calling dir(x) would
        only list the regular attributes and methods. If your __getattr__()
        method handles an attribute dynamically, dir(x) would not list
        this attribute as one of the available attributes. Overriding the __dir__() method
        allows you to list the previous attribute as an available attribute, which is helpful for other
        people who wish to use your class without digging into the internals of it.

        Exemple:
        dir(x) will call x.__dir__()
        """

    """ 
		----- The following methods are reserved to classes that act like numbers -----
		Each method (except the "inplace" ones) should return another instance of the class newly created.

		These methods are divided in 4 categories: 
			- Methods that take the first approach : given x / y, they provide a way for x to say "I know how to divide myself by y"
			- Methods that take the second approach : given x / y, they provide a way for y to say "I know how to be the denominator and divide myself into x.""
			- Inplace operations (x /= y)
			- Mathematical operations that can be performed by itself

	"""

    """ -- First categorie (Methods that take the first approach) -- """

    def __add__(self, other):
        """
        To add itself with another object.

        Exemple:
        x + y will call x.__add__(y)
        """

        new_instance = ClassName()

        # some code

        return new_instance

    def __sub__(self, other):
        """
        To substract itself with another object.

        Exemple:
        x - y will call x.__sub__(y)
        """

        new_instance = ClassName()

        # some code

        return new_instance

    def __mul__(self, other):
        """
        To multiply itself with another object.

        Exemple:
        x * y will call x.__mul__(y)
        """

        new_instance = ClassName()

        # some code

        return new_instance

    def __truediv__(self, other):
        """
        To divide itself with another object.

        Exemple:
        x / y will call x.__truediv__(y)
        """

        new_instance = ClassName()

        # some code

        return new_instance

    def __floordiv__(self, other):
        """
        To perform floor division with another object.

        Exemple:
        x // y will call x.__floordiv__(y)
        """

        new_instance = ClassName()

        # some code

        return new_instance

    def __mod__(self, other):
        """
        To perform the modulo (remainder) operation with another object.

        Exemple:
        x % y will call x.__mod__(y)
        """

        new_instance = ClassName()

        # some code

        return new_instance

    def __divmod__(self, other):
        """
        To perform floor division and modulo (with the "divmod()" function) with another object.

        Exemple:
        divmod(x, y) will call x.__divmod__(y)
        """

        new_instance = ClassName()

        # some code

        return new_instance

    def __pow__(self, other):
        """
        To raise itself to the power of another object.

        Exemple:
        x ** y will call x.__pow__(y)
        """

        new_instance = ClassName()

        # some code

        return new_instance

    def __lshift__(self, other):
        """
        To perform left bit-shift with another object.

        Exemple:
        x << y will call x.__lshift__(y)
        """

        new_instance = ClassName()

        # some code

        return new_instance

    def __rshift__(self, other):
        """
        To perform right bit-shift with another object.

        Exemple:
        x >> y will call x.__rshift__(y)
        """

        new_instance = ClassName()

        # some code

        return new_instance

    def __and__(self, other):
        """ "
        To perform bitwise "and" with another object.

        Exemple:
        x & y will call x.__and__(y)
        """

        new_instance = ClassName()

        # some code

        return new_instance

    def __xor__(self, other):
        """
        To perform bitwise "xor" with another object.

        Exemple:
        x ^ y will call x.__xor__(y)
        """

        new_instance = ClassName()

        # some code

        return new_instance

    def __or__(self, other):
        """
        To perform bitwise "or" with another object.

        Exemple:
        x | y will call x.__or__(y)
        """

        new_instance = ClassName()

        # some code

        return new_instance

    """ -- Second categorie (Methods that take the second approach) -- """

    def __radd__(self, other):
        """
        To add itself with another object.

        Exemple:
        x + y will call y.__radd__(x)
        """

        new_instance = ClassName()

        # some code

        return new_instance

    def __rsub__(self, other):
        """
        To substract itself with another object.

        Exemple:
        x - y will call y.__rsub__(x)
        """

        new_instance = ClassName()

        # some code

        return new_instance

    def __rmul__(self, other):
        """
        To multiply itself with another object.

        Exemple:
        x * y will call y.__rmul__(x)
        """

        new_instance = ClassName()

        # some code

        return new_instance

    def __rtruediv__(self, other):
        """
        To divide itself with another object.

        Exemple:
        x / y will call y.__rtruediv__(x)
        """

        new_instance = ClassName()

        # some code

        return new_instance

    def __rfloordiv__(self, other):
        """
        To perform floor division with another object.

        Exemple:
        x // y will call y.__rfloordiv__(x)
        """

        new_instance = ClassName()

        # some code

        return new_instance

    def __rmod__(self, other):
        """
        To perform the modulo (remainder) operation with another object.

        Exemple:
        x % y will call y.__rmod__(x)
        """

        new_instance = ClassName()

        # some code

        return new_instance

    def __rdivmod__(self, other):
        """
        To perform floor division and modulo (with the "divmod()" function) with another object.

        Exemple:
        divmod(x, y) will call y.__rdivmod__(x)
        """

        new_instance = ClassName()

        # some code

        return new_instance

    def __rpow__(self, other):
        """
        To raise itself to the power of another object.

        Exemple:
        x ** y will call y.__rpow__(x)
        """

        new_instance = ClassName()

        # some code

        return new_instance

    def __rlshift__(self, other):
        """
        To perform left bit-shift with another object.

        Exemple:
        x << y will call y.__rlshift__(x)
        """

        new_instance = ClassName()

        # some code

        return new_instance

    def __rrshift__(self, other):
        """
        To perform right bit-shift with another object.

        Exemple:
        x >> y will call y.__rrshift__(x)
        """

        new_instance = ClassName()

        # some code

        return new_instance

    def __rand__(self, other):
        """ "
        To perform bitwise "and" with another object.

        Exemple:
        x & y will call y.__rand__(x)
        """

        new_instance = ClassName()

        # some code

        return new_instance

    def __rxor__(self, other):
        """
        To perform bitwise "xor" with another object.

        Exemple:
        x ^ y will call y.__rxor__(x)
        """

        new_instance = ClassName()

        # some code

        return new_instance

    def __ror__(self, other):
        """
        To perform bitwise "or" with another object.

        Exemple:
        x | y will call y.__ror__(x)
        """

        new_instance = ClassName()

        # some code

        return new_instance

    """ --	Third categorie (Methods to make in-place operations) -- """

    def __iadd__(self, other):
        """
        To add itself with another object in-place.

        Exemple:
        x += y will call x.__iadd__(y)
        """

        pass

    def __isub__(self, other):
        """
        To substract itself with another object in-place.

        Exemple:
        x -= y will call x.__isub__(y)
        """

        pass

    def __imul__(self, other):
        """
        To multiply itself with another object in-place.

        Exemple:
        x *= y will call x.__imul__(y)
        """

        pass

    def __itruediv__(self, other):
        """
        To divide itself with another object in-place.

        Exemple:
        x /= y will call x.__itruediv__(y)
        """

        pass

    def __ifloordiv__(self, other):
        """
        To perform in-place floor division with another object.

        Exemple:
        x //= y will call x.__ifloordiv__(y)
        """

        pass

    def __imod__(self, other):
        """
        To perform the modulo (remainder) operation in-place with another object.

        Exemple:
        x %= y will call x.__imod__(y)
        """

        pass

    def __ipow__(self, other):
        """
        To raise itself to the power of another object in-place.

        Exemple:
        x **= y will call x.__ipow__(y)
        """

        pass

    def __ilshift__(self, other):
        """
        To perform in-place left bit-shift with another object.

        Exemple:
        x <<= y will call x.__ilshift__(y)
        """

        pass

    def __irshift__(self, other):
        """
        To perform in-place right bit-shift with another object.

        Exemple:
        x >>= y will call x.__irshift__(y)
        """

        pass

    def __iand__(self, other):
        """ "
        To perform in-place bitwise "and" with another object.

        Exemple:
        x &= y will call x.__iand__(y)
        """

        pass

    def __ixor__(self, other):
        """
        To perform in-place bitwise "xor" with another object.

        Exemple:
        x ^= y will call x.__ixor__(y)
        """

        pass

    def __ior__(self, other):
        """
        To perform in-place bitwise "or" with another object.

        Exemple:
        x |= y will call x.__ior__(y)
        """

        pass

    """ -- Forth categorie (Mathematical operations that can be performed by itself) -- """

    def __neg__(self):
        """
        The __neg__ method returns the negative value of your class(if your_class == 2: return -2).

        Exemple:
        -x will call x.__neg__()
        """

        pass

    def __pos__(self):
        """
        The __pos__ method returns the positive value of your class (if your_class == -2: return 2).

        Exemple:
        +x will call x.__pos__()
        """

        pass

    def __abs__(self):
        """
        The __abs__ method returns the absolute value of your class.

        Exemple:
        abs(x) will call x.__abs__()
        """

        pass

    def __invert__(self):
        """
        The __invert__ method returns the inverse of the value of your class.

        Exemple:
        ~x will call x.__invert__()
        """

        pass

    def __complex__(self):
        """
        the __complex__ method returns the complex value of your class.

        Exemple:
        complex(x) will call x.__complex__()
        """

        pass

    def __int__(self):
        """
        The __int__ method returns the integer value of your class.

        Exemple:
        int(x) will call x.__int__()
        """

        pass

    def __float__(self):
        """
        The __float__ method returns the float value of your class.

        Exemple:
        float(x) will call x.__float__()
        """

        pass

    def __round__(self, n=None):
        """
        The __round__ method returns the value of your class rounded to the nearest integer if there is no parameter.
        It returns the value of your class rounded to the nearest n integer if there is a specified parameter.

        Exemple:
        round(x) will call x.__round__()
        round(x, n) will call x.__round__(n)
        """

        pass

    def __ceil__(self):
        """
        The __ceil__ method returns the smallest integer >= the value of your class.

        Exemple:
        math.ceil(x) will call x.__ceil__()
        """

        pass

    def __floor__(self):
        """
        The __floor__ method returns the largest integer <= the value of your class.

        Exemple:
        maths.floor(x) will call x.__floor__()
        """

        pass

    def __trunc__(self):
        """
        The __trunc__ method truncate the value of your class to the nearest integer toward 0.

        Exemple:
        math.trunc(x) will call x.__trunc__()
        """

        pass

    """ ----- The following methods are reserved for classes that can be used in a "with" block ----- """

    def __enter__(self):
        """
        The __enter__ method is used to do something special when entering a "with" block.

        Exemple:
        with x: will call x.__enter__()
        """

        pass

    def __exit__(self, exc_type, exc_value, traceback):
        """
        The __exit__ method is used to do something special when leaving a "with" block.

        Exemple:
        with x: will call x.__exit__(exc_type, exc_value, traceback) when reaching the end.
        """

    """
		----- The following methods are reserved for classes that can be compared -----

		All of these methods should return a boolean value.

		Sorry for the lack of explication but these methods are very simple to understand.
	"""

    def __eq__(self, other):
        """
        For equality check

        Exemple:
        x == y will call x.__eq__(y)
        """

        pass

    def __ne__(self, other):
        """
        For inequality check

        Exemple:
        x != y will call x.__ne__(y)
        """

        pass

    def __lt__(self, other):
        """
        For "less than" check

        Exemple:
        x < y will call x.__lt__(y)
        """

        pass

    def __le__(self, other):
        """
        For "less than or equal to" check

        Exemple:
        x <= y will call x.__le__(y)
        """

        pass

    def __gt__(self, other):
        """
        For "greater than" check

        Exemple:
        x > y will call x.__gt__(y)
        """

        pass

    def __ge__(self, other):
        """
        For "greater or equal to" check

        Exemple:
        x >= y will call x.__ge__(y)
        """

        pass

    def __bool__(self):
        """
        The __bool__ method is called to get the truth value in a boolean context.

        Exemple:
        if x: will call x.__bool__()
        """

        pass

    """ ----- This method concern classes that act like functions, that can be called ----- """

    def __call__(self):
        """
        The __call__ method is used to call an instance like a function.

        To use this method, the instance has to be already created (to be verified).

        Exemple:
        my_instance() will call my_instance.__call__()
        """

        pass

    """ 
		----- The following methods are reserved for classes that can be serialized, also known as pickling -----
		To learn what pickling is, check out : https://diveintopython3.net/serializing.html

		You will need the "pickle" python module in order to be able to serialize data.

		I don't know much about seriazilation, so the help given on the docstring isn't very detailled
		or helpful.

	"""

    def __copy__(self):
        """
        The __copy__ method is called to create a copy of an instance of your class.
        This returns another instance newly created.

        Exemple:
        y = copy.copy(x) will call x.__copy__()
        """

        copy = ClassName()

        # Copying all of the attributes

        return copy

    def __deepcopy__(self):
        """
        The __deppcopy__ method is called to create a deepcopy of an instance of your class.
        This returns another instance newly created.

        To figure out the difference between a copy and a deepcopy, check out :
        https://www.geeksforgeeks.org/copy-python-deep-copy-shallow-copy/#:~:text=A%20shallow%20copy%20constructs%20a,objects%20found%20in%20the%20original.

        Exemple:
        y = copy.deepcopy(x) will call x.__deepcopy__()
        """

        deepcopy = ClassName()

        # Copying all of the attributes

        return deepcopy

    def __getstate__(self):
        """
        The __getstate__ method is called to get an object's state before pickling.

        Exemple:
        pickle.dump(x, file) will call x.__getstate__() if x isn't already pickeld
        """

        pass

    def __reduce__(self):
        """
        The __reduce__ method is called to serialize an object.

        Exemple:
        pickle.dump(x, file) will call x.__reduce__()
        """

        pass

    def __reduce_ex__(self, protocol_version):
        """
        The __reduce_ex__ method is called to serialize an object (new pickling protocol).

        Exemple:
        pickle.dump(x, file, protocol_version) will call x.__reduce_ex__(protocol_version)
        """

        pass

    def __getnewargs__(self):
        """
        The __getnewargs__ method is used to control over how an object is created during unpickling.

        Exemple:
        x = pickle.load(file) will call x.__getnewargs__()
        """

        pass

    def __setstate__(self):
        """
        The __setstate__ method is used to restore an object's state after pickling.

        Exemple:
        x = pickle.load(file) will call x.__setstate__()
        """

        pass

    """ ----- The following methods are quite unusual. Use them if you know what youâ€™re
		doing and you want to gain almost complete control over your classe. ----- """

    def __new__(self):
        """
        The __new__ method is a custom class constructor. It is different than the __init__ method tho.
         __new__ handles object creation and __init__ handles object initialization.

        For more detailled informations, check out:
        https://spyhce.com/blog/understanding-new-and-init#:~:text=Understanding%20the%20difference%20between%20__,they%20work%2C%20when%20defined%20differently.
        """

        pass

    def __del__(self):
        """
        The __del__ method is a class destructor. It is called when deleting an instance of the class.

        Exemple:
        del x will call x.__del__()
        """

        pass

    def __hash__(self):
        """
        The __hash__ value is used to create a custom hash value.
        Hash values are just integers that are used to compare dictionary keys during a dictionary lookup quickly.
        If this method is not defined, the object will inherit the __hash__ method of its parent class.

        For more info, ckeck out : https://www.programiz.com/python-programming/methods/built-in/hash

        Exemple:
        hash(x) will call x.__hash__()
        """

        hash_value = None

        # defining what the hash value is

        return hash_value  # should be an integer

    def __instancecheck__(self, instance):
        """
        The __instancecheck__ method is used to control whether an object is an instance of your class.
        This method is defined by default, but if you wanna change it go ahead.

        Exemple:
        isinstance(x, ClassName) will call ClassName.__instancecheck__(x)
        """

        return isinstance(instance, ClassName)

    def __subclasscheck__(self, other_class):
        """
        The __subclasscheck__ method is used to control whether a class is a subclass of your class.
        This method is defined by default, but if you wanna change it go ahead.

        Exemple:
        issubclass(C, ClassName) will call ClassName.__subclasscheck__(C)
        """

        return issubclass(other_class, ClassName)

    """
		Thats it for the special methods, but you can define your own custom methods now.
		The syntaxe is :
			def method_name(self):
				# whatever you want
		and you can then call it inside other methods with "self.method_name()" without the self as argument.
		To call personnal methods outside of your class, just write "x.method_name()" assuming x is an instance of the class.

		Thats it for this template, I hope it helped you.
	"""
