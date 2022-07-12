from __future__ import annotations

from hashlib import sha1
from typing import Any, List, Optional

from metricflow.errors.errors import ParsingException
from metricflow.model.objects.common import Metadata
from metricflow.model.objects.constraints.where import WhereClauseConstraint
from metricflow.model.objects.base import HashableBaseModel, ModelWithMetadataParsing, PydanticCustomInputParser
from metricflow.object_utils import ExtendedEnum
from metricflow.specs import MeasureReference
from metricflow.time.time_granularity import TimeGranularity
from metricflow.time.time_granularity import string_to_time_granularity


class MetricType(ExtendedEnum):
    """Currently supported metric types"""

    MEASURE_PROXY = "measure_proxy"
    RATIO = "ratio"
    EXPR = "expr"
    CUMULATIVE = "cumulative"


class CumulativeMetricWindow(PydanticCustomInputParser, HashableBaseModel):
    """Describes the window of time the metric should be accumulated over. ie '1 day', '2 weeks', etc"""

    count: int
    granularity: TimeGranularity

    def to_string(self) -> str:  # noqa: D
        return f"{self.count} {self.granularity.value}"

    @classmethod
    def _from_yaml_value(cls, input: Any) -> CumulativeMetricWindow:
        """Parses a CumulativeMetricWindow from a string input found in a user provided model specification

        The CumulativeMetricWindow is always expected to be provided as a string in user-defined YAML configs.
        It may also be a CumulativeMetricWindow in cases where we are internally constructing Metric objects.
        """
        if isinstance(input, str):
            return CumulativeMetricWindow.parse(input)
        elif isinstance(input, CumulativeMetricWindow):
            # This is internally constructed, pass it through and ignore it in error messaging
            return input
        else:
            raise ValueError(
                f"CumulativeMetricWindow inputs from model configs are expected to always be of type string, but got "
                f"type {type(input)} with value: {input}"
            )

    @staticmethod
    def parse(window: str) -> CumulativeMetricWindow:
        """Returns window values if parsing succeeds, None otherwise

        Output of the form: (<time unit count>, <time granularity>, <error message>) - error message is None if window is formatted properly
        """
        parts = window.split(" ")
        if len(parts) != 2:
            raise ParsingException(
                f"Invalid window ({window}) in cumulative metric. Should be of the form `<count> <granularity>`, ie `28 days`",
            )

        granularity = parts[1]
        # if we switched to python 3.9 this could just be `granularity = parts[0].removesuffix('s')
        if granularity.endswith("s"):
            # months -> month
            granularity = granularity[:-1]
        if granularity not in [item.value for item in TimeGranularity]:
            raise ParsingException(
                f"Invalid time granularity {granularity} in cumulative metric window string: ({window})",
            )

        count = parts[0]
        if not count.isdigit():
            raise ParsingException(f"Invalid count ({count}) in cumulative metric window string: ({window})")

        return CumulativeMetricWindow(
            count=int(count),
            granularity=string_to_time_granularity(granularity),
        )


class MetricTypeParams(HashableBaseModel):
    """Type params add additional context to certain metric types (the context depends on the metric type)"""

    measure: Optional[str]
    measures: Optional[List[str]]
    numerator: Optional[str]
    denominator: Optional[str]
    expr: Optional[str]
    window: Optional[CumulativeMetricWindow]
    grain_to_date: Optional[TimeGranularity]

    @property
    def numerator_measure_reference(self) -> Optional[MeasureReference]:  # noqa: D
        return MeasureReference(element_name=self.numerator) if self.numerator else None

    @property
    def denominator_measure_reference(self) -> Optional[MeasureReference]:  # noqa: D
        return MeasureReference(element_name=self.denominator) if self.denominator else None


class Metric(HashableBaseModel, ModelWithMetadataParsing):
    """Describes a metric"""

    name: str
    description: Optional[str]
    type: MetricType
    type_params: MetricTypeParams
    constraint: Optional[WhereClauseConstraint]
    metadata: Optional[Metadata]

    @property
    def measure_references(self) -> List[MeasureReference]:  # noqa: D
        tp = self.type_params
        res = tp.measures or []
        if tp.measure:
            res.append(tp.measure)
        if tp.numerator:
            res.append(tp.numerator)
        if tp.denominator:
            res.append(tp.denominator)

        return [MeasureReference(element_name=x) for x in res]

    @property
    def definition_hash(self) -> str:  # noqa: D
        values: List[Optional[str]] = [self.name, self.type_params.expr or ""]
        if self.constraint:
            values.append(self.constraint.where)
            if self.constraint.linkable_names:
                values.extend(self.constraint.linkable_names)
        values.extend([m.element_name for m in self.measure_references])

        hash_builder = sha1()
        for s in values:
            if s is None:
                continue
            hash_builder.update(s.encode("utf-8"))
        return hash_builder.hexdigest()
