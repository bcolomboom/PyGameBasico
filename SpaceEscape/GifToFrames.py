from PIL import Image


def extract_frames_gif(input_path, output_prefix="frame"):
    # Open the GIF file
    img = Image.open("spacegif.gif")

    # Check if it's actually animated
    if not getattr(img, "is_animated", False):
        print("This GIF is not animated.")
        return

    frame_count = 0
    try:
        while True:
            # Save current frame
            frame_filename = f"{output_prefix}_{frame_count:04d}.png"
            img.save(frame_filename, "PNG")
            print(f"Saved {frame_filename}")

            frame_count += 1
            # Go to next frame
            img.seek(img.tell() + 1)

    except EOFError:
        # No more frames
        pass

    print(f"Extracted {frame_count} frames.")


# Usage
extract_frames_gif("your_animated.gif", "spaceGifFrame")