__author__ = "Yannick Brenning"
__email__ = "yannickbrenning2@gmail.com"


import math

import spotipy
from flask import Flask, render_template
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__, template_folder="chart/src", static_folder="chart/src/static")
app.config["DEBUG"] = True

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


@app.route("/")
def danceabilityScatter() -> str:
    assert (
        top_tracks_short := sp.current_user_top_tracks(
            limit=50, time_range="short_term"
        )
    ) is not None

    assert (
        top_tracks_mid := sp.current_user_top_tracks(limit=50, time_range="medium_term")
    ) is not None

    assert (
        top_tracks_long := sp.current_user_top_tracks(limit=50, time_range="long_term")
    ) is not None

    print([track["name"] for track in top_tracks_long["items"]])

    assert (
        top_artists_recent := sp.current_user_top_artists(
            limit=50, time_range="short_term"
        )
    ) is not None

    assert (
        feats_short := sp.audio_features(
            [item["id"] for item in top_tracks_short["items"]]
        )
    ) is not None

    assert (
        feats_mid := sp.audio_features([item["id"] for item in top_tracks_mid["items"]])
    ) is not None

    assert (
        feats_long := sp.audio_features(
            [item["id"] for item in top_tracks_long["items"]]
        )
    ) is not None

    data_short, data_mid, data_long = [], [], []
    for index, features in enumerate(feats_short[::-1]):
        data_short.append(
            {
                "x": features["loudness"],
                "y": features["energy"],
                "r": math.sqrt(index + 1),
            }
        )

    for index, features in enumerate(feats_mid[::-1]):
        data_mid.append(
            {
                "x": features["loudness"],
                "y": features["energy"],
                "r": math.sqrt(index + 1),
            }
        )

    for index, features in enumerate(feats_long[::-1]):
        data_long.append(
            {
                "x": features["loudness"],
                "y": features["energy"],
                "r": math.sqrt(index + 1),
            }
        )

    return render_template(
        "index.html",
        title="Loudness vs Energy in top 50 tracks",
        dataShort=data_short,
        dataMid=data_mid,
        dataLong=data_long,
    )


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
