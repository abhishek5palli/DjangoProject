var ctx = document.getElementById("myChart").getContext("2d");

var myChart = new Chart(ctx, {
    type: "bar",
    data: {
        labels: ["Python", "JavaScript", "PHP", "Java", "C#", "C++"],
        datasets: [
            {
                data: [13, 15, 5, 10, 9, 10],
            },
        ],
    },
});