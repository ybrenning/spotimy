function drawLoudnessEnergyBubble(title, dataShort, dataMid, dataLong) {
    var ctx = document.getElementById("myChart").getContext("2d");

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

function drawTopGenresBar(
    title, 
    labels, 
    dataShort,
    dataMid,
    dataLong
    ) {
    var ctx = document.getElementById("myChart2").getContext("2d");

    new Chart(
      ctx,
      {
        type: "bar",
        data: {
            labels: labels,
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
                },
            ]
        },
        options: {
            animation: {
                onComplete: () => {
                    delayed = true;
                },
                delay: (context) => {
                    let delay = 0;
                    if (context.type === "data" && context.mode === "default") {
                        delay = context.dataIndex * 300;
                    }

                    return delay;
                }
            },
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: title
                }
            }
        }
      }
    );
}
