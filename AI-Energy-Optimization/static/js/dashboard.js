/**
 * Dashboard Visualizations (Chart.js)
 */

document.addEventListener("DOMContentLoaded", async () => {
  try {
    const res = await fetch("/api/dashboard-charts");
    if (!res.ok) throw new Error("Failed to load chart data");
    const data = await res.json();

    const isDark = document.documentElement.getAttribute("data-theme") === "dark";
    const textColor = isDark ? "#9ca3af" : "#64748b";
    const gridColor = isDark ? "rgba(255,255,255,0.06)" : "rgba(0,0,0,0.05)";

    // 1. Daily Trend Chart
    const dailyCanvas = document.getElementById("dailyTrendChart");
    if (dailyCanvas) {
      const ctx = dailyCanvas.getContext("2d");
      const gradient = ctx.createLinearGradient(0, 0, 0, 260);
      gradient.addColorStop(0, "rgba(16, 185, 129, 0.35)");
      gradient.addColorStop(1, "rgba(16, 185, 129, 0.0)");

      new Chart(dailyCanvas, {
        type: "line",
        data: {
          labels: data.daily.labels,
          datasets: [{
            label: "Daily Energy (kWh)",
            data: data.daily.values,
            borderColor: "#10b981",
            backgroundColor: gradient,
            borderWidth: 2.5,
            fill: true,
            tension: 0.35,
            pointBackgroundColor: "#10b981",
            pointRadius: 4,
            pointHoverRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: (ctx) => ` Consumption: ${ctx.parsed.y} kWh`
              }
            }
          },
          scales: {
            x: { grid: { color: gridColor }, ticks: { color: textColor } },
            y: { grid: { color: gridColor }, ticks: { color: textColor }, title: { display: true, text: "kWh", color: textColor } }
          }
        }
      });
    }

    // 2. Peak Hours Chart
    const peakCanvas = document.getElementById("peakHoursChart");
    if (peakCanvas) {
      // Color peak hours (18 - 22) differently
      const bgColors = data.peak_hours.labels.map((lbl, idx) => {
        return (idx >= 18 && idx <= 22) ? "#f43f5e" : "#0ea5e9";
      });

      new Chart(peakCanvas, {
        type: "bar",
        data: {
          labels: data.peak_hours.labels,
          datasets: [{
            label: "Hourly Avg (kWh)",
            data: data.peak_hours.values,
            backgroundColor: bgColors,
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: (ctx) => ` Avg Usage: ${ctx.parsed.y} kWh`
              }
            }
          },
          scales: {
            x: { grid: { display: false }, ticks: { color: textColor, maxRotation: 45 } },
            y: { grid: { color: gridColor }, ticks: { color: textColor }, title: { display: true, text: "kWh", color: textColor } }
          }
        }
      });
    }

    // 3. Appliance Breakdown Doughnut
    const applianceCanvas = document.getElementById("applianceDoughnutChart");
    if (applianceCanvas) {
      new Chart(applianceCanvas, {
        type: "doughnut",
        data: {
          labels: data.appliances.labels,
          datasets: [{
            data: data.appliances.values,
            backgroundColor: ["#10b981", "#0ea5e9", "#f59e0b", "#8b5cf6", "#64748b"],
            borderWidth: 0,
            hoverOffset: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: "bottom",
              labels: { color: textColor, padding: 14, boxWidth: 12 }
            },
            tooltip: {
              callbacks: {
                label: (ctx) => ` ${ctx.label}: ${ctx.parsed}%`
              }
            }
          },
          cutout: "70%"
        }
      });
    }

    // 4. Actual vs Predicted Chart
    const actualVsPredCanvas = document.getElementById("actualVsPredChart");
    if (actualVsPredCanvas) {
      new Chart(actualVsPredCanvas, {
        type: "line",
        data: {
          labels: data.actual_vs_predicted.labels,
          datasets: [
            {
              label: "Actual Usage (kWh)",
              data: data.actual_vs_predicted.actual,
              borderColor: "#3b82f6",
              backgroundColor: "transparent",
              borderWidth: 2,
              tension: 0.3,
              pointRadius: 4
            },
            {
              label: "AI Prediction (kWh)",
              data: data.actual_vs_predicted.predicted,
              borderColor: "#10b981",
              borderDash: [5, 5],
              backgroundColor: "transparent",
              borderWidth: 2,
              tension: 0.3,
              pointRadius: 4
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: "top",
              labels: { color: textColor }
            }
          },
          scales: {
            x: { grid: { color: gridColor }, ticks: { color: textColor } },
            y: { grid: { color: gridColor }, ticks: { color: textColor }, title: { display: true, text: "kWh", color: textColor } }
          }
        }
      });
    }

  } catch (err) {
    console.error("Dashboard charts error:", err);
  }
});
