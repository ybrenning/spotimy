__author__ = "Yannick Brenning"
__email__ = "yannickbrenning2@gmail.com"


import os
import spotipy
from flask import Flask, redirect, render_template, request, session
from flask_session import Session

from data import (get_audio_features, get_genre_counts, get_genre_counts_data,
                  get_loudness_energy_data, get_rank_popularity_data,
                  get_top_artists, get_top_tracks)

app = Flask(__name__, template_folder="chart/src/templates", static_folder="chart/src/static")
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)


@app.route("/")
def index():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope=["user-top-read", "user-read-recently-played", "user-library-read","playlist-read-private"],
                                                cache_handler=cache_handler,
                                                show_dialog=True)
    if request.args.get("code"):
        # Step 2. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/')

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 1. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return f'<h2><a href="{auth_url}">Sign in</a></h2>'
    sp = spotipy.Spotify(auth_manager=auth_manager)

    top_tracks, top_artists = get_top_tracks(sp), get_top_artists(sp)

    loudness_energy_data = get_loudness_energy_data((get_audio_features(sp, top_tracks)))

    genre_counts = get_genre_counts(top_artists)
    genre_counts_labels_overlap = sorted(
        list(genre_counts[0].keys() & genre_counts[1].keys() & genre_counts[2].keys())
    )
    genre_counts_data = get_genre_counts_data(genre_counts_labels_overlap, genre_counts)

    rank_popularity_data = get_rank_popularity_data(top_artists)

    return render_template(
        "index.html",
        loudnessTitle="Loudness vs Energy in top 50 tracks",
        loudnessEnergyDataShort=loudness_energy_data[0],
        loudnessEnergyDataMid=loudness_energy_data[1],
        loudnessEnergyDataLong=loudness_energy_data[2],
        genreCountsTitle="Genres in top 50 artists",
        genreCountsLabels=genre_counts_labels_overlap,
        genreCountsDataShort=genre_counts_data[0],
        genreCountsDataMid=genre_counts_data[1],
        genreCountsDataLong=genre_counts_data[2],
        rankPopularityTitle="Personal popularity (rank) vs general popularity",
        rankPopularityDataShort=rank_popularity_data[0],
        rankPopularityDataMid=rank_popularity_data[1],
        rankPopularityDataLong=rank_popularity_data[2],
    )


if __name__ == "__main__":
    app.run(threaded=True, port=int(os.environ.get("PORT",
                                                   os.environ.get("SPOTIPY_REDIRECT_URI", 8080).split(":")[-1])))
