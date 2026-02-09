# Adding Your Profile Image

To display your profile picture in the chatbot:

## Option 1: Add Image File (Recommended)

1. **Get your profile image**:
   - Use a professional headshot or profile photo
   - Recommended size: 400x400 pixels or larger (will be resized to 100x100)
   - Supported formats: JPG, PNG, JPEG

2. **Add to project**:
   - Save your image as `profile.jpg` or `profile.png`
   - Place it in the **root directory** of KavanaBot (same folder as app.py)

3. **If using PNG** (update app.py):
   - Change line in app.py from `st.image("profile.jpg", width=100)` 
   - To: `st.image("profile.png", width=100)`

## Option 2: Use URL

If your image is hosted online:

1. Get the direct image URL (should end in .jpg, .png, etc.)
2. Update `app.py` line to use your URL:
   ```python
   st.image("YOUR_IMAGE_URL_HERE", width=100)
   ```

## Option 3: Use LinkedIn Photo

1. Go to your LinkedIn profile
2. Right-click your profile photo
3. Select "Copy image address"
4. Update `app.py` with that URL

## Current Setup

Currently using a placeholder image. Once you add `profile.jpg` to the project root, it will display automatically.

---

**Note**: The app will work fine without an image - it just shows a placeholder until you add yours.
