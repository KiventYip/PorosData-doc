# PorosData-Processor

## Positioning

`Processor` is the quality-preparation module in PorosData. It does not create the final structured delivery package. Instead, it turns upstream parser outputs into cleaner, more stable intermediate data that downstream workflows can trust.

In short:

- `Processor` answers whether the source content is clean and stable enough to keep moving
- `Designer` answers how that content should be organized into final deliverables
{: .tight-list}

## What It Handles

`Processor` is designed for recurring issues such as:
{: .section-intro}

- OCR noise, broken spacing, and fragmented numbers
- Corrupted terms, material names, units, and chemical expressions
- Noisy captions, table titles, and footnotes
- Citation, formula, and context boundaries that became unstable after parsing
{: .tight-list}

## Inputs and Outputs

### Typical Inputs

`Processor` usually works from upstream parser results such as:
{: .section-intro}

- body text blocks
- figure captions and table titles
- image-related metadata
- content-list style files such as `*_content_list.json`
{: .tight-list}

### Typical Outputs

Standard outputs are usually written to `data/processed/`, including:
{: .section-intro}

- cleaned content lists
- reusable copies of image assets
- a batch report such as `processing_report.json`
- review-oriented quality checks and suspicious-pattern clues
{: .tight-list}

This layer is still an intermediate stage, but it strongly determines how reliable later structured outputs will be.

## What Users Gain

After `Processor`, users typically get:
{: .section-intro}

- clearer numbers, units, and formula boundaries
- more stable terms and material names
- captions and footnotes that are easier to extract from
- text that is better suited for training, retrieval, and rule-based processing
{: .tight-list}

## Scope of Cleaning

`Processor` is not limited to main body text. It also covers key metadata fields such as:
{: .section-intro}

- `text`
- `image_caption`
- `image_footnote`
- `table_caption`
- `table_footnote`
{: .tight-list}

This helps keep the main text and figure-related content under the same quality standard before the next stage.

## Typical Repairs

| Type | Common Problem | Target Result |
|------|------|------|
| Numerical repair | `0 . 0 1 0 n m` | `0.010nm` |
| Element repair | `N i` | `Ni` |
| Line-break repair | `110 \\n s` | `110s` |
| Term normalization | `Zr based` / `Zr-based` | keep one stable form within the document |
| Citation normalization | `[2,3]`, `[1-3]` | normalize into one stable protocol |

## Runtime and Deployment Guidance

### Recommended Environment

- Linux is preferred for long-running batch jobs
- Python `3.8+`
- SSD or NVMe is recommended for routine batch runs
- No GPU is required
{: .tight-list}

### Reference Sizing

| Scenario | Suggested Setup |
|------|------|
| Small validation | 4 vCPU / 16 GB RAM |
| Routine batch processing | 8 vCPU / 32 GB RAM |
| Large long-running jobs | 16 vCPU / 64 GB RAM |

### Usage Recommendations

- Prioritize stability for routine batch cleaning
- Run extra evaluation features separately when needed for spot checks or audits
- Reduce concurrency when many very long documents are involved
{: .tight-list}

## Runtime Expectations

`Processor` is typically CPU-bound. Overall runtime is mostly affected by:
{: .section-intro}

- document length and formula complexity
- worker count
- optional evaluation features
- whether the environment is Windows or Linux
{: .tight-list}

If logs continue to show progress and reports keep updating, the job is usually still healthy even when a few files take longer than expected.

## Review and Acceptance Loop

For external delivery projects, `Processor` should support more than one cleaning pass. A practical quality loop looks like this:
{: .section-intro}

1. run the batch and produce standard intermediate outputs
2. review the outputs and identify suspicious patterns or residual issues
3. improve the correction strategy for recurring problems
4. rerun and review again until the results are stable enough for delivery
{: .tight-list}

This makes the product easier to use in real delivery scenarios and helps reduce repeated noise over time.

## Known Boundaries

When using `Processor`, keep in mind:
{: .section-intro}

- it does not build the final structured schema
- it does not replace business-level field design
- for highly complex formulas or layouts, it favors structural safety over aggressive rewriting
{: .tight-list}

## Relationship with `Designer`

The more stable the `Processor` output is, the more reliable the `Designer` delivery becomes. It should be treated as the quality gate of the delivery chain, not as the final product layer.