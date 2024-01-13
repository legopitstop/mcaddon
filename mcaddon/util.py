from typing import Self
import json
import re

from .constant import Category

__all__ = ['Identifier', 'Saveable', 'Molang', 'MenuCategory']

# Should use datapackutils.Identifier
class Identifier:
    DEFAULT_NAMESPACE = 'minecraft'
    SEPERATOR = ':'
    def __init__(self, namespace:str, path:str=None):
        if path is None:
            id = Identifier.parse(namespace)
            self.namespace = id.namespace
            self.path = id.path
        else:
            self.namespace = namespace
            self.path = path

    def __repr__(self) -> str:
        return repr(str(self))

    def __str__(self) -> str:
        return self.namespace if self.path is None else self.namespace+str(self.SEPERATOR)+self.path

    def __eq__(self, other) -> bool:
        other = Identifier(other)
        return self.namespace == other.namespace and self.path == other.path

    def __add__(self, other) -> str:
        if isinstance(other, Identifier):
            return str(self) + str(other)
        return str(self) + other

    def __inter__(self):
        for x in self.split():
            yield x

    def __hash__(self):
        return hash((self.namespace, self.path))

    @property
    def __dict__(self) -> dict:
        data = {
            'namespace': self.namespace,
            'path': self.path
        }
        return data

    @property
    def namespace(self) -> str:
        return getattr(self, '_namespace', self.DEFAULT_NAMESPACE)
    
    @namespace.setter
    def namespace(self, value:str|None):
        if value is None or value=='': setattr(self, '_namespace', self.DEFAULT_NAMESPACE)
        elif isinstance(value, Identifier):
            self.namespace = value.namespace
        elif self.is_namespace_valid(value): 
            setattr(self, '_namespace', str(value).strip())
        else:
            raise ValueError(value)

    @property
    def path(self) -> str|None:
        return getattr(self, '_path', 'air')
    
    @path.setter
    def path(self, value:str):
        if value is None or value =='': setattr(self, '_path', None)
        elif isinstance(value, Identifier):
            self.path = value.path
        elif self.is_path_valid(str(value)):
            setattr(self, '_path', str(value).strip())
        else:
            raise ValueError(value)
    
    def is_path_valid(self, path:str=None) -> bool:
        """
        Validates the path

        :param path: The path to validate, defaults to self.path
        :type path: str, optional
        :return: Whether or not it's valid
        :rtype: bool
        """
        v = self.path if path is None else path
        res = re.match(r'^[a-z-0-9/_]+$', v)
        return res is not None
    
    def is_namespace_valid(self, namespace:str=None) -> bool:
        """
        Validates the namespace

        :param namespace: The namespace to validate, defaults to self.namespace
        :type namespace: str, optional
        :return: Whether or not it's valid
        :rtype: bool
        """
        v = self.namespace if namespace is None else namespace
        res = re.match(r'^[a-z0-9/_]+$', v)
        return res is not None

    @classmethod
    def parse(cls, value:str) -> Self:
        """
        Parse this value as an identifier

        :param value: The value to parse
        :type value: str
        :rtype: Identifier
        """
        self = cls.__new__(cls)
        if isinstance(value, Identifier):
            return value.copy()
        
        if str(value).count(self.SEPERATOR) == 0:
            self.path = value
        else:
            x = str(value).split(self.SEPERATOR)
            self.namespace = x[0]
            self.path = x[1]
        return self
    
    def copy(self) -> Self:
        """
        Returns a copy of this identifier

        :rtype: Identifier
        """
        return Identifier(self.namespace, self.path)
    
    def copy_with_path(self, path:str) -> Self:
        """
        Returns a copy of this identifier with a new path

        :rtype: Identifier
        """
        id = self.copy()
        id.path = path
        return id
    
    def copy_with_namespace(self, namespace:str) -> Self:
        """
        Returns a copy of this identifier with a new namespace

        :rtype: Identifier
        """
        id = self.copy()
        id.namespace = namespace
        return id

    def split(self) -> tuple:
        """
        Returns (namespace, path)
        """
        return (self.namespace, self.path)

    def replace(self, old, new, count=-1) -> Self:
        self.path.replace(old, new, count)
        return self

class Saveable:
    @classmethod
    def from_dict(cls, data:dict):
        """
        Load object from DICT

        :param data: DICT data to load from
        :type data: dict
        """
        raise NotImplementedError()

    def json(self, **kw) -> str:
        """
        Convert object to a string in JSON format

        :return: Stringified JSON
        :rtype: str
        """
        return json.dumps(self.__dict__, **kw)
    
    def save(self, fp:str, indent:int=2, **kw) -> Self:
        """
        Save file as JSON

        :param fp: File path to save as
        :type fp: str
        :param indent: indent level, defaults to 2
        :type indent: int, optional
        """
        with open(fp, 'w') as f:
            f.write(self.json(indent=indent, **kw))
        return self

