# Learned features, K = 32_base+sess_s42

 0. count: rec_skip over 1.00 any track, kernel 1.00 decay 90d
 1. count: rec_skip + org_skip over 1.00 cf-similar tracks, kernel 1.00 current session
 2. count: rec_lp over 1.00 any track, kernel 1.00 decay 7d
 3. count: nothing over 1.00 same track, kernel 1.00 decay 6h
 4. count: rec_lp + rec_skip + org_lp + org_skip over 1.00 same track, kernel 1.00 all history
 5. count: rec_lp + org_lp + org_skip over 1.00 any track, kernel 1.00 current session
 6. count: rec_lp + org_lp over 1.00 same track, kernel 1.00 last track
 7. count: rec_lp + org_skip over 1.00 any track, kernel 1.00 current session
 8. count: rec_lp over 1.00 same track, kernel 1.00 decay 90d
 9. count: rec_skip + org_lp + org_skip over 1.00 any track, kernel 1.00 last 3 tracks
10. count: rec_lp + org_lp + org_skip over 1.00 same album, kernel 1.00 last 3 tracks
11. count: rec_skip over 1.00 cf-similar tracks, kernel 1.00 decay 1h
12. count: rec_lp over 1.00 same track, kernel 1.00 last 10 tracks
13. count: rec_skip over 1.00 same track, kernel 1.00 decay 1d
14. count: rec_skip + org_lp + org_skip over 1.00 same track, kernel 1.00 decay 90d
15. count: rec_lp over 1.00 same track, kernel 1.00 decay 6h
16. rate: (rec_skip) / (rec_lp + rec_skip) over 0.90 any track + 0.10 cf-similar tracks, kernel 1.00 decay 30d
17. rate: (nothing) / (rec_lp + rec_skip + org_skip) over 1.00 any track, kernel 1.00 current session
18. rate: (rec_skip + org_skip) / (rec_lp + rec_skip + org_skip) over 1.00 cf-similar tracks, kernel 1.00 current session
19. rate: (rec_skip + org_skip) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 any track, kernel 1.00 last track
20. rate: (rec_skip) / (rec_lp + rec_skip) over 1.00 any track, kernel 1.00 decay 1h
21. rate: (nothing) / (rec_lp + org_lp) over 1.00 any track, kernel 1.00 decay 1h
22. rate: (org_lp) / (rec_lp + org_lp + org_skip) over 1.00 same album, kernel 1.00 all history
23. rate: (nothing) / (rec_lp) over 1.00 any track, kernel 1.00 last 10 tracks
24. rate: (nothing) / (rec_lp + org_lp) over 1.00 cf-similar tracks, kernel 1.00 last 3 tracks
25. rate: (rec_lp + org_lp) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 same album, kernel 1.00 decay 30d
26. rate: (rec_lp + rec_skip + org_skip) / (rec_lp + rec_skip + org_skip) over 1.00 same album, kernel 1.00 decay 1h
27. rate: (rec_lp + org_lp) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 any track, kernel 1.00 decay 90d
28. rate: (rec_lp + org_lp) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 same track, kernel 1.00 all history
29. rate: (rec_skip) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 any track, kernel 1.00 last 3 tracks
30. rate: (rec_skip + org_skip) / (rec_skip + org_skip) over 1.00 same album, kernel 1.00 decay 90d
31. rate: (rec_skip) / (rec_skip) over 1.00 any track, kernel 1.00 last 10 tracks
