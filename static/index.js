import Chartist from "https://cdn.skypack.dev/chartist";

for (let el of document.querySelectorAll(".pie-chart")) {
  const values = el.dataset.values.split(",").map((v) => parseInt(v));

  new Chartist.Pie(
    el,
    { series: values },
    {
      donut: true,
      donutWidth: 6,
      total: values.reduce((v, a) => v + a, 0),
      showLabel: false,
    }
  );
}

for (let el of document.querySelectorAll(".line-chart")) {
  const values = el.dataset.values.split(",").map((v) => parseInt(v));
  console.log(values);

  new Chartist.Line(
    el,
    {
      series: [values],
    },
    {
      fullWidth: true,
      showPoint: false,
      axisX: {
        showLabel: false,
        showGrid: false,
      },
      axisY: {
        offset: 24,
      },
    }
  );
}
