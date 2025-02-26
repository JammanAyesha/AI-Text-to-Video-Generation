import torch
from diffusers import StableDiffusionPipeline
import cv2
import os
import numpy as np
from datetime import datetime

# Function to initialize the Stable Diffusion pipeline
def initialize_pipeline():
    print("Loading Stable Diffusion model...")
    try:
        pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        pipe = pipe.to(device)
        print(f"Model loaded successfully and set to use {device.upper()}.")
    except Exception as e:
        print("Error initializing Stable Diffusion pipeline:", e)
        exit()
    return pipe

# Function to create an output directory for saving frames
def create_output_directory(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Directory '{output_dir}' created.")
    else:
        print(f"Directory '{output_dir}' already exists.")

# Function to generate a single frame
def generate_frame(pipe, prompt, output_path):
    try:
        print(f"Generating frame: {prompt}")
        image = pipe(prompt).images[0]
        image.save(output_path)
        print(f"Saved frame at {output_path}")
    except Exception as e:
        print(f"Error generating frame: {e}")

# Function to generate multiple frames
def generate_video_frames(pipe, text_description, num_frames, output_dir):
    print(f"Generating {num_frames} frames for the description: {text_description}")
    for i in range(num_frames):
        prompt = f"{text_description}, time of day: {i / num_frames * 24:.1f} hours"
        frame_path = os.path.join(output_dir, f"frame_{i:03d}.png")
        generate_frame(pipe, prompt, frame_path)

# Function to create a video from frames using OpenCV
def create_video_from_frames(output_dir, video_path, fps=30):
    print(f"Creating video from frames stored in {output_dir}")
    frame_files = sorted([f for f in os.listdir(output_dir) if f.endswith('.png')])

    if not frame_files:
        print("No frames found to create the video!")
        return

    first_frame = cv2.imread(os.path.join(output_dir, frame_files[0]))
    height, width, _ = first_frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

    for frame_file in frame_files:
        frame = cv2.imread(os.path.join(output_dir, frame_file))
        out.write(frame)

    out.release()
    print(f"Video saved at {video_path}")

# Logging setup for capturing the process of frame generation and video creation
def setup_logging():
    log_file = f"video_creation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    print(f"Logging to {log_file}")
    log = open(log_file, 'w')
    return log

def log_message(log, message):
    log.write(message + "\n")
    print(message)

# Function to merge multiple videos into a single video
def merge_videos(video_paths, output_video_path, fps=30):
    print(f"Merging videos into {output_video_path}...")
    # Open the first video to extract properties (width, height)
    cap = cv2.VideoCapture(video_paths[0])
    
    if not cap.isOpened():
        print("Error: Could not open first video.")
        return

    # Get the frame width and height from the first video
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Set up the video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    for video_path in video_paths:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Could not open video {video_path}. Skipping.")
            continue
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)

        cap.release()

    out.release()
    print(f"Final merged video saved at {output_video_path}")

# Main function to execute the entire text-to-video pipeline
def main():
    video_path = "generated_video.mp4"
    num_frames = 10
    fps = 1

    # Text descriptions for various rainy day scenes
    text_descriptions = [
         "Walk through a rainy street in a quiet town",
         "Sit by a window on a rainy day, watching the rain fall on the streets",
         "Walk along a cobblestone street on a rainy evening"
    ]

    # Initialize logging
    log = setup_logging()

    # Initialize the text-to-image generation pipeline
    pipeline = initialize_pipeline()

    # Temporary list to store the paths of generated videos
    generated_videos = []

    # Iterate through all the text descriptions
    for text_description in text_descriptions:
        # Create a directory specific to this description
        output_dir = f"video_frames_{text_description[:10].replace(' ', '_')}"
        create_output_directory(output_dir)

        # Log the description being processed
        log_message(log, f"Generating frames for: {text_description}")

        # Generate video frames from the text description
        generate_video_frames(pipeline, text_description, num_frames, output_dir)

        # Create a video from the generated frames
        video_file_path = f"{output_dir}.mp4"
        create_video_from_frames(output_dir, video_file_path, fps)

        # Add the generated video path to the list
        generated_videos.append(video_file_path)

    # Now, merge all the generated videos into one final video
    merge_videos(generated_videos, video_path, fps)

    # Close the log file after completion
    log_message(log, "Process completed successfully.")
    log.close()

# Execute the main function
if __name__ == "__main__":
    main()
