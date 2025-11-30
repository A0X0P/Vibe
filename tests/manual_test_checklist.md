# Manual Testing Checklist for MP3 Music Player

## Test Date: 30 November 2025 
## Tester: A.N. Prosper
## Version: 0.0.1

---

## Setup
- [ ] All required images are in Images/ folder
- [ ] At least 3 test MP3 files are available
- [ ] Python dependencies installed (`pip install -r requirements.txt`)
- [ ] Application launches without errors

---

## Playback Controls
- [ ] Play button starts music playback
- [ ] Pause button pauses music
- [ ] Resume works correctly after pause
- [ ] Next button advances to next song
- [ ] Previous button goes to previous song
- [ ] Next from last song wraps to first
- [ ] Previous from first song wraps to last
- [ ] Double-clicking controls doesn't cause issues

---

## Visual Feedback
- [ ] Play/pause button icon switches correctly
- [ ] Platter rotates smoothly when playing (no lag/stutter)
- [ ] Platter stops when paused
- [ ] Platter stops when song ends
- [ ] Needle moves to platter when playing starts
- [ ] Needle returns to rest when paused
- [ ] Needle returns to rest when song ends
- [ ] Needle animation is smooth (no jumps)

---

## Progress Slider
- [ ] Slider doesn't crash when no song loaded
- [ ] Dragging slider seeks to correct position
- [ ] Slider updates continuously during playback
- [ ] Slider reaches 100% at song end
- [ ] Left time (current position) updates in real-time
- [ ] Right time (total length) stays constant
- [ ] Both times format correctly (M:SS)
- [ ] Seeking near end of song works correctly
- [ ] Seeking to beginning works correctly
- [ ] Seeking while paused works correctly
- [ ] Can drag slider during playback

---

## Volume Slider
- [ ] Volume slider changes audio level
- [ ] Volume at 0 is silent
- [ ] Volume at 100 is maximum
- [ ] Volume persists across song changes
- [ ] Can adjust volume while paused
- [ ] Can adjust volume while stopped

---

## Loop Modes
- [ ] Loop button cycles through 3 states
- [ ] Loop Off: Song stops at end, shows play button
- [ ] Loop All: Next song plays automatically
- [ ] Loop One: Same song repeats indefinitely
- [ ] Loop icon updates correctly for each mode
- [ ] Loop button visual feedback works (press effect)
- [ ] Can change loop mode while playing
- [ ] Can change loop mode while stopped

---

## Playlist Management
- [ ] Add songs button opens file dialog
- [ ] Multiple MP3 files can be selected
- [ ] First song plays automatically after adding
- [ ] Song metadata displays correctly (title/artist)
- [ ] Songs without metadata show "Unknown"
- [ ] Long song titles scroll correctly
- [ ] Long artist names scroll correctly
- [ ] Scrolling text wraps around smoothly
- [ ] Can add new songs while playing (replaces playlist)

---

## Options Menu
- [ ] Ellipse button opens options menu
- [ ] Cancel button closes options menu
- [ ] Add songs works from options menu
- [ ] Menu overlay appears correctly
- [ ] Menu has rounded corners
- [ ] Can't interact with ellipse button when menu is open
- [ ] Menu overlay doesn't interfere with playback

---

## Edge Cases
- [ ] Empty playlist doesn't crash
- [ ] Clicking controls with no playlist doesn't crash
- [ ] Very short songs (< 10 seconds) work correctly
- [ ] Very long songs (> 10 minutes) work correctly
- [ ] Songs exactly 1 minute long display correctly
- [ ] Corrupted MP3 shows error gracefully (doesn't crash)
- [ ] MP3 without ID3 tags displays properly
- [ ] MP3 with very long title/artist names handled
- [ ] Rapid clicking doesn't cause issues
- [ ] Rapid slider dragging doesn't cause issues
- [ ] Window resize doesn't break layout (if resizable)
- [ ] Seeking to 0:00 works correctly
- [ ] Seeking to end of song works correctly

---

## Performance
- [ ] No lag or stuttering during playback
- [ ] Animations are smooth (60 FPS)
- [ ] UI remains responsive during song changes
- [ ] Memory usage stays reasonable over time
- [ ] No memory leaks after playing 10+ songs
- [ ] CPU usage is reasonable (< 5% when idle)

---

## User Experience
- [ ] All buttons have visible press effects
- [ ] Button hitboxes feel appropriate (not too small)
- [ ] Slider is easy to grab and drag
- [ ] Text is readable at all times
- [ ] No visual glitches or artifacts
- [ ] No console spam/excessive debug output
- [ ] Error messages are helpful (if any occur)

---

## Cross-Platform 
- [ ] Works on Windows
- [ ] Works on macOS
- [ ] Works on Linux
- [ ] File dialogs work on all platforms
- [ ] Paths handle both / and \ correctly

---

## Final Checks
- [ ] No console errors during normal operation
- [ ] All buttons respond to clicks
- [ ] All sliders respond to dragging
- [ ] Application closes cleanly (no hanging processes)
- [ ] No "pygame parachute" crashes
- [ ] Can restart application without issues

---

## Bugs Found
| # | Description | Severity | Steps to Reproduce|
|---|-------------|----------|-------------------|
| 1 |             |          |                   |
| 2 |             |          |                   |
---

## Notes
(Additional observations, suggestions, or comments)
under normal conditions the app works properly.