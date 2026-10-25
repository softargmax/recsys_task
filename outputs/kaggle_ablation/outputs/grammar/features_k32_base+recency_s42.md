# Learned features, K = 32_base+recency_s42

 0. count: rec_skip over 1.00 same track, kernel 1.00 all history
 1. count: rec_skip over 1.00 cf-similar tracks, kernel 1.00 last 10 tracks
 2. count: org_lp over 1.00 any track, kernel 1.00 decay 3d
 3. count: rec_skip + org_lp + org_skip over 1.00 same track, kernel 1.00 last 10 tracks
 4. count: rec_lp + rec_skip + org_skip over 1.00 same album, kernel 1.00 last event, decay 1d
 5. count: org_lp + org_skip over 1.00 any track, kernel 1.00 last track
 6. count: rec_lp over 1.00 same track, kernel 1.00 decay 90d
 7. count: rec_lp + rec_skip + org_lp + org_skip over 1.00 any track, kernel 1.00 last track
 8. count: nothing over 1.00 same track, kernel 1.00 decay 6h
 9. count: rec_lp + org_lp over 1.00 any track, kernel 1.00 last 3 tracks
10. count: rec_lp + org_lp over 1.00 same album, kernel 1.00 decay 3d
11. count: rec_skip over 1.00 cf-similar tracks, kernel 1.00 decay 3d
12. count: rec_lp + rec_skip over 1.00 same track, kernel 1.00 last 10 tracks
13. count: org_lp over 1.00 same track, kernel 1.00 decay 90d
14. count: nothing over 1.00 same track, kernel 1.00 decay 1h
15. count: nothing over 1.00 any track, kernel 1.00 decay 1d
16. rate: (rec_skip) / (rec_lp + rec_skip) over 1.00 any track, kernel 1.00 decay 1h
17. rate: (rec_lp) / (rec_lp + rec_skip) over 1.00 any track, kernel 1.00 decay 7d
18. rate: (rec_lp) / (rec_lp + rec_skip + org_skip) over 1.00 cf-similar tracks, kernel 1.00 all history
19. rate: (nothing) / (rec_skip) over 1.00 any track, kernel 1.00 last 3 tracks
20. rate: (nothing) / (rec_skip + org_skip) over 1.00 any track, kernel 1.00 decay 30d
21. rate: (nothing) / (rec_lp) over 1.00 cf-similar tracks, kernel 1.00 last 10 tracks
22. rate: (rec_skip + org_skip) / (rec_skip + org_skip) over 1.00 any track, kernel 1.00 all history
23. rate: (rec_skip) / (rec_lp + rec_skip + org_lp) over 1.00 any track, kernel 1.00 all history
24. rate: (rec_lp + org_lp) / (rec_lp + rec_skip + org_lp) over 1.00 cf-similar tracks, kernel 1.00 decay 6h
25. rate: (rec_skip) / (rec_skip + org_lp) over 1.00 cf-similar tracks, kernel 0.99 last event, decay 1d
26. rate: (nothing) / (rec_skip + org_lp) over 1.00 same album, kernel 1.00 decay 1d
27. rate: (rec_lp + rec_skip + org_lp + org_skip) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 same track, kernel 1.00 decay 1d
28. rate: (rec_lp + rec_skip + org_skip) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 any track, kernel 1.00 decay 6h
29. rate: (rec_lp + org_lp) / (rec_lp + org_lp) over 1.00 same artist, kernel 1.00 decay 1d
30. rate: (rec_skip + org_lp + org_skip) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 same album, kernel 1.00 last event, decay 1d
31. rate: (rec_skip + org_lp) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 any track, kernel 1.00 last event, decay 30d
