# Copyright 2021 eprbell
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from decimal import Decimal, FloatOperation, getcontext

from rp2_error import RP2TypeError

CRYPTO_DECIMALS: int = 13
CRYPTO_DECIMAL_MASK: Decimal = Decimal("1." + "0" * int(CRYPTO_DECIMALS))

USD_DECIMALS: int = 2
USD_DECIMAL_MASK: Decimal = Decimal("1." + "0" * int(USD_DECIMALS))


class RP2Decimal(Decimal):

    # RP2Decimal initialization code. In Python there is no static constructor: the closest alternative is to add static initialization code
    # directly inside the class. Use arbitrarily high precision (sextillion + CRYPTO_DECIMALS decimal digits)
    getcontext().prec = CRYPTO_DECIMALS + 21
    getcontext().traps[FloatOperation] = True

    @classmethod
    def is_equal_within_precision(cls, n1: Decimal, n2: Decimal, precision_mask: Decimal) -> bool:
        return (n1 - n2).quantize(precision_mask) == 0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Decimal):
            raise RP2TypeError(f"Operand has non-Decimal value {repr(other)}")
        return (self - other).quantize(CRYPTO_DECIMAL_MASK).__eq__(ZERO)

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, Decimal):
            raise RP2TypeError(f"Operand has non-Decimal value {repr(other)}")
        return (self - other).quantize(CRYPTO_DECIMAL_MASK).__ge__(ZERO)

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Decimal):
            raise RP2TypeError(f"Operand has non-Decimal value {repr(other)}")
        return (self - other).quantize(CRYPTO_DECIMAL_MASK).__gt__(ZERO)

    def __le__(self, other: object) -> bool:
        return not self.__gt__(other)

    def __lt__(self, other: object) -> bool:
        return not self.__ge__(other)


ZERO: RP2Decimal = RP2Decimal("0")
