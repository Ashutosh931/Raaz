/**
 * Interactive Energy Saving Simulator Scripts
 * Real-time reactive updates for college final-year project demonstration.
 */

document.addEventListener("DOMContentLoaded", () => {
  const sliderAC = document.getElementById("simSliderAC");
  const sliderLighting = document.getElementById("simSliderLighting");
  const sliderAppliances = document.getElementById("simSliderAppliances");
  const sliderPeak = document.getElementById("simSliderPeak");
  const checkStandby = document.getElementById("simCheckStandby");
  const inputBaseline = document.getElementById("simInputBaseline");
  const inputTariff = document.getElementById("simInputTariff");

  const badgeAC = document.getElementById("simBadgeAC");
  const badgeLighting = document.getElementById("simBadgeLighting");
  const badgeAppliances = document.getElementById("simBadgeAppliances");
  const badgePeak = document.getElementById("simBadgePeak");

  // Output Elements
  const outSavedKwh = document.getElementById("simOutSavedKwh");
  const outMoneySavedMo = document.getElementById("simOutMoneySavedMo");
  const outMoneySavedYr = document.getElementById("simOutMoneySavedYr");
  const outProjectedKwh = document.getElementById("simOutProjectedKwh");
  const outProjectedBill = document.getElementById("simOutProjectedBill");
  const outPercentSaved = document.getElementById("simOutPercentSaved");
  const outProgressBar = document.getElementById("simOutProgressBar");

  // Breakdown fields
  const outBreakdownAC = document.getElementById("simBreakdownAC");
  const outBreakdownApp = document.getElementById("simBreakdownApp");
  const outBreakdownLight = document.getElementById("simBreakdownLight");
  const outBreakdownPeak = document.getElementById("simBreakdownPeak");
  const outBreakdownStandby = document.getElementById("simBreakdownStandby");

  if (!sliderAC) return; // Exit if not on optimization/simulator page

  async function updateSimulation() {
    const acVal = parseFloat(sliderAC.value) || 0;
    const lightVal = parseFloat(sliderLighting.value) || 0;
    const appVal = parseFloat(sliderAppliances.value) || 0;
    const peakVal = parseFloat(sliderPeak.value) || 0;
    const standbyVal = checkStandby.checked;
    const baselineKwh = parseFloat(inputBaseline.value) || 240;
    const tariff = parseFloat(inputTariff.value) || 8.0;

    // Update Slider Badges
    if (badgeAC) badgeAC.textContent = `${acVal}%`;
    if (badgeLighting) badgeLighting.textContent = `${lightVal}%`;
    if (badgeAppliances) badgeAppliances.textContent = `${appVal}%`;
    if (badgePeak) badgePeak.textContent = `${peakVal}%`;

    try {
      const res = await fetch("/api/simulate-savings", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          baseline_monthly_kwh: baselineKwh,
          tariff: tariff,
          reduce_ac_pct: acVal,
          reduce_lighting_pct: lightVal,
          reduce_appliances_pct: appVal,
          shift_peak_pct: peakVal,
          eliminate_standby: standbyVal
        })
      });

      if (!res.ok) throw new Error("Simulation calculation failed");
      const result = await res.json();
      const sim = result.data;

      // Update DOM
      if (outSavedKwh) outSavedKwh.textContent = `${sim.total_kwh_saved} kWh`;
      if (outMoneySavedMo) outMoneySavedMo.textContent = `${sim.money_saved_monthly.toLocaleString()}`;
      if (outMoneySavedYr) outMoneySavedYr.textContent = `${sim.money_saved_yearly.toLocaleString()}`;
      if (outProjectedKwh) outProjectedKwh.textContent = `${sim.projected_monthly_kwh} kWh`;
      if (outProjectedBill) outProjectedBill.textContent = `${sim.projected_monthly_cost.toLocaleString()}`;
      if (outPercentSaved) outPercentSaved.textContent = `${sim.percentage_saved}%`;

      if (outProgressBar) {
        outProgressBar.style.width = `${Math.min(100, sim.percentage_saved)}%`;
        outProgressBar.setAttribute("aria-valuenow", sim.percentage_saved);
      }

      if (outBreakdownAC) outBreakdownAC.textContent = `${sim.breakdown.cooling_saved_kwh} kWh`;
      if (outBreakdownApp) outBreakdownApp.textContent = `${sim.breakdown.appliances_saved_kwh} kWh`;
      if (outBreakdownLight) outBreakdownLight.textContent = `${sim.breakdown.lighting_saved_kwh} kWh`;
      if (outBreakdownPeak) outBreakdownPeak.textContent = `${sim.breakdown.peak_shift_saved_kwh} kWh`;
      if (outBreakdownStandby) outBreakdownStandby.textContent = `${sim.breakdown.standby_saved_kwh} kWh`;

    } catch (err) {
      console.error("Simulation error:", err);
    }
  }

  // Attach event listeners
  [sliderAC, sliderLighting, sliderAppliances, sliderPeak, checkStandby, inputBaseline, inputTariff].forEach(elem => {
    if (elem) {
      elem.addEventListener("input", updateSimulation);
      elem.addEventListener("change", updateSimulation);
    }
  });

  // Initial calculation trigger
  updateSimulation();
});
