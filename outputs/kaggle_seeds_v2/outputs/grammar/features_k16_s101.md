# Learned features, K = 16_s101

 0. count: rec_lp + novel_lp over 1.00 same album, kernel 1.00 decay 1d
 1. count: rec_skip + org_lp + org_skip over 1.00 any track, kernel 1.00 last event, decay 1d
 2. count: nothing over 1.00 same track, kernel 1.00 decay 6h
 3. count: rec_lp + rec_skip + org_lp + org_skip over 0.99 any track, kernel 1.00 last 3 tracks
 4. count: rec_skip over 1.00 any track, kernel 1.00 decay 7d
 5. count: rec_lp + rec_skip + org_skip + novel_lp over 1.00 same album, kernel 1.00 last event, decay 1d
 6. count: rec_lp + novel_lp over 1.00 any track, kernel 1.00 decay 1d
 7. count: rec_lp + novel_lp over 1.00 same artist, kernel 1.00 decay 30d
 8. rate: (ratio) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 last 3 tracks
 9. rate: (rec_lp + org_lp + org_skip + ratio) / (rec_lp + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same track, kernel 1.00 last event, decay 30d
10. rate: (rec_lp + rec_skip + org_lp + org_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp) over 1.00 cf-similar tracks, kernel 1.00 decay 1h
11. rate: (rec_lp + ratio + novel_lp + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same track, kernel 1.00 all history
12. rate: (rec_lp + rec_skip + org_lp) / (rec_lp + rec_skip + org_lp + ratio + novel_skip) over 1.00 same album, kernel 1.00 decay 7d
13. rate: (rec_lp + rec_skip + novel_skip) / (rec_lp + rec_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 decay 30d
14. rate: (rec_skip + org_skip + ratio) / (rec_skip + org_lp + org_skip + ratio + novel_skip) over 1.00 any track, kernel 1.00 last event, decay 1d
15. rate: (rec_lp + ratio + novel_lp) / (rec_lp + rec_skip + ratio + novel_lp) over 1.00 any track, kernel 1.00 last 10 tracks
