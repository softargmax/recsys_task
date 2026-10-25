# Learned features, K = 32_base+recency_s7

 0. count: nothing over 1.00 same artist, kernel 1.00 decay 6h
 1. count: rec_lp over 1.00 any track, kernel 1.00 all history
 2. count: rec_lp + rec_skip + org_skip over 1.00 same album, kernel 1.00 last track
 3. count: rec_skip + org_skip over 1.00 any track, kernel 1.00 decay 1h
 4. count: rec_lp over 1.00 any track, kernel 1.00 decay 7d
 5. count: rec_skip over 1.00 cf-similar tracks, kernel 1.00 decay 1h
 6. count: rec_lp + rec_skip over 1.00 cf-similar tracks, kernel 1.00 decay 7d
 7. count: org_lp + org_skip over 1.00 any track, kernel 1.00 all history
 8. count: rec_lp + rec_skip + org_lp + org_skip over 1.00 same track, kernel 1.00 decay 90d
 9. count: rec_lp + org_lp over 1.00 same track, kernel 0.99 last 3 tracks
10. count: rec_skip over 1.00 cf-similar tracks, kernel 1.00 decay 3d
11. count: nothing over 1.00 same track, kernel 1.00 decay 7d
12. count: rec_skip over 1.00 any track, kernel 1.00 decay 90d
13. count: rec_lp + rec_skip over 1.00 same artist, kernel 1.00 last event, decay 30d
14. count: rec_lp + org_lp over 1.00 cf-similar tracks, kernel 1.00 decay 3d
15. count: rec_lp over 1.00 cf-similar tracks, kernel 1.00 decay 1h
16. rate: (rec_lp + org_lp) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 cf-similar tracks, kernel 1.00 decay 30d
17. rate: (rec_skip) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 same artist, kernel 1.00 last event, decay 30d
18. rate: (rec_lp + org_lp) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 any track, kernel 1.00 last event, decay 1d
19. rate: (rec_skip + org_lp) / (rec_lp + rec_skip + org_lp) over 1.00 any track, kernel 1.00 last event, decay 30d
20. rate: (org_lp) / (rec_skip + org_lp + org_skip) over 1.00 same track, kernel 1.00 decay 30d
21. rate: (rec_skip + org_skip) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 any track, kernel 1.00 last 3 tracks
22. rate: (rec_skip + org_skip) / (rec_skip + org_skip) over 1.00 any track, kernel 1.00 decay 30d
23. rate: (rec_lp) / (rec_lp) over 1.00 cf-similar tracks, kernel 1.00 decay 90d
24. rate: (rec_lp) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 same track, kernel 1.00 decay 3d
25. rate: (rec_skip) / (rec_skip) over 1.00 any track, kernel 1.00 last 3 tracks
26. rate: (nothing) / (rec_lp) over 1.00 any track, kernel 1.00 decay 1h
27. rate: (rec_skip) / (rec_lp + rec_skip) over 1.00 same track, kernel 1.00 decay 90d
28. rate: (nothing) / (rec_skip + org_lp + org_skip) over 1.00 cf-similar tracks, kernel 1.00 decay 1d
29. rate: (rec_skip + org_skip) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 same album, kernel 1.00 all history
30. rate: (rec_skip) / (rec_skip) over 1.00 any track, kernel 1.00 last 10 tracks
31. rate: (rec_skip + org_skip) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 any track, kernel 1.00 decay 90d
