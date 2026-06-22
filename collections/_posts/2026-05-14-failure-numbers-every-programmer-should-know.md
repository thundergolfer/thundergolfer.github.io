---
layout: post
title: "Failure numbers every programmer should know"
date: 2026-05-14
categories: software reliability
summary: Reliability napkin math for hardware, cloud services, and software defects.
permalink: failure-numbers
side_footnotes: true
---

Peter Norvig's ["Latency Numbers Every Programmer Should Know"](/latency-numbers) are a classic in software engineer training. The original sixteen numbers represent, for programmers, the hard constraints of our hardware. In the early 2000s, if you cared about writing fast code you knew that a disk seek cost about 10 milliseconds.

> "You don't have to be an engineer to be a racing driver, but you do have to have Mechanical Sympathy."

Latency numbers are for programmers who want their systems to be fast.

Failure numbers are for programmers who want their systems to be *reliable*.

<div class="failure-table-shell" id="failure-table-shell" markdown="1">
<div class="failure-table-toolbar">
  <button
    type="button"
    class="failure-table-toggle"
    aria-controls="failure-mttf-chart"
    aria-pressed="false"
  >
    Show chart
  </button>
</div>

| Thing | Type | MTTF (years) | AFR | Notes |
| --- | --- | ---: | ---: | --- |
| CPU failure | Hardware | ~1,700 | ~0.06% | Server CPUs very rarely fail outright. Intel IT measured a 0.06% CPU AFR across 223,050 CPUs in 207,956 HPC servers, which converts to an MTTF of roughly 1,700 years by the simple reciprocal math used here.[^intel-component-afr] |
| Motherboard failure | Hardware | ~260 | ~0.38% | Motherboards are still rare failures, but less rare than CPUs. In the same Intel IT dataset, motherboards had a 0.38% AFR, or roughly 260 years MTTF by the same conversion.[^intel-component-afr] |
| SSD failure | Hardware | ~100 | ~1% | Enterprise SSD field data is usually around or below 1% AFR at the headline level, with model, age, and write workload hiding underneath. Backblaze's SSD boot-drive data is in this ballpark, though it is a much smaller SSD sample than its HDD fleet.[^backblaze-ssd] |
| HDD failure | Hardware | ~60 | ~1.5% | Backblaze's 2025 fleet snapshot reports 1.36% annual AFR and 1.30% lifetime AFR across hundreds of thousands of drives.[^backblaze-hdd] Use 1-2% unless you know the specific drive model and age. |
| RAM uncorrectable error | Hardware | ~75 | ~1-4% | In Google's DRAM study, 1.29% of machines per year had at least one uncorrectable error, with individual platforms reaching 4.15%.[^dram-errors] One uncorrectable error typically means a machine shutdown and DIMM replacement. |
| AWS regional outage, non-us-east-1 | Service | ~4 | ~25% | Here a failure means a region-scale incident big enough to require application-level mitigation, not every status page blip. |
| AWS regional outage, us-east-1 | Service | ~2 | ~50% | us-east-1 deserves its own row because it is old, huge, and entangled with many AWS control planes. See the [October 2025 AWS outage](/blog/aws-us-east-1-outage-oct20) for the shape of one such event. |
| ElastiCache 50-node cluster failover rate | Service | ~0.2 (73 days) | ~500% | AWS documents node replacement and failover as normal ElastiCache operating behavior.[^elasticache-resilience] I here use a 10-year MTTF based on observations of our clusters at Modal. This is a cluster-level operational rate, not a per-node failure rate. |
| NVIDIA A100 critical error[^gpu-critical] | Hardware | ~0.18 (65 days) | ~560% | Internal Modal fleet measurements. At this rate, a fleet of 1,000 A100s should expect about 15 critical GPU errors per day. |
| NVIDIA H100 critical error | Hardware | ~0.14 (50 days) | ~730% | Internal Modal fleet measurements. |
| Cloud VM unavailability | Service | ~20-100 | ~1-5% | Cloud providers publish availability SLAs, not clean per-VM failure rates.[^aws-compute-sla] For a single cloud VM, I use 1-5% as a rough annual chance that the VM needs recovery or replacement because the underlying host, network, or power failed underneath it. |
| Cloud VM disk loss | Service | ~500-1,000 | ~0.1-0.2% | AWS EBS gp2, gp3, io1, st1, and sc1 volumes are documented at 99.8-99.9% durability, which AWS also states as 0.1-0.2% annual failure rate.[^ebs-volume-types] io2 Block Express is a different class at 99.999% durability, or 0.001% AFR. |
| Production bug or defect | Software | ~0.001-0.005 (12h-2d) | ~20k-100k% | The most frequent failure mode is us. For active services deploying many times per day, DORA's change fail rate and deployment rework rate turn into a daily rhythm of defects, hotfixes, and regressions.[^dora-metrics] |

