# Local inputs and recovery

The supplied Lab 1 archive, datasets, and instructor PDFs are intentionally ignored. Keep a separate backup: a fresh clone of the latest commit does not contain these inputs. This cleanup retains the existing local copies and does not erase older Git history.

The course source is recorded in the assignment README. The exact download URL and upstream revision of the supplied archive were not recorded; do not assume a newer download is identical. `input-checksums.sha256` identifies the local copies verified on October 11, 2026. All 16 dataset files and `docs/instruction.pdf` were checked byte-for-byte against the corresponding entries in `backups/LAB1.zip`.

To restore on another computer, obtain the matching `LAB1.zip` and `HW1-26.pdf` from your separate backup or course materials and place them in `assignments/labs/lab1/backups/`. From the repository root, extract into a temporary directory so that instructor starter code cannot overwrite your implementation:

```bash
unzip assignments/labs/lab1/backups/LAB1.zip -d /tmp/ai3002-lab1-inputs
```

Use an empty temporary destination. Copy its `LAB1/datasets/` directory to `../scr`. Copy `LAB1/README.pdf` to both `assignments/labs/lab1/docs/instruction.pdf` and `assignments/labs/lab1/backups/LAB1.pdf`. Restore the supporting homework PDF at both `assignments/labs/lab1/backups/HW1-26.pdf` and `assignments/homeworks/hw1/docs/HW1-26.pdf`. Create missing destination directories first. Do not overwrite existing inputs without checking their identity.

Verify from the repository root:

```bash
sha256sum -c assignments/labs/lab1/docs/input-checksums.sha256
```

Every entry should report `OK`. A mismatch means the restored input differs; investigate before comparing experiment results. The duplicated PDF copies are retained locally to preserve existing paths, but none is tracked in the new snapshot.

Report intermediates and `report/report.template.pdf` are ignored. Keep the `.tex` source tracked, and place deliberately selected final deliverables in `submission/`. The output-directory ignore rules do not exclude `submission/`.
