File Outline:

To prepare the videos for classification, you must first run the video througb 2 separate programs:
1) demo.py --> To get the raw direction score with respect to the subject's head
2) body_detection.py --> To get the bounding boxes of each subject

Once you complete these program runs, you may run the classification.py to get the raw decision map on stares per 1/3 of a second

You may duration_graph.py to get a clear plot of the duration for each scenario
