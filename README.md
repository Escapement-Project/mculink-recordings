# MCU-Link recordings

Logic analyser recordings of MCU-Link probes driving a target's debug pins, in
[tickwave](https://github.com/Escapement-Project/tickwave)'s format. The
[measurements page](https://escapement-project.github.io/measurements/) cites them: a figure in its
"On the wire" section opens the stretch of wire it comes from.

Each set is a folder named by the date of its measurements. A recording, `NAME.tickwave`, has its
annotations beside it. `NAME.annotations.toml` is written by hand and includes the files a decoder
writes, such as `NAME.wire_swd.jsonl`. A decoder rewrites its own file whole, so a hand edit never
gets lost. tickwave's viewer opens a recording from its URL or from disk, and its command line
describes one with `tickwave info NAME.tickwave`.

## 2026-11-04

The probe is an MCU-Link Pro running Verge, built with GCC at df11e14, or NXP's firmware V3.174.
SWD runs to an MSPM0L1306, JTAG and cJTAG to a CC1312R1. The analyser samples every 1 ns. Its
leads load the lines, so some reads sample a cycle later than they do without them, and the
throughput behind these recordings is not the page's: those runs had nothing on the lines.

| Recording | What it holds |
|---|---|
| `gcc-swd-reads` | Verge (GCC): 64 KiB flash reads at 50, 37.5, 30 and 10 MHz |
| `gcc-swd-reads-capture100000` | Verge (GCC): 64 KiB flash reads at 50, 37.5 and 30 MHz, capturing energy at 100,000 pairs/s |
| `stock-swd-reads` | NXP's firmware: 64 KiB flash reads at 10, 20, 25 and 50 MHz |
| `gcc-jtag-probe-rs` | Verge (GCC): probe-rs JTAG throughput |
| `gcc-jtag-capture100000` | Verge (GCC): probe-rs JTAG throughput, capturing energy at 100,000 pairs/s |
| `stock-jtag-probe-rs` | NXP's firmware: probe-rs JTAG throughput |
| `stock-reads` | NXP's firmware: 256 KiB JTAG reads at 1, 10, 20, 30 and 50 MHz |
| `gcc-oscan1-probe-rs` | Verge (GCC): probe-rs cJTAG OScan1 throughput |
| `gcc-oscan2-probe-rs` | Verge (GCC): probe-rs cJTAG OScan2 throughput |
| `gcc-oscan5-probe-rs` | Verge (GCC): probe-rs cJTAG OScan5 throughput |
| `gcc-oscan6-probe-rs` | Verge (GCC): probe-rs cJTAG OScan6 throughput |

The annotations come from three decoders. `wire_swd` finds each SWD transfer and marks an example of
each kind and clock with its phases, and the first few unusual acknowledges, read parity failures
and longer data periods, with how many there are. `wire_cjtag` marks example cJTAG frames by length.
`wire_clock` groups a clock's bursts by period. They live in mculink-bench's `tools/wire/`, and each
annotation file's first line names the decoder and the hash of the version that wrote it.

In the SWD reads, each session's annotation also states its figures as values: the clock asked for,
and the request, read data and write data clocks measured, in MHz. `wire-clock-request.chart.json`,
`wire-clock-read.chart.json` and `wire-clock-write.chart.json` chart them against the clock asked
for, in tickwave's chart format, and each point names the session it comes from. mculink-bench's
`tools/wire/wire_chart.py` writes them from the annotations.

## Licence

The recordings and their annotations are licensed under the Creative Commons Attribution 4.0
International licence (CC BY 4.0), in `LICENSE`. Credit the Escapement Project.