<div id="failure-mttf-chart" class="failure-mttf-chart" hidden></div>
</div>

- **MTTF** is mean time to failure: the average elapsed time between failures of a component, such as a disk. For repairable systems this is often discussed as [MTBF](https://en.wikipedia.org/wiki/Mean_time_between_failures).
- **AFR** is annualized failure rate. For low-rate component failures, read it as the approximate fraction of a population expected to fail in a year. For repeat-failing rows above 100%, read it as an annualized event rate: 300% means about three failures per component-year.
- I use the simple conversion `MTTF ~= 1 / AFR` when AFR is expressed as failures per component-year. This is a napkin-math table, not a claim that failures are independent, exponentially distributed, or evenly spread over time. The hardware papers are very clear that failures are correlated and messy.
- Obviously these estimates hinge on the definition of a *failure*. A fault is usually one component deviating from its specification. A failure is when the system as a whole stops servicing the client or user. An example of a fault is [when a memory cell in an NVIDIA GPU dies](/blog/nvidia-gpu-memory-capacity). This does not necessarily fail the device.
- This table does not attempt to rank severity. Severity is dependent on the relationship of the failed component to the rest of the system. A dead disk in a healthy replicated storage system is routine; a dead disk under a single-node Postgres instance can be the whole show.

<style>
  .failure-table-shell {
    position: relative;
  }

  .failure-table-toolbar {
    display: flex;
    justify-content: flex-start;
    margin: 1.5rem 0 0.65rem;
  }

  .failure-table-toggle {
    border: 1px solid #222;
    border-radius: 0.25rem;
    background: transparent;
    color: #222;
    cursor: pointer;
    font-family: inherit;
    font-size: 0.82rem;
    font-weight: 700;
    line-height: 1;
    padding: 0.48rem 0.7rem;
  }

  .failure-table-toggle:hover,
  .failure-table-toggle:focus {
    background: #222;
    color: #fff;
  }

  .failure-table-shell.is-chart-view table {
    display: none;
  }

  .failure-mttf-chart {
    margin: 0.75rem 0 1.25rem;
    border-top: 1px solid rgba(53, 53, 52, 0.16);
    border-bottom: 1px solid rgba(53, 53, 52, 0.16);
  }

  .failure-chart__header,
  .failure-chart__row {
    display: grid;
    grid-template-columns: minmax(8rem, 1.2fr) minmax(13rem, 2.4fr) minmax(5rem, 0.7fr);
    gap: 0.75rem;
    align-items: center;
  }

  .failure-chart__header {
    padding: 0.7rem 0;
    color: #777;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
  }

  .failure-chart__row {
    padding: 0.6rem 0;
    border-top: 1px solid rgba(53, 53, 52, 0.1);
    outline-offset: 0.18rem;
  }

  .failure-chart__row:focus {
    outline: 1px solid rgba(34, 34, 34, 0.45);
  }

  .failure-chart__row.is-scale-anchor .failure-chart__name {
    font-weight: 700;
  }

  .failure-chart__name {
    color: #222;
    font-size: 0.88rem;
    line-height: 1.2;
  }

  .failure-chart__type {
    display: block;
    margin-top: 0.15rem;
    color: #777;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.02em;
    text-transform: uppercase;
  }

  .failure-chart__track {
    position: relative;
    height: 0.9rem;
    background: rgba(53, 53, 52, 0.08);
    border-radius: 999px;
  }

  .failure-chart__bar {
    width: var(--bar-size);
    min-width: 0.15rem;
    max-width: 100%;
    height: 100%;
    background: var(--bar-color);
    border-radius: inherit;
    transition: width 160ms ease;
  }

  .failure-chart__track.is-clipped::after {
    content: "";
    position: absolute;
    top: 50%;
    right: -0.56rem;
    width: 0;
    height: 0;
    border-top: 0.35rem solid transparent;
    border-bottom: 0.35rem solid transparent;
    border-left: 0.48rem solid var(--bar-color);
    transform: translateY(-50%);
  }

  .failure-chart__hidden-label {
    position: absolute;
    top: 50%;
    right: 1rem;
    color: #fff;
    font-family: "Source Code Pro", monospace;
    font-size: 0.64rem;
    line-height: 1;
    pointer-events: none;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.35);
    transform: translateY(-50%);
    white-space: nowrap;
  }

  .failure-chart__value {
    color: #222;
    font-family: "Source Code Pro", monospace;
    font-size: 0.72rem;
    text-align: right;
  }

  .failure-chart__caption {
    margin: 0.75rem 0;
    color: #777;
    font-size: 0.74rem;
    line-height: 1.35;
  }

  @media screen and (min-width: 78em) {
    .failure-table-toolbar {
      position: absolute;
      top: 0;
      left: calc(100% + 3rem);
      display: block;
      width: 16rem;
      margin: 0;
    }
  }

  @media screen and (max-width: 34em) {
    .failure-chart__track {
      width: calc(100% - 0.7rem);
    }

    .failure-chart__hidden-label {
      font-size: 0.58rem;
      right: 0.82rem;
    }
  }

  @media screen and (max-width: 48em) {
    .failure-chart__header {
      display: none;
    }

    .failure-chart__row {
      grid-template-columns: 1fr;
      gap: 0.35rem;
    }

    .failure-chart__value {
      text-align: left;
    }
  }
