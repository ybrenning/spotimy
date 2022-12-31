__author__ = "Yannick Brenning"
__email__ = "yannickbrenning2@gmail.com"


import math
import os
from collections import defaultdict
from dotenv import load_dotenv
from typing import Any

import spotipy
from flask import Flask, render_template
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__, template_folder="chart/src", static_folder="chart/src/static")

load_dotenv()

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri="http://localhost:8888/callback",
        scope=[
            "user-top-read",
            "user-read-recently-played",
            "user-library-read",
            "playlist-read-private",
        ],
    )
)


def get_top_tracks() -> tuple[Any, Any, Any]:
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

    return (top_tracks_short, top_tracks_mid, top_tracks_long)


def get_audio_features(tracks: tuple[Any, Any, Any]) -> tuple[Any, Any, Any]:
    top_tracks_short, top_tracks_mid, top_tracks_long = tracks
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

    return (feats_short, feats_mid, feats_long)


def get_loudness_energy_data(
    feats: tuple[Any, Any, Any]
) -> tuple[list[dict[str, float]], list[dict[str, float]], list[dict[str, float]]]:
    feats_short, feats_mid, feats_long = feats
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

    return (data_short, data_mid, data_long)


def get_genre_counts(
    top_artists: tuple[Any, Any, Any]
) -> tuple[dict[str, int], dict[str, int], dict[str, int]]:
    top_artists_short, top_artists_mid, top_artists_long = top_artists

    genre_counts_short = defaultdict(lambda: 0)
    for item in top_artists_short["items"]:
        for genre in item["genres"]:
            genre_counts_short[genre] += 1

    for k, v in genre_counts_short.copy().items():
        if v == 1:
            del genre_counts_short[k]
            genre_counts_short["other"] += 1

    genre_counts_mid = defaultdict(lambda: 0)
    for item in top_artists_mid["items"]:
        for genre in item["genres"]:
            genre_counts_mid[genre] += 1

    for k, v in genre_counts_mid.copy().items():
        if v == 1:
            del genre_counts_mid[k]
            genre_counts_mid["other"] += 1

    genre_counts_long = defaultdict(lambda: 0)
    for item in top_artists_long["items"]:
        for genre in item["genres"]:
            genre_counts_long[genre] += 1

    for k, v in genre_counts_long.copy().items():
        if v == 1:
            del genre_counts_long[k]
            genre_counts_long["other"] += 1

    return (dict(genre_counts_short), dict(genre_counts_mid), dict(genre_counts_long))


def get_top_artists() -> tuple[Any, Any, Any]:
    assert (
        top_artists_short := sp.current_user_top_artists(
            limit=50, time_range="short_term"
        )
    ) is not None

    assert (
        top_artists_mid := sp.current_user_top_artists(
            limit=50, time_range="medium_term"
        )
    ) is not None

    assert (
        top_artists_long := sp.current_user_top_artists(
            limit=50, time_range="long_term"
        )
    ) is not None

    return (top_artists_short, top_artists_mid, top_artists_long)


def get_genre_counts_data(
    genre_counts_labels: list[str],
    genre_counts: tuple[dict[str, int], dict[str, int], dict[str, int]],
) -> list[list[int]]:
    genre_counts_data = []

    for index, gc in enumerate(genre_counts):
        genre_counts_data.append([])
        for label in genre_counts_labels:
            for k, v in gc.items():
                if label == k:
                    genre_counts_data[index].append(v)

    assert [len(data) == len(genre_counts_labels) for data in genre_counts_data]

    return genre_counts_data


@app.route("/")
def index() -> str:
    loudness_energy_data = get_loudness_energy_data(
        (get_audio_features(get_top_tracks()))
    )

    genre_counts = get_genre_counts(get_top_artists())
    genre_counts_labels_overlap = sorted(
        list(genre_counts[0].keys() & genre_counts[1].keys() & genre_counts[2].keys())
    )
    genre_counts_data = get_genre_counts_data(genre_counts_labels_overlap, genre_counts)

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
    )


if __name__ == "__main__":
    app.run(debug=True)
