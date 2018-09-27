import pytest
from mock import Mock

from src.controller.camera import Camera


@pytest.fixture
def cam_fixture():
    return Mock(spec=Camera)


def test_temp_value(cam_fixture):
    assert isinstance(Camera.get_temperature(cam_fixture)[0], str)


test_temp_value(cam_fixture)
# (1, 0.0, 15.45475770529314, -9.787817267811569)
