# Learned features, K = 32_rich-sess_s42

 0. count: rec_skip over 1.00 any track, kernel 1.00 all history
 1. count: rec_lp + novel_lp over 1.00 cf-similar tracks, kernel 1.00 last 10 tracks
 2. count: org_skip + ratio over 1.00 any track, kernel 1.00 last 10 tracks
 3. count: rec_skip + org_skip over 1.00 same track, kernel 1.00 last 10 tracks
 4. count: rec_lp + rec_skip + org_lp + org_skip + novel_lp over 1.00 same album, kernel 1.00 last event, decay 1d
 5. count: rec_lp + novel_lp over 1.00 any track, kernel 1.00 decay 3d
 6. count: rec_lp + rec_skip + org_lp + ratio over 1.00 same track, kernel 1.00 decay 90d
 7. count: rec_lp + org_lp + ratio over 1.00 same track, kernel 1.00 last 3 tracks
 8. count: nothing over 1.00 same track, kernel 1.00 decay 6h
 9. count: rec_skip + org_skip + ratio over 1.00 any track, kernel 1.00 last event, decay 1d
10. count: org_lp + org_skip + novel_skip over 1.00 same album, kernel 1.00 decay 3d
11. count: novel_lp over 1.00 cf-similar tracks, kernel 1.00 decay 3d
12. count: rec_skip + org_skip + novel_skip over 1.00 cf-similar tracks, kernel 1.00 decay 3d
13. count: rec_lp over 1.00 same track, kernel 1.00 decay 7d
14. count: rec_lp + ratio over 1.00 same track, kernel 1.00 decay 1h
15. count: rec_lp + rec_skip + org_skip + ratio over 1.00 any track, kernel 1.00 decay 1d
16. rate: (rec_lp + rec_skip + org_lp + org_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp) over 0.95 cf-similar tracks, kernel 1.00 decay 1h
17. rate: (rec_lp + ratio) / (rec_lp + rec_skip + org_skip + ratio + novel_skip) over 1.00 same album, kernel 1.00 decay 7d
18. rate: (rec_lp + ratio + novel_lp) / (rec_lp + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 all history
19. rate: (ratio) / (rec_lp + rec_skip + org_lp + org_skip + ratio) over 1.00 any track, kernel 1.00 last 3 tracks
20. rate: (rec_skip + org_skip + ratio + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 decay 30d
21. rate: (rec_lp + org_lp + org_skip + ratio) / (rec_lp + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same track, kernel 1.00 last event, decay 30d
22. rate: (rec_skip + org_lp) / (rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 all history
23. rate: (ratio) / (rec_skip + org_skip + ratio) over 1.00 same track, kernel 1.00 all history
24. rate: (ratio + novel_lp) / (rec_lp + rec_skip + org_skip + ratio + novel_lp) over 1.00 cf-similar tracks, kernel 1.00 decay 3d
25. rate: (rec_skip) / (rec_lp + rec_skip + org_skip + ratio + novel_lp + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 last event, decay 1d
26. rate: (rec_skip + ratio + novel_skip) / (rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same album, kernel 1.00 decay 1d
27. rate: (org_lp + org_skip) / (rec_skip + org_lp + org_skip + ratio + novel_skip) over 1.00 any track, kernel 1.00 last event, decay 30d
28. rate: (ratio + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_skip) over 1.00 same track, kernel 1.00 decay 30d
29. rate: (rec_lp + ratio) / (rec_lp + rec_skip + org_lp + ratio + novel_lp + novel_skip) over 1.00 same artist, kernel 1.00 decay 1d
30. rate: (rec_lp + ratio + novel_lp) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same album, kernel 1.00 last event, decay 1d
31. rate: (org_lp + ratio + novel_lp) / (rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 last event, decay 30d
