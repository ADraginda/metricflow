import copy
import re

import pytest
from metricflow.model.objects.metric import Metric, MetricInputMeasure, MetricType, MetricTypeParams
from metricflow.model.objects.user_configured_model import UserConfiguredModel
from metricflow.model.model_validator import ModelValidator
from metricflow.model.validations.validator_helpers import ModelValidationException
from metricflow.object_utils import flatten_nested_sequence
from metricflow.test.test_utils import find_data_source_with


def test_metric_missing_measure(simple_model__pre_transforms: UserConfiguredModel) -> None:
    """Tests the basic MetricMeasuresRule, which asserts all measure inputs to a metric exist in the model"""
    model = copy.deepcopy(simple_model__pre_transforms)
    metric_name = "invalid_measure_metric_do_not_add_to_model"
    measure_name = "this_measure_cannot_exist_or_else_it_breaks_tests"

    with pytest.raises(
        ModelValidationException,
        match=f"Measure {measure_name} referenced in metric {metric_name} is not defined in the model!",
    ):
        model.metrics.append(
            Metric(
                name=metric_name,
                description="Metric with invalid measure",
                type=MetricType.EXPR,
                type_params=MetricTypeParams(measures=[MetricInputMeasure(name=measure_name)]),
            )
        )

        ModelValidator().checked_validations(model=model)


def test_measures_only_exist_in_one_data_source(simple_model__pre_transforms: UserConfiguredModel) -> None:  # noqa: D
    model = copy.deepcopy(simple_model__pre_transforms)

    build = ModelValidator().validate_model(model)
    duplicate_measure_message = "Found measure with name .* in multiple data sources with names"
    found_issue = False

    if build.issues is not None:
        for issue in build.issues.all_issues:
            if re.search(duplicate_measure_message, issue.message):
                found_issue = True

    assert found_issue is False

    # add measure present in one data source to another
    first_data_source, _ = find_data_source_with(
        model, lambda data_source: data_source.measures is not None and len(data_source.measures) > 0
    )

    second_data_source, _ = find_data_source_with(
        model, lambda data_source: data_source.measures is not None and data_source.name != first_data_source.name
    )

    measure = first_data_source.measures[0]
    second_data_source.measures = list(flatten_nested_sequence([second_data_source.measures, [measure]]))

    build = ModelValidator().validate_model(model)

    if build.issues is not None:
        for issue in build.issues.all_issues:
            if re.search(duplicate_measure_message, issue.message):
                found_issue = True

    assert found_issue is True


def test_measure_alias_is_set_when_required(simple_model__pre_transforms: UserConfiguredModel) -> None:
    """Tests to ensure that an appropriate error appears when a required alias is missing"""
    model = copy.deepcopy(simple_model__pre_transforms)
    measure_name = find_data_source_with(model, lambda data_source: len(data_source.measures) > 0)[0].measures[0].name
    model.metrics.append(
        Metric(
            name="metric1",
            type=MetricType.EXPR,
            type_params=MetricTypeParams(
                measures=[
                    MetricInputMeasure(name=measure_name),
                    MetricInputMeasure(name=measure_name, constraint="is_instant"),
                ]
            ),
        )
    )

    build = ModelValidator().validate_model(model)

    assert len(build.issues.errors) == 1
    expected_error_substring = f"depends on multiple different constrained versions of measure {measure_name}"
    actual_error = build.issues.errors[0].as_readable_str()
    assert (
        actual_error.find(expected_error_substring) != -1
    ), f"Expected error {expected_error_substring} not found in error string! Instead got {actual_error}"


def test_invalid_measure_alias_name(simple_model__pre_transforms: UserConfiguredModel) -> None:
    """Tests measures with aliases that don't pass the unique and valid name rule"""
    model = copy.deepcopy(simple_model__pre_transforms)
    measure_name = find_data_source_with(model, lambda data_source: len(data_source.measures) > 0)[0].measures[0].name
    invalid_alias = "_can't_do_this_"
    model.metrics.append(
        Metric(
            name="metric1",
            type=MetricType.EXPR,
            type_params=MetricTypeParams(
                measures=[MetricInputMeasure(name=measure_name, constraint="is_instant", alias=invalid_alias)]
            ),
        )
    )

    build = ModelValidator().validate_model(model)

    assert len(build.issues.errors) == 1
    expected_error_substring = f"Invalid name `{invalid_alias}` - names should only consist of"
    actual_error = build.issues.errors[0].as_readable_str()
    assert (
        actual_error.find(expected_error_substring) != -1
    ), f"Expected error {expected_error_substring} not found in error string! Instead got {actual_error}"


