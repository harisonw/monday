# AI Meta-Process Notes

These notes summarize how external AI assistants were used while building the Crestview onboarding POC and presentation materials. The goal was not to outsource judgment, but to move faster while keeping the work explainable, reviewable, and aligned with the task requirements.

## How AI Was Used

- I first read the task manually to form my own understanding of the objective, constraints, and deliverables.
- I then used AI to validate that understanding and to help me structure the work into a practical plan.
- After reviewing that plan, I made changes manually and then used AI again to refine the plan until it matched the way I wanted to execute the project.
- I scaffolded the project structure myself, then used AI to generate most of the implementation code.
- Because this was a POC, I reviewed the code at a high level instead of doing a line-by-line manual rewrite, and I asked AI to produce supporting Markdown notes so I could review the result faster.
- I used AI for architecture discussions to compare implementation options and identify tradeoffs before settling on the final approach.
- I also used AI to generate PowerPoint-style presentation material more quickly, then edited that output manually.
- Speech-to-text tools were used heavily to speed up prompting and preserve more of the reasoning context during interaction.

## Prompt Iteration Pattern

The workflow was usually:

1. State the goal in plain language.
2. Ask AI to restate the task or propose a plan.
3. Review the response against the actual requirements.
4. Correct any missing constraints, sequencing issues, or scope creep.
5. Re-run the prompt with tighter instructions.
6. Use the improved output as a draft, not a final authority.

This made the interaction more like collaborative drafting than automatic generation.

## Examples of Iteration and Correction

### Planning

- AI helped convert the task into a phased execution plan.
- The first pass did not always reflect the exact order I wanted, so I adjusted the plan manually and then had AI revise it.
- When the plan drifted from my intent, I used plan-mode style prompting and direct clarification questions to realign the output.

### Architecture

- I used AI to discuss different architectural approaches for the onboarding pipeline.
- Some proposed directions were too abstract or not aligned with the POC scope, so I narrowed the discussion to the simplest workable design.
- The final approach favored clarity, sequential processing, and easy explainability over complexity.

### Code Generation

- AI wrote most of the code after the project was scaffolded.
- I reviewed the output at a structural level to confirm it matched the intended flow.
- When the generated code was too broad, I redirected it toward the specific POC requirements and the monday.com integration path.

### Presentation Material

- I initially used Gemini to help generate PowerPoint content.
- The first output was not strong enough, so I switched to the Anthropic PowerPoint skill inside Anti-Gravity and used a different model path.
- That produced better slides, which I then edited manually to improve fit, clarity, and executive tone.

## Where AI Fell Short

- Some responses did not stay tightly aligned to the plan, especially when the prompt was broad.
- Early presentation output was generic and needed a second pass before it was usable.
- In a few cases, AI was too eager to expand scope instead of staying inside the POC boundaries.
- Some architecture suggestions were useful as discussion material but not suitable as final decisions.

## Human Course-Corrections

- I kept the task framing anchored to the business problem and deliverables instead of letting the tool wander.
- I manually reviewed and edited the plan before moving into implementation.
- I chose the simplest viable architecture rather than the most elaborate one.
- I asked for Markdown summaries to speed up review, but still made the final judgment myself.
- I changed tools when the first one did not produce the quality level I needed.
- I used AI output as a draft layer and applied manual judgment to anything customer-facing or presentation-facing.

## How Output Quality Was Evaluated

I checked AI output against a few concrete criteria:

- Does it match the task requirements exactly?
- Is it sequential and operationally coherent?
- Does it explain the compliance and risk logic clearly?
- Is it concise enough for an executive or demo context?
- Does it reduce review time without hiding important mistakes?
- Can I defend the result if someone asks why this approach was chosen?

If the answer to any of those was weak, I revised the prompt or edited the output directly.

## Summary

AI was used as an accelerator for planning, coding, architecture discussion, documentation, and presentation drafting. The final work still depended on human review, correction, and judgment, especially where the output needed to be precise, defensible, or executive-ready.