# TEMP: Should use molang package
class Molang:
    def __init__(self, string:str=''):
        self.string = string

    def __str__(self) -> str:
        return self.string
    
    @property
    def string(self) -> str:
        return getattr(self, '_string')
    
    @string.setter
    def string(self, value:str):
        setattr(self, '_string', str(value))

    @classmethod
    def parse(cls, s:str) -> Self:
        self = cls.__new__(cls)
        self.string = s
        return self

    def append(self, s:str) -> Self:
        self.string += str(s)
        return self
    
    def prepend(self, s:str) -> Self:
        self.string = str(s)+self.string
        return self

    def paren(self, lang) -> Self:
        self.append(f"({lang.string})")
        return self

    # LOGICAL OPERATORS

    def _ops(self, char, a, b) -> Self:
        self.append(f'{a} {char} {b}')
        return self
    
    def and_(self, a, b) -> Self:
        self._ops('&&', a, b)
        return self
    
    def or_(self, a, b) -> Self:
        self._ops('||', a, b)
        return self
    
    def lt(self, a, b) -> Self:
        self._ops('<', a, b)
        return self
    
    def gt(self, a, b) -> Self:
        self._ops('>', a, b)
        return self
    
    def lteq(self, a, b) -> Self:
        self._ops('<=', a, b)
        return self
    
    def gteq(self, a, b) -> Self:
        self._ops('>=', a, b)
        return self
    
    def not_(self, a, b) -> Self:
        self._ops('!=', a, b)
        return self

    # MATH OPERATORS

    def add(self, a, b) -> Self:
        return self._ops('+', a, b)
    
    def sub(self, a, b) -> Self:
        return self._ops('-', a, b)
    
    def mul(self, a, b) -> Self:
        return self._ops('*', a, b)
    
    def div(self, a, b) -> Self:
        return self._ops('/', a, b)

    # MATH

    def _math(self, function_name:str, *args) -> Self:
        """
        Various math functions

        :param function_name: The name of the function
        :type function_name: str
        """
        if args:
            self.string += f'math.{function_name}({", ".join(args)})'
        else:
            self.string += f'math.{function_name}'
        return self
    
    def abs(self, value) -> Self:
        """
        Absolute value of value
        """
        return self._math('abs', value)
    
    def acos(self, value) -> Self:
        """
        arccos of value
        """
        return self._math('acos', value)
    
    def asin(self, value) -> Self:
        """
        arcsin of value
        """
        return self._math('asin', value)
    
    def atan(self, value) -> Self:
        """
        arctan of value
        """
        return self._math('atan', value)
    
    def atan2(self, y,x) -> Self:
        """
        arctan of y/x. NOTE: the order of arguments!
        """
        return self._math('atan2', y,x)
    
    def cell(self, value) -> Self:
        """
        Round value up to nearest integral number
        """
        return self._math('cell', value)
    
    def clamp(self, value, min, max) -> Self:
        """
        Clamp value to between min and max inclusive
        """
        return self._math('clamp', value, min, max)
    
    def cos(self, value) -> Self:
        """
        Cosine (in degrees) of value
        """
        return self._math('cos', value)
    
    def die_roll(self, num, low, high) -> Self:
        """
        returns the sum of 'num' random numbers, each with a value from low to high`. Note: the generated random numbers are not integers like normal dice. For that, use `math.die_roll_integer`.
        """
        return self._math('die_roll', num, low, high)
    
    def die_roll_integer(self, num, low, high) -> Self:
        """
        returns the sum of 'num' random integer numbers, each with a value from low to high`. Note: the generated random numbers are integers like normal dice.
        """
        return self._math('die_roll_integer', num, low, high)
    
    def exp(self, value) -> Self:
        """
        Calculates e to the value'th power
        """
        return self._math('exp', value)
    
    def floor(self, value) -> Self:
        """
        Round value down to nearest integral number
        """
        return self._math('floor', value)
    
    def hermite_blend(self, value) -> Self:
        """
        Useful for simple smooth curve interpolation using one of the Hermite Basis functions: `3t^2 - 2t^3`. Note that while any valid float is a valid input, this function works best in the range [0,1].
        """
        return self._math('hermite_blend', value)
    
    def lerp(self, start, zero_to_one) -> Self:
        """
        Lerp from start to end via 0_to_1
        """
        return self._math('lerp', start, zero_to_one)
    
    def lerprotate(self, start, end, zero_to_one) -> Self:
        """
        Lerp the shortest direction around a circle from start degrees to end degrees via 0_to_1
        """
        return self._math('lerprotate', start, end, zero_to_one)
    
    def ln(self, value) -> Self:
        """
        Natural logarithm of value
        """
        return self._math('ln', value)
    
    def max(self, a, b) -> Self:
        """
        Return highest value of A or B
        """
        return self._math('max', a, b)
    
    def min(self, a, b) -> Self:
        """
        Return lowest value of A or B
        """
        return self._math('min', a, b)
    
    def min_angle(self, value) -> Self:
        """
        Minimize angle magnitude (in degrees) into the range [-180, 180)
        """
        return self._math('min_angle', value)
    
    def mod(self, value, denominator) -> Self:
        """
        Return the remainder of value / denominator
        """
        return self._math('mod', value, denominator)
    
    def pi(self) -> Self:
        """
        Returns the float representation of the constant pi.
        """
        return self._math('pi')
    
    def pow(self, base, exponent) -> Self:
        """
        Elevates `base` to the `exponent`'th power
        """
        return self._math('pow', base, exponent)
    
    def random(self, low, high) -> Self:
        """
        Random value between low and high inclusive
        """
        return self._math('random', low, high)
    
    def random_integer(self, low, high) -> Self:
        """
        Random integer value between low and high inclusive
        """
        return self._math('random_integer', low, high)
    
    def round(self, value) -> Self:
        """
        Round value to nearest integral number
        """
        return self._math('round', value)
    
    def sin(self, value) -> Self:
        """
        Sine (in degrees) of value
        """
        return self._math('sin', value)
    
    def sqrt(self, value) -> Self:
        """
        Square root of value
        """
        return self._math('sqrt', value)
    
    def trunc(self, value) -> Self:
        """
        Round value towards zero
        """
        return self._math('trunc', value)

    # QUERY

    def query(self, function_name:str, *args) -> Self:
        """
        Access to an entity's properties

        :param function_name: The name of the function
        :type function_name: str
        """
        if args:
            self.string += f'q.{function_name}({", ".join(args)})'
        else:
            self.string += f'q.{function_name}'
        return self
    
    def block_state(self, state:str) -> Self:
        return self.query('block_state', state)
    
    def has_block_state(self, state:str) -> Self:
        return self.query('has_block_state', state)
    
    # MISC

    def geometry(self, texture_name:str) -> Self:
        """
        A reference to a geometry named in the entity definition

        :param texture_name: The name of the geometry
        :type texture_name: str
        """
        self.string += f'geometry.{texture_name}'
        return self
    
    def material(self, texture_name:str) -> Self:
        """
        A reference to a material named in the entity definition

        :param texture_name: The name of the material
        :type texture_name: str
        """
        self.string += f'material.{texture_name}'
        return self
    
    def texture(self, texture_name:str) -> Self:
        """
        A reference to a texture named in the entity definition

        :param texture_name: The name of the texture
        :type texture_name: str
        """
        self.string += f'texture.{texture_name}'
        return self
    
    def variable(self, variable_name:str) -> Self:
        """
        Read/write storage on an actor

        :param variable_name: The name of the variable
        :type variable_name: str
        """
        self.string += f'v.{variable_name}'
        return self
    
    def temp(self, variable_name:str) -> Self:
        """
        Read/write temporary storage

        :param variable_name: The name of the variable
        :type variable_name: str
        """
        self.string += f't.{variable_name}'
        return self
    
    def context(self, variable_name:str) -> Self:
        """
        Read-only storage provided by the game in certain scenarios

        :param variable_name: The name of the variable
        :type variable_name: str
        """
        self.string += f'c.{variable_name}'
        return self
    