def test_measure_alias_measure_name_conflict(simple_model__pre_transforms: UserConfiguredModel) -> None:
    """Tests measures with aliases that already exist as measure names"""
    model = copy.deepcopy(simple_model__pre_transforms)
    measures = find_data_source_with(model, lambda data_source: len(data_source.measures) > 1)[0].measures
    measure_name = measures[0].name
    invalid_alias = measures[1].name
    model.metrics.append(
        Metric(
            name="metric1",
            type=MetricType.EXPR,
            type_params=MetricTypeParams(
                measures=[MetricInputMeasure(name=measure_name, constraint="is_instant", alias=invalid_alias)]
            ),
        )
    )

    build = ModelValidator().validate_model(model)

    assert len(build.issues.errors) == 1
    expected_error_substring = (
        f"Alias `{invalid_alias}` for measure `{measure_name}` conflicts with measure names "
        f"defined elsewhere in the model!"
    )
    actual_error = build.issues.errors[0].as_readable_str()
    assert (
        actual_error.find(expected_error_substring) != -1
    ), f"Expected error {expected_error_substring} not found in error string! Instead got {actual_error}"


def test_reused_measure_alias(simple_model__pre_transforms: UserConfiguredModel) -> None:
    """Tests measures with aliases that have been used as measure aliases elsewhere in the model"""
    model = copy.deepcopy(simple_model__pre_transforms)
    measures = find_data_source_with(model, lambda data_source: len(data_source.measures) > 1)[0].measures
    first_measure_name = measures[0].name
    second_measure_name = measures[1].name
    invalid_alias = "duplicate_alias"
    model.metrics.append(
        Metric(
            name="metric1",
            type=MetricType.EXPR,
            type_params=MetricTypeParams(
                measures=[MetricInputMeasure(name=first_measure_name, constraint="is_instant", alias=invalid_alias)]
            ),
        ),
    )
    model.metrics.append(
        Metric(
            name="metric2",
            type=MetricType.EXPR,
            type_params=MetricTypeParams(
                measures=[MetricInputMeasure(name=second_measure_name, constraint="is_instant", alias=invalid_alias)]
            ),
        ),
    )

    build = ModelValidator().validate_model(model)

    assert len(build.issues.errors) == 1
    expected_error_substring = (
        f"Measure alias {invalid_alias} conflicts with a measure alias used elsewhere in the model!"
    )
    actual_error = build.issues.errors[0].as_readable_str()
    assert (
        actual_error.find(expected_error_substring) != -1
    ), f"Expected error {expected_error_substring} not found in error string! Instead got {actual_error}"


def test_reused_measure_alias_within_metric(simple_model__pre_transforms: UserConfiguredModel) -> None:
    """Tests measures with aliases that have been used as measure aliases in the same metric spec

    This covers a boundary case in the logic where alias checking must always include aliases from the current
    metric under consideration, instead of simply checking against the previous seen values
    """
    model = copy.deepcopy(simple_model__pre_transforms)
    measures = find_data_source_with(model, lambda data_source: len(data_source.measures) > 1)[0].measures
    first_measure_name = measures[0].name
    second_measure_name = measures[1].name
    invalid_alias = "duplicate_alias"
    model.metrics.append(
        Metric(
            name="metric1",
            type=MetricType.EXPR,
            type_params=MetricTypeParams(
                measures=[
                    MetricInputMeasure(name=first_measure_name, constraint="is_instant", alias=invalid_alias),
                    MetricInputMeasure(name=second_measure_name, constraint="is_instant", alias=invalid_alias),
                ]
            ),
        ),
    )

    build = ModelValidator().validate_model(model)

    assert len(build.issues.errors) == 1
    expected_error_substring = (
        f"Measure alias {invalid_alias} conflicts with a measure alias used elsewhere in the model!"
    )
    actual_error = build.issues.errors[0].as_readable_str()
    assert (
        actual_error.find(expected_error_substring) != -1
    ), f"Expected error {expected_error_substring} not found in error string! Instead got {actual_error}"
