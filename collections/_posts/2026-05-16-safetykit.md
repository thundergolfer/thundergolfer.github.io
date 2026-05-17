---
layout: post
title: "safetykit"
date: 2026-05-16
summary: A small collection of safety demos for human-in-the-loop scripts.
categories: software safety
permalink: safetykit
---

<figure style="margin: 0; margin-bottom: 1em;">
  <div style="display: flex; width: 100%; border-radius: 0.4em; overflow: hidden">
    <div style="flex: 1; overflow: hidden;">
      <img src="images/safetykit-lockout.jpg" alt="Lockout tags left on controls in an abandoned power plant" style="width: 100%;">
    </div>
  </div>
  <figcaption style="color: #777;">Tags left in place in a powerplant after it was shut down, decommissioned, and abandoned</figcaption>
</figure>

I made a small Python gist called [`safetykit`](https://gist.github.com/thundergolfer/931f08687d6b1b215083dbeb56f29f50). It is not meant to be a polished package. It is a set of runnable demonstrations for a simple idea: production scripts should have seatbelts.

The gist exists to make common safety techniques concrete. Instead of saying "be careful with destructive scripts", it shows a few ways a script can slow down, explain itself, ask for help, recover from interruption, and leave evidence behind.

<style>
  .safetykit-cast {
    margin: 1rem 0 2rem;
    overflow: hidden;
    border: 1px solid #252a33;
    border-radius: 0.4em;
    background: #0f1117;
  }

  .safetykit-cast__bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding: 0.45rem 0.7rem;
    color: #c8d0dc;
    background: #171b23;
    border-bottom: 1px solid #252a33;
    font-family: "Source Code Pro", Menlo, Consolas, monospace;
    font-size: 0.8rem;
  }

  .safetykit-cast__button {
    padding: 0.15rem 0.45rem;
    color: #dbeafe;
    background: transparent;
    border: 1px solid #475569;
    border-radius: 0.25rem;
    font: inherit;
    cursor: pointer;
  }

  .safetykit-cast__button:hover,
  .safetykit-cast__button:focus {
    border-color: #93c5fd;
  }

  .safetykit-cast__body {
    min-height: 10rem;
    max-height: 24rem;
    margin: 0;
    padding: 0.85rem;
    overflow: auto;
    color: #d1d5db;
    background: #0f1117;
    font-family: "Source Code Pro", Menlo, Consolas, monospace;
    font-size: 0.82rem;
    line-height: 1.45;
    white-space: pre-wrap;
  }
</style>

