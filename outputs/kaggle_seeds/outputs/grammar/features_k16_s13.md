# Learned features, K = 16_s13

 0. count: rec_lp + rec_skip + org_skip + novel_lp + novel_skip over 1.00 same artist, kernel 1.00 decay 3d
 1. count: rec_lp + novel_lp over 1.00 cf-similar tracks, kernel 1.00 decay 90d
 2. count: rec_skip + novel_skip over 1.00 any track, kernel 1.00 decay 7d
 3. count: novel_lp over 1.00 any track, kernel 1.00 decay 7d
 4. count: rec_lp + rec_skip + novel_lp over 1.00 same artist, kernel 1.00 last 3 tracks
 5. count: rec_skip over 1.00 cf-similar tracks, kernel 1.00 all history
 6. count: rec_lp + rec_skip + org_skip over 1.00 same album, kernel 1.00 last event, decay 30d
 7. count: rec_lp over 1.00 same album, kernel 1.00 current session
 8. rate: (nothing) / (rec_lp + ratio + novel_lp) over 1.00 any track, kernel 1.00 decay 1h
 9. rate: (rec_lp + rec_skip + org_lp) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_skip) over 1.00 same artist, kernel 1.00 last event, decay 1d
10. rate: (ratio) / (rec_skip + org_lp + org_skip + ratio + novel_skip) over 1.00 any track, kernel 1.00 last event, decay 1d
11. rate: (rec_lp + ratio) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp) over 1.00 same album, kernel 1.00 decay 90d
12. rate: (rec_lp + rec_skip + org_lp) / (rec_lp + rec_skip + org_lp + ratio) over 1.00 cf-similar tracks, kernel 1.00 decay 1h
13. rate: (ratio + novel_lp) / (rec_lp + rec_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 last 10 tracks
14. rate: (ratio) / (rec_lp + rec_skip + org_lp + org_skip + ratio) over 1.00 any track, kernel 1.00 last 3 tracks
15. rate: (rec_lp + ratio) / (rec_lp + rec_skip + ratio + novel_lp) over 1.00 same artist, kernel 1.00 decay 3d
