# CSS guide

This short guide explains the site's CSS structure and conventions.

## Where styles live

- Global SASS partials: `_sass/_variables.scss`, `_sass/_mixins.scss` — tokens and helpers.
- Component SCSS partials: `_sass/components/` — each component gets its own partial (e.g. `_referral-links-cards.scss`).
- The compiled stylesheet is `assets/css/style.scss`, which imports the token/mixin partials and components (in that order).

## Naming conventions

- Prefer component-scoped classes to avoid collisions. Example:
  - `.referral-card`, `.referral-card__illustration`, `.referral-card--light`.
- For legacy elements already widely used (e.g., `.project-card`) it's OK to continue, but prefer new components use a clear prefix.
- Keep selectors shallow — one or two levels deep.

## How to add a new component

1. Create `_sass/components/_your-component.scss`.
2. Add styles scoped to the new class, e.g. `.your-component { ... }`.
3. Import the component from `assets/css/style.scss` (maintain the order: tokens, mixins, components).
4. Use the component in your layout or include.

## Includes vs frontmatter

- Keep Markdown pages minimal: frontmatter and page content only. Use includes for repeated UI (we use `{% include referral_links.html %}` for project links).
- If a layout always shows a component, wire the include in the layout and let pages control behavior via frontmatter (e.g., `github_url`).

## Accessibility

- Use `aria` attributes as needed.
- Use the `visually-hidden` mixin for labels that should be hidden visually but available to screen readers.

## Build / Troubleshooting

- If Sass import errors occur, check the import path: `assets/css/style.scss` imports partials from `_sass` and `_sass/components`.
- Local build:

```bash
bundle install
bundle exec jekyll build
bundle exec jekyll serve
```

## Next steps

- Consider adding `stylelint` in CI and a small `htmlproofer` job to catch broken links.

If you'd like, I can automatically convert other portfolio/research pages to use `{% include referral_links.html %}`; say `yes` and I'll do it.
