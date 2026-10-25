# Learned features, K = 32_base+sess_s7

 0. count: nothing over 1.00 same artist, kernel 1.00 decay 1h
 1. count: rec_skip + org_skip over 1.00 same album, kernel 1.00 last 10 tracks
 2. count: rec_lp + org_lp over 1.00 same artist, kernel 1.00 last 10 tracks
 3. count: rec_lp + org_lp over 1.00 same album, kernel 1.00 decay 7d
 4. count: rec_lp + org_lp over 1.00 same track, kernel 1.00 last track
 5. count: rec_skip over 1.00 cf-similar tracks, kernel 1.00 decay 1d
 6. count: rec_lp over 1.00 cf-similar tracks, kernel 1.00 decay 3d
 7. count: rec_lp + org_lp over 1.00 any track, kernel 1.00 last 3 tracks
 8. count: nothing over 1.00 same artist, kernel 1.00 decay 6h
 9. count: rec_lp over 1.00 same track, kernel 1.00 all history
10. count: rec_skip over 1.00 any track, kernel 1.00 decay 30d
11. count: rec_lp + rec_skip + org_lp + org_skip over 1.00 any track, kernel 1.00 decay 1h
12. count: rec_lp over 1.00 same album, kernel 1.00 decay 1h
13. count: rec_skip + org_skip over 1.00 same artist, kernel 1.00 last track
14. count: rec_lp + org_lp over 1.00 same album, kernel 1.00 last 3 tracks
15. count: rec_lp over 1.00 cf-similar tracks, kernel 1.00 decay 7d
16. rate: (rec_skip + org_lp) / (rec_skip + org_lp + org_skip) over 1.00 cf-similar tracks, kernel 1.00 last track
17. rate: (rec_lp + rec_skip + org_lp + org_skip) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 same track, kernel 1.00 decay 1d
18. rate: (rec_skip) / (rec_lp + rec_skip + org_lp) over 1.00 any track, kernel 1.00 decay 1h
19. rate: (rec_lp) / (rec_lp) over 1.00 any track, kernel 1.00 decay 1h
20. rate: (rec_skip) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 cf-similar tracks, kernel 1.00 decay 6h
21. rate: (rec_skip) / (rec_skip + org_lp + org_skip) over 1.00 any track, kernel 1.00 decay 1d
22. rate: (rec_lp) / (rec_lp + rec_skip) over 1.00 any track, kernel 1.00 decay 90d
23. rate: (org_lp + org_skip) / (rec_skip + org_lp + org_skip) over 1.00 any track, kernel 1.00 last 3 tracks
24. rate: (rec_lp + org_lp) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 same track, kernel 1.00 decay 1d
25. rate: (rec_skip) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 any track, kernel 1.00 last track
26. rate: (rec_lp + org_lp) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 any track, kernel 1.00 last 10 tracks
27. rate: (rec_skip) / (rec_lp + rec_skip + org_lp) over 1.00 cf-similar tracks, kernel 1.00 last 10 tracks
28. rate: (rec_lp + rec_skip + org_lp + org_skip) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 same album, kernel 1.00 decay 1d
29. rate: (rec_skip) / (rec_lp + rec_skip) over 1.00 same album, kernel 1.00 decay 30d
30. rate: (rec_skip + org_lp + org_skip) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 any track, kernel 1.00 last track
31. rate: (rec_lp + org_lp) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 same track, kernel 1.00 decay 90d
