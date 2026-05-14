import sys
# Pass arguments by calling `python pipeline.py arg1 arg2 etc`
print("arguments", sys.argv)

day = int(sys.argv[1])
print(f"Running pipeline for day {day}")