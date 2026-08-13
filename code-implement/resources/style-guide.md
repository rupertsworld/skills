# Default style guide

Applies when the project doesn't have its own. A project style guide overrides this entirely.

Examples are written in TypeScript idiom; in another language, map each convention to that language's norms — the principles carry, the letter follows the language.

## Comments — generous and high-signal

Err on the side of more comments, not fewer. The bar is signal, not brevity:

- **Module headers.** Any non-trivial file opens with a short comment: what this module is, the model behind it, how its pieces relate. A reader should know whether they're in the right file without reading the code.
- **Why-comments with real context.** When code exists because of a constraint, gotcha, or non-obvious interaction, write it down properly — a few full sentences covering the situation, the reason, and what would break without it. One cryptic line that needs archaeology is worse than five clear ones.
- **Doc comments on every export.** At minimum a one-liner (`/** Thrown by TelevisionClient on transport failure. */`); full param/return docs when the signature alone doesn't carry it.
- **Section banners** to divide long files into named regions.
- What's still banned: narrating the obvious (`// increment counter`), commented-out code, and comments addressed to a reviewer rather than the next reader.

## Naming

- Descriptive, never abbreviated: `ResolvedCardPlacement`, not `RCP`. Functions are verbs, values are nouns, predicates read as questions (`isReady`, `hasTab`).
- Casing follows the language's norms (in TS: files kebab-case, functions/variables camelCase, types PascalCase, shared constants UPPER_CASE, file-local ones lowercase).
- Suffixes carry meaning or don't exist. Role suffixes describe a contract — a `Manager` owns a collection's lifecycle, a `Client` speaks a protocol, `*Event`/`*Error` mark what they are. Numbers carry their unit (`debounceMs`, `widthPx`). No decorative suffixes.

## Shape

- Idiomatic and vanilla wherever practicable. Lean on the language and platform before reaching for a dependency or framework; write the plain, conventional form of a thing before a clever one. New dependencies need to earn their place.
- Do things the proper way. Hold the line on implementation standards: sound, modular architecture — self-contained pieces with clear boundaries and one-direction dependencies, composed rather than entangled. No spaghetti, no shortcuts that smear responsibilities across layers. When a quick hack and a correct implementation diverge, build the correct one; if a workaround is genuinely unavoidable, comment why the proper way didn't work.
- A file is one thing. Internal order: imports, constants, types, main logic, helpers below. Tests colocate (`foo.ts` → `foo.test.ts`) unless the language's convention dictates otherwise. No barrel grab-bags.
- The simplest design that does the job: no speculative generality, no config for things that never vary, no abstraction with one caller built "for later".
- Smallest surface — export only what callers need.
- Match the surrounding code's idiom; consistency with the file beats personal preference.

## Types and data

- Explicit types on exported signatures; inference is fine internally. Prefer the language's safe unknown-data idiom over escape hatches (in TS: `unknown` plus type guards, never `any`).
- Validate at boundaries (HTTP, IPC, storage), trust types internally.
- Immutability by default: pure functions take state and return new state; mutation and side effects live at the edges, named so you can tell.
- Plain data and functions first. Classes only where state and behavior genuinely belong together (services, connections, components) — never as data holders.

## Errors

- Typed/named errors only for failures callers branch on; plain `Error` for the unexpected. Map them to the boundary's vocabulary (e.g. HTTP codes) in one place.
- Handle errors where something can be done about them; fail loudly, never swallow silently.

## Functions

- Early returns for guards; fail fast. Most functions fit in a screen.
- Extract a helper when a block needs a *what*-comment; inline an abstraction that wraps a single trivial call.
