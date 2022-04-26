import Chartist from "https://cdn.skypack.dev/chartist";
import Humanize from "https://cdn.skypack.dev/humanize-plus";

document.querySelectorAll(".pie-chart").forEach((el) => {
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
});

document.querySelectorAll(".line-chart.line-chart--small").forEach((el) => {
  const values = el.dataset.values.split(",").map((v) => parseFloat(v));

  new Chartist.Line(
    el,
    { series: [values] },
    {
      fullWidth: true,
      fullHeight: true,
      showPoint: false,
      axisX: {
        showLabel: false,
        showGrid: false,
        offset: 0,
      },
      axisY: {
        showLabel: false,
        showGrid: false,
        offset: 0,
      },
    }
  );
});

document.querySelectorAll(".line-chart.line-chart--big").forEach((el) => {
  const values = el.dataset.values.split(",").map((v) => parseFloat(v));

  new Chartist.Line(
    el,
    { series: [values] },
    {
      fullWidth: true,
      showPoint: false,
      axisX: {
        showLabel: false,
        showGrid: false,
      },
      axisY: {
        offset: 24,
        labelInterpolationFnc: (value) =>
          Humanize.compactInteger(
            value,
            value >= 1000000 || (value >= 1000 && value < 10000) ? 1 : 0
          ),
      },
    }
  );
});

document.querySelectorAll("[data-set-tab]").forEach((el) => {
  el.addEventListener("click", function (e) {
    e.preventDefault();

    document
      .querySelectorAll(".tab--active")
      .forEach((el) => el.classList.remove("tab--active"));

    document
      .querySelectorAll(`[data-set-tab="${el.dataset.setTab}"]`)
      .forEach((el) => el.classList.add("tab--active"));

    document
      .querySelectorAll("[data-tab]:not(.hidden)")
      .forEach((el) => el.classList.add("hidden"));

    document
      .querySelectorAll(`[data-tab="${el.dataset.setTab}"]`)
      .forEach((el) => {
        el.classList.remove("hidden");
        if (el.__chartist__) {
          el.__chartist__.update();
        }
      });
  });
});
