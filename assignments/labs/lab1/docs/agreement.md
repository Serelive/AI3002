# Agreement

## Program Stage
We use "phase" and "increment" to name a specific period of program. 
For convenience, 
use `f"p{x:02d}` for phase x, use `f"p{y:02d}"` for increment y. 
These are merely lightweight markers, 
not strict partitions of project stages. 

## Documentation

### Directory structure
In the documentation folder structure, 
we only organize directories at the phase level, 
without dedicated folders for the increment level. 

### Naming
Use `[<scope>_]<type>[-rNN][_<keywords>].md` to name a document. 
For example, in "ms_quickguide.md", type is "ms", and the keyword is "quickguide". 

- scope
  - pNN-iNN: phase NN, increment NN
  - pNN: phase NN, global in phase, valid for all its increments
  - NULL: global, valid for all phases and increments
- type
  - plan
  - reference
  - roadmap
  - agreement
  - review: Used only when an independent review is implemented. 
- keywords: More than two keywords should be linked with "-".
- `[-rNN]`: Used only when an existing file is reviewed. A review for an independent review should be like "review-r01", and a review for that should be like "review-r02"

### Version control
Use git rather than the name of file to control version. When a new file is created or validly modified, add it to git and commit once. 

## About the Lab
There are 3 tasks in lab1.
When I use "task 1", "task1", "Task1" or "Task 1", 
I refer to the first task in lab 1.
