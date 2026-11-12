import random
import sys

_types: list = ["_integers", "_characters", "_symbols"]
_integers: list = [0, 1, 2, 3, 4, 5, 7, 8, 9]
_characters: list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
_symbols: list = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']
_bit_range: int = 0
_default_bits: int = 800
_key = "ws:"


def type():
  global _types
  return random.choices(_types)


def key_size_in_bits(key: str):
  """
  Validate the key size in processing mode. Using encode method to read string
  and multiply it with * 8. Because a single character = 1 byte.
  1 byte = 8 bits.
  Multiply 1 btye into 8 making 8 bits.
  For example:
    A key is 13 characters long e.g. "this_is_the_key", it's 13 bytes longer multiplying
    it into 8 giving the actual size of string in bits.

  Because encoding method could prefer the actual characters sizes, not everytime a single character could be = 1 byte,
  they could be 2 characters = 1 byte.
  """
  return len(key.encode('utf-8')) * 8


def random_letter(include_symbols: bool = True, include_integers: bool = True, include_characters: bool = True):
  global _integers, _characters, _symbols
  """
  Getting random letter to help in loop for making a long string of key.
  """
  _type = str(type())
  if "characters" in _type.lower() and include_characters:
    _selected = random.choices(_characters)
    return _selected[0]
  elif "symbols" in _type.lower() and include_symbols:
    _selected = random.choices(_symbols)
    return _selected[0]
  elif "integers" in _type.lower() and include_integers:
    _selected = random.choices(_integers)
    return _selected[0]

  else:
    return None
    

def generate_key(
include_symbols: bool = False, 
include_integers: bool = True, 
include_characters: bool = True,
bits: int = _default_bits
):
  """
  Generating a key using while loop with special parameter features.
  include_symbols=True, means to include symbols in key;
  include_integers=True, means to include integers in key;
  include_characters=True, means to include characters in key;

  Making false them all, will not generate a key.
  """
  if not include_symbols and not include_integers and not include_characters:
    return f"Make True/Available at least one of them!"
  
  global _key, _bit_range
  _bit_range = bits / 8
  print(int(_bit_range))

  while True:
    r_letter = random_letter(
            include_symbols=include_symbols, 
            include_integers=include_integers,
            include_characters=include_characters
            )
    if r_letter is not None:
        _key = _key + str(r_letter)
        _key_size = key_size_in_bits(_key)
        if _key_size >= bits:
          break
  return _key


# Testing Version
import time

start_time = time.perf_counter()
bits = generate_key(include_symbols=False, include_integers=True, include_characters=True, bits=240)
print(bits, sys.getsizeof(bits))
end_time = time.perf_counter() - start_time
print(round(end_time, 3), "seconds taken!")


print(len(bits.encode('utf-8')) * 8)
