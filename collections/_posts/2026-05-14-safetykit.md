---
layout: post
title: "safetykit"
date: 2026-05-14
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

The demos:

- **dryrun** (`praise_dryrun`) - Separates planning from execution by printing what would happen before anything actually changes.
- **confirm** (`ask_for_confirmation`) - Requires a typed confirmation before deleting a selected file, using a stronger guard than a reflexive y/n prompt.
- **pause** (`pause_a_beat`) - Inserts a deliberate delay before a scary action so the human operator has time to interrupt.
- **abort** (`abort_safely`) - Writes through a temporary file and atomic replace so cancellation does not leave a corrupt partial output.
- **undo** (`undo`) - Moves a file into quarantine first, waits briefly for a cancel key, and only commits the delete if the user does not undo it.
- **feedback** (`feedback`) - Ramps CPU pressure on one logical core while printing color-coded progress, making the system's changing state visible.
- **audit** (`audit`) - Emits a JSON Lines audit trail with hash chaining so a run has a durable record of what happened.
- **two_person** (`two_person_rule`) - Requires a second independently run script, with a shared secret, before the initiating script proceeds.

None of these techniques is exotic. That is the point. Most scripts can be made much safer with small, boring additions.
