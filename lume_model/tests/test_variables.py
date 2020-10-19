import pytest
import numpy as np
from pydantic import ValidationError
from lume_model.variables import (
    ScalarInputVariable,
    ScalarOutputVariable,
    ImageInputVariable,
    ImageOutputVariable,
)


@pytest.mark.parametrize(
    "variable_name,default,value_range",
    [
        ("test", 0.1, [0.1, 2]),
        pytest.param("test", np.array([1, 2, 3, 4]), [0, 1], marks=pytest.mark.xfail),
    ],
)
def test_input_scalar_variable(variable_name, default, value_range):
    # test correctly typed
    ScalarInputVariable(name=variable_name, default=default, value_range=value_range)

    # test missing name
    with pytest.raises(ValidationError):
        ScalarInputVariable(default=default, value_range=value_range)

    # test missing default
    with pytest.raises(ValidationError):
        ScalarInputVariable(name=variable_name, value_range=value_range)

    # test missing range
    with pytest.raises(ValidationError):
        ScalarInputVariable(
            name=variable_name, default=default,
        )


@pytest.mark.parametrize(
    "variable_name,default,value_range,is_constant,assign,assignment",
    [
        ("test", 0.1, [1, 2], False, True, 2.0),
        pytest.param("test", 0.1, [1, 2], True, True, 2.0, marks=pytest.mark.xfail),
    ],
)
def test_constant_input_scalar_variable(
    variable_name, default, value_range, is_constant, assign, assignment
):

    variable = ScalarInputVariable(
        name=variable_name,
        default=default,
        value_range=value_range,
        is_constant=is_constant,
    )

    # test assignment
    if assign:
        variable.default = assignment


@pytest.mark.parametrize(
    "variable_name,default,value_range",
    [
        ("test", 0.1, [0.1, 2]),
        pytest.param("test", np.array([1, 2, 3, 4]), [0, 1], marks=pytest.mark.xfail),
    ],
)
def test_output_scalar_variable(variable_name, default, value_range):
    # test correctly typed
    ScalarOutputVariable(name=variable_name, default=default, value_range=value_range)

    # test missing name
    with pytest.raises(ValidationError):
        ScalarOutputVariable(default=default, value_range=value_range)

    # test missing value
    ScalarOutputVariable(name=variable_name, value_range=value_range)

    # test missing range
    ScalarOutputVariable(
        name=variable_name, default=default,
    )


@pytest.mark.parametrize(
    "variable_name,default,value_range,axis_labels,x_min,y_min,x_max,y_max",
    [
        ("test", np.array([[1, 2,], [3, 4]]), [0, 1], ["x", "y"], 0, 0, 1, 1),
        pytest.param(
            "test", 1.0, [0, 1], ["x", "y"], 0, 0, 1, 1, marks=pytest.mark.xfail
        ),
    ],
)
def test_input_image_variable(
    variable_name, default, value_range, axis_labels, x_min, y_min, x_max, y_max
):
    # test correctly typed
    ImageInputVariable(
        name=variable_name,
        default=default,
        value_range=value_range,
        axis_labels=axis_labels,
        x_min=x_min,
        y_min=y_min,
        x_max=x_max,
        y_max=y_max,
    )

    # test missing name
    with pytest.raises(ValidationError):
        ImageInputVariable(
            default=default,
            value_range=value_range,
            axis_labels=axis_labels,
            x_min=x_min,
            y_min=y_min,
            x_max=x_max,
            y_max=y_max,
        )

    # test missing value
    with pytest.raises(ValidationError):
        ImageInputVariable(
            name=variable_name,
            value_range=value_range,
            axis_labels=axis_labels,
            x_min=x_min,
            y_min=y_min,
            x_max=x_max,
            y_max=y_max,
        )

    # test missing range
    with pytest.raises(ValidationError):
        ImageInputVariable(
            name=variable_name,
            default=default,
            axis_labels=axis_labels,
            x_min=x_min,
            y_min=y_min,
            x_max=x_max,
            y_max=y_max,
        )

    # test missing axis labels
    with pytest.raises(ValidationError):
        ImageInputVariable(
            name=variable_name,
            default=default,
            value_range=value_range,
            x_min=x_min,
            y_min=y_min,
            x_max=x_max,
            y_max=y_max,
        )


@pytest.mark.parametrize(
    "variable_name,default,axis_labels",
    [
        ("test", np.array([[1, 2,], [3, 4]]), ["x", "y"],),
        pytest.param("test", 1.0, ["x", "y"], marks=pytest.mark.xfail),
    ],
)
def test_output_image_variable(variable_name, default, axis_labels):
    shape = default.shape
    ImageOutputVariable(
        name=variable_name, default=default, shape=shape, axis_labels=axis_labels,
    )

    # test missing name
    with pytest.raises(ValidationError):
        ImageOutputVariable(
            default=default, shape=shape, axis_labels=axis_labels,
        )

    # test missing axis labels
    with pytest.raises(ValidationError):
        ImageOutputVariable(
            name=variable_name, default=default,
        )

    # test missing value
    ImageOutputVariable(
        name=variable_name, axis_labels=axis_labels,
    )
