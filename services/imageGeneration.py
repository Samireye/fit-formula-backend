import base64
from PIL import Image, ImageDraw, ImageFont
import io
import os
import logging
from typing import Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImageGenerationService:
    def __init__(self):
        self.assets_dir = os.path.join(
            os.path.dirname(__file__),
            "..",
            "assets"
        )
        # Create assets directory if it doesn't exist
        os.makedirs(self.assets_dir, exist_ok=True)
        
        # Create exercise type to image mapping
        self.exercise_images = {
            'push': ('pushup.png', 'Push-ups', (0, 0, 255)),  # Blue
            'squat': ('squat.png', 'Squats', (0, 128, 0)),    # Green
            'plank': ('plank.png', 'Plank', (255, 0, 0)),     # Red
            'lunge': ('lunge.png', 'Lunges', (128, 0, 128)),  # Purple
            'crunch': ('crunch.png', 'Crunches', (255, 165, 0)), # Orange
            'default': ('exercise.png', 'Exercise', (128, 128, 128)) # Gray
        }
        
        # Force recreate all images
        self._create_placeholder_images(force_recreate=True)

    def _draw_stick_figure(self, draw: ImageDraw, position: Tuple[int, int], exercise_type: str):
        """Draw a simple stick figure in different exercise positions"""
        x, y = position
        
        # Make lines thicker and white for better visibility
        line_width = 5
        figure_color = 'white'
        
        if exercise_type == 'push':
            # Push-up position stick figure
            draw.line((x-40, y, x+40, y), fill=figure_color, width=line_width)  # Body
            draw.line((x-30, y-20, x-30, y+20), fill=figure_color, width=line_width)  # Left arm
            draw.line((x+30, y-20, x+30, y+20), fill=figure_color, width=line_width)  # Right arm
            draw.line((x-15, y+30, x-15, y+60), fill=figure_color, width=line_width)  # Left leg
            draw.line((x+15, y+30, x+15, y+60), fill=figure_color, width=line_width)  # Right leg
            draw.ellipse((x-15, y-40, x+15, y-10), fill=figure_color)  # Head
            
        elif exercise_type == 'squat':
            # Squat position stick figure
            draw.line((x, y-30, x, y+20), fill=figure_color, width=line_width)  # Body
            draw.line((x-40, y-10, x, y-20), fill=figure_color, width=line_width)  # Left arm
            draw.line((x+40, y-10, x, y-20), fill=figure_color, width=line_width)  # Right arm
            # Legs in squat position
            draw.line((x, y+20, x-30, y+60), fill=figure_color, width=line_width)  # Left leg
            draw.line((x, y+20, x+30, y+60), fill=figure_color, width=line_width)  # Right leg
            draw.ellipse((x-15, y-50, x+15, y-20), fill=figure_color)  # Head
            
        elif exercise_type == 'plank':
            # Plank position stick figure
            draw.line((x-50, y, x+50, y), fill=figure_color, width=line_width)  # Body
            draw.line((x-40, y-20, x-40, y+20), fill=figure_color, width=line_width)  # Left arm
            draw.line((x+40, y-20, x+40, y+20), fill=figure_color, width=line_width)  # Right arm
            draw.line((x-25, y, x-25, y+40), fill=figure_color, width=line_width)  # Left leg
            draw.line((x+25, y, x+25, y+40), fill=figure_color, width=line_width)  # Right leg
            draw.ellipse((x-65, y-20, x-35, y+10), fill=figure_color)  # Head
            
        else:
            # Default standing stick figure
            draw.line((x, y-40, x, y+40), fill=figure_color, width=line_width)  # Body
            draw.line((x, y-20, x-30, y), fill=figure_color, width=line_width)  # Left arm
            draw.line((x, y-20, x+30, y), fill=figure_color, width=line_width)  # Right arm
            draw.line((x, y+40, x-20, y+80), fill=figure_color, width=line_width)  # Left leg
            draw.line((x, y+40, x+20, y+80), fill=figure_color, width=line_width)  # Right leg
            draw.ellipse((x-15, y-65, x+15, y-35), fill=figure_color)  # Head

    def _create_placeholder_images(self, force_recreate=False):
        """Create simple placeholder images with stick figures for different exercise types"""
        for exercise_type, (filename, title, color) in self.exercise_images.items():
            filepath = os.path.join(self.assets_dir, filename)
            if force_recreate or not os.path.exists(filepath):
                # Create a larger image for better quality
                img = Image.new('RGB', (400, 400), color=color)
                draw = ImageDraw.Draw(img)
                
                # Draw stick figure
                self._draw_stick_figure(draw, (200, 200), exercise_type)
                
                # Add exercise title
                try:
                    # Try to get a system font
                    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
                except:
                    font = ImageFont.load_default()
                    logger.warning(f"Could not load Helvetica font, using default")
                
                # Draw title with outline for better visibility
                text_bbox = draw.textbbox((0, 0), title, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_x = (400 - text_width) // 2
                
                # Draw text outline
                outline_color = 'black'
                for offset in [(1,1), (-1,-1), (1,-1), (-1,1)]:
                    draw.text((text_x + offset[0], 40 + offset[1]), title, font=font, fill=outline_color)
                
                # Draw main text
                draw.text((text_x, 40), title, fill='white', font=font)
                
                # Save with high quality
                img.save(filepath, quality=95)
                logger.info(f"Created exercise image for {exercise_type} at {filepath}")

    def _get_exercise_type(self, exercise_name: str) -> str:
        """Determine exercise type from name"""
        exercise_name = exercise_name.lower()
        logger.info(f"Finding exercise type for: {exercise_name}")
        for exercise_type in self.exercise_images.keys():
            if exercise_type in exercise_name:
                logger.info(f"Matched exercise type: {exercise_type}")
                return exercise_type
        logger.info("No specific exercise type found, using default")
        return 'default'

    def generate_exercise_image(self, exercise_description: str) -> str:
        """
        Return a pre-generated image based on exercise type.
        """
        try:
            logger.info(f"Generating image for exercise: {exercise_description}")
            
            # Determine exercise type and get corresponding image
            exercise_type = self._get_exercise_type(exercise_description)
            image_filename = self.exercise_images[exercise_type][0]
            image_path = os.path.join(self.assets_dir, image_filename)
            
            logger.info(f"Using image {image_filename} for exercise: {exercise_description}")
            
            # Load and convert image to base64
            with Image.open(image_path) as img:
                buffered = io.BytesIO()
                img.save(buffered, format="PNG", quality=95)
                img_str = base64.b64encode(buffered.getvalue()).decode()
                logger.info(f"Successfully encoded image for {exercise_description}")
                return img_str

        except Exception as e:
            logger.error(f"Error generating image: {str(e)}")
            return ""

    def generate_workout_images(self, exercises):
        """Generate images for a list of exercises"""
        logger.info(f"Generating images for {len(exercises)} exercises")
        return [self.generate_exercise_image(ex.name) for ex in exercises]
