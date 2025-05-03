from testme import create_intermediate_images

def test_intermediate_images_creation(tmp_path):

    print("✅ Starting image comparison...")

    # Setup dummy input paths and output path
    # You'd usually prepare some small test images here
    image_1 = "1996.jpg"
    dummy_image = tmp_path / "dummy.png"
    dummy_image.write_bytes(b"FakeImageData")  # Replace with real image data in practice

    # This won't work without real image data, but shows the structure
    try:
        create_intermediate_images(str(image_1), str(dummy_image), num_intermediates=2, out_folder=str(tmp_path))
    except Exception as e:
        assert False, f"Function raised an exception: {e}"
    print("✅ Done image comparison...")