class MenuCategory:
    def __init__(self, category:Category, group:str, is_hidden_in_commands:bool=False):
        self.category = category
        self.group = group
        self.is_hidden_in_commands = is_hidden_in_commands

    @property
    def __dict__(self) -> dict:
        data = {
            'category': self.category._value_,
            'group': self.group
        }
        if self.is_hidden_in_commands:
            data['is_hidden_in_commands'] = self.is_hidden_in_commands
        return data
    
    @property
    def category(self) -> Category:
        return getattr(self, '_category')
    
    @category.setter
    def category(self, value:Category):
        if not isinstance(value, Category): raise TypeError(f"Expected Category but got '{value.__class__.__name__}' instead") 
        setattr(self, '_category', value)

    @property
    def group(self) -> str:
        return getattr(self, '_group')
    
    @group.setter
    def group(self, value:str):
        setattr(self, '_group', str(value))

    @property
    def is_hidden_in_commands(self) -> bool:
        return getattr(self, '_is_hidden_in_commands')
    
    @is_hidden_in_commands.setter
    def is_hidden_in_commands(self, value:bool):
        if not isinstance(value, bool): raise TypeError(f"Expected bool but got '{value.__class__.__name__}' instead")
        setattr(self, '_is_hidden_in_commands', value)

    @classmethod
    def from_dict(cls, data:dict) -> Self:
        self = cls.__new__(cls)
        if 'category' in data: self.category = data.pop('category')
        if 'group' in data: self.group = data.pop('group')
        if 'is_hidden_in_commands' in data: self.is_hidden_in_commands = data.pop('is_hidden_in_commands')
        return self
