from testme import create_intermediate_images, create_movie

def test_intermediate_images_creation(tmp_path):

    print("✅ Starting image comparison...")

    # Setup dummy input paths and output path
    # You'd usually prepare some small test images here
    image_1 = "start.jpg"
    image_2 = "end.jpg"

    # This won't work without real image data, but shows the structure
    try:
        create_intermediate_images(str(image_1), str(image_2), num_intermediates=10, out_folder=str(tmp_path))
        create_movie(str(tmp_path), "transition.mp4", fps=10)
    except Exception as e:
        assert False, f"Function raised an exception: {e}"
    print("✅ Done image comparison...")

