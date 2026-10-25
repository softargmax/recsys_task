# Learned features, K = 16

 0. count: rec_skip + org_skip over 1.00 any track, kernel 1.00 last 3 tracks
 1. count: rec_skip over 1.00 cf-similar tracks, kernel 1.00 decay 1h
 2. count: rec_skip + org_lp + org_skip over 1.00 any track, kernel 1.00 last track
 3. count: nothing over 1.00 same track, kernel 1.00 decay 3d
 4. count: rec_skip over 1.00 cf-similar tracks, kernel 1.00 decay 90d
 5. count: rec_lp over 1.00 any track, kernel 1.00 decay 6h
 6. count: rec_lp + rec_skip + org_lp + org_skip over 1.00 same track, kernel 0.99 last track
 7. count: rec_skip over 1.00 any track, kernel 1.00 decay 7d
 8. rate: (rec_lp) / (rec_lp + rec_skip + org_skip) over 1.00 same track, kernel 1.00 decay 7d
 9. rate: (rec_skip + org_skip) / (rec_lp + rec_skip + org_skip) over 1.00 any track, kernel 1.00 decay 90d
10. rate: (rec_lp + rec_skip + org_lp + org_skip) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 same album, kernel 1.00 last 10 tracks
11. rate: (rec_lp + org_lp + org_skip) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 any track, kernel 1.00 last track
12. rate: (rec_lp) / (rec_lp) over 1.00 cf-similar tracks, kernel 1.00 all history
13. rate: (rec_skip) / (rec_skip) over 1.00 any track, kernel 1.00 last 10 tracks
14. rate: (rec_lp + org_lp) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 same track, kernel 1.00 decay 90d
15. rate: (rec_lp) / (rec_lp + org_lp) over 1.00 any track, kernel 1.00 last 10 tracks
