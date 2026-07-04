# Atelier — code-native representational illustration

A pipeline for illustrating scenes without diffusion models: **sculpt** subjects from code
(mesh primitives, metaball clay, parametric MakeHuman bodies with a real wardrobe), **stage**
them into scenes by relation (placement, attention, light, camera), **paint** the rendered
G-buffers with twelve subject-aware style engines — every step iterated with vision over the
rendered output. Born inside [generative-arcana](https://github.com/mbilokonsky/generative-arcana)
to illustrate tarot decks; extracted along the seam its own control plane predicted.

- **[PRINCIPLES.md](./PRINCIPLES.md)** — the method, distilled so any model with vision over
  its own output can follow it. Includes the Expert Witness Test.
- **[CONTROL_PLANE.md](./CONTROL_PLANE.md)** — the formal contract between layers: the
  sculptor's info-dict, the G-buffer schema, and the **direction plane** — knobs, bindings,
  axes, buffers, stock — that lets semantic art direction drive any engine.

## Install

The painter (pure Python: numpy + Pillow) installs as a command:

```bash
uv tool install git+https://github.com/mbilokonsky/atelier     # or: pipx install git+...
atelier bindings                                               # every engine's knob table
atelier paint render.png aux.npz comic out.png 11 focus=0.7 palette="core:8a93a0;accent:5b8fd9"
```

The 3D side (Blender scenes, MPFB parametric humans, the MakeHuman wardrobe) works from a
checkout — heavyweight tools vendor themselves into gitignored directories, never the repo:

```bash
git clone https://github.com/mbilokonsky/atelier && cd atelier
python vendor/bootstrap.py blender --install     # Blender 4.5 LTS (headless backend)
python vendor/bootstrap.py mpfb --install        # MakeHuman-in-Blender (parametric bodies)
atelier render projects/byrne/minors.py projects/byrne/out/structures3 structures3
atelier paint projects/byrne/out/structures3/card.png projects/byrne/out/structures3/aux.npz \
        blueprint out.png 11 edge=0.75 order=0.65
```

## The engines

Twelve, all speaking one six-knob vocabulary (`edge · focus · order · chroma · weight · pull`)
through per-engine binding tables — an engine responds meaningfully or shrugs honestly:

vangogh · monet · picasso · sketch · watercolor · comic · **stagelight** (light does the
drawing) · **screenprint** (the stock IS the ink set) · **blueprint** · **linocut** ·
**cutout** · **chrono** (chronophotography). Stocks are role-structured palettes
(`core/accent/dark/light`) with value-preserving Oklab pulls.

## Layout

```
core/                 the engine (installable as the `atelier` package)
  styles.py           the painter: 12 engines, knobs, bindings, stocks    → atelier.styles
  cli.py              the `atelier` command                               → atelier.cli
  sdflib.py stage.py sculpt.py    the original numpy backend
  blender/            the Blender backend: bsculpt (builders + clay),
                      bstage (scene/light/camera/G-buffer), runner (headless driver + bake)
vendor/               manifest.json + bootstrap.py; installs are gitignored
                      (blender 4.5 · MPFB 2.0 · MakeHuman CC0 asset pack)
projects/<name>/      one folder per deck or study: models, scene scripts, gitignored out/
  studies/ fable/     the original spike arc; Aesop's Fox & Crow
  ulysses/            Joyce: the Dublin set (a Rawls-grade 1904 city model, game-exportable),
                      scene scripts, Linati per-episode stocks, expert-audit protocol
  byrne/              David Byrne: MPFB figure pipeline (posed, dressed, Big-Suit-fitted),
                      majors + minors, per-era stocks
report/               build_report.py → report.html
```

## Provenance

Built in collaboration between Mykola Bilokonsky and Claude (Anthropic), one render → look →
revise loop at a time. The journals, audits, and lessons live in the project folders and in
each file's comments — the six-limbed dancer, the marshmallow jacket, and the mirror that
had to learn it was metal are all in there.
