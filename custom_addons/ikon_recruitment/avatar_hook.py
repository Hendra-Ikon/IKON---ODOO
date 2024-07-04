import base64

def avatar_hooks(self):
        # Assuming you have the binary image data in user.partner_id.image_1920
        # Convert the binary image data to base64
        base64_encoded_image = base64.b64encode(self.env.user_id.image_1920).decode('utf-8')
        print(f"here is the image {base64_encoded_image}")

        # Return the context dictionary
        return {
            'user_image': base64_encoded_image,
            # Other context variables
        }
