from sympy import sieve, nextprime # type: ignore
from random import choice

# Define Variables

separation: int = 3

# Define Character Code

codeToChar: dict = {
    10: ' ', 11: '!', 12: '"', 13: '#', 14: '$', 15: '%', 16: '&', 17: "'", 18: '(', 19: ')',
    20: '*', 21: '+', 22: ',', 23: '-', 24: '.', 25: '/', 26: '0', 27: '1', 28: '2', 29: '3',
    30: '4', 31: '5', 32: '6', 33: '7', 34: '8', 35: '9', 36: ':', 37: ';', 38: '<', 39: '=',
    40: '>', 41: '?', 42: '@', 43: 'A', 44: 'B', 45: 'C', 46: 'D', 47: 'E', 48: 'F', 49: 'G',
    50: 'H', 51: 'I', 52: 'J', 53: 'K', 54: 'L', 55: 'M', 56: 'N', 57: 'O', 58: 'P', 59: 'Q',
    60: 'R', 61: 'S', 62: 'T', 63: 'U', 64: 'V', 65: 'W', 66: 'X', 67: 'Y', 68: 'Z', 69: '[',
    70: '\\', 71: ']', 72: 'z', 73: '-', 74: 'a', 75: 'b', 76: 'c', 77: 'd', 78: 'e', 79: 'f',
    80: 'f', 81: 'g', 82: 'h', 83: 'i', 84: 'j', 85: 'k', 86: 'l', 87: 'm', 88: 'n', 89: 'o',
    90: 'p', 91: 'q', 92: 'r', 93: 's', 94: 't', 95: 'u', 96: 'v', 97: 'w', 98: 'x', 99: 'y',
}

charToCode: dict = {
    ' ': 10, '!': 11, '"': 12, '#': 13, '$': 14, '%': 15, '&': 16, "'": 17,
    '(': 18, ')': 19, '*': 20, '+': 21, ',': 22, '-': 73, '.': 24, '/': 25,
    '0': 26, '1': 27, '2': 28, '3': 29, '4': 30, '5': 31, '6': 32, '7': 33,
    '8': 34, '9': 35, ':': 36, ';': 37, '<': 38, '=': 39, '>': 40, '?': 41,
    '@': 42, 'A': 43, 'B': 44, 'C': 45, 'D': 46, 'E': 47, 'F': 48, 'G': 49,
    'H': 50, 'I': 51, 'J': 52, 'K': 53, 'L': 54, 'M': 55, 'N': 56, 'O': 57,
    'P': 58, 'Q': 59, 'R': 60, 'S': 61, 'T': 62, 'U': 63, 'V': 64, 'W': 65,
    'X': 66, 'Y': 67, 'Z': 68, '[': 69, '\\': 70, ']': 71, 'z': 72, 'a': 74,
    'b': 75, 'c': 76, 'd': 77, 'e': 78, 'f': 80, 'g': 81, 'h': 82, 'i': 83,
    'j': 84, 'k': 85, 'l': 86, 'm': 87, 'n': 88, 'o': 89, 'p': 90, 'q': 91,
    'r': 92, 's': 93, 't': 94, 'u': 95, 'v': 96, 'w': 97, 'x': 98, 'y': 99
}

# Number to Text and Text to Number

def _decode(text: str) -> str:
  res = [str(charToCode[i]) for i in text]
  return ''.join(res)

def decode(text: str, separation: int) -> list:
  raw = _decode(text)
  sep = [int(raw[x:x+2*separation]) for x in range(0, len(raw), 2*separation)]
  return sep

def encode(text: str) -> str:
  sep = [text[x:x+2] for x in range(0, len(text), 2)]
  res = [codeToChar[int(i)] for i in sep]
  return ''.join(res)

# Encryption and Decryption

def encrypt(plain: int, n: int, e: int) -> int:
  encrypted: int = pow(plain, e, n)
  return encrypted

def decrypt(encrypted: int, n: int, d: int) -> int:
  decrypted: int = pow(encrypted, d, n)
  return decrypted

# Get `p`, `q`, and `e`

def extended_gcd(a, b):
  """
  拡張ユークリッドの互除法

  Args:
    a: 整数
    b: 整数

  Returns:
    d: aとbの最大公約数
    x: ax + by = d を満たすx
    y: ax + by = d を満たすy
  """
  if b == 0:
    return (a, 1, 0)
  else:
    (d, p, q) = extended_gcd(b, a % b)
    x = q
    y = p - q * (a // b)
    return (d, x, y)

def calculate_d(e, phi):
  """秘密鍵dを計算する

  Args:
    e: 公開鍵e
    phi: オイラーのトーシェント関数

  Returns:
    d: 秘密鍵d
  """
  (d, x, y) = extended_gcd(e, phi)
  if x < 0:
      x += phi
  return x

def calc_pqe(plain: int) -> tuple:
  p: int = 0
  q: int = 0
  e: int = 0
  primelist = [i for i in sieve.primerange(2, 10 ** (2*separation) * 5)]
  while True:
    p = choice(primelist)
    q = choice(primelist)
    e = choice(primelist)
    if p * q > plain and (p - 1) * (q - 1) % e != 0:
      break
  return p, q, e

if __name__ == '__main__':
  plain_text = input("平文: ")
  plain = decode(plain_text, 2*separation)
  print(f"平文 (decoded): {plain}")

  p, q, e = calc_pqe(plain[0])
  print(f"p: {p}, q: {q}, e: {e}")
  n = p * q
  phi = (p - 1) * (q - 1)
  print(f"n: {n}, phi: {phi}")
  d = calculate_d(e, phi)
  print(f"d: {d}")

  encrypted: list = []
  for pl in plain:
    _encrypted = encrypt(pl, n, e)
    encrypted.append(str(_encrypted))
  print(f"暗号文 (decimal | partial): {encrypted}")

  decrypted: str = ""
  for en in encrypted:
    _decrypted: str = str(decrypt(int(en), n, d))
    decrypted += _decrypted

  result = encode(decrypted)
  print(f"復元文 (encoded): {result}")
