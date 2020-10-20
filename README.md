# StitchIg!

<img src="https://raw.githubusercontent.com/dhruvs009/StitchIg/master/logo.png" width="500"></img>

A simple web application that fetches images from your Instagram feed (requires authentication from your Instagram account) and returns a stitched 196x196 image in a square grid, with square thumbnails of these images. Adios.

### How to use (doesn't work yet, this application needs permissions from Instagram): 
1. Go to [my website](https://dhruvs009.github.io/me/), open the Menu dropdown from the header bar (or from the side drawer if on the mobile browser) and click on StitchIg! (or open [this link](https://www.instagram.com/oauth/authorize?client_id=3311032495590903&redirect_uri=https://stitchig.herokuapp.com/&scope=user_profile,user_media&response_type=code)).
2. Authorize the app to access your Instagram images.
3. Voila!

### How to clone:
1. Follow the Instagram API guide to obtain a Client ID, Client Secret, and a redirect URI [here](https://developers.facebook.com/docs/instagram-basic-display-api/getting-started).
2. Clone the project on your system.
3. Create a .env file having CLIENT_ID, CLIENT_SECRET, REDIRECT_URI as obtained.
4. Install all dependencies and run `python app.py`.
5. Open `https://www.instagram.com/oauth/authorize?client_id=3311032495590903&redirect_uri={redirect-uri}&scope=user_profile,user_media&response_type=code` in a browser, replacing `{redirect-uri}` with REDIRECT_URI.
6. The browser redirects to `{redirect-uri}/?code={code}`.
7. Change `{redirect-uri}` to `localhost:5000` to get the stitched image.
8. Alternatively, you may deploy the Flask app to some hosting service, and change `{redirect-uri}` as per your convenience.


> [Dhruv Sahnan](https://github.com/dhruvs009) <br>
> Quarantine | COVID-19 <br>
> What to do when you're on house arrest.
