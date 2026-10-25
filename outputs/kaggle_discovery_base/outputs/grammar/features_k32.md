# Learned features, K = 32

 0. count: rec_skip + org_skip over 1.00 any track, kernel 1.00 decay 1h
 1. count: rec_lp over 1.00 cf-similar tracks, kernel 1.00 decay 6h
 2. count: rec_lp over 1.00 any track, kernel 1.00 decay 3d
 3. count: rec_skip over 1.00 any track, kernel 1.00 decay 30d
 4. count: rec_lp + org_skip over 1.00 same album, kernel 1.00 last 10 tracks
 5. count: rec_lp over 1.00 same artist, kernel 1.00 decay 30d
 6. count: nothing over 1.00 same track, kernel 1.00 decay 1d
 7. count: rec_skip over 1.00 any track, kernel 1.00 all history
 8. count: rec_skip + org_lp over 1.00 same track, kernel 1.00 last track
 9. count: org_lp + org_skip over 1.00 any track, kernel 1.00 decay 6h
10. count: rec_skip over 1.00 same album, kernel 1.00 decay 30d
11. count: org_lp over 1.00 cf-similar tracks, kernel 1.00 last track
12. count: rec_lp over 1.00 same track, kernel 1.00 decay 6h
13. count: rec_lp + rec_skip + org_lp + org_skip over 1.00 same track, kernel 0.98 last track
14. count: org_lp over 1.00 same track, kernel 1.00 decay 30d
15. count: rec_lp over 1.00 same track, kernel 1.00 decay 30d
16. rate: (rec_lp) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 any track, kernel 1.00 last track
17. rate: (rec_skip + org_skip) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 any track, kernel 1.00 last track
18. rate: (rec_lp + org_lp) / (rec_lp + org_lp) over 1.00 cf-similar tracks, kernel 1.00 last 3 tracks
19. rate: (rec_lp + org_lp) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 any track, kernel 1.00 last 3 tracks
20. rate: (rec_skip + org_skip) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 any track, kernel 1.00 last 3 tracks
21. rate: (rec_skip) / (rec_skip + org_lp) over 1.00 cf-similar tracks, kernel 1.00 decay 6h
22. rate: (rec_lp) / (rec_lp + rec_skip) over 1.00 any track, kernel 1.00 decay 30d
23. rate: (rec_skip) / (rec_lp + rec_skip + org_lp) over 1.00 cf-similar tracks, kernel 1.00 last 10 tracks
24. rate: (rec_skip + org_skip) / (rec_lp + rec_skip + org_skip) over 1.00 cf-similar tracks, kernel 1.00 decay 90d
25. rate: (rec_lp + org_lp + org_skip) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 any track, kernel 1.00 last track
26. rate: (rec_skip) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 same album, kernel 1.00 all history
27. rate: (nothing) / (rec_lp) over 1.00 any track, kernel 1.00 decay 1h
28. rate: (rec_skip + org_skip) / (rec_lp + rec_skip + org_skip) over 1.00 same track, kernel 1.00 decay 30d
29. rate: (rec_skip + org_lp) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 any track, kernel 1.00 last 3 tracks
30. rate: (rec_skip + org_skip) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 same artist, kernel 1.00 decay 3d
31. rate: (rec_skip) / (rec_lp + rec_skip) over 1.00 any track, kernel 1.00 last 10 tracks
