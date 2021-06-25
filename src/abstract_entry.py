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

from datetime import datetime
from typing import List, Optional

from configuration import Configuration
from rp2_error import RP2TypeError


class AbstractEntry:
    def __init__(
        self,
        configuration: Configuration,
        asset: str,
    ) -> None:
        self.__configuration = Configuration.type_check("configuration", configuration)
        self.__asset: str = configuration.type_check_asset("asset", asset)

    @classmethod
    def type_check(cls, name: str, instance: "AbstractEntry") -> "AbstractEntry":
        Configuration.type_check_parameter_name(name)
        if not isinstance(instance, cls):
            raise RP2TypeError(f"Parameter '{name}' is not of type {cls.__name__}: {instance}")
        return instance

    # Parametrized and extensible method to generate string representation
    def to_string(self, indent: int = 0, repr_format: bool = True, extra_data: Optional[List[str]] = None) -> str:
        raise NotImplementedError("Abstract method")

    @property
    def configuration(self) -> Configuration:
        return self.__configuration

    @property
    def asset(self) -> str:
        return self.__asset

    @property
    def id(self) -> str:  # pylint: disable=C0103
        raise NotImplementedError("Abstract property")

    @property
    def timestamp(self) -> datetime:
        raise NotImplementedError("Abstract property")

    # How much crypto was gained / lost with this entry
    @property
    def crypto_balance_change(self) -> float:
        raise NotImplementedError("Abstract property")

    # How much usd was gained / lost with this entry
    @property
    def usd_balance_change(self) -> float:
        raise NotImplementedError("Abstract property")