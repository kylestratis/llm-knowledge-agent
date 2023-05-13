from string import Template

obsidian_source_note_template = Template(
    """
---
publish: $publish
---

> [!META]- Inline Metadata
> [tags:: $tags]
> [author:: $author]
> [full title:: $title]
> [status:: $status]
> [link:: $link]

## Summary
$summary

## Outline
$outline
"""
)


obsidian_evergreen_note_template = Template(
    """
---
publish: $publish
---

> [!META]- Inline Metadata
> [status:: $status]
> [source:: $metadata_sources]
> [tags:: $tags]
> [up:: ]

$text

## Sources
$body_sources
    """
)