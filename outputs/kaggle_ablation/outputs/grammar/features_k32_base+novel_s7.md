# Learned features, K = 32_base+novel_s7

 0. count: rec_lp + org_lp + novel_lp over 1.00 same track, kernel 1.00 last track
 1. count: nothing over 1.00 same album, kernel 1.00 decay 1h
 2. count: rec_lp + novel_skip over 1.00 same artist, kernel 1.00 decay 6h
 3. count: org_skip + novel_lp over 1.00 same album, kernel 1.00 last 10 tracks
 4. count: rec_skip + novel_skip over 1.00 same artist, kernel 1.00 all history
 5. count: rec_lp + org_lp + novel_lp over 1.00 cf-similar tracks, kernel 1.00 decay 7d
 6. count: rec_lp + org_lp over 1.00 cf-similar tracks, kernel 1.00 last track
 7. count: rec_lp + novel_lp over 1.00 any track, kernel 1.00 last 10 tracks
 8. count: nothing over 1.00 same artist, kernel 1.00 decay 6h
 9. count: rec_lp + rec_skip + org_skip over 1.00 same track, kernel 1.00 last 10 tracks
10. count: rec_lp + org_lp + novel_lp over 1.00 any track, kernel 1.00 decay 90d
11. count: rec_lp + org_lp over 1.00 same track, kernel 1.00 decay 30d
12. count: rec_skip + novel_skip over 1.00 any track, kernel 1.00 all history
13. count: rec_lp over 1.00 same artist, kernel 1.00 decay 7d
14. count: rec_skip + novel_skip over 1.00 cf-similar tracks, kernel 1.00 all history
15. count: rec_lp + novel_lp + novel_skip over 1.00 cf-similar tracks, kernel 1.00 decay 6h
16. rate: (rec_lp + rec_skip + org_lp + org_skip + novel_lp) / (rec_lp + rec_skip + org_lp + org_skip + novel_lp + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 decay 6h
17. rate: (rec_lp + rec_skip + org_lp + org_skip + novel_lp + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + novel_lp + novel_skip) over 1.00 same track, kernel 1.00 last 3 tracks
18. rate: (rec_lp + org_lp) / (rec_lp + org_lp) over 1.00 any track, kernel 1.00 last 3 tracks
19. rate: (rec_skip) / (rec_skip + org_lp + org_skip + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 last 3 tracks
20. rate: (rec_lp + org_lp + org_skip + novel_lp) / (rec_lp + rec_skip + org_lp + org_skip + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 last track
21. rate: (rec_skip + novel_skip) / (rec_lp + rec_skip + org_lp + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 last 10 tracks
22. rate: (rec_skip + org_skip) / (rec_lp + rec_skip + org_skip + novel_lp) over 1.00 any track, kernel 1.00 decay 1h
23. rate: (novel_lp) / (rec_lp + rec_skip + org_lp + org_skip + novel_lp + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 decay 3d
24. rate: (rec_lp + org_lp) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 same track, kernel 1.00 all history
25. rate: (org_lp) / (rec_skip + org_lp + org_skip + novel_lp + novel_skip) over 1.00 same artist, kernel 1.00 decay 3d
26. rate: (rec_lp + novel_lp) / (rec_lp + rec_skip + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 decay 30d
27. rate: (rec_lp) / (rec_lp + rec_skip) over 1.00 cf-similar tracks, kernel 1.00 decay 1h
28. rate: (rec_lp) / (rec_lp + rec_skip + org_lp + org_skip + novel_skip) over 1.00 any track, kernel 1.00 last track
29. rate: (rec_skip + org_skip) / (rec_lp + rec_skip + org_lp + org_skip + novel_lp) over 1.00 same album, kernel 1.00 decay 7d
30. rate: (nothing) / (rec_skip + org_lp + org_skip + novel_skip) over 1.00 any track, kernel 1.00 decay 30d
31. rate: (rec_lp + novel_lp) / (rec_lp + rec_skip + org_lp + org_skip + novel_lp + novel_skip) over 1.00 same track, kernel 1.00 last 3 tracks