</style>

<script>
  (function () {
    var rows = [
      { name: "CPU failure", type: "Hardware", years: 1667, label: "~1,700 years" },
      { name: "Cloud VM disk loss", type: "Service", years: 707, label: "~500-1,000 years" },
      { name: "Motherboard failure", type: "Hardware", years: 263, label: "~260 years" },
      { name: "SSD failure", type: "Hardware", years: 100, label: "~100 years" },
      { name: "RAM uncorrectable error", type: "Hardware", years: 75, label: "~75 years" },
      { name: "HDD failure", type: "Hardware", years: 60, label: "~60 years" },
      { name: "Cloud VM unavailability", type: "Service", years: 45, label: "~20-100 years" },
      { name: "AWS regional outage, non-us-east-1", type: "Service", years: 4, label: "~4 years" },
      { name: "AWS regional outage, us-east-1", type: "Service", years: 2, label: "~2 years" },
      { name: "ElastiCache 50-node cluster failover rate", type: "Service", years: 0.2, label: "~73 days" },
      { name: "NVIDIA A100 critical error", type: "Hardware", years: 0.18, label: "~65 days" },
      { name: "NVIDIA H100 critical error", type: "Hardware", years: 0.14, label: "~50 days" },
      { name: "Production bug or defect", type: "Software", years: 0.003, label: "~12h-2d" }
    ];

    var colors = {
      Hardware: "#0085ca",
      Service: "#278f5b",
      Software: "#a44a3f"
    };

    function initFailureChart() {
      var shell = document.getElementById("failure-table-shell");
      var button = shell && shell.querySelector(".failure-table-toggle");
      var chart = document.getElementById("failure-mttf-chart");

      if (!shell || !button || !chart) {
        return;
      }

      var maxYears = Math.max.apply(null, rows.map(function (row) {
        return row.years;
      }));
      var anchorBarFraction = 0.05;
      var defaultCaption = "Scale max: ~1,700 years. Arrowheads mark durations beyond the current scale.";

      chart.innerHTML = [
        '<div class="failure-chart__header" aria-hidden="true">',
        "  <span>Thing</span>",
        "  <span>MTTF, linear scale</span>",
        "  <span>Duration</span>",
        "</div>",
        rows.map(function (row, index) {
          return [
            '<div class="failure-chart__row" tabindex="0" data-row-index="' + index + '">',
            '  <div class="failure-chart__name">',
            "    " + row.name,
            '    <span class="failure-chart__type">' + row.type + "</span>",
            "  </div>",
            '  <div class="failure-chart__track" title="' + row.label + '" style="--bar-color: ' + colors[row.type] + ';">',
            '    <div class="failure-chart__bar"></div>',
            '    <span class="failure-chart__hidden-label" aria-hidden="true"></span>',
            "  </div>",
            '  <div class="failure-chart__value">' + row.label + "</div>",
            "</div>"
          ].join("");
        }).join(""),
        '<p class="failure-chart__caption">' + defaultCaption + '</p>'
      ].join("");

      var chartRows = chart.querySelectorAll(".failure-chart__row");
      var caption = chart.querySelector(".failure-chart__caption");

      function setScale(scaleMax, anchorIndex) {
        rows.forEach(function (row, index) {
          var chartRow = chartRows[index];
          var track = chartRow.querySelector(".failure-chart__track");
          var bar = chartRow.querySelector(".failure-chart__bar");
          var hiddenLabel = chartRow.querySelector(".failure-chart__hidden-label");
          var barSize = (row.years / scaleMax) * 100;
          var clipped = barSize > 100;

          bar.style.setProperty("--bar-size", (clipped ? 100 : barSize).toFixed(3) + "%");
          hiddenLabel.textContent = clipped ? formatHiddenPercent((1 - scaleMax / row.years) * 100) + "% of duration hidden" : "";
          track.classList.toggle("is-clipped", clipped);
          chartRow.classList.toggle("is-scale-anchor", index === anchorIndex);
        });

        if (anchorIndex === null) {
          caption.textContent = defaultCaption;
        } else {
          if (scaleMax === maxYears) {
            caption.textContent = "Scale max: ~1,700 years. This row is already large enough on the full linear scale.";
          } else {
            caption.textContent = "Scale reference: " + rows[anchorIndex].label + " at 5% width. Arrowheads mark durations beyond the current scale.";
          }
        }
      }

      function formatHiddenPercent(hiddenPercent) {
        if (hiddenPercent >= 99.5) {
          return "99.9";
        }

        if (hiddenPercent >= 10) {
          return Math.round(hiddenPercent).toString();
        }

        return hiddenPercent.toFixed(1).replace(/\.0$/, "");
      }

      function rowFromTarget(target) {
        var chartRow = target && target.closest && target.closest(".failure-chart__row");

        return chartRow && chart.contains(chartRow) ? chartRow : null;
      }

      function scaleToRow(chartRow) {
        var index = Number(chartRow.getAttribute("data-row-index"));

        if (Number.isNaN(index) || !rows[index]) {
          return;
        }

        setScale(Math.min(maxYears, rows[index].years / anchorBarFraction), index);
      }

      function resetWhenLeavingRow(event) {
        var nextRow = rowFromTarget(event.relatedTarget);

        if (!nextRow) {
          setScale(maxYears, null);
        }
      }

      chart.addEventListener("mouseover", function (event) {
        var chartRow = rowFromTarget(event.target);

        if (chartRow) {
          scaleToRow(chartRow);
        }
      });

      chart.addEventListener("click", function (event) {
        var chartRow = rowFromTarget(event.target);

        if (chartRow) {
          scaleToRow(chartRow);
        }
      });

      chart.addEventListener("mouseout", resetWhenLeavingRow);

      chart.addEventListener("focusin", function (event) {
        var chartRow = rowFromTarget(event.target);

        if (chartRow) {
          scaleToRow(chartRow);
        }
      });

      chart.addEventListener("focusout", resetWhenLeavingRow);

      function setChartMode(showChart) {
        shell.classList.toggle("is-chart-view", showChart);
        chart.hidden = !showChart;
        button.setAttribute("aria-pressed", showChart ? "true" : "false");
        button.textContent = showChart ? "Show table" : "Show chart";
        setScale(maxYears, null);
      }

      button.addEventListener("click", function () {
        setChartMode(!shell.classList.contains("is-chart-view"));
      });

      setScale(maxYears, null);
      setChartMode(false);
    }

    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", initFailureChart);
    } else {
      initFailureChart();
    }
  })();
