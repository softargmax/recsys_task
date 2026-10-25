# Learned features, K = 8

 0. count: rec_skip + org_skip over 1.00 any track, kernel 0.97 last 10 tracks
 1. count: rec_lp + org_lp over 1.00 cf-similar tracks, kernel 1.00 last 3 tracks
 2. count: rec_skip over 1.00 any track, kernel 1.00 last 10 tracks
 3. count: rec_skip over 1.00 any track, kernel 1.00 decay 90d
 4. rate: (rec_lp + rec_skip + org_lp + org_skip) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 same album, kernel 0.99 last track
 5. rate: (nothing) / (rec_lp + rec_skip + org_lp) over 1.00 same track, kernel 1.00 decay 7d
 6. rate: (rec_lp) / (rec_lp + rec_skip) over 0.42 any track + 0.32 same track + 0.26 cf-similar tracks, kernel 1.00 decay 30d
 7. rate: (rec_lp + org_lp) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 any track, kernel 0.50 last 3 tracks + 0.50 last track
