function drawLoudnessEnergyBubble(title, dataShort, dataMid, dataLong) {
    var ctx = document.getElementById("mychart").getContext("2d");

    new Chart(
      ctx,
      {
        type: "bubble",
        data: {
            animation: {
                duration: 10
            },
            datasets: [
                {
                    label: "Past 4 weeks",
                    data: dataShort
                },
                {
                    label: "Past 6 months",
                    data: dataMid
                },
                {
                    label: "All time",
                    data: dataLong
                }
            ]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: title
                },
                tooltip: {
                    callbacks: {
                        label: (context) => {
                            return [
                                `loudness: ${context.raw.x}`, 
                                `energy: ${context.raw.y}`, 
                                `popularity: ${Math.round(context.raw.r * 2) / 2}`
                            ];
                        }
                    }
                }
            }
        }
      }
    );
}