</script>

[^intel-component-afr]: Intel IT's [Green Computing at Scale](https://www.intel.com/content/dam/www/central-libraries/us/en/documents/intel-it-green-computing-at-scale-paper.pdf) reports component annualized failure rates from 207,956 HPC servers observed from May 2019 through June 2020, including 223,050 CPUs and 207,956 motherboards.

[^backblaze-ssd]: [SSD Edition: 2022 Backblaze Drive Stats Review](https://www.backblaze.com/blog/ssd-drive-stats-2022/)

[^backblaze-hdd]: [Backblaze Drive Stats: hard drive reliability test data](https://www.backblaze.com/cloud-storage/resources/hard-drive-test-data)

[^dram-errors]: [DRAM Errors in the Wild: A Large-Scale Field Study](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/35162.pdf)

[^elasticache-resilience]: [Resilience in Amazon ElastiCache](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/disaster-recovery-resiliency.html)

[^gpu-critical]: "Critical error" here means an NVIDIA Xid or SXid error that is not recoverable without application and GPU reset. NVIDIA's Xid docs classify some errors with immediate actions such as `RESET_GPU` or `RESTART_APP`. See [NVIDIA Xid Errors](https://docs.nvidia.com/deploy/xid-errors/).

[^aws-compute-sla]: [Amazon Compute Service Level Agreement](https://aws.amazon.com/compute/sla/)

[^ebs-volume-types]: [Amazon EBS volume types](https://docs.aws.amazon.com/ebs/latest/userguide/ebs-volume-types.html)

[^dora-metrics]: [A history of DORA's software delivery metrics](https://dora.dev/insights/dora-metrics-history/)
