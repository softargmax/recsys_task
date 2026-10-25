# Learned features, K = 16_s7

 0. count: rec_lp over 1.00 same artist, kernel 1.00 decay 1d
 1. count: rec_skip + org_lp + org_skip + ratio over 1.00 same album, kernel 1.00 last 3 tracks
 2. count: org_lp + ratio over 1.00 same album, kernel 1.00 last event, decay 30d
 3. count: nothing over 1.00 same album, kernel 1.00 decay 6h
 4. count: rec_skip + org_skip over 1.00 same artist, kernel 1.00 last event, decay 1d
 5. count: rec_lp + novel_lp over 1.00 cf-similar tracks, kernel 1.00 decay 1d
 6. count: rec_lp + novel_lp over 1.00 cf-similar tracks, kernel 1.00 decay 90d
 7. count: rec_skip over 1.00 any track, kernel 1.00 decay 1h
 8. rate: (rec_skip + org_lp + novel_skip) / (rec_lp + rec_skip + org_lp + ratio + novel_lp + novel_skip) over 1.00 same artist, kernel 1.00 decay 90d
 9. rate: (rec_lp + rec_skip + org_lp) / (rec_lp + rec_skip + org_lp + ratio + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 last 10 tracks
10. rate: (rec_lp + rec_skip + org_lp) / (rec_lp + rec_skip + org_lp + ratio + novel_lp) over 1.00 any track, kernel 1.00 last 10 tracks
11. rate: (rec_lp + ratio) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same track, kernel 1.00 all history
12. rate: (rec_skip + org_skip + ratio + novel_lp) / (rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 0.96 last event, decay 30d
13. rate: (rec_lp + rec_skip + org_lp + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 all history
14. rate: (rec_lp + org_skip + ratio + novel_lp + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same album, kernel 1.00 last 10 tracks
15. rate: (rec_lp + rec_skip + org_lp + org_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 last 3 tracks
