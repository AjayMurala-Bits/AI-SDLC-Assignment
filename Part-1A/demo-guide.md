# Part-1A Manual Demo Guide

This is a short demonstration of the implemented Movie Ticket Booking CLI.
Use a fresh temporary store so the demonstration does not affect any existing
data or evidence.

## Setup

Run from the Part-1A root in PowerShell. If needed, activate the project
environment first:

```powershell
& .\.venv\Scripts\Activate.ps1
```

Create and enter a fresh demo store, then set the source path:

```powershell
$demo = Join-Path (Get-Location) (".demo-store-" + (Get-Date -Format "yyyy-MM-ddTHH-mm-ss.fffzzz").Replace(":", "-"))
New-Item -ItemType Directory -Path $demo | Out-Null
$env:PYTHONPATH = (Join-Path (Get-Location) "src")
Set-Location $demo
```

## Command list and speaking notes

Run one command at a time.

1. Say: “I’m listing the two fixed shows.”

   ```powershell
   python -m movie_booking list-shows
   ```

   Expected output: `S1` and `S2`.

2. Say: “S1 starts with all ten seats available.”

   ```powershell
   python -m movie_booking view-seats S1
   ```

   Expected output: `A1 A2 A3 A4 A5 A6 A7 A8 A9 A10`.

3. Say: “I’m booking two seats; at INR 200 each, the total must be INR 400.”

   ```powershell
   python -m movie_booking book S1 A1 A2
   ```

   Expected output includes: `Booking 1`, `seats=A1, A2`, `total=INR 400`, and `status=active`.

4. Say: “This request overlaps A1 but also asks for free A3. The whole request must be rejected.”

   ```powershell
   python -m movie_booking book S1 A1 A3
   ```

   Expected result: an error stating that `A1` is already booked or unavailable.

5. Say: “Because the overlapping request was rejected atomically, A3 is still available.”

   ```powershell
   python -m movie_booking view-seats S1
   ```

   Expected result: A1 and A2 are unavailable, while A3 through A10 remain available.

6. Say: “The booking is persisted and can be viewed by its booking ID.”

   ```powershell
   python -m movie_booking view-booking 1
   ```

   Expected output: Booking 1 for S1, seats A1 and A2, total INR 400, status active.

7. Say: “I’m cancelling the booking.”

   ```powershell
   python -m movie_booking cancel 1
   ```

   Expected output: Booking 1 with `status=cancelled`.

8. Say: “The cancelled seats are released again.”

   ```powershell
   python -m movie_booking view-seats S1
   ```

   Expected output: `A1 A2 A3 A4 A5 A6 A7 A8 A9 A10`.

These are demonstration expectations only. Record personal observations or
acceptance separately; this guide does not create acceptance evidence.
