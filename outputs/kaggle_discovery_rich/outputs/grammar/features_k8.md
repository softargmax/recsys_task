# Learned features, K = 8

 0. count: rec_lp + rec_skip + org_lp + org_skip + ratio over 1.00 any track, kernel 1.00 last 10 tracks
 1. count: rec_lp + novel_lp over 1.00 cf-similar tracks, kernel 1.00 decay 90d
 2. count: rec_skip + org_skip over 1.00 any track, kernel 1.00 decay 1h
 3. count: rec_lp over 1.00 same track, kernel 1.00 last 10 tracks
 4. rate: (rec_lp + rec_skip + org_lp + org_skip + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same album, kernel 1.00 decay 1d
 5. rate: (ratio) / (rec_skip + org_skip + ratio + novel_lp + novel_skip) over 1.00 same track, kernel 1.00 decay 30d
 6. rate: (ratio + novel_lp) / (rec_lp + rec_skip + org_lp + ratio + novel_lp + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 all history
 7. rate: (ratio) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 0.80 last event, decay 1d + 0.15 last 3 tracks
