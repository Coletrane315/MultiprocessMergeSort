This repository is a collection of Python scripts (all can be run independently) to compare the traditional merge-sort algorithm to a multiprocessing variant on NumPy arrays. 
mergeInPlace.py and mergeOutPlace.py run the traditional merge sort algorithm, in-place and out-of-place variants, and return execution times for various array sizes.
mergeOutPlaceMulti.py runs the multiprocessing variant of the merge-sort algorithm and returns execution times for various array sizes, additionally has a function to perform the ratio test 
  to confirm its rate of convergence.
mergeGetRatios.py performs the ratio test to confirm rate of convergence for the traditional out-of-place merge-sort.
mergeOutMultiFindIntcpt.py determines the array size for which the multiprocessing variant is faster than the traditional merge-sort.
This data is summarized in an Excel file, Writing3.xlsx, and incorporated into a written document for easier understanding, MergeSortMulti.docx
