# Assignments

Current coursework uses `labs/lab1/` and `homeworks/hw1/`. Keep these established paths. Lab 1 is the active implementation workspace; see its [README](labs/lab1/README.md) and the [HPC handoff](../docs/HPC.md).

For a new assignment, use its course identifier or an `Axx-topic` directory and add it to the root README. Start its README from `../templates/assignment/README.md`.

Create only the subdirectories the assignment needs:

```text
assignments/A01-topic/
  README.md
  prompt/       # Original instructions; ignored by Git
  data/         # Immutable assignment inputs; ignored by Git
  work/         # Scripts, notebooks, and report sources
  output/       # Reproducible generated artifacts; ignored by Git
  submission/   # Deliberately selected final deliverables
```

An assignment may use code from `src/course_utils/`, but it must not import code from another assignment directory.
