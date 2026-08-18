/**
 * Analytics Page Visualizations (Chart.js)
 */

document.addEventListener("DOMContentLoaded", async () => {
  try {
    const res = await fetch("/api/analytics-data");
    if (!res.ok) throw new Error("Failed to fetch analytics datasets");
    const data = await res.json();

    const isDark = document.documentElement.getAttribute("data-theme") === "dark";
    const textColor = isDark ? "#9ca3af" : "#64748b";
    const gridColor = isDark ? "rgba(255,255,255,0.06)" : "rgba(0,0,0,0.05)";

    // 1. Timeline Trend Chart
    const trendCanvas = document.getElementById("analyticsTrendChart");
    if (trendCanvas) {
      const ctx = trendCanvas.getContext("2d");
      const gradient = ctx.createLinearGradient(0, 0, 0, 300);
      gradient.addColorStop(0, "rgba(14, 165, 233, 0.3)");
      gradient.addColorStop(1, "rgba(14, 165, 233, 0.0)");

      new Chart(trendCanvas, {
        type: "line",
        data: {
          labels: data.trend.labels,
          datasets: [{
            label: "Daily Consumption (kWh)",
            data: data.trend.values,
            borderColor: "#0ea5e9",
            backgroundColor: gradient,
            fill: true,
            tension: 0.35,
            borderWidth: 2.5,
            pointRadius: 3
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { grid: { color: gridColor }, ticks: { color: textColor } },
            y: { grid: { color: gridColor }, ticks: { color: textColor }, title: { display: true, text: "kWh", color: textColor } }
          }
        }
      });
    }

    // 2. Weekly Monday to Sunday Chart
    const weeklyCanvas = document.getElementById("analyticsWeeklyChart");
    if (weeklyCanvas) {
      new Chart(weeklyCanvas, {
        type: "bar",
        data: {
          labels: data.weekly.labels,
          datasets: [{
            label: "Average Usage (kWh)",
            data: data.weekly.values,
            backgroundColor: "#10b981",
            borderRadius: 8
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { grid: { display: false }, ticks: { color: textColor } },
            y: { grid: { color: gridColor }, ticks: { color: textColor }, title: { display: true, text: "Avg kWh", color: textColor } }
          }
        }
      });
    }

    // 3. Monthly Chart
    const monthlyCanvas = document.getElementById("analyticsMonthlyChart");
    if (monthlyCanvas) {
      new Chart(monthlyCanvas, {
        type: "bar",
        data: {
          labels: data.monthly.labels,
          datasets: [{
            label: "Monthly Total (kWh)",
            data: data.monthly.values,
            backgroundColor: "#6366f1",
            borderRadius: 8
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { grid: { display: false }, ticks: { color: textColor } },
            y: { grid: { color: gridColor }, ticks: { color: textColor }, title: { display: true, text: "Total kWh", color: textColor } }
          }
        }
      });
    }

    // 4. Peak Hours Chart
    const peakCanvas = document.getElementById("analyticsPeakChart");
    if (peakCanvas) {
      const bgColors = data.peak_hours.labels.map((_, idx) => (idx >= 18 && idx <= 22) ? "#f43f5e" : "#06b6d4");
      new Chart(peakCanvas, {
        type: "bar",
        data: {
          labels: data.peak_hours.labels,
          datasets: [{
            label: "Hourly Consumption (kWh)",
            data: data.peak_hours.values,
            backgroundColor: bgColors,
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { grid: { display: false }, ticks: { color: textColor, maxRotation: 45 } },
            y: { grid: { color: gridColor }, ticks: { color: textColor }, title: { display: true, text: "Avg kWh", color: textColor } }
          }
        }
      });
    }

    // 5. Temperature vs Energy Consumption (Scatter Plot)
    const scatterCanvas = document.getElementById("analyticsScatterChart");
    if (scatterCanvas) {
      new Chart(scatterCanvas, {
        type: "scatter",
        data: {
          datasets: [{
            label: "Records (°C vs kWh)",
            data: data.scatter,
            backgroundColor: "rgba(244, 63, 94, 0.65)",
            borderColor: "#f43f5e",
            pointRadius: 5,
            pointHoverRadius: 7
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: (ctx) => ` Temp: ${ctx.parsed.x}°C -> Energy: ${ctx.parsed.y} kWh`
              }
            }
          },
          scales: {
            x: { grid: { color: gridColor }, ticks: { color: textColor }, title: { display: true, text: "Ambient Temperature (°C)", color: textColor } },
            y: { grid: { color: gridColor }, ticks: { color: textColor }, title: { display: true, text: "Energy Consumption (kWh)", color: textColor } }
          }
        }
      });
    }

    // 6. Appliance Breakdown Doughnut
    const applianceCanvas = document.getElementById("analyticsApplianceChart");
    if (applianceCanvas) {
      new Chart(applianceCanvas, {
        type: "doughnut",
        data: {
          labels: data.appliances.labels,
          datasets: [{
            data: data.appliances.values,
            backgroundColor: ["#10b981", "#0ea5e9", "#f59e0b", "#8b5cf6", "#64748b"],
            borderWidth: 0
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: "bottom", labels: { color: textColor, padding: 14 } }
          },
          cutout: "65%"
        }
      });
    }

  } catch (err) {
    console.error("Analytics chart render error:", err);
  }
});