<script>
  (function () {
    const ansiColours = {
      "91": "#f87171",
      "92": "#86efac",
      "93": "#fde047",
      "94": "#7dd3fc",
      "38;5;208": "#fb923c",
    };

    const escapeHtml = (value) =>
      value
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;");

    const terminalHtml = (value) => {
      let html = "";
      let cursor = 0;
      let openSpan = false;
      const ansiPattern = /\u001b\[([0-9;]+)m/g;
      let match;

      while ((match = ansiPattern.exec(value)) !== null) {
        html += escapeHtml(value.slice(cursor, match.index));
        if (openSpan) {
          html += "</span>";
          openSpan = false;
        }

        const colour = ansiColours[match[1]];
        if (colour) {
          html += `<span style="color: ${colour}">`;
          openSpan = true;
        }

        cursor = ansiPattern.lastIndex;
      }

      html += escapeHtml(value.slice(cursor));
      if (openSpan) {
        html += "</span>";
      }
      return html;
    };

    const normaliseTerminalText = (value) =>
      value.replace(/\r\n/g, "\n").replace(/\r/g, "\n");

    const loadCast = async (container) => {
      const title = container.dataset.title || "terminal";
      container.innerHTML = `
        <div class="safetykit-cast__bar">
          <span>${escapeHtml(title)}</span>
          <button class="safetykit-cast__button" type="button">Play</button>
        </div>
        <pre class="safetykit-cast__body" aria-label="${escapeHtml(title)} terminal recording"></pre>
      `;

      const body = container.querySelector(".safetykit-cast__body");
      const button = container.querySelector(".safetykit-cast__button");
      const response = await fetch(container.dataset.cast);
      const lines = (await response.text()).trim().split("\n");
      const events = lines
        .slice(1)
        .map((line) => JSON.parse(line))
        .filter((event) => event[1] === "o");

      let timers = [];
      const clearTimers = () => {
        timers.forEach((timer) => clearTimeout(timer));
        timers = [];
      };
      const render = (text) => {
        body.innerHTML = terminalHtml(normaliseTerminalText(text));
        body.scrollTop = body.scrollHeight;
      };
      const renderInitial = () => render(events[0]?.[2] || "");

      button.addEventListener("click", () => {
        clearTimers();
        let transcript = "";
        let accumulatedDelay = 500;
        let previousTime = 0;
        button.disabled = true;
        button.textContent = "Playing...";
        render("");

        events.forEach((event) => {
          const eventTime = event[0];
          accumulatedDelay += Math.max(40, Math.min(1600, (eventTime - previousTime) * 1000));
          previousTime = eventTime;
          timers.push(
            setTimeout(() => {
              transcript += event[2];
              render(transcript);
            }, accumulatedDelay)
          );
        });

        timers.push(
          setTimeout(() => {
            button.disabled = false;
            button.textContent = "Replay";
          }, accumulatedDelay + 50)
        );
      });

      renderInitial();
    };

    const initialisePlayers = () => {
      document.querySelectorAll(".safetykit-cast").forEach((container) => {
        loadCast(container).catch(() => {
          container.textContent = "Could not load terminal recording.";
        });
      });
    };

    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", initialisePlayers);
    } else {
      initialisePlayers();
    }
  })();
</script>

## dryrun

Separates planning from execution by printing what would happen first, then shows the wet run committing the same delete.

<div class="safetykit-cast" data-title="python safetykit.py dryrun, then wet run" data-cast="/images/safetykit-casts/dryrun.cast"></div>

## confirm

Requires a typed confirmation before deleting a selected file, using a stronger guard than a reflexive y/n prompt. One cautionary reference is Leveson and Turner's [Therac-25 accident investigation](https://web.mit.edu/6.033/2004/wwwdocs/papers/Therac_1.html), where repeated proceed prompts helped train operators into dangerous reflexes.

<div class="safetykit-cast" data-title="python safetykit.py confirm" data-cast="/images/safetykit-casts/confirm.cast"></div>

## pause

Inserts a deliberate delay before a scary action so the human operator has time to interrupt.

<div class="safetykit-cast" data-title="python safetykit.py pause" data-cast="/images/safetykit-casts/pause.cast"></div>

## abort

Writes through a temporary file and atomic replace so cancellation does not leave a corrupt partial output.

<div class="safetykit-cast" data-title="python safetykit.py abort" data-cast="/images/safetykit-casts/abort.cast"></div>

## undo

Moves a file into quarantine first, waits briefly for a cancel key, and only commits the delete if the user does not undo it.

<div class="safetykit-cast" data-title="python safetykit.py undo" data-cast="/images/safetykit-casts/undo.cast"></div>

## feedback

Ramps CPU pressure on one logical core while printing color-coded progress, then stops cleanly when the user interrupts.

<div class="safetykit-cast" data-title="python safetykit.py feedback" data-cast="/images/safetykit-casts/feedback.cast"></div>

## audit

Emits a JSON Lines audit trail with hash chaining so a run has a durable record of what happened.

<div class="safetykit-cast" data-title="python safetykit.py audit" data-cast="/images/safetykit-casts/audit.cast"></div>

## two_person

Requires a second independently run script, with a shared secret, before the initiating script proceeds.

<div class="safetykit-cast" data-title="python safetykit.py two_person" data-cast="/images/safetykit-casts/two-person.cast"></div>

None of these techniques is exotic. That is the point. Most scripts can be made much safer with small, boring additions.
