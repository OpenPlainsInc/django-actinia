from grass.serializers.InputParameterSerializer import InputParameterSerializer


def test_InputParameterSerializer():
    data = {
        "param": "raster",
        "value": "elevation30m@PERMANENT",
        "import_descr": {"import_type": "raster", "import_path": "/path/to/raster.tif"},
    }
    serializer = InputParameterSerializer(data=data)
    if serializer.is_valid():
        assert serializer.validated_data["param"] == "raster"
        assert serializer.validated_data["value"] == "elevation30m@PERMANENT"
        assert serializer.validated_data["import_descr"]["import_type"] == "raster"
        assert (
            serializer.validated_data["import_descr"]["import_path"]
            == "/path/to/raster.tif"
        )
    else:
        print("Serializer is not valid.")
