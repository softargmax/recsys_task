# Learned features, K = 16_s2024

 0. count: rec_skip over 1.00 cf-similar tracks, kernel 1.00 decay 30d
 1. count: rec_lp + ratio + novel_lp over 1.00 same track, kernel 1.00 last 3 tracks
 2. count: rec_lp + rec_skip + ratio + novel_lp over 1.00 any track, kernel 1.00 decay 1d
 3. count: rec_skip + org_skip over 1.00 any track, kernel 1.00 decay 1h
 4. count: org_lp + org_skip over 1.00 same track, kernel 1.00 last 3 tracks
 5. count: rec_lp over 1.00 same track, kernel 1.00 decay 90d
 6. count: nothing over 1.00 same artist, kernel 1.00 decay 1h
 7. count: rec_lp + org_skip + novel_lp over 1.00 same track, kernel 1.00 last event, decay 1d
 8. rate: (org_lp) / (rec_lp + org_lp + ratio + novel_lp) over 1.00 any track, kernel 1.00 last 10 tracks
 9. rate: (rec_lp + rec_skip + org_lp) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 last 3 tracks
10. rate: (org_lp + org_skip + ratio + novel_skip) / (rec_skip + org_lp + org_skip + ratio + novel_skip) over 1.00 any track, kernel 1.00 last event, decay 30d
11. rate: (rec_lp + novel_lp) / (rec_lp + rec_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 decay 7d
12. rate: (org_skip + ratio + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 last 10 tracks
13. rate: (rec_lp + rec_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same artist, kernel 1.00 decay 1h
14. rate: (rec_lp + rec_skip + org_lp + org_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_skip) over 0.99 cf-similar tracks, kernel 0.98 last event, decay 30d
15. rate: (rec_skip + ratio + novel_skip) / (rec_skip + org_lp + org_skip + ratio + novel_skip) over 1.00 any track, kernel 1.00 last event, decay 30d
