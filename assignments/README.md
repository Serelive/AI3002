# Assignments

Create one `Axx-topic` directory per real assignment, then add it to the table in the root README. Start its README from `../templates/assignment/README.md`.

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
