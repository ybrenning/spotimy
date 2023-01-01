__author__ = "Yannick Brenning"
__email__ = "yannickbrenning2@gmail.com"


from flask import Flask, render_template
from data import (
    get_top_tracks,
    get_audio_features,
    get_loudness_energy_data,
    get_top_artists,
    get_genre_counts,
    get_genre_counts_data,
)

app = Flask(__name__, template_folder="chart/src", static_folder="chart/src/static")


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
