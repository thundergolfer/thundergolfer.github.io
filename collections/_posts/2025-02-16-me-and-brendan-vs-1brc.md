---
layout: post
title: "Me and Brendan Gregg vs. the 1 billion row challenge: a worklog (Part 1)"
date: 2025-02-16
categories: software performance linux
summary: Is one book and a can-do attitude all you need to write fast code?
permalink: /blog/1brc
---

![Black and White Minimalist Paper Mockup Facebook Post.png](/images/me-and-brendan-hero.png)

I just got through a front-to-back read of Brendan’s Gregg’s tome, *Systems Performance*. The book is great, packed with valuable information that I feared would slip away without exercise. I’m a decidedly mid performance engineer, but I’m keen to get better with reading and exercises.

Performance engineering is a particularly challenging subdomain of software engineering, and until now I’d read zero books dedicated to the subject. Surely, [you must read at least one book to ride](https://ludic.mataroa.blog/blog/you-must-read-at-least-one-book-to-ride/).

I wondered, with just this book’s methodologies and reference material—no internet!—how fast could I get on an interesting performance challenge? The challenge I chose had been on my to-do list for about a year: the [1 Billion Row challenge (1brc)](https://github.com/gunnarmorling/1brc).

# The 1brc

To save a click and scroll, here’s what the 1 billion row challenge involves.

You get a text file 1,000,000,000 lines long and must compute exact statistics over its data.

> The text file contains temperature values for a range of weather stations. Each row is one measurement in the format `<string: station name>;<double: measurement>`, with the measurement value having exactly one fractional digit. The following shows ten rows as an example:
> 
> 
> ```
> Hamburg;12.0
> Bulawayo;8.9
> Palembang;38.8
> St. John's;15.2
> Cracow;12.6
> Bridgetown;26.9
> Istanbul;6.2
> Roseau;34.4
> Conakry;31.2
> Istanbul;23.0
> 
> ```
> 
> The task is to write a ~~Java~~ Rust program which reads the file, calculates the min, mean, and max temperature value per weather station, and emits the results on stdout like this (i.e. sorted alphabetically by station name, and the result values per station in the format `<min>/<mean>/<max>`, rounded to one fractional digit):
> 
> ```
> {Abha=-23.0/18.0/59.2, Abidjan=-16.2/26.0/67.3, Abéché=-10.0/29.4/69.0, Accra=-10.1/26.4/66.4, Addis Ababa=-23.7/16.0/67.0, Adelaide=-27.8/17.3/58.5, ...}
> 
> ```
> 

## Summary

I’ll start with a naive kernel and step-by-step apply optimizations until I give up and read how the fastest implementations acheived their speed. As said above, I’m not a great performance engineer so I expect I won’t get close to the record speed. 

<style>
.table-header {
    background-color: #f5f5f5;
    font-weight: bold;
}
</style>

<table>
<tr class="table-header">
    <th>Implementation</th>
    <th>Instructions count</th>
    <th>Wall clock time</th>
    <th>Performance relative to fastest implementation</th>
</tr>
<tr>
    <td>0. Napkin math</td>
    <td>300 billion</td>
    <td>100 seconds</td>
    <td style="color: gray;">Dunno! No spoilers yet.</td>
</tr>
<tr>
    <td>1. Naive</td>
    <td>1.5 trillion</td>
    <td>146.913 seconds</td>
    <td style="color: gray;">Dunno! No spoilers yet.</td>
</tr>
<tr>
    <td>2. Multi-threading</td>
    <td></td>
    <td></td>
    <td style="color: gray;">Upcoming…</td>
</tr>
<tr>
    <td>🥇 Rust record holder</td>
    <td>?</td>
    <td>?</td>
    <td style="color: gray;">Dunno! No spoilers yet.</td>
</tr>
</table>

## Implementation 0: napkin math

<div class="callout-panel callout-panel-note">
    <span class="callout-panel-icon callout-panel-note-icon">
        <span class="sc-bZQynM TunNK" role="img" aria-label="Panel note">
            <svg width="24" height="24" viewBox="0 0 24 24" focusable="false" role="presentation">
                <path d="M8 4h8a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2zm1.5 4a.5.5 0 0 0-.5.5v1a.5.5 0 0 0 .5.5h5a.5.5 0 0 0 .5-.5v-1a.5.5 0 0 0-.5-.5h-5zm0 4a.5.5 0 0 0-.5.5v1a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-1a.5.5 0 0 0-.5-.5h-3z" fill="currentColor" fill-rule="evenodd"></path>
            </svg>
        </span>
    </span>
    <div class="ak-editor-panel__content">
        <p data-renderer-start-pos="97">
            See <a href="/latency-numbers" style="text-decoration: none; box-shadow: none; border: none">'Beyond 'latency numbers every programmer should know'</a> for my affirmation of napkin math practice.
        </p>
    </div>
</div>


To get a quick sense of expected performance on this problem *without* writing code, let’s do some [napkin math](https://sirupsen.com/napkin).

- Each row is around 10 characters for the name, 1 char for the separator, 3 chars for the float, and 1 char for the newline. Let’s round to 15 characters for ease.
- The characters look all ASCII, so one byte per char.
- So the file is approx. `15 * 10**9` bytes or 15 GiB. That’s quite a lot of data!

Let’s keep things simple and ignore more advanced x86 instructions (e.g. SIMD) and think about single-threaded performance first. This problem is embarassingly parallel though, so we should definitely think about multi-threading at some point.

- Single-threaded memory bandwidth is around 10 GiB/s, so a naive implementation has to take over a second.
- But is this program memory bandwidth bounded?

A naive solution is going to scan through the file, stopping at each `\n` and acquiring a line. 

Reading characters with just [`fgetc`](https://www.ibm.com/docs/en/i/7.5?topic=functions-fgetc-read-character) involves a dozen or so instructions per call to do buffer management and memory reading (⚠️: bit hand-wavy here). I’ll use a round number of 10 per char, so `10 * 15 * 10 ** 9` instructions just for reading characters.

Then we’ll split on `;` to get a name and a value. 

That’s roughly `15 * 10**9` char comparisons for line splitting and then roughly `10 * 10 ** 9` char comparisons to split out the parts (the number is 5 chars). So 25 in total. At 3GHz just the char comparisons will take around 8 seconds.

But at each line boundary, we also need to have done on the weather station’s hashmap entry:

- A counter increment, to enable a mean calculation.
- An addition for SUM calcuation.
- A compare-and-set for MIN calculation.
- A compare-and-set for MAX calcuation.

These are simple instructions on floats so they take around 1 clock cycle. (Float multiply or divide would be a different, slower story.)

Oh we can’t do these operations until we parse the number into `f64`! I’m not familiar with how this would be implemented efficiently, but it has to involve some floating-point multiplication and char comparison, so I’ll ballpark it at around 10 clock cycles. These values are tempuratures on Earth so they’ll be in the range -150.0F → 150.00F.

I also have ignored hashing the weather station name to find the addresses for the min, max, sum, and count! That’s important so let’s add that in. That’ll be roughly a further 10 operations per line to get a hashmap bucket index and then a memory access for the entry of around 100ns (main memory).

We now have:

- `150 ** 10**9` instructions for char reads
- `15 * 10**9` char comparison clock cycles for line splitting.
- `10 * 10**9` char comparison clock cyles for splitting name from value.
- `10 * 10**9` float parsing clock cycles
- `10 * 10**9` hash calculation clock cycles
- `100 * 10**9` entry retrieval clock cycles
- `4 * 10**9` calculating instructions.

That’s 299 billion cycles. Call it an even 300 billion.

This ignores the mean calculations but this is O(num unique stations) not O(num lines) and will probably be insignificant.

Alright, all this considered, I think we’re bound by instruction throughput and estimated that on a modern, roughly 3GHz CPU processor, single-threaded and using no fancy instructions, a solution will take…

🥁…

100 seconds to calculate.

(There’s some tuning we could do to account for instruction pipelining, but whatever.)

Overall this was a more involving bit of napkin math estimation than I typically do. I only have medium confidence that there’s not a serious mistake throwing off the estimate.

I’m tempted to look up what the naive solution is, but I said no internet, so I’ll just have to implement it and find out myself!

## Implementation 1: Naive implementation

Our napkin mathing above required going through the algorithm, so I’ll avoid repeating myself and just get into a naive implementation in Rust.

```rust
///! 1️⃣🐝🏎️ The One Billion Row Challenge.
use std::collections::HashMap;
use std::fs::File;
use std::error::Error;
use std::io::{BufRead, BufReader};

#[derive(Debug)]
struct StationStats {
    count: u64,
    sum: f64,
    min: f64,
    max: f64,
}

fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} <filepath>", args[0]);
        std::process::exit(1);
    }

    let mut station_stats: HashMap<String, StationStats> = HashMap::new();
    let filepath = &args[1];
    let f = BufReader::new(File::open(filepath)?);
    for line in f.lines() {
        // Each line is formatted as: $NAME;$TEMPERATURE.
        // For example: "Goodlettsville;41.6"
        let line = line?;
        let line_parts: Vec<&str> = line.split(';').collect();
        let station_name = line_parts[0];
        let temperature = line_parts[1].parse::<f64>().unwrap();
        
        let station_stats = if let Some(stats) = station_stats.get_mut(station_name) {
            stats
        } else {
            station_stats.entry(station_name.to_string()).or_insert(StationStats {
                count: 0,
                sum: 0.0,
                min: f64::MAX,
                max: f64::MIN,
            })
        };
        station_stats.count += 1;
        station_stats.sum += temperature;
        station_stats.min = if temperature < station_stats.min { temperature } else { station_stats.min };
        station_stats.max = if temperature > station_stats.max { temperature } else { station_stats.max };
    }

    // Print out min/mean/max values per station in alphabetical order.
    // e.g. {Abha=5.0/18.0/27.4, Abidjan=15.7/26.0/34.1, Abéché=12.1/29.4/35.6, Accra=14.7/26.4/33.1, Addis Ababa=2.1/16.0/24.3, Adelaide=4.1/17.3/29.7, ...}
    let mut stations: Vec<(&String, &StationStats)> = station_stats.iter().collect();
    stations.sort_by(|a, b| a.0.cmp(b.0));
    
    let mut output = String::with_capacity(stations.len() * 30);
    for (station_name, stats) in stations.iter() {
        let mean = stats.sum / stats.count as f64;
        output.push_str(&format!("{}={:.1}/{:.1}/{:.1}\n", 
            station_name,
            stats.min,
            mean.round(),
            stats.max
        ));
    }
    println!("{}", output);

    Ok(())
}
```

The implementation is a buffered reader with line splitting. On each line, it splits on the semicolon and parses the tempurature string into an f64. The entry is then populated or retrieved, and processed.

### Benchmark it!

I’m running this benchmark on an AWS EC2 `m6i.4xlarge` instance which has 16 vCPUs and 64 GiB of RAM. 

I let [hyperfine](https://github.com/sharkdp/hyperfine) chew on it while I did some brief household chores.

```python
(modal) ubuntu@ip-10-1-8-45:~/uni/performance/onebillionrowschallenge$ hyperfine 'target/release/onebillionrowschallenge data/measurements.txt'
Benchmark 1: target/release/onebillionrowschallenge data/measurements.txt
 ⠧ Current estimate: 146.913 s █████████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ ETA 00:17:09
```

It came back with ~147 seconds or 2.45 minutes.

I estimated 100 seconds with napkin math so I was off by a factor of **1.5**. This is within an order of magnitude so it’s a good estimate. It’ll be interesting to try and find out whether I was close by accident!

**Is the program disk/memory bottlenecked?**

To validate our napkin math against the baseline/naive implementation, let’s look at I/O latency. If page cache is cold, sequential disk read throughput is 2GiB/s (~6s of reading). If page cache is warm, single-threaded memory bandwidth is about 10GB/s (1s of reading). 

Simply reading the file is indeed fast; we’re not memory-bound:

```bash
$ time cat ./data/measurements.txt > /dev/null

real	0m1.689s  # 8.771 GiB/s
user	0m0.000s
sys	0m1.689s
```

Dumping page cache, we get the expected disk throughput:

```bash
$ dd of=/dev/null if=./data/measurements.txt iflag=nocache count=0
0+0 records in
0+0 records out
0 bytes copied, 4.2777e-05 s, 0.0 kB/s
# IMPORTANT: measurements.txt file should be on a local NVME disk, not EBS NAS.
$ time cat ./data/measurements.txt > /dev/null

real	0m6.632s  # 2.23 GiB/s
user	0m0.019s
sys	0m4.570s
```

<div class="callout-panel callout-panel-note">
    <span class="callout-panel-icon callout-panel-note-icon">
        <span class="sc-bZQynM TunNK" role="img" aria-label="Panel note">
            <svg width="24" height="24" viewBox="0 0 24 24" focusable="false" role="presentation">
                <path d="M8 4h8a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2zm1.5 4a.5.5 0 0 0-.5.5v1a.5.5 0 0 0 .5.5h5a.5.5 0 0 0 .5-.5v-1a.5.5 0 0 0-.5-.5h-5zm0 4a.5.5 0 0 0-.5.5v1a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-1a.5.5 0 0 0-.5-.5h-3z" fill="currentColor" fill-rule="evenodd"></path>
            </svg>
        </span>
    </span>
    <div class="ak-editor-panel__content">
        <p data-renderer-start-pos="97">
            If you’re on an EC2 instance be careful about the fact that the disk is probably network attached storage and thus you can get 10x worse results without page cache population. For example, use M6i<strong>d</strong> instances which have local NVMe-based solid state drive (SSD), <em>not</em> M6i.
        </p>
    </div>
</div>

**Is the program instruction bottlenecked?** 

The napkin math analysis indicated that this program was bottlenecked on CPU instruction throughput. We can easily confirm this (on a bare metal) instance by using *Perform Monitoring Counters,* a.k.a hardware events, and kernel software events (Gregg, 16.1.6, pg. 789).

```bash
$ perf stat ./target/release/onebillionrowschallenge ./data/measurements.txt

<-- snip program stdout output! -->

 Performance counter stats for './target/release/onebillionrowschallenge ./data/measurements.txt':

         153530.17 msec task-clock                #    1.000 CPUs utilized
               341      context-switches          #    2.221 /sec
                 0      cpu-migrations            #    0.000 /sec
               697      page-faults               #    4.540 /sec
      536187309805      cycles                    #    3.492 GHz
     1537076929793      instructions              #    2.87  insn per cycle
      308555080896      branches                  #    2.010 G/sec
        3645809573      branch-misses             #    1.18% of all branches
     2680933769020      slots                     #   17.462 G/sec
     1433877571908      topdown-retiring          #     49.3% retiring
      651834877173      topdown-bad-spec          #     22.4% bad speculation
      630793453075      topdown-fe-bound          #     21.7% frontend bound
      193645176043      topdown-be-bound          #      6.7% backend bound

     153.537660753 seconds time elapsed

     151.698994000 seconds user
       1.831939000 seconds sys
```

Wow so we actually executed *1.53 trillion* instructions, not 0.3 trillion as I claimed in the napkin math. I was off by a factor of 5, quite bad. The 2.87 instructions per cycle (instruction parallelism) and higher clockspeed (3.492 GHz actual vs. 3GHz napkin) brought my estimate much closer than it should have been.

**Recap**

So to recap, I implemented a naive, single-threaded implementation of the 1brc and got 2.45 minutes, executing 1.53 trillion instructions according to `perf`. I underestimated instruction count in my napkin math, but was correct that the solution is currently instruction-bound.

I need to either execute way more instructions per second or execute way fewer instructions overall.

## Implementation 2: multi-threading

### Assembly check!

I was off by a factor of 5 on the number of instructions, so before proceeding to the most obvious optimization, multi-threading, let’s find out where I undercounted instructions.

First port of call will be using [Godbolt.org](http://Godbolt.org) to where the program’s instruction is coming from.

[https://godbolt.org/z/zxonEEnTc](https://godbolt.org/z/zxonEEnTc)

*More coming soon…*

---

<style>
.callout-panel {
    border-radius: 3px;
    margin: 1.145rem 0px 1rem 0px;
    padding: 12px;
    min-width: 48px;
    display: flex;
    /*-webkit-box-align: baseline;*/
    /*align-items: baseline;*/
    word-break: break-word;
    border: none;
}

.callout-panel p {
    margin-bottom: 0;
    line-height: 24px;
}

.callout-panel-icon {
    display: block;
    flex-shrink: 0;
    height: 24px;
    width: 24px;
    box-sizing: content-box;
    padding-right: 8px;
    color: rgb(0, 82, 204);
}

.callout-panel-note {
    background-color: rgb(234, 230, 255);
}

.callout-panel-note-icon {
    color: purple;
}


.callout-panel-info {
    background-color: rgb(222, 235, 255);
}

.callout-panel-info-icon {
    color: blue;
}

.callout-panel-warning {
    background-color: rgb(255, 250, 200);
}

.callout-panel-warning-icon {
    color: orange;
}

</style>
