__author__ = "Yannick Brenning"
__email__ = "yannickbrenning2@gmail.com"


import spotipy
from flask import Flask, render_template
from spotipy.oauth2 import SpotifyOAuth


app = Flask(__name__, template_folder="chart/src", static_folder="chart/src/static")
app.config["DEBUG"] = True


@app.route("/")
def bar() -> str:
    labels = ["2010", "2011", "2012", "2013", "2014", "2015", "2016"]
    values = [10, 20, 15, 25, 22, 30, 28]

    return render_template("index.html", title="Spotimy", labels=labels, values=values)


def get_feats() -> None:
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id="234c6a0dc44f448c852994904a94dc54",
            client_secret="af2922d4fc174a46866abffe3134a281",
            redirect_uri="http://localhost:8888/callback",
            scope=[
                "user-top-read",
                "user-read-recently-played",
                "user-library-read",
                "playlist-read-private",
            ],
        )
    )

    assert (
        top_tracks := sp.current_user_top_tracks(limit=50, time_range="short_term")
    ) is not None
    print([item["name"] for item in top_tracks["items"]])

    assert (
        top_artists := sp.current_user_top_artists(limit=50, time_range="short_term")
    ) is not None
    print([item["name"] for item in top_artists["items"]])

    feats = sp.audio_features([item["id"] for item in top_tracks["items"]])
    print(feats)


if __name__ == "__main__":
    app.run(debug=True)
